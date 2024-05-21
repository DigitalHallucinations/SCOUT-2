# modules/Tools/Voip_app.py

import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QHBoxLayout, QVBoxLayout
from modules.Tools.Comms.Voip.modules.header_frame import create_header_frame
from modules.Tools.Comms.Voip.modules.phone import PhoneFrame
from modules.Tools.Comms.Voip.modules.messages import ConversationFrame
from modules.Tools.Comms.Voip.modules.contacts_frame import ContactsFrame
from modules.Tools.Comms.Voip.modules.Contacts.contact_details import ContactDetailsFrame
from modules.Tools.Comms.Voip.modules.Contacts.upload_profile_picture import UploadProfilePictureFrame
from modules.logging.logger import setup_logger

logger = setup_logger('Voip_app.py')

class VoIPApp(QMainWindow):
    def __init__(self):
        super().__init__()
        logger.info("Initializing VoIPApp")
        try:
            self.setWindowTitle("VoIP App")
            self.setGeometry(100, 100, 400, 600)

            central_widget = QWidget()
            central_widget.setStyleSheet("background-color: transparent;")
            main_layout = QVBoxLayout(central_widget)
            self.setCentralWidget(central_widget)

            create_header_frame(self, main_layout)

            self.content_layout = QHBoxLayout()
            main_layout.addLayout(self.content_layout)

            self.contacts_frame = ContactsFrame(self)
            self.content_layout.addWidget(self.contacts_frame)
            self.contacts_frame.hide()

            right_side_layout = QVBoxLayout()
            self.content_layout.addLayout(right_side_layout, 2)

            self.conversation_frame = ConversationFrame()
            right_side_layout.addWidget(self.conversation_frame)

            self.phone_frame = PhoneFrame()
            right_side_layout.addWidget(self.phone_frame)
            self.phone_frame.hide()

            self.contact_details_frame = ContactDetailsFrame(self)
            right_side_layout.addWidget(self.contact_details_frame)
            self.contact_details_frame.hide()

            self.upload_profile_picture_frame = UploadProfilePictureFrame(self)
            right_side_layout.addWidget(self.upload_profile_picture_frame)
            self.upload_profile_picture_frame.hide()

            self.previous_frame = None

            logger.debug("VoIPApp initialized successfully")
        except Exception as e:
            logger.error(f"An error occurred while initializing the VoIPApp: {e}", exc_info=True)

    def toggle_contact_details(self):
        logger.info("Attempting to toggle contact details.")
        try:
            if self.contact_details_frame.isVisible():
                logger.debug("Contact details frame is visible, hiding it.")
                self.contact_details_frame.hide()
                if self.previous_frame:
                    self.previous_frame.show()
            else:
                logger.debug("Contact details frame is not visible, showing it.")
                self.previous_frame = None
                if self.conversation_frame.isVisible():
                    self.previous_frame = self.conversation_frame
                    self.conversation_frame.hide()
                elif self.phone_frame.isVisible():
                    self.previous_frame = self.phone_frame
                    self.phone_frame.hide()
                self.contact_details_frame.show()
        except Exception as e:
            logger.error(f"An error occurred while toggling contact details: {e}", exc_info=True)

    def toggle_upload_frame(self):
        logger.info("Attempting to toggle upload profile picture frame.")
        try:
            if self.upload_profile_picture_frame.isVisible():
                logger.debug("Upload profile picture frame is visible, hiding it.")
                self.upload_profile_picture_frame.hide()
                self.contact_details_frame.show()
            else:
                logger.debug("Upload profile picture frame is not visible, showing it.")
                self.contact_details_frame.hide()
                self.upload_profile_picture_frame.show()
        except Exception as e:
            logger.error(f"An error occurred while toggling upload profile picture frame: {e}", exc_info=True)

    def toggle_call_button(self):
        try:
            if self.sender().isChecked():
                self.sender().setText("End")
            else:
                self.sender().setText("Call")
        except Exception as e:
            logger.error(f"An error occurred while toggling the call button: {e}", exc_info=True)

    def toggle_contacts(self):
        try:
            if self.contacts_frame.isVisible():
                self.contacts_frame.hide()
            else:
                self.contacts_frame.show()
        except Exception as e:
            logger.error(f"An error occurred while toggling contacts: {e}", exc_info=True)

    def show_phone_page(self):
        try:
            self.conversation_frame.hide()
            self.contact_details_frame.hide()
            self.upload_profile_picture_frame.hide()
            self.phone_frame.show()
        except Exception as e:
            logger.error(f"An error occurred while showing the phone page: {e}", exc_info=True)

    def show_messages_page(self):
        try:
            self.phone_frame.hide()
            self.contact_details_frame.hide()
            self.upload_profile_picture_frame.hide()
            self.conversation_frame.show()
        except Exception as e:
            logger.error(f"An error occurred while showing the messages page: {e}", exc_info=True)

    def update_profile_picture(self, profile_pic_data):
        try:
            self.contact_details_frame.update_profile_picture(profile_pic_data)
        except Exception as e:
            logger.error(f"An error occurred while updating the profile picture: {e}", exc_info=True)

    def update_current_contact(self, contact_name):
        self.conversation_frame.update_current_contact(contact_name)
        self.phone_frame.update_current_contact(contact_name)

if __name__ == "__main__":
    try:
        app = QApplication(sys.argv)
        window = VoIPApp()
        window.show()
        sys.exit(app.exec())
    except Exception as e:
        logger.error(f"An error occurred in the main application: {e}", exc_info=True)