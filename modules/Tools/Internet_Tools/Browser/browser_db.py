# modules/Tools/Internet_Tools/Browser/browser_db.py

import sqlite3
import os
from modules.logging.logger import setup_logger

logger = setup_logger('browser_db.py')

class BrowserDatabase:
    def __init__(self, db_name='browser.db'):
        logger.info("Initializing BrowserDatabase")
        self.db_name = db_name
        self.conn = None
        self.cursor = None
        self.create_database()



    def create_database(self):
        logger.info("Creating database and tables if they don't exist")
        db_path = os.path.join('modules', 'Tools', 'Internet_Tools', 'Browser', self.db_name)
        os.makedirs(os.path.dirname(db_path), exist_ok=True)

        try:
            self.conn = sqlite3.connect(self.db_name)
            self.cursor = self.conn.cursor()

            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS history (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    url TEXT,
                    title TEXT,
                    visit_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)

            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS bookmarks (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    url TEXT,
                    title TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)

            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS cookies (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT,
                    value TEXT,
                    domain TEXT,
                    path TEXT,
                    expiration TIMESTAMP,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)

            self.conn.commit()
            logger.debug("Database and tables created successfully")
        except sqlite3.Error as e:
            logger.error(f"An error occurred while creating the database: {e}")
        finally:
            if self.conn:
                self.conn.close()

    def add_history(self, url, title):
        logger.info("Adding new history entry to the database")
        logger.debug(f"Adding history: {url}")
        try:
            self.conn = sqlite3.connect(self.db_name)
            self.cursor = self.conn.cursor()

            self.cursor.execute("""
                INSERT INTO history (url, title)
                VALUES (?, ?)
            """, (url, title))
            self.conn.commit()
            logger.debug(f"History entry {url} added successfully")
        except sqlite3.Error as e:
            logger.error(f"An error occurred while adding the history entry: {e}")
        finally:
            self.conn.close()

    def get_all_history(self):
        """Retrieves all history entries from the database."""
        logger.info("Retrieving all history entries from the database")
        try:
            self.conn = sqlite3.connect(self.db_name)
            self.cursor = self.conn.cursor()

            self.cursor.execute("SELECT * FROM history")
            history = self.cursor.fetchall()

            logger.debug(f"Retrieved {len(history)} history entries")
            return history
        except sqlite3.Error as e:
            logger.error(f"An error occurred while retrieving history entries: {e}")
            return []
        finally:
            if self.conn:
                self.conn.close()

    def add_bookmark(self, url, title):
        logger.info("Adding new bookmark to the database")
        logger.debug(f"Adding bookmark: {url}")
        try:
            self.conn = sqlite3.connect(self.db_name)
            self.cursor = self.conn.cursor()

            self.cursor.execute("""
                INSERT INTO bookmarks (url, title)
                VALUES (?, ?)
            """, (url, title))
            self.conn.commit()
            logger.debug(f"Bookmark {url} added successfully")
        except sqlite3.Error as e:
            logger.error(f"An error occurred while adding the bookmark: {e}")
        finally:
            self.conn.close()

    def get_all_bookmarks(self):
        """Retrieves all bookmarks from the database."""
        logger.info("Retrieving all bookmarks from the database")
        try:
            self.conn = sqlite3.connect(self.db_name)
            self.cursor = self.conn.cursor()

            self.cursor.execute("SELECT * FROM bookmarks")
            bookmarks = self.cursor.fetchall()

            logger.debug(f"Retrieved {len(bookmarks)} bookmarks")
            return bookmarks
        except sqlite3.Error as e:
            logger.error(f"An error occurred while retrieving bookmarks: {e}")
            return []
        finally:
            if self.conn:
                self.conn.close()

    def add_cookie(self, name, value, domain, path, expiration):
        logger.info("Adding new cookie to the database")
        logger.debug(f"Adding cookie: {name}")
        try:
            self.conn = sqlite3.connect(self.db_name)
            self.cursor = self.conn.cursor()

            self.cursor.execute("""
                INSERT INTO cookies (name, value, domain, path, expiration)
                VALUES (?, ?, ?, ?, ?)
            """, (name, value, domain, path, expiration))
            self.conn.commit()
            logger.debug(f"Cookie {name} added successfully")
        except sqlite3.Error as e:
            logger.error(f"An error occurred while adding the cookie: {e}")
        finally:
            self.conn.close()

    def get_all_cookies(self):
        """Retrieves all cookies from the database."""
        logger.info("Retrieving all cookies from the database")
        try:
            self.conn = sqlite3.connect(self.db_name)
            self.cursor = self.conn.cursor()

            self.cursor.execute("SELECT * FROM cookies")
            cookies = self.cursor.fetchall()

            logger.debug(f"Retrieved {len(cookies)} cookies")
            return cookies
        except sqlite3.Error as e:
            logger.error(f"An error occurred while retrieving cookies: {e}")
            return []
        finally:
            if self.conn:
                self.conn.close()