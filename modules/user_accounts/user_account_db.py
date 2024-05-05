
import sqlite3
import os
from modules.logging.logger import setup_logger

logger = setup_logger('convo_manager.py')

class UserAccountDatabase:
    def __init__(self, db_name="User.db"):
        
        root_dir = os.path.dirname(os.path.abspath(__file__)) 
        user_profiles_dir = os.path.join(root_dir, 'user_profiles')  

        if not os.path.exists(user_profiles_dir):
            os.makedirs(user_profiles_dir)

        db_path = os.path.join(user_profiles_dir, db_name)

        self.conn = sqlite3.connect(db_path, check_same_thread=False)
        self.cursor = self.conn.cursor()

        self.create_table()

    def create_table(self):
        query = """
        CREATE TABLE IF NOT EXISTS user_accounts (
            id INTEGER PRIMARY KEY,
            username TEXT NOT NULL,
            password TEXT NOT NULL,
            email TEXT NOT NULL,
            name TEXT,
            DOB TEXT
        );
        """
        self.cursor.execute(query)
        self.conn.commit()

    def add_user(self, username, password, email, name, dob):
        query = """
        INSERT INTO user_accounts (username, password, email, name, DOB)
        VALUES (?, ?, ?, ?, ?)
        """
        self.cursor.execute(query, (username, password, email, name, dob))
        self.conn.commit()       

    def get_user(self, username):
        query = "SELECT * FROM user_accounts WHERE username = ?"
        self.cursor.execute(query, (username,))
        return self.cursor.fetchone()

    def get_all_users(self):
        query = "SELECT * FROM user_accounts"
        self.cursor.execute(query)
        return self.cursor.fetchall()
    
    def get_user_profile(self, username):
        query = "SELECT * FROM user_accounts WHERE username = ?"
        self.cursor.execute(query, (username,))
        result = self.cursor.fetchone()
        
        return result

    def close_connection(self):
        """Close the connection to the SQLite database."""
        try:
            self.conn.close()
        except sqlite3.Error as e:
            logger.info(f"Error closing connection: {e}")
            raise 

    def update_user(self, username, password=None, email=None, name=None, dob=None):
        if password:
            query = "UPDATE user_accounts SET password = ? WHERE username = ?"
            self.cursor.execute(query, (password, username))
        if email:
            query = "UPDATE user_accounts SET email = ? WHERE username = ?"
            self.cursor.execute(query, (email, username))
        if name:
            query = "UPDATE user_accounts SET name = ? WHERE username = ?"
            self.cursor.execute(query, (name, username))
        if dob:
            query = "UPDATE user_accounts SET DOB = ? WHERE username = ?"
            self.cursor.execute(query, (dob, username))
        self.conn.commit()
