# modules/Tools/Comms/Voip/modules/phone.py

from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout, QPushButton, QGridLayout, QHBoxLayout
from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap
from modules.logging.logger import setup_logger
from modules.Tools.Comms.Voip.modules.Contacts.contacts_db import ContactsDatabase

logger = setup_logger('phone.py')

class PhoneFrame(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.db = ContactsDatabase()  # Initialize the ContactsDatabase
        logger.info("Initializing PhoneFrame")
        try:
            layout = QVBoxLayout(self)

            self.profile_pic_label = QLabel()
            self.profile_pic_label.setFixedSize(100, 100)
            self.profile_pic_label.setStyleSheet("border: 1px solid #ffffff; border-radius: 50px;")
            layout.addWidget(self.profile_pic_label, alignment=Qt.AlignCenter)

            self.number_display = QLabel("")
            self.number_display.setAlignment(Qt.AlignCenter)
            layout.addWidget(self.number_display, 1)

            dialpad_layout = QGridLayout()
            layout.addLayout(dialpad_layout, 2)
            for i, digit in enumerate("123456789*0#"):
                button = QPushButton(digit)
                button.clicked.connect(lambda _, digit=digit: self.update_number_display(digit))
                button.setStyleSheet("""
                    QPushButton {
                        background-color: #2d2d2d; 
                        color: #ffffff;
                        border-radius: 50%; 
                        padding: 10px; 
                    }
                """)
                dialpad_layout.addWidget(button, i // 3, i % 3)

            # Call Control Buttons
            call_controls_layout = QHBoxLayout()
            layout.addLayout(call_controls_layout)

            self.call_button = QPushButton("Call")
            self.call_button.setCheckable(True)
            self.call_button.setStyleSheet("""
                QPushButton {
                    background-color: #2d2d2d; 
                    color: #ffffff;
                    border-radius: 15px; 
                    padding: 10px; 
                }
            """)
            call_controls_layout.addWidget(self.call_button)

            for label in ["Mute", "Hold"]:
                button = QPushButton(label)
                button.setStyleSheet("""
                    QPushButton {
                        background-color: #2d2d2d; 
                        color: #ffffff;
                        border-radius: 15px; 
                        padding: 10px; 
                    }
                """)
                call_controls_layout.addWidget(button)

            logger.info("PhoneFrame initialized successfully")
        except Exception as e:
            logger.error(f"An error occurred while initializing the PhoneFrame: {e}", exc_info=True)

    def update_number_display(self, digit):
        try:
            current_text = self.number_display.text()
            self.number_display.setText(current_text + digit)
        except Exception as e:
            logger.error(f"An error occurred while updating the number display: {e}", exc_info=True)

    def update_profile_picture(self, contact):
        try:
            logger.info(f"Updating profile picture for contact: {contact}")
            if contact[10]:  # Check if there is a profile picture
                pixmap = QPixmap()
                pixmap.loadFromData(contact[10])
                self.profile_pic_label.setPixmap(pixmap.scaled(100, 100, Qt.KeepAspectRatio, Qt.SmoothTransformation))
                logger.info("Profile picture updated successfully")
            else:
                self.profile_pic_label.clear()
                logger.info("No profile picture found for contact")
        except Exception as e:
            logger.error(f"An error occurred while updating the profile picture: {e}", exc_info=True)

    def update_current_contact(self, contact_name):
        try:
            self.number_display.setText(contact_name)
            contact = self.db.get_contact_by_name(contact_name)
            if contact and contact[10]: 
                pixmap = QPixmap()
                pixmap.loadFromData(contact[10])
                self.profile_pic_label.setPixmap(pixmap.scaled(100, 100, Qt.KeepAspectRatio, Qt.SmoothTransformation))
            else:
                self.profile_pic_label.clear()
            logger.info(f"Current contact updated to: {contact_name}")
        except Exception as e:
            logger.error(f"Failed to update current contact: {e}")