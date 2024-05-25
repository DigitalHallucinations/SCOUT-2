# modules/Tools/Comms/Voip/modules/messages.py

from PySide6.QtWidgets import QWidget, QLabel, QTextEdit, QVBoxLayout, QSpacerItem, QHBoxLayout, QSizePolicy, QFrame, QPushButton
from PySide6.QtGui import QIcon, QFont, QPixmap
from PySide6.QtCore import Qt, QDateTime, QSize
from modules.Tools.Comms.Voip.modules.emoji.emoji_picker import EmojiPicker
from modules.Tools.Comms.Voip.modules.messaging.Twilio.send_sms_twilio import send_sms
from modules.Tools.Comms.Voip.modules.Contacts.contacts_db import ContactsDatabase
from modules.Tools.Comms.Voip.modules.messaging.Twilio.Twilio_verify import TwilioVerify
from modules.logging.logger import setup_logger


logger = setup_logger('messages.py')


class ConversationFrame(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent  
        self.db = ContactsDatabase()  

        # Twilio Verify instance
        self.twilio_verify = TwilioVerify('your_account_sid', 'your_auth_token', 'your_verify_service_sid')

        rich_text_tool_bar_icon_size = 24
        sidebar_frame_icon_size = 30

        # Main Layout
        main_layout = QHBoxLayout(self)

        # Left Side: Conversation, Rich text Toolbar, and Input
        left_layout = QVBoxLayout()
        left_layout.setSpacing(5)
        main_layout.addLayout(left_layout)

        # Current contact Display
        self.current_contact = QWidget()
        self.current_contact.setStyleSheet("""
            QWidget {
                background-color: #2d2d2d; 
                color: #ffffff; 
                border-radius: 10px; 
                padding: 5px; 
                border: 1px solid #ffffff;
            }
        """)
        contact_layout = QHBoxLayout(self.current_contact)
        self.contact_label = QLabel(self.current_contact)
        self.contact_label.setContentsMargins(0, 0, 0, 0)
        self.contact_label.setStyleSheet("color: #ffffff;")
        contact_layout.addWidget(self.contact_label)

        # Profile Picture
        self.profile_pic_label = QLabel(self.current_contact)
        self.profile_pic_label.setFixedSize(50, 50)
        self.profile_pic_label.setStyleSheet("border-radius: 25px; border: 1px solid #ffffff;")
        contact_layout.addWidget(self.profile_pic_label)

        left_layout.addWidget(self.current_contact)

        # Conversation Area
        self.conversation_area = QLabel("")
        self.conversation_area.setAlignment(Qt.AlignTop)
        self.conversation_area.setStyleSheet("""
            QLabel {
                background-color: #2d2d2d; 
                color: #ffffff; 
                border-radius: 10px; 
                padding: 5px; 
            }
        """)
        self.conversation_area.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        left_layout.addWidget(self.conversation_area)

        # Spacer
        spacer = QSpacerItem(20, 4, QSizePolicy.Minimum, QSizePolicy.Fixed)
        left_layout.addItem(spacer)

        # Text Input Frame
        input_frame = QWidget()
        input_frame.setStyleSheet("""
            QWidget {
                background-color: #2d2d2d; 
                color: #ffffff; 
                border-radius: 10px; 
                padding: 5px; 
            }
        """)
        input_layout = QVBoxLayout(input_frame)
        input_layout.setContentsMargins(0, 0, 0, 0)
        input_layout.setSpacing(0)

        # Text Input 
        text_input_layout = QHBoxLayout()
        text_input_layout.setContentsMargins(0, 0, 0, 0)
        text_input_layout.setSpacing(0)

        self.text_input = QTextEdit()
        self.text_input.setStyleSheet("""
            QTextEdit {
                background-color: #2d2d2d; 
                color: #ffffff; 
                border-radius: 10px; 
                padding: 5px; 
            }
        """)
        self.text_input.setLineWrapMode(QTextEdit.WidgetWidth)  
        self.text_input.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.text_input.setFixedHeight(self.text_input.fontMetrics().lineSpacing() * 15)
        text_input_layout.addWidget(self.text_input)

        # sidebar Frame
        sidebar_frame = QFrame()
        button_layout = QVBoxLayout(sidebar_frame)
        button_layout.setContentsMargins(0, 0, 0, 0)
        button_layout.setSpacing(0)

        # Spacer
        button_layout.addStretch()

        # Attach Button
        attach_button = QPushButton()
        attach_button.setIcon(QIcon("assets/SCOUT/Icons/Voip_icons/paperclip_wt.png"))
        attach_button.setIconSize(QSize(sidebar_frame_icon_size, sidebar_frame_icon_size))
        attach_button.setStyleSheet("background: transparent;")
        attach_button.clicked.connect(self.do_nothing)
        button_layout.addWidget(attach_button)

        def on_attach_button_hover(event):
            attach_button.setIcon(QIcon("assets/SCOUT/Icons/Voip_icons/paperclip_bl.png"))

        def on_attach_button_leave(event):
            attach_button.setIcon(QIcon("assets/SCOUT/Icons/Voip_icons/paperclip_wt.png"))

        attach_button.enterEvent = lambda event: on_attach_button_hover(event)
        attach_button.leaveEvent = lambda event: on_attach_button_leave(event)

        # Send Button
        send_button = QPushButton()
        send_button.setIcon(QIcon("assets/SCOUT/Icons/Voip_icons/send_wt.png"))
        send_button.setIconSize(QSize(sidebar_frame_icon_size, sidebar_frame_icon_size))
        send_button.setStyleSheet("background: transparent;")
        send_button.clicked.connect(self.send_message)
        button_layout.addWidget(send_button)

        def on_send_button_hover(event):
            send_button.setIcon(QIcon("assets/SCOUT/Icons/Voip_icons/send_bl.png"))

        def on_send_button_leave(event):
            send_button.setIcon(QIcon("assets/SCOUT/Icons/Voip_icons/send_wt.png"))

        send_button.enterEvent = lambda event: on_send_button_hover(event)
        send_button.leaveEvent = lambda event: on_send_button_leave(event)

        text_input_layout.addWidget(sidebar_frame)
        input_layout.addLayout(text_input_layout)

        # Rich Text Button Frame
        rich_text_tool_bar = QFrame()
        rich_text_tool_bar.setFixedHeight(35)
        rich_text_tool_bar.setStyleSheet(""" 
            QFrame { 
                background-color: #2d2d2d; 
                border-radius: 10px; 
                padding: 5px; 
            }
        """)
        button_layout = QHBoxLayout(rich_text_tool_bar)
        button_layout.setContentsMargins(0, 0, 0, 0)
        button_layout.setSpacing(0)

        bold_button = QPushButton()
        bold_button.setIcon(QIcon("assets/SCOUT/Icons/Voip_icons/bold_wt.png"))
        bold_button.setIconSize(QSize(rich_text_tool_bar_icon_size, rich_text_tool_bar_icon_size))
        bold_button.setStyleSheet("background: transparent;")
        bold_button.clicked.connect(self.make_text_bold)
        button_layout.addWidget(bold_button)

        def on_bold_button_hover(event):
            bold_button.setIcon(QIcon("assets/SCOUT/Icons/Voip_icons/bold_bl.png"))

        def on_bold_button_leave(event):
            bold_button.setIcon(QIcon("assets/SCOUT/Icons/Voip_icons/bold_wt.png"))

        bold_button.enterEvent = lambda event: on_bold_button_hover(event)
        bold_button.leaveEvent = lambda event: on_bold_button_leave(event)

        italic_button = QPushButton()
        italic_button.setIcon(QIcon("assets/SCOUT/Icons/Voip_icons/italic_wt.png"))
        italic_button.setIconSize(QSize(rich_text_tool_bar_icon_size, rich_text_tool_bar_icon_size))
        italic_button.setStyleSheet("background: transparent;")
        italic_button.clicked.connect(self.make_text_italic)
        button_layout.addWidget(italic_button)

        def on_italic_button_hover(event):
            italic_button.setIcon(QIcon("assets/SCOUT/Icons/Voip_icons/italic_bl.png"))

        def on_italic_button_leave(event):
            italic_button.setIcon(QIcon("assets/SCOUT/Icons/Voip_icons/italic_wt.png"))

        italic_button.enterEvent = lambda event: on_italic_button_hover(event)
        italic_button.leaveEvent = lambda event: on_italic_button_leave(event)

        underline_button = QPushButton()
        underline_button.setIcon(QIcon("assets/SCOUT/Icons/Voip_icons/underline_wt.png"))
        underline_button.setIconSize(QSize(rich_text_tool_bar_icon_size, rich_text_tool_bar_icon_size))
        underline_button.setStyleSheet("background: transparent;")
        underline_button.clicked.connect(self.make_text_underline)
        button_layout.addWidget(underline_button)

        def on_underline_button_hover(event):
            underline_button.setIcon(QIcon("assets/SCOUT/Icons/Voip_icons/underline_bl.png"))

        def on_underline_button_leave(event):
            underline_button.setIcon(QIcon("assets/SCOUT/Icons/Voip_icons/underline_wt.png"))

        underline_button.enterEvent = lambda event: on_underline_button_hover(event)
        underline_button.leaveEvent = lambda event: on_underline_button_leave(event)

        # Emoji Button
        emoji_button = QPushButton()
        emoji_button.setIcon(QIcon("assets/SCOUT/Icons/Voip_icons/emoji_sml.png"))
        emoji_button.setIconSize(QSize(rich_text_tool_bar_icon_size, rich_text_tool_bar_icon_size))
        emoji_button.setStyleSheet("background: transparent;")
        emoji_button.clicked.connect(self.insert_emoji)
        button_layout.addWidget(emoji_button)

        def on_emoji_button_hover(event):
            emoji_button.setIcon(QIcon("assets/SCOUT/Icons/Voip_icons/emoji_lg.png"))

        def on_emoji_button_leave(event):
            emoji_button.setIcon(QIcon("assets/SCOUT/Icons/Voip_icons/emoji_sml.png"))

        emoji_button.enterEvent = lambda event: on_emoji_button_hover(event)
        emoji_button.leaveEvent = lambda event: on_emoji_button_leave(event)

        # Spacer
        button_layout.addStretch()

        input_layout.addWidget(rich_text_tool_bar)

        left_layout.addWidget(input_frame)

        # Verify Button
        self.verify_button = QPushButton("Verify")
        self.verify_button.clicked.connect(self.send_verification_request)
        left_layout.addWidget(self.verify_button)

    def send_message(self):
        try:
            message = self.text_input.toPlainText()  # Extract plain text from QTextEdit
            if message:
                timestamp = QDateTime.currentDateTime().toString("hh:mm ap")
                new_message = f"<font color='gray'>{timestamp}</font> <font color='blue'>[Sent]</font> {message}<br>"
                self.conversation_area.setText(self.conversation_area.text() + new_message)
                self.text_input.clear()

                # Send the message via Twilio
                contact_name = self.contact_label.text()
                contact_phone_number = self.get_contact_phone_number(contact_name)
                if contact_phone_number:
                    send_sms(contact_phone_number, message)
                    logger.info(f"Message sent to {contact_name} ({contact_phone_number}): {message}")
                else:
                    logger.warning(f"Contact phone number not found for {contact_name}")
        except Exception as e:
            logger.error(f"Failed to send message: {e}")

    def make_text_bold(self):
        try:
            self.text_input.setFontWeight(QFont.Bold if self.text_input.fontWeight() != QFont.Bold else QFont.Normal)
        except Exception as e:
            logger.error(f"Failed to toggle bold text: {e}")

    def make_text_italic(self):
        try:
            self.text_input.setFontItalic(not self.text_input.fontItalic)
        except Exception as e:
            logger.error(f"Failed to toggle italic text: {e}")

    def make_text_underline(self):
        try:
            self.text_input.setFontUnderline(not self.text_input.fontUnderline)
        except Exception as e:
            logger.error(f"Failed to toggle underline text: {e}")

    def insert_emoji(self):
        try:
            emoji_picker = EmojiPicker(self)
            if emoji_picker.exec():
                emoji = emoji_picker.selected_emoji
                self.text_input.insertPlainText(emoji)
        except Exception as e:
            logger.error(f"Failed to insert emoji: {e}")

    def do_nothing(self):
        logger.info("Attach button clicked, but no action is defined.")

    def update_current_contact(self, contact_name):
        try:
            self.contact_label.setText(contact_name)
            contact = self.db.get_contact_by_name(contact_name)
            if contact and contact[11]:  # Assuming the image is stored in the 11th column
                pixmap = QPixmap()
                if isinstance(contact[11], bytes) and len(contact[11]) > 0:
                    pixmap.loadFromData(contact[11])
                    if not pixmap.isNull():
                        self.profile_pic_label.setPixmap(pixmap.scaled(self.profile_pic_label.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation))
                    else:
                        logger.warning(f"Failed to load profile picture for contact: {contact_name}")  # Log contact name instead of data
                else:
                    logger.warning(f"Invalid image data for contact: {contact_name}")  # Log contact name instead of data
            else:
                self.profile_pic_label.clear()
            logger.info(f"Current contact updated to: {contact_name}")
        except Exception as e:
            logger.error(f"Failed to update current contact: {e}")

    def get_contact_phone_number(self, contact_name):
        try:
            contact = self.db.get_contact_by_name(contact_name)
            if contact:
                return contact[2]  
            return None
        except Exception as e:
            logger.error(f"Failed to get contact phone number for {contact_name}: {e}")
            return None

    def send_verification_request(self):
        try:
            contact_name = self.contact_label.text()
            contact_phone_number = self.get_contact_phone_number(contact_name)
            if contact_phone_number:
                # Send verification request using Twilio Verify API
                verification_sid = self.twilio_verify.send_verification_request(contact_phone_number)
                if verification_sid:
                    logger.info(f"Verification request sent to {contact_name} ({contact_phone_number})")
                else:
                    logger.warning(f"Failed to send verification request to {contact_name} ({contact_phone_number})")
            else:
                logger.warning(f"Contact phone number not found for {contact_name}")
        except Exception as e:
            logger.error(f"Failed to send verification request: {e}")

    def check_verification_status(self, contact_phone_number, code):
        try:
            is_verified = self.twilio_verify.check_verification_status(contact_phone_number, code)
            if is_verified:
                logger.info(f"Verification successful for {contact_phone_number}")
            else:
                logger.warning(f"Verification failed for {contact_phone_number}")
            return is_verified
        except Exception as e:
            logger.error(f"Failed to check verification status: {e}")
            return False