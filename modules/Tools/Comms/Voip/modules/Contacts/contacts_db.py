# modules/Tools/Comms/Voip/modules/Contacts/contacts_db.py

import sqlite3
from modules.logging.logger import setup_logger

logger = setup_logger('contacts_db.py')

class ContactsDatabase:
    def __init__(self, db_name='contacts.db'):
        logger.info("Initializing ContactsDatabase")
        self.db_name = db_name
        self.conn = None
        self.cursor = None
        self.create_database()

    def create_database(self):
        """Creates the contacts database if it doesn't exist."""
        logger.info("Creating database and tables if they don't exist")
        try:
            self.conn = sqlite3.connect(self.db_name)
            self.cursor = self.conn.cursor()

            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS contacts (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT,
                    numbers TEXT,
                    email TEXT,
                    address TEXT,
                    company TEXT,
                    position TEXT,
                    notes TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    image BLOB 
                )
            """)

            self.conn.commit()
            logger.debug("Database and tables created successfully")
        except sqlite3.Error as e:
            logger.error(f"An error occurred while creating the database: {e}")

    def add_contact(self, name, numbers, email, address, company, position, notes, image):
        """Adds a new contact to the database."""
        logger.info("Adding new contact to the database")
        logger.debug(f"Adding contact: {name}")
        try:
            self.conn = sqlite3.connect(self.db_name)
            self.cursor = self.conn.cursor()

            self.cursor.execute("""
                INSERT INTO contacts (name, numbers, email, address, company, position, notes, image)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (name, numbers, email, address, company, position, notes, image))

            self.conn.commit()
            logger.debug(f"Contact {name} added successfully")
        except sqlite3.Error as e:
            logger.error(f"An error occurred while adding the contact: {e}")
        finally:
            self.conn.close()

    def get_all_contacts(self):
        """Retrieves all contacts from the database."""
        logger.info("Retrieving all contacts from the database")
        try:
            self.conn = sqlite3.connect(self.db_name)
            self.cursor = self.conn.cursor()

            self.cursor.execute("SELECT * FROM contacts")
            contacts = self.cursor.fetchall()
            logger.debug(f"Retrieved {len(contacts)} contacts")

            return contacts
        except sqlite3.Error as e:
            logger.error(f"An error occurred while retrieving contacts: {e}")
            return []
        finally:
            self.conn.close()

    def get_contact_by_id(self, contact_id):
        """Retrieves a specific contact by its ID."""
        logger.info(f"Retrieving contact with ID: {contact_id}")
        try:
            self.conn = sqlite3.connect(self.db_name)
            self.cursor = self.conn.cursor()

            self.cursor.execute("SELECT * FROM contacts WHERE id = ?", (contact_id,))
            contact = self.cursor.fetchone()
            logger.debug(f"Retrieved contact: {contact}")

            return contact
        except sqlite3.Error as e:
            logger.error(f"An error occurred while retrieving the contact: {e}")
            return None
        finally:
            self.conn.close()

    def get_contact_by_name(self, name):
        """Retrieves a specific contact by its name."""
        logger.info(f"Retrieving contact with name: {name}")
        try:
            self.conn = sqlite3.connect(self.db_name)
            self.cursor = self.conn.cursor()

            self.cursor.execute("SELECT * FROM contacts WHERE name = ?", (name,))
            contact = self.cursor.fetchone()
            logger.debug(f"Retrieved contact: {contact}")

            return contact
        except sqlite3.Error as e:
            logger.error(f"An error occurred while retrieving the contact: {e}")
            return None
        finally:
            self.conn.close()

    def update_contact(self, contact_id, name, numbers, email, address, company, position, notes, image):
        """Updates an existing contact in the database."""
        logger.info(f"Updating contact with ID: {contact_id}")
        try:
            self.conn = sqlite3.connect(self.db_name)
            self.cursor = self.conn.cursor()

            self.cursor.execute("""
                UPDATE contacts 
                SET name = ?, numbers = ?, email = ?, address = ?, company = ?, position = ?, notes = ?, image = ?
                WHERE id = ?
            """, (name, numbers, email, address, company, position, notes, image, contact_id))

            self.conn.commit()
            logger.debug(f"Contact with ID {contact_id} updated successfully")
        except sqlite3.Error as e:
            logger.error(f"An error occurred while updating the contact: {e}")
        finally:
            self.conn.close()

    def delete_contact(self, contact_id):
        """Deletes a contact from the database."""
        logger.info(f"Deleting contact with ID: {contact_id}")
        try:
            self.conn = sqlite3.connect(self.db_name)
            self.cursor = self.conn.cursor()

            self.cursor.execute("DELETE FROM contacts WHERE id = ?", (contact_id,))

            self.conn.commit()
            logger.debug(f"Contact with ID {contact_id} deleted successfully")
        except sqlite3.Error as e:
            logger.error(f"An error occurred while deleting the contact: {e}")
        finally:
            self.conn.close()