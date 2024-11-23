# modules/chat_history/memory_manager.py

import sqlite3
from .DatabaseContextManager import DatabaseContextManager
from modules.logging.logger import setup_logger
import openai

logger = setup_logger('memory_manager.py')

class MemoryManager:
    def __init__(self, db_file):
        self.db_file = db_file

    def get_history(self, user, conversation_id):
        """
        Fetch the message history for a user in a specific conversation.
        This is used to get all the messages with message_ids before summarization or compression of individual messages.

        Args:
        - user (str): User ID of the current user.
        - conversation_id (str): Conversation ID of the current conversation.

        Returns:
        - List of message dictionaries with role, content, and timestamp.
        """
        with DatabaseContextManager(self.db_file) as cursor:
            try:
                cursor.execute('SELECT role, content, timestamp FROM messages WHERE user = ? AND conversation_id = ?', (user, conversation_id,))
                return [{"role": role, "content": content, "timestamp": timestamp} for role, content, timestamp in cursor.fetchall()]
            except sqlite3.Error as e:
                logger.error(f"Error fetching history: {e}")
                raise   

    def get_cached_tool_response(self, user, conversation_id, function_call_id):
        """
        Retrieve a cached function call response based on the user, conversation_id, and function_call_id.
        This is used to recall the result of a function call after the parsed result is returned to the user.

        Args:
        - user (str): User ID.
        - conversation_id (str): ID of the conversation.
        - function_call_id (str): The ID of the function call.

        Returns:
        - The response data as a string, or None if not found.
        """
        with DatabaseContextManager(self.db_file) as cursor:
            try:
                cursor.execute('''
                    SELECT response_data FROM responses 
                    WHERE user = ? AND conversation_id = ? AND function_call_id = ?;
                ''', (user, conversation_id, function_call_id))
                row = cursor.fetchone()
                return row[0] if row else None
            except sqlite3.Error as e:
                logger.error(f"Error fetching cached tool response: {e}")
                raise

    def compress_message(self, message):
        """
        Compresses a long message by summarizing it using OpenAI's GPT model.

        Args:
        - message (str): The message content to be compressed.

        Returns:
        - The compressed (summarized) message.
        """
        try:
            response = openai.Completion.create(
                engine="davinci",
                prompt=f"Summarize the following message:\n\n{message}",
                max_tokens=50
            )
            compressed_message = response.choices[0].text.strip()
            logger.info("Message compressed successfully")
            return compressed_message
        except Exception as e:
            logger.error(f"Error compressing message: {e}")
            raise

    def save_compressed_message(self, user, conversation_id, message_id, compressed_message):
        """
        Saves the compressed message in the database.

        Args:
        - user (str): User ID.
        - conversation_id (str): Conversation ID.
        - message_id (str): The ID of the original message.
        - compressed_message (str): The compressed message content.

        Returns:
        - None
        """
        with DatabaseContextManager(self.db_file) as cursor:
            try:
                cursor.execute('''
                    UPDATE messages
                    SET compressed_content = ?
                    WHERE user = ? AND conversation_id = ? AND id = ?;
                ''', (compressed_message, user, conversation_id, message_id))
                logger.info("Compressed message saved successfully")
            except sqlite3.Error as e:
                logger.error(f"Error saving compressed message: {e}")
                raise

    def recall_compressed_message(self, user, conversation_id, message_id):
        """
        Recalls the original message for one turn and reverts to the compressed message on the next get_history call.

        Args:
        - user (str): User ID.
        - conversation_id (str): Conversation ID.
        - message_id (str): The ID of the message to be recalled.

        Returns:
        - The original message content, or None if not found.
        """
        with DatabaseContextManager(self.db_file) as cursor:
            try:
                cursor.execute('''
                    SELECT content FROM messages
                    WHERE user = ? AND conversation_id = ? AND id = ?;
                ''', (user, conversation_id, message_id))
                row = cursor.fetchone()
                if row:
                    original_message = row[0]
                    cursor.execute('''
                        UPDATE messages
                        SET compressed_content = NULL
                        WHERE user = ? AND conversation_id = ? AND id = ?;
                    ''', (user, conversation_id, message_id))
                    logger.info("Original message recalled successfully")
                    return original_message
                return None
            except sqlite3.Error as e:
                logger.error(f"Error recalling original message: {e}")
                raise

    def revert_to_compressed_message(self, user, conversation_id, message_id):
        """
        Reverts the message back to its compressed form after one turn.

        Args:
        - user (str): User ID.
        - conversation_id (str): Conversation ID.
        - message_id (str): The ID of the message to be reverted.

        Returns:
        - None
        """
        with DatabaseContextManager(self.db_file) as cursor:
            try:
                cursor.execute('''
                    SELECT compressed_content FROM messages
                    WHERE user = ? AND conversation_id = ? AND id = ?;
                ''', (user, conversation_id, message_id))
                row = cursor.fetchone()
                if row and row[0] is not None:
                    compressed_message = row[0]
                    cursor.execute('''
                        UPDATE messages
                        SET content = ?, compressed_content = NULL
                        WHERE user = ? AND conversation_id = ? AND id = ?;
                    ''', (compressed_message, user, conversation_id, message_id))
                    logger.info("Message reverted to compressed form successfully")
            except sqlite3.Error as e:
                logger.error(f"Error reverting to compressed message: {e}")
                raise

# Example usage
# db_file = "path/to/database.db"
# memory_manager = MemoryManager(db_file)
# history = memory_manager.get_history(user="user123", conversation_id="conv456")
# compressed_message = memory_manager.compress_message("This is a long message that needs to be summarized.")
# memory_manager.save_compressed_message("user123", "conv456", 1, compressed_message)
# original_message = memory_manager.recall_compressed_message("user123", "conv456", 1)
# memory_manager.revert_to_compressed_message("user123", "conv456", 1)
