# modules/Background_Services/CognitiveBackgroundServices.py

import os
import json
import sqlite3
import re
from modules.chat_history.DatabaseContextManager import DatabaseContextManager
from modules.logging.logger import setup_logger

logger = setup_logger('CognitiveBackgroundServices.py')

class CognitiveBackgroundServices:
    def __init__(self, db_file, user, provider_manager):
        self.user = user
        self.db_file = db_file
        self.provider_manager = provider_manager

    async def process_conversation(self, user, conversation_id, chat_log, name=None):
        """
        Description:
        Asynchronously processes the conversation by generating the conversation name and profile update instructions.

        When a user selects a persona from the persona menu, this method is called to generate a meaningful name for the conversation based on its content and generate instructions for updating the user profile.
        
        Side Effects:
        - Calls the provider API to generate the conversation name and profile update instructions.
        - Updates the conversation name in the database using the update_conversation_name method.
        - Updates the user profile using the update_user_profile method.
        
        Thread Safety:
        This method is asynchronous and should be called with the 'await' keyword to ensure proper execution.
        
        Usage:
        await process_conversation(user, conversation_id, chat_log, name)
        
        Dependencies:
        - update_conversation_name method
        - update_user_profile method
        - get_profile method
        - Provider specific API classes
        
        Error Handling:
        - Logs an error if the API response is invalid or empty.
        
        Parameters:
        - user (str): The user associated with the conversation.
        - conversation_id (str): The ID of the conversation.
        - chat_log (str): The chat log of the conversation.
        - name (str, optional): The name of the conversation if provided in the JSON input. Defaults to None.
        
        Returns:
        None
        """
        logger.info("Processing conversation")
        logger.debug(f"with user: {user}, conversation_id: {conversation_id}")
        if chat_log:
            conversation_data = [{"role": "user", "content": chat_log}]
            
            profile = self.get_profile()
            
            system_message_content = "You are ConversationManager. You excel at examining conversations and finding creative names for them. You pay close attention to details; if a conversation is strictly a story and it has a name, use it. The following conversation does not currently have a name. You are to output a conversationally relevant name for this conversation enclosed in double quotation marks (\"\"). Additionally, return a JSON array with the following structure for updating the user profile: [{\"operation\": \"addfield\", \"fieldName\": \"New Field Name\", \"content\": \"New Content goes here\", \"observations\": \"Explanation of why this new field is relevant and not redundant\"}]. If there are no updates, return a JSON array with a single element: [{\"operation\": \"None\"}]. Separate the conversation name and the JSON array with a newline character."
            
            profile_string = json.dumps(profile, ensure_ascii=False)
            system_message_content = system_message_content.replace('<<Profile>>', profile_string)

            payload = {
                #"model": "gpt-4-turbo-preview",
                #"model": "mistral-large-latest",
                "model": "claude-3-sonnet-20240229",
                "messages": [{"role": "system","content": system_message_content}] + conversation_data
            }
            logger.info("Payload being sent")
            logger.debug(f"to API: {json.dumps(payload, indent=2, ensure_ascii=False)}")
            logger.info("Payload being sent to API")
            
            response = await self.provider_manager.generate_cognitive_background_service(payload)
            
            if response and hasattr(response, 'content') and len(response.content) > 0:
                text_block = response.content[0]
                if hasattr(text_block, 'text'):
                    response_text = text_block.text.strip()
                    conversation_name = self.extract_conversation_name(response_text)
                    update_instructions = self.extract_update_instructions(response_text)
                else:
                    logger.error("Invalid response format from the API.")
                    return
            elif response and 'choices' in response and len(response['choices']) > 0 and 'message' in response['choices'][0]:
                response_text = response['choices'][0]['message']['content'].strip()
                conversation_name = self.extract_conversation_name(response_text)
                update_instructions = self.extract_update_instructions(response_text)
            else:
                logger.error("Empty or invalid response from the API.")
                return
            
            if name:
                conversation_name = name
            
            if conversation_name:
                self.update_conversation_name(user, conversation_id, conversation_name)
                logger.info("Conversation Named.")
                logger.debug(f": {conversation_name}")
            else:
                logger.error("Failed to generate conversation name.")
            
            await self.update_user_profile(user, update_instructions)

    def extract_conversation_name(self, response_text):
        """
        Description:
        Extracts the conversation name from the API response text.

        This method uses regular expressions to find the conversation name enclosed in double quotation marks.
        
        Side Effects:
        None
        
        Thread Safety:
        This method is thread-safe as it does not modify any shared resources.
        
        Usage:
        conversation_name = self.extract_conversation_name(response_text)
        
        Dependencies:
        - re module
        
        Error Handling:
        Returns None if no conversation name is found.
        
        Parameters:
        - response_text (str): The text response from the API.
        
        Returns:
        The conversation name enclosed in double quotation marks, or None if not found.
        """
        match = re.search(r'"(.*?)"', response_text)
        if match:
            return match.group(0)
        else:
            return None

    def extract_update_instructions(self, response_text):
        """
        Description:
        Extracts the profile update instructions from the API response text.

        This method assumes that the update instructions are in JSON format and appear after the conversation name in the response text.
        
        Side Effects:
        None
        
        Thread Safety:
        This method is thread-safe as it does not modify any shared resources.
        
        Usage:
        update_instructions = self.extract_update_instructions(response_text)
        
        Dependencies:
        None
        
        Error Handling:
        Returns None if no update instructions are found.
        
        Parameters:
        - response_text (str): The text response from the API.
        
        Returns:
        The profile update instructions in JSON format, or None if not found.
        """
        parts = response_text.split('\n', 1)
        if len(parts) > 1:
            return parts[1].strip()
        else:
            return None

    def update_conversation_name(self, user, conversation_id, name):
        """
        Description:
        Updates the name of the conversation in the database.

        When a user selects a persona from the persona menu, this method is called to update the conversation name in the database.
        
        Side Effects:
        Updates the conversation name in the database.
        
        Thread Safety:
        This method uses the DatabaseContextManager to ensure thread safety when accessing the database.
        
        Usage:
        update_conversation_name(user, conversation_id, name)
        
        Dependencies:
        - DatabaseContextManager
        - sqlite3 module
        
        Error Handling:
        Logs an error if there is an issue updating the conversation name in the database.
        
        Parameters:
        - user (str): The user associated with the conversation.
        - conversation_id (str): The ID of the conversation.
        - name (str): The new name for the conversation, enclosed in double quotation marks.
        
        Returns:
        None
        """
        name = name.strip('"')
        
        with DatabaseContextManager(self.db_file) as cursor:    
            try:
                cursor.execute('''
                    UPDATE conversations 
                    SET name = ? 
                    WHERE user = ? AND conversation_id = ?;
                ''', (name, user, conversation_id))
                logger.info(f"Conversation name added to database")
            except sqlite3.Error as e:
                logger.error(f"Error updating conversation name: {e}")
    
    async def update_user_profile(self, user, update_instructions):
        logger.info("Initiated update_user_profile method.")

        if update_instructions:
            try:
                update_data_list = json.loads(update_instructions)
            except json.JSONDecodeError as e:
                logger.error(f"Failed to parse update instructions: {e}")
                return

            for update_data in update_data_list:
                operation = update_data.get("operation")
                fieldName = update_data.get("fieldName")
                content = update_data.get("content")
                observations = update_data.get("observations", "")

                if operation == "appendContentByField":
                    self.append_content_by_field(user, fieldName, content, observations)
                elif operation == "addfield":
                    self.add_field(user, fieldName, content, observations)
                elif operation == "None":
                    logger.info("No update required for the user profile based on the latest conversation.")
                else:
                    logger.error("Unsupported operation.")
        else:
            logger.error("Invalid or empty update instructions.")
        
    def append_content_by_field(self, user, field_name, content, observations):
        """
        Description:
        Appends content to the 'Content' field and updates 'observations' of a specific category in the user's profile.

        When a user selects a persona from the persona menu, this method is called to append content to a specific field in the user profile.
        
        Side Effects:
        - Modifies the user profile by appending content to the specified field.
        - Saves the updated profile using the save_profile method.
        
        Thread Safety:
        This method is not explicitly thread-safe. Proper synchronization should be implemented if accessed concurrently.
        
        Usage:
        append_content_by_field(user, field_name, content, observations)
        
        Dependencies:
        - get_profile method
        - save_profile method
        
        Error Handling:
        None
        
        Parameters:
        - user (str): The user associated with the profile.
        - field_name (str): The name of the field to append content to.
        - content (str): The content to append to the field.
        - observations (str): The observations associated with the content.
        
        Returns:
        None
        """
        profile = self.get_profile()
        if field_name in profile:
            if isinstance(profile[field_name]['Content'], list):
                profile[field_name]['Content'].append(content)
            elif profile[field_name]['Content']:
                profile[field_name]['Content'] = [profile[field_name]['Content'], content]
            else:
                profile[field_name]['Content'] = content
            if observations:
                profile[field_name]['observations'] = observations
        else:
            profile[field_name] = {"Content": content, "observations": observations}
        
        self.save_profile(profile)

    def add_field(self, user, field_name, content, observations):
        """
        Description:
        Adds a new field with 'Content' and 'observations' to the user's profile.

        When a user selects a persona from the persona menu, this method is called to add a new field to the user profile.
        
        Side Effects:
        - Modifies the user profile by adding a new field.
        - Saves the updated profile using the save_profile method.
        
        Thread Safety:
        This method is not explicitly thread-safe. Proper synchronization should be implemented if accessed concurrently.
        
        Usage:
        add_field(user, field_name, content, observations)
        
        Dependencies:
        - get_profile method
        - save_profile method
        
        Error Handling:
        None
        
        Parameters:
        - user (str): The user associated with the profile.
        - field_name (str): The name of the new field to add.
        - content (str): The content of the new field.
        - observations (str): The observations associated with the new field.
        
        Returns:
        None
        """
        profile = self.get_profile()
        profile[field_name] = {"Content": content, "observations": observations}
        self.save_profile(profile)

   
    def save_profile(self, profile):
        """
        Description:
        Saves the user profile to a JSON file.

        When a user selects a persona from the persona menu, this method is called to save the updated user profile to a JSON file.
        
        Side Effects:
        - Writes the user profile to a JSON file.
        
        Thread Safety:
        This method is not explicitly thread-safe. Proper synchronization should be implemented if accessed concurrently.
        
        Usage:
        save_profile(profile)
        
        Dependencies:
        - os module
        - json module
        
        Error Handling:
        Logs an error if there is an issue saving the profile.
        
        Parameters:
        - profile (dict): The user profile to save.
        
        Returns:
        None
        """ 
        try:
            profile_path = os.path.abspath(os.path.join(
                os.path.dirname(__file__), '..', '..', 'modules', 'user_accounts', 'user_profiles',
                f"{self.user}.json"
            ))
            with open(profile_path, 'w', encoding='utf-8') as file:
                json.dump(profile, file, ensure_ascii=False, indent=4)
            logger.info("Profile updated successfully.")
        except Exception as e:
            logger.error(f"Error saving profile: {e}")
    
    def get_profile(self):
        """
        Description:
        Retrieves the latest simplified profile for the current user from a JSON file.

        When a user selects a persona from the persona menu, this method is called to retrieve the user profile from a JSON file.
        
        Side Effects:
        None
        
        Thread Safety:
        This method is thread-safe as it only reads the user profile from a file.
        
        Usage:
        get_profile()
        
        Dependencies:
        - os module
        - json module
        
        Error Handling:
        - Logs an error if the profile file does not exist.
        - Logs an error if there is an issue loading the profile.
        
        Parameters:
        None
        
        Returns:
        The user profile as a JSON object. If the profile file does not exist or an error occurs, an empty dictionary is returned.
        """
        try:
            profile_path = os.path.abspath(os.path.join(
                os.path.dirname(__file__), '..', '..', 'modules', 'user_accounts', 'user_profiles',
                f"{self.user}.json"
            ))

            logger.debug(f"Profile path: {profile_path}")

            if not os.path.exists(profile_path):
                logger.error(f"Profile file does not exist: {profile_path}")
                return {}

            with open(profile_path, 'r', encoding='utf-8') as file:
                profile = json.load(file)
                logger.info("Profile found")
                logger.debug(f": {profile}")
                return profile

        except Exception as e:
            logger.error(f"Error loading profile: {e}")
            return {}