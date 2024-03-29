# gui\Personas\persona_manager.py

import os
import re
import json
import logging
from logging.handlers import RotatingFileHandler
from modules.user_accounts.user_data_manager import UserDataManager

logger = logging.getLogger('persona_manager.py')

log_filename = 'SCOUT.log'
log_max_size = 10 * 1024 * 1024  # 10 MB
log_backup_count = 5

# Create rotating file handler for file logging
rotating_handler = RotatingFileHandler(log_filename, maxBytes=log_max_size, backupCount=log_backup_count, encoding='utf-8')
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
rotating_handler.setFormatter(formatter)

# Create stream handler for console logging
stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)

# Attach handlers to the logger
logger.addHandler(rotating_handler)
logger.addHandler(stream_handler)
logger.setLevel(logging.INFO)

def adjust_logging_level(level):
    """Adjust the logging level.
    
    Parameters:
    - level (str): Desired logging level. Can be 'DEBUG', 'INFO', 'WARNING', 'ERROR', or 'CRITICAL'.
    """
    levels = {
        'DEBUG': logging.DEBUG,
        'INFO': logging.INFO,
        'WARNING': logging.WARNING,
        'ERROR': logging.ERROR,
        'CRITICAL': logging.CRITICAL
    }
    
    logger.setLevel(levels.get(level, logging.WARNING))

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
        self.chat_component = chat_component
        self.default_persona_name = "SCOUT"  # Set the default persona name

        try:
            self.load_personas(self.PERSONAS_FILE_NAME, user)
            # Set the default persona based on the default_persona_name
            self.default_persona = next((persona for persona in self.personas if persona["name"] == self.default_persona_name), None)
            self.current_persona = self.personalize_persona(self.default_persona) if self.default_persona else None
        except Exception as e:
            logger.error(f"Error initializing PersonaManager: {e}")
                         
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
        logger.info("Attempting to load personas.")
        file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'modules', 'Personas', filename)
        with open(file_path, 'r', encoding='utf-8') as file:
            personas_data = json.load(file)
            self.personas = personas_data["personas"]
        logger.info("Personas loaded successfully")

    def updater(self, selected_persona_name):
        """
        Updates the system name and persona based on the selected persona name and generates a new conversation ID.

        This method updates the master application object with the new system name, tag, and current persona. If a database
        instance is present, it also generates a new conversation ID.

        Parameters:
            selected_persona_name (str): The name of the persona to switch to.

        Returns:
            None
        """
        logger.info("Attempting to update persona.")

        # Updating system name and tag
        self.master.system_name = selected_persona_name
        self.master.system_name_tag = selected_persona_name

        # Find and personalize the selected persona
        selected_persona = next((persona for persona in self.master.personas if persona["name"] == selected_persona_name), None)
        if selected_persona:
            personalized_persona = self.personalize_persona(selected_persona)
            self.master.current_persona = personalized_persona
            self.master.show_message("system", f"Persona switched to {selected_persona_name} and personalized")
        else:
            self.master.show_message("system", f"Persona {selected_persona_name} not found")
 
        # Generate a new conversation ID due to the change in persona
        if hasattr(self.master, 'database'):
            self.master.database.generate_new_conversation_id()
            logger.info(f"Conversation ID updated due to persona change to {selected_persona_name}")
        else:
            logger.warning("ConversationHistory instance not found in master.")

        # Log the persona change
        logger.info(f"Persona switched to {selected_persona_name} and personalized")
   
    def personalize_persona(self, persona):
        logging.info("Attempting to personalize persona with user content.")
        self.user_name = self.user
        logging.info(self.user_name)
        user_data_manager = UserDataManager(self.user)
        self.user_profile = user_data_manager.profile()
        self.user_emr = user_data_manager.emr()
        # Example placeholders and corresponding user data
        user_data = {
            "<<name>>": self.user_name,
            "<<Profile>>": self.user_profile,
            "<<emr>": self.user_emr,
        }
 
        # Replace each placeholder in the persona content with the user's data
        personalized_content = persona["content"]
        for placeholder, data in user_data.items():
            personalized_content = personalized_content.replace(placeholder, data)

        # Update the persona with personalized content
        personalized_persona = persona.copy()  # Make a copy to avoid altering the original
        personalized_persona["content"] = personalized_content

        return personalized_persona