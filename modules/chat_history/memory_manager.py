# modules/chat_history/memory_manager.py

import sqlite3
import logging
from logging.handlers import RotatingFileHandler
from .DatabaseContextManager import DatabaseContextManager

"""
This file is used to manage retrieval of messages and tool resonses that have been compressed or removed 
to reduce token usage across lengthy conversations.

NOT COMPLETELY IMPLEMENTED YET!!!
to do:
Create class MemoryManager
create function to compress messages after a certain token limit using call to model to summarize long messages.
creat function to save compressed message and return it instead of the full message
fix recall_compressed_message this should return the original message to it place in the message history for one 
turn and revert to compressed_message the on the next get_history call
"""

logger = logging.getLogger('memory_manager.py')

log_filename = 'SCOUT.log'
log_max_size = 10 * 1024 * 1024  
log_backup_count = 5

rotating_handler = RotatingFileHandler(log_filename, maxBytes=log_max_size, backupCount=log_backup_count, encoding='utf-8')
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
rotating_handler.setFormatter(formatter)

stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)

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

def get_history(self, user, conversation_id):
        """
        Used by MemoryManager to fetch the message history for a user in a specific conversation.
        This is used to get all the messages with message_ids before summarization or compression of invidual messages by the MemoryManager.
        Args:
        - user: User ID of current user
        - conversation_id: Conversation ID of current conversation    

        Returns:
        - List of message dictionaries with role, content, and timestamp
        """
        with DatabaseContextManager(self.db_file) as cursor:
            try:
                cursor.execute('SELECT role, content, timestamp FROM messages WHERE user = ? AND conversation_id = ?', (user, conversation_id,))
                return [{"role": role, "content": content, "timestamp": timestamp} for role, content, timestamp in cursor.fetchall()]
            except sqlite3.Error as e:
                logger.error(f"Error fetching history: {e}")
                raise
    
def get_compressed_message(Self, user, conversation_id, message_id):
     

def get_cached_tool_response(self, user, conversation_id, function_call_id):
        """
        Used by MemoryManager to retrieve a cached funtion call response based on the user, conversation_id, and function_call_id.
        This is used to recall the result of a function call after the parsed resut is returned to the user. 
        To save bandwidth and token usgage the original data is not returned to the model, only the function call id and params/query is returned.
        returning the function call id to the model allows it to choose to recall the data, 
        in case of additional data need by the model or by the user without making the same call more than once.

        Args:
        - user: User ID
        - conversation_id: ID of the conversation
        - function_call_id: The ID of the function call

        Returns:
        - The response data as a string, or None if not found
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
    
    