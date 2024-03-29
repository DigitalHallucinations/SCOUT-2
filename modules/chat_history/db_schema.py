# modules/chat_history/db_schema.py

class DatabaseSchema:    
    CREATE_USERS_TABLE_SQL = """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            persona_name TEXT UNIQUE NOT NULL
        );
    """

    CREATE_CONVERSATIONS_TABLE_SQL = """
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
    """

    CREATE_MESSAGES_TABLE_SQL = """
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user TEXT NOT NULL,
            conversation_id TEXT NOT NULL,
            role TEXT NOT NULL,
            content TEXT NOT NULL,
            timestamp TEXT NOT NULL,
            FOREIGN KEY (user) REFERENCES users(id)
        );
    """

    CREATE_FUNCTION_CALLS_TABLE_SQL = """
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
    """

    CREATE_RESPONSES_TABLE_SQL = """
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
    """