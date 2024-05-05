#gui/chat_history/convo_manager.py

import sqlite3
import uuid
import time
import asyncio

from modules.chat_history.db_schema import DatabaseSchema
from .DatabaseContextManager import DatabaseContextManager
from modules.Background_Services.CognitiveBackgroundServices import CognitiveBackgroundServices
from modules.logging.logger import setup_logger

logger = setup_logger('convo_manager.py')

class ConversationManager:   
    def __init__(self, user, persona_name, provider_manager):
        if not isinstance(persona_name, str):
            raise ValueError("persona_name must be a string")
        self.persona_name = persona_name
        self.user = user
        self.conversation_id = None
        self.message_id = None
        self.function_call_id = None
        self.loaded_conversations = set()
        self.db_file = f"modules/Personas/{persona_name}/Memory/{persona_name}.db"
        self.cognitive_services = CognitiveBackgroundServices(self.db_file, user, provider_manager)        
        self.schema = DatabaseSchema()
        self.create_all_tables()

    def init_conversation_id(self):
        """Initialize the conversation ID for the session."""
        self.conversation_id = f"{self.user}_{int(time.time())}_{uuid.uuid4()}"
        logger.info(f"Conversation ID initialized: {self.conversation_id}")
        return self.conversation_id

    def create_all_tables(self):
        """
        Create all necessary tables if they don't exist.
        """
        with DatabaseContextManager(self.db_file) as cursor:
            logger.info("Creating all necessary tables if not exists")
            try:
                cursor.execute(self.schema.CREATE_USERS_TABLE_SQL)
                cursor.execute(self.schema.CREATE_CONVERSATIONS_TABLE_SQL)
                cursor.execute(self.schema.CREATE_MESSAGES_TABLE_SQL)
                cursor.execute(self.schema.CREATE_FUNCTION_CALLS_TABLE_SQL)
                cursor.execute(self.schema.CREATE_RESPONSES_TABLE_SQL)
                logger.info("All tables created or verified")
            except sqlite3.Error as e:
                logger.error(f"Error creating tables: {e}")
                raise     

    def generate_new_conversation_id(self):
        """Generate a new conversation ID for the current session."""
        self.conversation_id = f"{self.user}_{int(time.time())}_{uuid.uuid4()}"
        logger.info(f"New Conversation ID generated: {self.conversation_id}")

    def update_conversation_id(self, new_conversation_id):
        """Update the conversation ID with a new value."""
        self.conversation_id = new_conversation_id
        logger.info(f"Conversation ID updated to: {new_conversation_id}")        

    def close_connection(self):
        """Close the connection to the SQLite database."""
        try:
            self.conn.close()
        except sqlite3.Error as e:
            logger.info(f"Error closing connection: {e}")
            raise 

    def conversation_exists(self, user, conversation_id):
        """
        Check if a conversation with the given conversation_id already exists for the user.

        Args:
        - user: User ID
        - conversation_id: ID of the conversation

        Returns:
        - True if the conversation exists, False otherwise
        """
        with DatabaseContextManager(self.db_file) as cursor:
            try:
                cursor.execute('''
                    SELECT 1 FROM conversations WHERE user = ? AND conversation_id = ?;
                ''', (user, conversation_id))
                return cursor.fetchone() is not None
            except sqlite3.Error as e:
                logger.error(f"Error checking if conversation exists: {e}")
                raise
    
    async def insert_conversation(self, user, conversation_id, chat_log, timestamp, persona):
        """
        Used in chist_ functions, app.py and chist_functions.py to save chat_log by inserting the entire chat_log into the 'conversations' table.

        Args:
        - user: User ID
        - conversation_id: ID of the conversation
        - chat_log: The content of the chat_log
        - timestamp: Timestamp of the conversation
        - persona: Persona involved in the conversation
        """

        if conversation_id in self.loaded_conversations:
            logger.info(f"Continuing conversation_id {conversation_id} for user {user}. Deleting old conversation.")
            self.delete_conversation(user, conversation_id)
            self.loaded_conversations.remove(conversation_id)
        elif self.conversation_exists(user, conversation_id):
            logger.info(f"Conversation with ID {conversation_id} already exists for user {user}. Skipping insertion.")
            return

        logger.info(f"Inserting Conversation for user: {user}, conversation_id: {conversation_id}")
        with DatabaseContextManager(self.db_file) as cursor:    
            try:
                current_time = time.strftime("%Y-%m-%d %H:%M:%S")
                cursor.execute('''
                    INSERT INTO conversations (user, conversation_id, chat_log, timestamp, persona, date_modified)
                    VALUES (?, ?, ?, ?, ?, ?);
                ''', (user, conversation_id, chat_log, timestamp, persona, current_time))
                logger.info("Message inserted successfully")
            except sqlite3.Error as e:
                logger.error(f"Error inserting conversation: {e}")
                raise

        asyncio.create_task(self.cognitive_services.generate_and_update_conversation_name(user, conversation_id, chat_log))

    def get_conversations(self, user, persona=None, conversation_id=None):
        """
        Used in chist_functions to retrieve a list of conversations for a specific user and optionally for a specific persona 
        and conversation ID from the 'conversations' table.

        Args:
        - user: User ID
        - persona: Optional. Specific persona to retrieve.
        - conversation_id: Optional. Specific conversation ID to retrieve.

        Returns:
        - Populates Chat History listbox with list of chat logs, timestamps, personas, and names for the specified user. 
        """
        with DatabaseContextManager(self.db_file) as cursor:
            try:
                query = 'SELECT chat_log, timestamp, persona, conversation_id, name FROM conversations WHERE user = ?'
                params = [user]

                if persona:
                    query += ' AND persona = ?'
                    params.append(persona)

                if conversation_id:
                    query += ' AND conversation_id = ?'
                    params.append(conversation_id)

                logger.info(f"Executing query")    
                logger.debug(f"Executing query: {query} with params: {params}")

                cursor.execute(query, params)
                results = cursor.fetchall()
                logger.info(f"Query results")
                logger.debug(f"Query results: {results}")
                return results
            except sqlite3.Error as e:
                logger.error(f"Error fetching conversation: {e}")
                raise

    def delete_conversation(self, user, conversation_id):
        """
        # used in chist_functions.py to delete all entries related to a specific conversation_id from all relevant tables.

        Args:
        - user: The user ID
        - conversation_id: The conversation ID to be deleted
        """
        with DatabaseContextManager(self.db_file) as cursor: 
            try:
                cursor.execute('DELETE FROM conversations WHERE user = ? AND conversation_id = ?;', (user, conversation_id))
                cursor.execute('DELETE FROM messages WHERE user = ? AND conversation_id = ?;', (user, conversation_id))
                cursor.execute('DELETE FROM function_calls WHERE user = ? AND conversation_id = ?;', (user, conversation_id))
                logger.info(f"All related data deleted successfully for conversation_id: {conversation_id}")
            except sqlite3.Error as e:
                logger.error(f"Error deleting conversation and related data: {e}")
                raise          

    def get_chat_log(self, user, conversation_id):
        """
        Used in Chat settings to retrieve chat_history for a specific chat log from the 'conversations' table based on user and conversation ID.
        All conversations for the given user and conversation_id are returned.
        When used in chist_functions, the conversation name is filtered and diplayed in the Chat History window when selecting a history entry.
        Args:
        - user: User ID
        - conversation_id: The ID of the conversation

        Returns:
        The chat log as a string, or None if not found.
        """
        with DatabaseContextManager(self.db_file) as cursor:
            try:
                cursor.execute('''
                    SELECT chat_log FROM conversations
                    WHERE user = ? AND conversation_id = ?;
                ''', (user, conversation_id))
                row = cursor.fetchone()
                return row[0] if row is not None else None
            except sqlite3.Error as e:
                logger.error(f"Error fetching conversation: {e}")
                raise
            
    def add_response(self, user, conversation_id, response_data, timestamp):
        """
        Used in OA_gen_response to insert a response into the 'responses' table with a placeholder for function_call_id.

        Args:
        - user: User ID
        - conversation_id: Conversation ID
        - response_data: The response data to be stored
        - timestamp: Timestamp of the response

        Returns:
        - The ID of the inserted response
        """
        function_call_id_placeholder = "[function_call_id]"
        with DatabaseContextManager(self.db_file) as cursor:
            try:
                cursor.execute('''
                    INSERT INTO responses (user, conversation_id, function_call_id, response_data, timestamp)
                    VALUES (?, ?, ?, ?, ?);
                ''', (user, conversation_id, function_call_id_placeholder, response_data, timestamp))
                response_id = cursor.lastrowid

                if self.function_call_id is not None:
                    cursor.execute('''
                        UPDATE responses SET function_call_id = ? WHERE id = ?;
                    ''', (self.function_call_id, response_id))

                logger.info("Response inserted and updated successfully with function_call_id")
                return response_id
            except sqlite3.Error as e:
                logger.error(f"Error inserting response: {e}")
                raise  
        
    def add_function_call(self, user, conversation_id, function_name, arguments, timestamp):
        """
        Used in Tool_Manager to insert a function call into the 'function_calls' table, then update the function call
        to include its own ID and update the function_call_id attribute of the class.

        Args:
        - user: User ID
        - conversation_id: Conversation ID
        - function_name: Name of the function
        - arguments: Raw data or arguments of the function call
        - timestamp: Timestamp of the function call

        Returns:
        - function_call_id: The ID of the inserted function call
        """
        if self.message_id is None:
            logger.error("No message_id available to associate with the function call.")
            return None

        placeholder = "[function_call_id]"
        full_arguments = f"{arguments}\nFunction_call_id: {placeholder}"
        with DatabaseContextManager(self.db_file) as cursor:
            try:
                cursor.execute('''
                    INSERT INTO function_calls (user, conversation_id, message_id, function_name, arguments, timestamp)
                    VALUES (?, ?, ?, ?, ?, ?);
                ''', (user, conversation_id, self.message_id, function_name, full_arguments, timestamp))
                function_call_id = cursor.lastrowid
                updated_arguments = full_arguments.replace(placeholder, str(function_call_id))
                cursor.execute('''
                    UPDATE function_calls SET arguments = ? WHERE id = ?;
                ''', (updated_arguments, function_call_id))
                logger.info(f"Function call inserted with ID: {function_call_id}")
                return function_call_id
            except sqlite3.Error as e:
                logger.error(f"Error inserting function call: {e}")
                raise
        
    def add_message(self, user, conversation_id, role, message, timestamp):
        """
        Used in OA_gen_response to insert a message into the 'messages' table and return the message ID.

        Args:
        - user: User ID
        - conversation_id: Conversation ID
        - role: Role of the user (e.g., 'admin', 'user', etc.)
        - message: The message content
        - timestamp: Timestamp of the message

        Returns:
        - message_id: The ID of the inserted message
        """
        message_id_placeholder = "Message ID: 1005"
        function_call_id_placeholder = "<[function_call_id]>"

        full_message = f"{message}\n{message_id_placeholder}"
        if self.function_call_id is not None:
            function_call_id_content = f"Function Call ID: {self.function_call_id}"
            full_message += f"\n{function_call_id_content}"

        with DatabaseContextManager(self.db_file) as cursor:
            try:
                cursor.execute('''
                    INSERT INTO messages (user, conversation_id, role, content, timestamp)
                    VALUES (?, ?, ?, ?, ?);
                ''', (user, conversation_id, role, full_message, timestamp))
                message_id = cursor.lastrowid

                updated_message = full_message.replace("Message ID: 1005", f"Message ID: {message_id}")
                if self.function_call_id is not None:
                    updated_message = updated_message.replace("<[function_call_id]>", f"Function Call ID: {self.function_call_id}")

                cursor.execute('''
                    UPDATE messages SET content = ? WHERE id = ?;
                ''', (updated_message, message_id))
                logger.info(f"Message inserted with ID: {message_id}")

                return message_id
            except sqlite3.Error as e:
                logger.error(f"Error inserting message: {e}")
                raise
    
    def get_history(self, user, conversation_id):
        """
        Used in OA_gen_response to fetch the message history for a user in a specific conversation.
        This method removes the message_id from the message content before returning the history to gen_response.
        Args:
        - user: User ID
        - conversation_id: Conversation ID

        Returns:
        - List of message dictionaries with role, content, and timestamp, with message_id removed from content.
        """
        with DatabaseContextManager(self.db_file) as cursor:
            try:
                cursor.execute('SELECT role, content, timestamp FROM messages WHERE user = ? AND conversation_id = ?', (user, conversation_id,))
                messages = []
                for role, content, timestamp in cursor.fetchall():
                    if 'Message ID: ' in content:
                        # Remove the message ID from the content
                        content = content.rsplit('Message ID: ', 1)[0].strip()
                    messages.append({"role": role, "content": content, "timestamp": timestamp})
                return messages
            except sqlite3.Error as e:
                logger.error(f"Error fetching history: {e}")
                raise

    