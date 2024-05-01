# modules/Background_Services/CognitiveBackgroundServices.py

import os
import json
import sqlite3
from modules.chat_history.DatabaseContextManager import DatabaseContextManager
from modules.logging.logger import setup_logger

logger = setup_logger('CognitiveBackgroundServices.py')

class CognitiveBackgroundServices:
    def __init__(self, db_file, user, provider_manager):
        self.user = user
        self.db_file = db_file
        self.provider_manager = provider_manager


    async def generate_and_update_conversation_name(self, user, conversation_id, chat_log):
        """
        Description:
        Asynchronously generates and updates the conversation name using the provided chat log.

        When a user selects a persona from the persona menu, this method is called to generate a meaningful name for the conversation based on its content and update it in the database.
        
        Side Effects:
        - Calls the generate_conversation_name method to generate the conversation name.
        - Updates the conversation name in the database using the update_conversation_name method.
        - Updates the user profile using the update_user_profile method.
        
        Thread Safety:
        This method is asynchronous and should be called with the 'await' keyword to ensure proper execution.
        
        Usage:
        await generate_and_update_conversation_name(user, conversation_id, chat_log)
        
        Dependencies:
        - generate_conversation_name method
        - update_conversation_name method
        - update_user_profile method
        
        Error Handling:
        - Logs an error if the conversation name generation fails or returns an invalid response.
        - Logs an error if the conversation name is empty.
        
        Parameters:
        - user (str): The user associated with the conversation.
        - conversation_id (str): The ID of the conversation.
        - chat_log (str): The chat log of the conversation.
        
        Returns:
        None
        """
        if chat_log:
            conversation_data = [{"role": "user", "content": chat_log}]
            response = await self.generate_conversation_name(conversation_data)
            logger.debug(f"Provider API response for conversation name: {response}")
            logger.info("Provider API response for conversation name")

            conversation_name = None

            if response and hasattr(response, 'content') and len(response.content) > 0:
                text_block = response.content[0]
                if hasattr(text_block, 'text'):
                    conversation_name = text_block.text.strip()
            elif response and 'choices' in response and len(response['choices']) > 0 and 'message' in response['choices'][0]:
                conversation_name = response['choices'][0]['message'].get('content', '').strip()

            if conversation_name:
                self.update_conversation_name(user, conversation_id, conversation_name)
                logger.info(f"Model named the conversation: {conversation_name}")
                await self.update_user_profile(user, conversation_data)
            else:
                logger.error("Failed to generate conversation name or invalid response format.")


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
        - name (str): The new name for the conversation.
        
        Returns:
        None
        """
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

    async def generate_conversation_name(self, conversation_data):
        """
        Description:
        Generates a conversation name based on the provided conversation data.

        When a user selects a persona from the persona menu, this method is called to generate a meaningful name for the conversation using the OpenAI API.
        
        Side Effects:
        Calls the OpenAI API to generate the conversation name.
        
        Thread Safety:
        This method is asynchronous and should be called with the 'await' keyword to ensure proper execution.
        
        Usage:
        await generate_conversation_name(conversation_data)
        
        Dependencies:
        - Provider specific API classes
        
        Error Handling:
        None
        
        Parameters:
        - conversation_data (list): The conversation data in the format required by the OpenAI API.
        
        Returns:
        The response from the OpenAI API containing the generated conversation name.
        """
        payload = { 
            #"model": "gpt-4-1106-preview",
            #"model": "mistral-large-latest",
            "model": "claude-3-haiku-20240307",
            "messages": [{"role": "system", "content": "You are ConversationManager. You accel at examining conversations and finding creative names for them. You pay close attention to details, if a conversation is strictly a story and it has a name use it. The following conversation does not currently have a name. You are to output a conversationally relevant name for this conversation in up to 3 words."}] + conversation_data
        }
        return await self.provider_manager.generate_cognitive_background_service(payload)
    
    async def update_user_profile(self, user, conversation_data):
        logger.info("Initiated update_user_profile method.")
        response = await self.generate_profile_update(conversation_data)
        logger.info("ProfileManager responded")

        update_instructions = None

        if response and hasattr(response, 'content') and len(response.content) > 0:
            # Handle Anthropic API response format
            text_block = response.content[0]
            if hasattr(text_block, 'text'):
                # Extract the JSON array string from the text block
                json_array_string = text_block.text.strip()
                # Find the start and end indices of the JSON array
                start_index = json_array_string.find('[')
                end_index = json_array_string.rfind(']') + 1
                if start_index != -1 and end_index != -1:
                    # Extract the JSON array string
                    json_string = json_array_string[start_index:end_index]
                    try:
                        update_instructions = json.loads(json_string)
                    except json.JSONDecodeError as e:
                        logger.error(f"Failed to parse ProfileManager response: {e}")
                else:
                    logger.error("Invalid JSON array format in ProfileManager response.")
        elif response and 'choices' in response and len(response['choices']) > 0:
            # Handle previous response format used by other providers
            update_instructions = response['choices'][0]['message']['content']

        if update_instructions:
            if isinstance(update_instructions, str):
                try:
                    update_data_list = json.loads(update_instructions)
                except json.JSONDecodeError as e:
                    logger.error(f"Failed to parse ProfileManager response: {e}")
                    return
            else:
                update_data_list = update_instructions

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
            logger.error("Invalid response format or no response from ProfileManager.")
        
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

    async def generate_profile_update(self, conversation_data):
        """
        Description:
        Generates profile update instructions based on the provided conversation data.

        When a user selects a persona from the persona menu, this method is called to generate instructions for updating the user profile using the latest conversation data.
        
        Side Effects:
        - Calls the OpenAI API or Mistral API to generate the profile update instructions.
        
        Thread Safety:
        This method is asynchronous and should be called with the 'await' keyword to ensure proper execution.
        
        Usage:
        await generate_profile_update(conversation_data)
        
        Dependencies:
        - get_profile method
        - OpenAIAPI class
        - MistralAPI class
        
        Error Handling:
        None
        
        Parameters:
        - conversation_data (list): The conversation data used to generate the profile update instructions.
        
        Returns:
        The response from the API containing the generated profile update instructions.
        """
        logger.debug(f"Initiated generate_profile_update method. {conversation_data}")
        logger.info("Initiated generate_profile_update method.")
        profile = self.get_profile()
            
        system_message_content = "As the ProfileManager, your job is to update the User Profile using information from the latest conversation. Review the conversation, identify new and relevant Content about the user, and integrate these into the User profile. The following is a conversation between a user and an AI assistant. You must find new entries to add to the user profile. To add entries to a field, use the correct .json appendContentByField output for the specific entry you want to append the data to. Ensure that the observations field provides unique insights that are not already covered by the content. To add a new field to the profile, use the correct .json addfield output and give it a fieldname along with content and observations, but only if such a field does not already exist and the information is not captured elsewhere in the profile. When there is no new data to add to the profile, use the correct .json no update output.\\n\\nPlease make sure that any observations added are concise and offer additional context not evident from the content alone. Avoid redundancy by not repeating information that is already clear from the content fields.\\n\\nExample appendContentByField output:\\n\\n{\\n  \"operation\": \"appendContentByField\",\\n  \"fieldName\": \"Favorite Movies\",\\n  \"content\": \"New Movie Goes Here\",\\n  \"observations\": \"Unique insight or context not evident from the content\"\\n}\\n\\nExample addfield output:\\n\\n{\\n  \"operation\": \"addfield\",\\n  \"fieldName\": \"New Field Name\",\\n  \"content\": \"New Content goes here\",\\n  \"observations\": \"Explanation of why this new field is relevant and not redundant\"\\n}\\n\\nExample no update output:\\n\\n{\\n  \"operation\": \"None\"\\n}\\n\\nAll outputs MUST be structured as described and keep observations short and to the point.\\n\\nIMPORTANT: Return a list of update instructions, even if there is only one update. If there are no updates, return a list with a single 'None' operation."
            
        profile_string = json.dumps(profile, ensure_ascii=False)
        system_message_content = system_message_content.replace('<<Profile>>', profile_string)

        payload = {
            #"model": "gpt-4-turbo-preview",
            #"model": "mistral-large-latest",
            "model": "claude-3-haiku-20240307",
            "messages": [{"role": "system","content": system_message_content}] + conversation_data
        }
            
        logger.debug(f"Payload being sent to API: {json.dumps(payload, indent=2, ensure_ascii=False)}")
        logger.info("Payload being sent to API")
        return await self.provider_manager.generate_cognitive_background_service(payload)
    
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

            logger.info(f"Profile path: {profile_path}")

            if not os.path.exists(profile_path):
                logger.error(f"Profile file does not exist: {profile_path}")
                return {}

            with open(profile_path, 'r', encoding='utf-8') as file:
                profile = json.load(file)
               # logger.info(f"Profile found: {profile}")
                logger.info("Profile found")
                return profile

        except Exception as e:
            logger.error(f"Error loading profile: {e}")
            return {}
        
    