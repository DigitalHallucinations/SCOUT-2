# modules/Tools/Voip/modules/contacts.py

from PySide6 import QtWidgets as qtw
from PySide6 import QtGui as qtg
from PySide6 import QtCore as qtc
from modules.Tools.Comms.Voip.modules.Contacts.contacts_db import ContactsDatabase
from modules.logging.logger import setup_logger

logger = setup_logger('Contacts_Frame.py')

class ContactsFrame(qtw.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.setStyleSheet("background-color: transparent;")
        layout = qtw.QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        # Create a frame for the buttons and add it to the layout
        button_frame = qtw.QFrame()
        button_layout = qtw.QHBoxLayout(button_frame)
        button_layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(button_frame)

        icon_size = 24

        self.add_button = qtw.QPushButton(button_frame)
        self.add_button.setIcon(qtg.QIcon("assets/SCOUT/Icons/Voip_icons/add_wt.png"))
        self.add_button.setIconSize(qtc.QSize(icon_size, icon_size))
        self.add_button.setStyleSheet("QPushButton { background-color: transparent; border: none; }")
        self.add_button.clicked.connect(self.show_contact_details)
        button_layout.addWidget(self.add_button)

        self.edit_button = qtw.QPushButton(button_frame)
        self.edit_button.setIcon(qtg.QIcon("assets/SCOUT/Icons/Voip_icons/edit_wt.png"))
        self.edit_button.setIconSize(qtc.QSize(icon_size, icon_size))
        self.edit_button.setStyleSheet("QPushButton { background-color: transparent; border: none; }")
        self.edit_button.clicked.connect(self.edit_contact)
        button_layout.addWidget(self.edit_button)

        # Create the contact list and add it to the layout
        self.contact_list = qtw.QListWidget()
        self.contact_list.setStyleSheet("""
            QListWidget {
                background-color: #2d2d2d;
                color: #ffffff;
                border: none;
                border-radius: 10px;
                padding: 2px 0 0 2px;
            }
            QListWidgetItem {
                padding-left: 2px;
            }
        """)
        layout.addWidget(self.contact_list)

        self.contact_list.setContextMenuPolicy(qtc.Qt.CustomContextMenu)
        self.contact_list.customContextMenuRequested.connect(self.show_context_menu)
        self.contact_list.itemClicked.connect(self.display_selected_contact)

        self.db = ContactsDatabase()
        self.load_contacts()

    def load_contacts(self):
        logger.info("Loading contacts from the database")
        try:
            self.contact_list.clear()  # Clear the list before loading new contacts
            contacts = self.db.get_all_contacts()
            max_width = 0
            for contact in contacts:
                self.contact_list.addItem(contact[1])
                # Calculate the width of the contact name
                font_metrics = self.contact_list.fontMetrics()
                width = font_metrics.horizontalAdvance(contact[1])
                if width > max_width:
                    max_width = width
            # Set the width of the QListWidget to the width of the longest contact name
            self.contact_list.setFixedWidth(max_width + 20)  # Add some padding
            logger.debug(f"Loaded {len(contacts)} contacts successfully")
        except Exception as e:
            logger.error(f"An error occurred while loading contacts: {e}")

    def show_contact_details(self):
        logger.info("Attempting to show contact details page.")
        if self.parent:
            logger.debug("Parent exists, calling toggle_contact_details.")
            self.parent.toggle_contact_details()
        else:
            logger.debug("Parent does not exist, cannot call toggle_contact_details.")

    def edit_contact(self):
        logger.info("Editing contact")
        try:
            selected_item = self.contact_list.currentItem()
            if selected_item is not None:
                current_name = selected_item.text()
                contact_id = self.get_contact_id_by_name(current_name)
                if contact_id is not None:
                    contact = self.db.get_contact_by_id(contact_id)
                    if self.parent:
                        self.parent.contact_details_frame.load_contact(contact)
                        self.parent.toggle_contact_details()
        except Exception as e:
            logger.error(f"An error occurred while editing the contact: {e}")

    def get_contact_id_by_name(self, name):
        logger.info(f"Retrieving contact ID for {name}")
        try:
            contacts = self.db.get_all_contacts()
            for contact in contacts:
                if contact[1] == name:
                    logger.debug(f"Found contact ID: {contact[0]}")
                    return contact[0]
            logger.debug(f"Contact ID not found for {name}")
            return None
        except Exception as e:
            logger.error(f"An error occurred while retrieving the contact ID: {e}")
            return None

    def show_context_menu(self, position):
        menu = qtw.QMenu()
        edit_contact_action = menu.addAction("Edit Contact")
        edit_contact_action.triggered.connect(self.edit_contact)

        menu.exec_(self.contact_list.viewport().mapToGlobal(position))

    def display_selected_contact(self, item):
        contact_name = item.text()
        if self.parent:
            self.parent.conversation_frame.update_current_contact(contact_name)

    def get_contact_phone_number(self, contact_name):
        logger.info(f"Retrieving phone number for contact: {contact_name}")
        try:
            contact = self.db.get_contact_by_name(contact_name)
            if contact:
                phone_number = contact[2]  
                logger.debug(f"Phone number for {contact_name} is {phone_number}")
                return phone_number
            else:
                logger.debug(f"No contact found with name: {contact_name}")
                return None
        except Exception as e:
            logger.error(f"An error occurred while retrieving the phone number: {e}")
            return None