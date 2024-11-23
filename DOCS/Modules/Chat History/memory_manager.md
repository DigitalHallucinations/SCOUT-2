## Module: memory_manager.py
This module is used to manage retrieval of messages and tool responses that have been compressed or removed to reduce token usage across lengthy conversations. It includes functionalities to compress messages, save compressed messages, recall original messages, and manage overall memory within the chat application.

---

# Imports:

- `sqlite3`: Standard library for interacting with SQLite databases.
- `DatabaseContextManager` from `.DatabaseContextManager`: Internal module for managing database connections.
- `setup_logger` from `modules.logging.logger`: Internal module for setting up logging.
- `openai`: Third-party library for interacting with OpenAI's API for summarizing messages.

---

## Class: MemoryManager

### Constructor  
#### Method: `__init__`

The constructor initializes the MemoryManager class, setting up the database file for managing chat history and memory.

- **Parameters:**
  - `db_file` (str, required): The path to the SQLite database file used for storing chat history and memory.

- **Returns:** None

### Methods

## Method: `get_history`
Fetches the message history for a user in a specific conversation. This method retrieves all the messages with message IDs before summarization or compression by the MemoryManager.

- **Parameters:**
  - `user` (str, required): User ID of the current user.
  - `conversation_id` (str, required): Conversation ID of the current conversation.

- **Returns:**
  - `messages` (list): List of message dictionaries with role, content, and timestamp.

**Example usage:**

history = memory_manager.get_history(user="user123", conversation_id="conv456")


## Method: `get_cached_tool_response`
Retrieves a cached function call response based on the user, conversation_id, and function_call_id. This is used to recall the result of a function call after the parsed result is returned to the user.

- **Parameters:**
  - `user` (str, required): User ID.
  - `conversation_id` (str, required): ID of the conversation.
  - `function_call_id` (str, required): The ID of the function call.

- **Returns:**
  - `response_data` (str): The response data as a string, or None if not found.

**Example usage:**

cached_response = memory_manager.get_cached_tool_response(user="user123", conversation_id="conv456", function_call_id="func789")


## Method: `compress_message`
Compresses a long message by summarizing it using OpenAI's GPT model.

- **Parameters:**
  - `message` (str, required): The message content to be compressed.

- **Returns:**
  - `compressed_message` (str): The compressed (summarized) message.

**Example usage:**

compressed_message = memory_manager.compress_message("This is a long message that needs to be summarized.")


## Method: `save_compressed_message`
Saves the compressed message in the database.

- **Parameters:**
  - `user` (str, required): User ID.
  - `conversation_id` (str, required): Conversation ID.
  - `message_id` (int, required): The ID of the original message.
  - `compressed_message` (str, required): The compressed message content.

- **Returns:** None

**Example usage:**

memory_manager.save_compressed_message("user123", "conv456", 1, compressed_message)


## Method: `recall_compressed_message`
Recalls the original message for one turn and reverts to the compressed message on the next get_history call.

- **Parameters:**
  - `user` (str, required): User ID.
  - `conversation_id` (str, required): Conversation ID.
  - `message_id` (int, required): The ID of the message to be recalled.

- **Returns:**
  - `original_message` (str): The original message content, or None if not found.

**Example usage:**

original_message = memory_manager.recall_compressed_message("user123", "conv456", 1)


## Method: `revert_to_compressed_message`
Reverts the message back to its compressed form after one turn.

- **Parameters:**
  - `user` (str, required): User ID.
  - `conversation_id` (str, required): Conversation ID.
  - `message_id` (int, required): The ID of the message to be reverted.

- **Returns:** None

**Example usage:**

memory_manager.revert_to_compressed_message("user123", "conv456", 1)
