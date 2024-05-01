# gui\Personas\persona_manager.py

import os
import json
from modules.user_accounts.user_data_manager import UserDataManager
from modules.logging.logger import setup_logger

logger = setup_logger('persona_manager.py')

class PersonaManager:
    """
    The PersonaManager class is responsible for managing personas within the application.
    It loads persona data from a JSON file and updates the current persona based on user selection.
    
    Attributes:
        master (object): A reference to the master application object.
        user (str): The username of the current user.
        personas (list): A list of loaded personas.
        current_persona (dict): The currently selected persona.
    """
    PERSONAS_FILE_NAME = 'system_personas.json'  

    def __init__(self, master, user, chat_component=None):
        self.master = master
        self.user = user
        self.default_persona_name = "SCOUT"  

        try:
            self.load_personas(self.PERSONAS_FILE_NAME, self.user)
            self.default_persona = next((persona for persona in self.personas if persona["name"] == self.default_persona_name), None)
            self.current_persona = self.personalize_persona(self.default_persona, self.user) if self.default_persona else None
        except Exception as e:
            logger.error(f"Error initializing PersonaManager: {e}")
                            
    def updater(self, selected_persona_name, user):
        logger.info("Attempting to update persona.")

        self.master.system_name = selected_persona_name
        self.master.system_name_tag = selected_persona_name

        if hasattr(self.master, 'database'):
            self.master.database.generate_new_conversation_id()
            logger.info(f"Conversation ID updated due to persona change to {selected_persona_name}")
        else:
            logger.warning("ConversationHistory instance not found in master.")

        logger.info(f"Persona switched to {selected_persona_name}")
    
    def personalize_persona(self, persona, user):
        logger.info("Attempting to personalize persona with user content.")
        self.user_name = user
        user_data_manager = UserDataManager(user)
        self.user_profile = user_data_manager.get_profile_text()
        self.user_emr = user_data_manager.get_emr()
        self.system_info = user_data_manager.get_system_info()  

        user_data = {
            "<<name>>": self.user_name,
            "<<Profile>>": self.user_profile,
            "<<emr>>": self.user_emr,
            "<<sysinfo>>": self.system_info,  
        }

        personalized_content = persona["content"]
        for placeholder, data in user_data.items():
            personalized_content = personalized_content.replace(placeholder, data)

        personalized_persona = persona.copy()  
        personalized_persona["content"] = personalized_content

        return personalized_persona
    
    def load_personas(self, filename, user_name):
        """
        Loads personas from a specified JSON file and processes them for use within the application.
        
        This method reads a JSON file containing persona definitions, replaces placeholders with
        user-specific data, and sets the default persona if specified. It also loads additional
        user data such as profiles and EMRs (Electronic Medical Records) to personalize the Medical personas.
        
        Parameters:
            filename (str): The name of the JSON file containing the persona definitions.
            user_name (str): The name of the user for whom the personas are being loaded.
            
        Raises:
            FileNotFoundError: If the JSON file does not exist at the expected path.
            json.JSONDecodeError: If the JSON file is not properly formatted.
            Exception: For any other issues that occur during the loading process.
        """
        file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'modules', 'Personas', filename)
        
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                personas_data = json.load(file)
                self.personas = personas_data["personas"]
            logger.info("Personas loaded successfully")
        except FileNotFoundError:
            logger.error(f"Personas file not found: {file_path}")
            self.personas = []
        except json.JSONDecodeError:
            logger.error(f"Invalid JSON format in personas file: {file_path}")
            self.personas = []
        except Exception as e:
            logger.error(f"Error loading personas: {e}")
            self.personas = []

    def show_message(self, role, message):
        if hasattr(self.master, 'chat_component'):
            chat_component = self.master.chat_component
            chat_component.show_message(role, message)
        else:
            logger.warning("ChatComponent instance not found in master. Unable to display message.")