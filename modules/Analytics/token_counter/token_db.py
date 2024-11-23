# modules/token_counter/token_db.py

import sqlite3

DATABASE_PATH = 'modules/Analytics/token_counter/token.db'

def setup_database():
    """
    Sets up the database tables if they do not exist.
    Adds an 'organization' column to the 'token_usage' table.
    """
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS token_usage (
            id INTEGER PRIMARY KEY,
            organization TEXT,
            user TEXT,
            session_id TEXT,
            conversation_id TEXT,  
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            model TEXT,
            prompt_tokens INTEGER,
            completion_tokens INTEGER,
            total_tokens INTEGER
        )''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS model_token_counters (
            model TEXT PRIMARY KEY,
            organization TEXT,
            cumulative_prompt_tokens INTEGER DEFAULT 0,
            cumulative_completion_tokens INTEGER DEFAULT 0,
            cumulative_total_tokens INTEGER DEFAULT 0
        )''')

    conn.commit()
    conn.close()


def insert_token_usage(organization, user, session_id, conversation_id, model, prompt_tokens, completion_tokens, total_tokens):
    """
    Inserts the token usage into the SQLite database.

    Parameters:
    - organization (str): The organization under which the query was made.
    - user (str): The user who made the query.
    - session_id (str): The session ID during which the query was made.
    - conversation_id (str): The conversation the query was made from.
    - model (str): The model used for the query.
    - prompt_tokens (int): The number of tokens used in the prompt.
    - completion_tokens (int): The number of tokens generated as completion.
    - total_tokens (int): The total number of tokens used.
    """
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()

    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()

    cursor.execute('''
        INSERT INTO token_usage (organization, user, session_id, conversation_id, model, prompt_tokens, completion_tokens, total_tokens) 
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)''',
                   (organization, user, session_id, conversation_id, model, prompt_tokens, completion_tokens, total_tokens))
    conn.commit()
    conn.close()

def update_model_token_counters(organization, model, prompt_tokens, completion_tokens, total_tokens):
    """
    Updates the rolling counters of individual model token usage.

    Parameters:
    - organization (str): The organization under which the query was made.
    - model (str): The model for which the tokens are counted.
    - prompt_tokens (int), completion_tokens (int), total_tokens (int): The token counts to be updated.
    """
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()

    cursor.execute('''
        SELECT cumulative_prompt_tokens, cumulative_completion_tokens, cumulative_total_tokens 
        FROM model_token_counters WHERE model = ? AND organization = ?''', (model, organization))
    row = cursor.fetchone()

    if row:
        new_prompt_tokens = row[0] + prompt_tokens
        new_completion_tokens = row[1] + completion_tokens
        new_total_tokens = row[2] + total_tokens

        cursor.execute('''
            UPDATE model_token_counters 
            SET cumulative_prompt_tokens = ?, cumulative_completion_tokens = ?, cumulative_total_tokens = ? 
            WHERE model = ? AND organization = ?''',
                       (new_prompt_tokens, new_completion_tokens, new_total_tokens, model, organization))
    else:
        cursor.execute('''
            INSERT INTO model_token_counters (organization, model, cumulative_prompt_tokens, cumulative_completion_tokens, cumulative_total_tokens)
            VALUES (?, ?, ?, ?, ?)''',
                       (organization, model, prompt_tokens, completion_tokens, total_tokens))

    conn.commit()
    conn.close()