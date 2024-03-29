# gui\user_accounts\delete_user.py

import sqlite3

class DeleteUser:
    def __init__(self, db_name="scout_chat.db"):
        self.conn = sqlite3.connect(db_name, check_same_thread=False)
        self.cursor = self.conn.cursor()

    def delete_specific_user(self, username_to_delete):
        self.cursor.execute("DELETE FROM user_accounts WHERE username=?", (username_to_delete,))
        self.conn.commit()

    def delete_all_users(self):
        self.cursor.execute("DELETE FROM user_accounts")
        self.conn.commit()
