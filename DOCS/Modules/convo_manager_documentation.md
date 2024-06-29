# DOCS/convo_manager_documentation.md

### Overview

The `convo_manager.py` file defines the `ConversationManager` class, which handles the management of conversations, including storing and retrieving conversation data, managing database connections, and handling background tasks related to conversations. The class interacts with a SQLite database to store conversations and related data.

### Table of Contents

1. [Imports](#imports)
2. [ConversationManager Class](#conversationmanager-class)
    - [Initialization](#initialization)
    - [Database Connection Management](#database-connection-management)
    - [Conversation Management](#conversation-management)
    - [Message and Function Call Management](#message-and-function-call-management)
    - [Background Task Management](#background-task-management)

### Imports

The script imports necessary modules for SQLite database operations, UUID generation, time management, asyncio for asynchronous operations, and custom modules for database schema, context management, cognitive background services, and logging.

### ConversationManager Class

The `ConversationManager` class manages the lifecycle of conversations, including initialization, insertion, retrieval, and deletion of conversations, as well as handling related messages and function calls. It uses a SQLite database to store conversation data.

#### Initialization

The `__init__` method initializes the `ConversationManager` with the user's ID, persona name, and provider manager. It validates the persona name, sets up the database file path, initializes the cognitive services, sets up database schema, and establishes a database connection.

#### Database Connection Management

- **establish_connection**: Establishes a connection to the SQLite database for chat history.
- **close_connection**: Closes the database connection and cancels any background tasks.

#### Conversation Management

- **init_conversation_id**: Initializes a unique conversation ID for the current session using the user's ID, current time, and a UUID.
- **create_all_tables**: Creates necessary tables in the database if they do not already exist, using SQL commands defined in the `DatabaseSchema`.
- **generate_new_conversation_id**: Generates a new conversation ID for the session.
- **update_conversation_id**: Updates the conversation ID to a new value.
- **conversation_exists**: Checks if a conversation with a given ID exists for a user in the database.
- **insert_conversation**: Inserts a new conversation into the database. If the conversation already exists, it deletes the old conversation and re-inserts it. This method also manages background tasks for processing the conversation.
- **get_conversations**: Retrieves a list of conversations for a specific user, optionally filtered by persona and conversation ID.
- **delete_conversation**: Deletes a specific conversation and all related data from the database.
- **get_chat_log**: Retrieves the chat log for a specific conversation.

#### Message and Function Call Management

- **add_response**: Inserts a response into the 'responses' table with a placeholder for the function call ID and updates it if necessary.
- **add_function_call**: Inserts a function call into the 'function_calls' table and updates the function call ID.
- **add_message**: Inserts a message into the 'messages' table and updates the message ID and function call ID if applicable.
- **get_history**: Retrieves the message history for a specific conversation, removing the message ID from the content.

#### Background Task Management

The `insert_conversation` method creates and manages background tasks for processing conversations using the `CognitiveBackgroundServices` class. These tasks run asynchronously to avoid blocking the main thread.

### Summary

The `ConversationManager` class in `convo_manager.py` is responsible for managing the entire lifecycle of conversations, from initialization to deletion, including storing and retrieving data from a SQLite database. It handles message and function call management and integrates with cognitive background services to process conversations in the background. The class ensures that database operations are thread-safe and manages connections efficiently.