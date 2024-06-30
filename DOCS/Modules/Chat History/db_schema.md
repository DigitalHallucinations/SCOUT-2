# DOCS/db_schema_documentation.md

The `db_schema.py` file defines the SQL schema for the chat history database used by the SCOUT application. It contains the SQL commands necessary to create the tables required to store users, conversations, messages, function calls, and responses.

### DatabaseSchema Class

The `DatabaseSchema` class encapsulates the SQL commands as class attributes. Each attribute holds a SQL statement that creates a specific table if it does not already exist. This ensures that the database schema is correctly set up when the application initializes.

#### CREATE_USERS_TABLE_SQL

```sql
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    persona_name TEXT UNIQUE NOT NULL
);
```

- **Purpose**: This table stores user information.
- **Columns**:
  - `id`: An auto-incrementing primary key.
  - `persona_name`: A unique and non-null text field to store the user's persona name.

#### CREATE_CONVERSATIONS_TABLE_SQL

```sql
CREATE TABLE IF NOT EXISTS conversations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user TEXT NOT NULL,
    conversation_id TEXT NOT NULL,
    chat_log TEXT NOT NULL,
    timestamp TEXT NOT NULL,
    persona TEXT NOT NULL,
    name TEXT,
    date_modified TEXT,
    FOREIGN KEY (user) REFERENCES users(id)
);
```

- **Purpose**: This table stores conversation details.
- **Columns**:
  - `id`: An auto-incrementing primary key.
  - `user`: A text field referencing the user who owns the conversation.
  - `conversation_id`: A unique identifier for the conversation.
  - `chat_log`: The content of the chat.
  - `timestamp`: The time when the conversation occurred.
  - `persona`: The persona associated with the conversation.
  - `name`: An optional name for the conversation.
  - `date_modified`: The date when the conversation was last modified.
  - **Foreign Key**: References the `id` field in the `users` table.

#### CREATE_MESSAGES_TABLE_SQL

```sql
CREATE TABLE IF NOT EXISTS messages (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user TEXT NOT NULL,
    conversation_id TEXT NOT NULL,
    role TEXT NOT NULL,
    content TEXT NOT NULL,
    timestamp TEXT NOT NULL,
    FOREIGN KEY (user) REFERENCES users(id)
);
```

- **Purpose**: This table stores individual messages within a conversation.
- **Columns**:
  - `id`: An auto-incrementing primary key.
  - `user`: A text field referencing the user who sent or received the message.
  - `conversation_id`: The ID of the conversation to which the message belongs.
  - `role`: The role of the message sender (e.g., user, system).
  - `content`: The content of the message.
  - `timestamp`: The time when the message was sent.
  - **Foreign Key**: References the `id` field in the `users` table.

#### CREATE_FUNCTION_CALLS_TABLE_SQL

```sql
CREATE TABLE IF NOT EXISTS function_calls (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user TEXT NOT NULL,
    conversation_id TEXT NOT NULL,
    message_id INTEGER,
    function_name TEXT NOT NULL,
    arguments TEXT NOT NULL,
    timestamp TEXT NOT NULL,
    FOREIGN KEY (user) REFERENCES users(id),
    FOREIGN KEY (message_id) REFERENCES messages(id)
);
```

- **Purpose**: This table stores details of function calls made during a conversation.
- **Columns**:
  - `id`: An auto-incrementing primary key.
  - `user`: A text field referencing the user who made the function call.
  - `conversation_id`: The ID of the conversation in which the function call was made.
  - `message_id`: The ID of the message associated with the function call.
  - `function_name`: The name of the function that was called.
  - `arguments`: The arguments passed to the function.
  - `timestamp`: The time when the function call was made.
  - **Foreign Keys**: References the `id` field in the `users` and `messages` tables.

#### CREATE_RESPONSES_TABLE_SQL

```sql
CREATE TABLE IF NOT EXISTS responses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user TEXT NOT NULL,
    conversation_id TEXT NOT NULL,
    function_call_id INTEGER NOT NULL,
    response_data TEXT NOT NULL,
    timestamp TEXT NOT NULL,
    FOREIGN KEY (user) REFERENCES users(id),
    FOREIGN KEY (function_call_id) REFERENCES function_calls(id)
);
```

- **Purpose**: This table stores responses generated during a conversation.
- **Columns**:
  - `id`: An auto-incrementing primary key.
  - `user`: A text field referencing the user who received the response.
  - `conversation_id`: The ID of the conversation in which the response was generated.
  - `function_call_id`: The ID of the function call associated with the response.
  - `response_data`: The data of the response.
  - `timestamp`: The time when the response was generated.
  - **Foreign Keys**: References the `id` field in the `users` and `function_calls` tables.

### Summary

The `DatabaseSchema` class provides the necessary SQL commands to create the database schema for storing users, conversations, messages, function calls, and responses. Each table is designed with appropriate fields and relationships to ensure data integrity and facilitate efficient data management for the SCOUT application.