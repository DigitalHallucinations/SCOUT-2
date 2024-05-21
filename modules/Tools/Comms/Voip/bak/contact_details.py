# modules/Tools/Comms/Voip/modules/Contacts/contact_details.py

from PySide6 import QtWidgets as qtw
from PySide6 import QtCore as qtc
from PySide6 import QtGui as qtg
from modules.logging.logger import setup_logger
from modules.Tools.Comms.Voip.modules.Contacts.contacts_db import ContactsDatabase  # Import ContactsDatabase

logger = setup_logger('contact_details.py')

class ContactDetailsFrame(qtw.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.db = ContactsDatabase()
        self.profile_pic_data = None
        self.setup_ui()

    def setup_ui(self):
        layout = qtw.QVBoxLayout(self)

        self.profile_pic_label = qtw.QLabel()
        self.profile_pic_label.setFixedSize(100, 100)
        self.profile_pic_label.setStyleSheet("border: 1px solid #ffffff; border-radius: 50px;")
        layout.addWidget(self.profile_pic_label, alignment=qtc.Qt.AlignCenter)

        self.profile_pic_button = qtw.QPushButton("Upload Profile Picture")
        self.profile_pic_button.clicked.connect(self.show_upload_profile_picture_frame)
        layout.addWidget(self.profile_pic_button)

        self.name_edit = qtw.QLineEdit()
        self.numbers_edit = qtw.QLineEdit()
        self.email_edit = qtw.QLineEdit()
        self.address_edit = qtw.QLineEdit()
        self.company_edit = qtw.QLineEdit()
        self.position_edit = qtw.QLineEdit()
        self.notes_edit = qtw.QTextEdit()
        self.group_combo = qtw.QComboBox()

        self.group_combo.addItems(["Family", "Friends", "Work", "Others"])
        layout.addWidget(self.group_combo)

        name_label = qtw.QLabel("Name:")
        number_label = qtw.QLabel("Number:")
        email_label = qtw.QLabel("Email:")
        address_label = qtw.QLabel("Address:")
        company_label = qtw.QLabel("Company:")
        position_label = qtw.QLabel("Position:")
        notes_label = qtw.QLabel("Notes:")

        layout.addWidget(name_label)
        layout.addWidget(self.name_edit)
        layout.addWidget(number_label)
        layout.addWidget(self.numbers_edit)
        layout.addWidget(email_label)
        layout.addWidget(self.email_edit)
        layout.addWidget(address_label)
        layout.addWidget(self.address_edit)
        layout.addWidget(company_label)
        layout.addWidget(self.company_edit)
        layout.addWidget(position_label)
        layout.addWidget(self.position_edit)
        layout.addWidget(notes_label)
        layout.addWidget(self.notes_edit)

        button_layout = qtw.QHBoxLayout()
        self.add_button = qtw.QPushButton("Add")
        self.edit_button = qtw.QPushButton("Edit")
        self.delete_button = qtw.QPushButton("Delete")

        button_layout.addWidget(self.add_button)
        button_layout.addWidget(self.edit_button)
        button_layout.addWidget(self.delete_button)

        layout.addLayout(button_layout)

        self.add_button.clicked.connect(self.add_contact)
        self.edit_button.clicked.connect(self.edit_contact)
        self.delete_button.clicked.connect(self.delete_contact)

        self.apply_styles()

    def apply_styles(self):
        self.setStyleSheet("""
            QWidget {
                background-color: #2d2d2d;
                color: #ffffff;
                border-radius: 10px;
            }
            QLineEdit, QTextEdit {
                background-color: #2d2d2d;
                color: #ffffff;
                border: 1px solid #ffffff;
                border-radius: 5px;
                padding: 5px;
            }
            QLabel {
                background-color: transparent;
                color: #ffffff;
            }
            QPushButton {
                background-color: #2d2d2d;
                color: #ffffff;
                border: 1px solid #ffffff;
                border-radius: 5px;
                padding: 5px;
            }
            QPushButton:hover {
                background-color: #3d3d3d;
            }
        """)

    def add_contact(self):
        logger.info("Adding contact")
        name = self.name_edit.text()
        number = self.numbers_edit.text()
        email = self.email_edit.text()
        address = self.address_edit.text()
        company = self.company_edit.text()
        position = self.position_edit.text()
        notes = self.notes_edit.toPlainText()

        if name and number:  # Ensure that name and number are provided
            try:
                self.db.add_contact(name, number, email, address, company, position, notes, None, self.profile_pic_data)
                self.parent.contacts_frame.load_contacts()  # Refresh the contact list
                logger.info(f"Contact {name} added successfully")
                self.parent.toggle_contact_details()  # Hide contact details frame
            except Exception as e:
                logger.error(f"An error occurred while adding the contact: {e}")
        else:
            qtw.QMessageBox.warning(self, 'Input Error', 'Name and Number are required fields.')

    def edit_contact(self):
        logger.info("Editing contact")
        selected_item = self.parent.contacts_frame.contact_list.currentItem()
        if selected_item is not None:
            current_name = selected_item.text()
            contact_id = self.parent.contacts_frame.get_contact_id_by_name(current_name)

            name = self.name_edit.text()
            number = self.numbers_edit.text()
            email = self.email_edit.text()
            address = self.address_edit.text()
            company = self.company_edit.text()
            position = self.position_edit.text()
            notes = self.notes_edit.toPlainText()

            if name and number:  # Ensure that name and number are provided
                try:
                    self.db.update_contact(contact_id, name, number, email, address, company, position, notes, self.profile_pic_data)
                    self.parent.contacts_frame.load_contacts()  # Refresh the contact list
                    logger.info(f"Contact {name} updated successfully")
                    self.parent.toggle_contact_details()  # Hide contact details frame
                except Exception as e:
                    logger.error(f"An error occurred while updating the contact: {e}")
            else:
                qtw.QMessageBox.warning(self, 'Input Error', 'Name and Number are required fields.')
        else:
            qtw.QMessageBox.warning(self, 'Selection Error', 'No contact selected to edit.')
            
    def delete_contact(self):
        logger.info("Deleting contact")
        selected_item = self.parent.contacts_frame.contact_list.currentItem()
        if selected_item is not None:
            current_name = selected_item.text()
            contact_id = self.parent.contacts_frame.get_contact_id_by_name(current_name)

            reply = qtw.QMessageBox.question(self, 'Delete Contact',
                                            f"Are you sure you want to delete {current_name}?",
                                            qtw.QMessageBox.Yes | qtw.QMessageBox.No, qtw.QMessageBox.No)
            if reply == qtw.QMessageBox.Yes:
                try:
                    self.db.delete_contact(contact_id)
                    self.parent.contacts_frame.load_contacts()  # Refresh the contact list
                    logger.info(f"Contact {current_name} deleted successfully")
                    self.parent.toggle_contact_details()  # Hide contact details frame
                except Exception as e:
                    logger.error(f"An error occurred while deleting the contact: {e}")
        else:
            qtw.QMessageBox.warning(self, 'Selection Error', 'No contact selected to delete.')

    def load_contact(self, contact):
        self.name_edit.setText(contact[1])
        self.numbers_edit.setText(contact[2])
        self.email_edit.setText(contact[3])
        self.address_edit.setText(contact[4])
        self.company_edit.setText(contact[5])
        self.position_edit.setText(contact[6])
        self.notes_edit.setPlainText(contact[7])
        if contact[10]:  # Check if there is a profile picture
            pixmap = qtg.QPixmap()
            pixmap.loadFromData(contact[10])
            self.profile_pic_label.setPixmap(pixmap.scaled(100, 100, qtc.Qt.KeepAspectRatio, qtc.Qt.SmoothTransformation))

    def show_upload_profile_picture_frame(self):
        if self.parent:
            self.parent.toggle_upload_frame()

    def update_profile_picture(self, profile_pic_data):
        self.profile_pic_data = profile_pic_data
        if self.profile_pic_data:
            pixmap = qtg.QPixmap()
            pixmap.loadFromData(self.profile_pic_data)  # Ensure this is bytes
            self.profile_pic_label.setPixmap(pixmap.scaled(100, 100, qtc.Qt.KeepAspectRatio, qtc.Qt.SmoothTransformation))
            logger.info("Profile picture updated successfully")
        else:
            self.profile_pic_label.clear()
            logger.info("No profile picture data available")