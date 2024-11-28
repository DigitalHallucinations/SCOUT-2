# modules/Personas/persona_manager.py

import os
import json
from typing import List, Optional, Dict
from modules.user_accounts.user_data_manager import UserDataManager
from modules.config import ConfigManager
from modules.logging.logger import setup_logger

class PersonaManager:
    """
    The PersonaManager class is responsible for managing personas within the application.
    It loads persona data from corresponding folders and updates the current persona based on user selection.

    Attributes:
        master (object): A reference to the master application object.
        user (str): The username of the current user.
        personas (dict): A cache of loaded personas.
        current_persona (dict): The currently selected persona.
        current_system_prompt (str): The system prompt generated based on the selected persona.
    """
    
    def __init__(self, master, user: str):
        self.master = master
        self.user = user
        self.config_manager = ConfigManager()
        self.logger = setup_logger(__name__)
        self.persona_base_path = os.path.join(os.path.dirname(__file__), '..', 'modules', 'Personas')
        self.persona_names: List[str] = self.load_persona_names(self.persona_base_path)
        self.personas: Dict[str, dict] = {}  # Cache for loaded personas
        self.default_persona_name = "SCOUT"
        self.current_persona = None
        self.current_system_prompt = None

        # Load the default persona and generate the system prompt
        self.load_default_persona()

    def load_default_persona(self):
        """Loads and personalizes the default persona."""
        persona = self.load_persona(self.default_persona_name)
        if persona:
            self.current_persona = persona
            self.current_system_prompt = self.build_system_prompt(persona)
            self.logger.info(f"Default persona '{self.default_persona_name}' loaded with personalized system prompt.")
        else:
            self.logger.error(f"Failed to load default persona: '{self.default_persona_name}'")

    def load_persona_names(self, persona_path: str) -> List[str]:
        """Get the list of persona directories."""
        try:
            persona_names = [name for name in os.listdir(persona_path) if os.path.isdir(os.path.join(persona_path, name))]
            self.logger.info(f"Persona names loaded: {persona_names}")
            return persona_names
        except OSError as e:
            self.logger.error(f"Error loading persona names: {e}")
            return []

    def load_persona(self, persona_name: str) -> Optional[dict]:
        """
        Load a single persona from its respective folder.

        Args:
            persona_name (str): The name of the persona to load.

        Returns:
            dict: The loaded persona data, or None if loading fails.
        """
        if persona_name in self.personas:  # Check cache first
            self.logger.info(f"Persona '{persona_name}' retrieved from cache.")
            return self.personas[persona_name]
        
        persona_folder = os.path.join(self.master.config_manager.get_app_root(), 'modules', 'Personas', persona_name, 'Persona')
        json_file = os.path.join(persona_folder, f'{persona_name}.json')

        self.logger.debug(f"Attempting to load persona from folder: {persona_folder}")
        self.logger.debug(f"Persona JSON file path: {json_file}")

        if os.path.exists(json_file):
            try:
                with open(json_file, 'r', encoding='utf-8') as file:
                    persona_data = json.load(file)
                    if "persona" in persona_data and isinstance(persona_data["persona"], list) and len(persona_data["persona"]) > 0:
                        self.personas[persona_name] = persona_data["persona"][0]  # Cache the loaded persona
                        self.logger.info(f"Persona '{persona_name}' loaded successfully from '{json_file}'.")
                        return self.personas[persona_name]
                    else:
                        self.logger.error(f"Invalid persona format in '{json_file}'. Expected a list under 'persona' key.")
                        return None
            except (FileNotFoundError, json.JSONDecodeError) as e:
                self.logger.error(f"Error loading persona '{persona_name}': {e}")
                return None
        else:
            self.logger.error(f"JSON file for persona '{persona_name}' not found at '{json_file}'.")
            return None


    def get_persona(self, persona_name: str) -> Optional[dict]:
        """Retrieve the persona by name, loading it from disk if necessary."""
        return self.load_persona(persona_name)

    def updater(self, selected_persona_name: str):
        """Update the current persona."""
        self.logger.info(f"Attempting to update persona to '{selected_persona_name}'.")
        
        persona = self.get_persona(selected_persona_name)
        if not persona:
            self.logger.error(f"Failed to update persona: '{selected_persona_name}' not found or invalid.")
            return

        self.current_persona = persona
        self.current_system_prompt = self.build_system_prompt(persona)

        self.master.system_name = selected_persona_name
        self.master.system_name_tag = selected_persona_name

        self.logger.info(f"Persona switched to '{selected_persona_name}' with new system prompt.")
        self.logger.info(f"Current persona is now: {self.current_persona}")


    def build_system_prompt(self, persona: dict) -> str:
        """
        Builds the system prompt using user-specific information,
        including the EMR only for medical personas and profile only if enabled.

        Args:
            persona (dict): The persona data to personalize.

        Returns:
            str: The personalized system prompt.
        """
        self.logger.info(f"Building system prompt for persona '{persona.get('name')}'.")
        user_data_manager = UserDataManager(self.user)

        # General user data available to all personas
        user_data = {
            "<<name>>": self.user,
        }

        # Only add Profile if user_profile_enabled is True
        if persona.get("user_profile_enabled") == "True":
            self.logger.info(f"Adding Profile to persona: '{persona['name']}'.")
            user_data["<<Profile>>"] = user_data_manager.get_profile_text()
        else:
            self.logger.info(f"Profile not added for persona: '{persona['name']}'.")
            user_data["<<Profile>>"] = "Profile not available for this persona."

        # Only add EMR if the persona is a medical persona
        if persona.get("medical_persona") == "True":
            self.logger.info(f"Adding EMR to medical persona: '{persona['name']}'.")
            user_data["<<emr>>"] = user_data_manager.get_emr()
        else:
            self.logger.info(f"EMR not added for non-medical persona: '{persona['name']}'.")
            user_data["<<emr>>"] = "EMR not available for this persona."

        # Only add sysinfo if the persona is a sys_admin_persona
        if persona.get("sys_info_enabled") == "True":
            self.logger.info(f"Adding system info to persona: '{persona['name']}'.")
            user_data["<<sysinfo>>"] = user_data_manager.get_system_info()
        else:
            self.logger.info(f"System info not added for persona: '{persona['name']}'.")
            user_data["<<sysinfo>>"] = "System info not available for this persona."

        # Assemble the system prompt from the content parts
        content = persona.get("content", {})
        parts = [
            content.get("start_locked", "").strip(),
            content.get("editable_content", "").strip(),
            content.get("end_locked", "").strip(),
        ]
        # Filter out empty strings and join with spaces
        personalized_content = ' '.join(filter(None, parts))

        # Replace placeholders in the assembled content with user data
        for placeholder, data in user_data.items():
            personalized_content = personalized_content.replace(placeholder, data)

        self.logger.info(f"System prompt built for persona '{persona['name']}': {personalized_content}")
        return personalized_content

    def update_persona(self, persona):
        """Update the persona settings and save them to the corresponding file."""
        persona_name = persona.get("name")
        persona_folder = os.path.join(self.persona_base_path, persona_name, 'Persona')
        json_file = os.path.join(persona_folder, f'{persona_name}.json')

        try:
            with open(json_file, 'w', encoding='utf-8') as file:
                json.dump({"persona": [persona]}, file, indent=4)
            self.logger.info(f"Persona '{persona_name}' updated successfully.")
        except OSError as e:
            self.logger.error(f"Error saving persona '{persona_name}': {e}")

    def show_message(self, role: str, message: str):
        """Display a message using the chat component, if available."""
        if hasattr(self.master, 'chat_component'):
            self.master.chat_component.show_message(role, message)
        else:
            self.logger.warning("ChatComponent instance not found in master. Unable to display message.")

    def get_current_persona_prompt(self) -> str:
        """Returns the current persona's system prompt."""
        return self.current_system_prompt
