## Module: convo_manager.py
This module manages the conversation history for a chat application. It handles tasks such as initializing conversation IDs, managing the database connection, creating necessary tables, inserting and retrieving conversations, and handling background tasks related to cognitive services.

---

# Imports:
- `sqlite3`: Standard library for interacting with SQLite databases.
- `uuid`: Standard library for generating unique identifiers.
- `time`: Standard library for handling time-related tasks.
- `asyncio`: Standard library for writing concurrent code using the async/await syntax.
- `DatabaseSchema` from `modules.chat_history.db_schema`: Internal module for database schema definitions.
- `DatabaseContextManager` from `.DatabaseContextManager`: Internal module for managing database connections.
- `CognitiveBackgroundServices` from `modules.Background_Services.CognitiveBackgroundServices`: Internal module for handling background cognitive services.
- `setup_logger` from `modules.logging.logger`: Internal module for setting up logging.

---

## Class: ConversationManager

### Constructor  
#### Method: `__init__`

The constructor initializes the ConversationManager class, setting up necessary parameters, database connections, and cognitive background services.

- **Parameters:**
  - `user` (str, required): The user ID for whom the conversation is managed.
  - `persona_name` (str, required): The persona associated with the conversation. Must be a string.
  - `provider_manager` (object, required): The provider manager for handling service providers.

- **Returns:** None

### Methods

## Method: `init_conversation_id`
Initializes a unique conversation ID for the session using the user ID, current timestamp, and a UUID.

- **Parameters:** None
- **Returns:** 
  - `conversation_id` (str): The newly initialized conversation ID.

**Example usage:**
```python
conversation_id = conversation_manager.init_conversation_id()
```

## Method: `create_all_tables`
Creates all necessary tables in the database if they do not already exist.

- **Parameters:** None
- **Returns:** None

**Example usage:**
```python
conversation_manager.create_all_tables()
```

## Method: `generate_new_conversation_id`
Generates a new unique conversation ID for the current session.

- **Parameters:** None
- **Returns:** None

**Example usage:**
```python
conversation_manager.generate_new_conversation_id()
```

## Method: `update_conversation_id`
Updates the conversation ID with a new value.

- **Parameters:**
  - `new_conversation_id` (str, required): The new conversation ID to be set.

- **Returns:** None

**Example usage:**
```python
conversation_manager.update_conversation_id(new_conversation_id)
```

## Method: `establish_connection`
Establishes a connection to the SQLite database for chat history.

- **Parameters:** None
- **Returns:** None

**Example usage:**
```python
conversation_manager.establish_connection()
```

## Method: `close_connection`
Closes the connection to the SQLite database.

- **Parameters:** None
- **Returns:** None

**Example usage:**
```python
conversation_manager.close_connection()
```

## Method: `conversation_exists`
Checks if a conversation with the given conversation_id already exists for the user.

- **Parameters:**
  - `user` (str, required): The user ID.
  - `conversation_id` (str, required): The conversation ID to check.

- **Returns:** 
  - `exists` (bool): True if the conversation exists, False otherwise.

**Example usage:**
```python
exists = conversation_manager.conversation_exists(user, conversation_id)
```

## Method: `insert_conversation`
Inserts a conversation into the 'conversations' table and manages background tasks.

- **Parameters:**
  - `user` (str, required): The user ID.
  - `conversation_id` (str, required): The conversation ID.
  - `chat_log` (str, required): The content of the chat log.
  - `timestamp` (str, required): Timestamp of the conversation.
  - `persona` (str, required): Persona involved in the conversation.

- **Returns:** None

**Example usage:**
```python
await conversation_manager.insert_conversation(user, conversation_id, chat_log, timestamp, persona)
```

## Method: `get_conversations`
Retrieves a list of conversations for a specific user, optionally filtered by persona and conversation ID.

- **Parameters:**
  - `user` (str, required): The user ID.
  - `persona` (str, optional): Specific persona to filter.
  - `conversation_id` (str, optional): Specific conversation ID to filter.

- **Returns:**
  - `results` (list): List of conversation details.

**Example usage:**
```python
conversations = conversation_manager.get_conversations(user, persona, conversation_id)
```

## Method: `delete_conversation`
Deletes all entries related to a specific conversation_id from all relevant tables.

- **Parameters:**
  - `user` (str, required): The user ID.
  - `conversation_id` (str, required): The conversation ID to be deleted.

- **Returns:** None

**Example usage:**
```python
conversation_manager.delete_conversation(user, conversation_id)
```

## Method: `get_chat_log`
Retrieves the chat log for a specific conversation based on user and conversation ID.

- **Parameters:**
  - `user` (str, required): The user ID.
  - `conversation_id` (str, required): The conversation ID.

- **Returns:**
  - `chat_log` (str): The chat log content or None if not found.

**Example usage:**
```python
chat_log = conversation_manager.get_chat_log(user, conversation_id)
```

## Method: `add_response`
Inserts a response into the 'responses' table with a placeholder for function_call_id.

- **Parameters:**
  - `user` (str, required): The user ID.
  - `conversation_id` (str, required): The conversation ID.
  - `response_data` (str, required): The response data to be stored.
  - `timestamp` (str, required): Timestamp of the response.

- **Returns:**
  - `response_id` (int): The ID of the inserted response.

**Example usage:**
```python
response_id = conversation_manager.add_response(user, conversation_id, response_data, timestamp)
```

## Method: `add_function_call`
Inserts a function call into the 'function_calls' table and updates the function call ID.

- **Parameters:**
  - `user` (str, required): The user ID.
  - `conversation_id` (str, required): The conversation ID.
  - `function_name` (str, required): Name of the function.
  - `arguments` (str, required): Raw data or arguments of the function call.
  - `timestamp` (str, required): Timestamp of the function call.

- **Returns:**
  - `function_call_id` (int): The ID of the inserted function call.

**Example usage:**
```python
function_call_id = conversation_manager.add_function_call(user, conversation_id, function_name, arguments, timestamp)
```

## Method: `add_message`
Inserts a message into the 'messages' table and returns the message ID.

- **Parameters:**
  - `user` (str, required): The user ID.
  - `conversation_id` (str, required): The conversation ID.
  - `role` (str, required): Role of the user (e.g., 'admin', 'user').
  - `message` (str, required): The message content.
  - `timestamp` (str, required): Timestamp of the message.

- **Returns:**
  - `message_id` (int): The ID of the inserted message.

**Example usage:**
```python
message_id = conversation_manager.add_message(user, conversation_id, role, message, timestamp)
```

## Method: `get_history`
Fetches the message history for a user in a specific conversation, removing the message_id from the content.

- **Parameters:**
  - `user` (str, required): The user ID.
  - `conversation_id` (str, required): The conversation ID.

- **Returns:**
  - `messages` (list): List of message dictionaries with role, content, and timestamp.

**Example usage:**
```python
history = conversation_manager.get_history(user, conversation_id)
```

---
