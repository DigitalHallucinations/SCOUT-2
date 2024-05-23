# modules/Tools/Comms/Voip/modules/phone.py

from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout, QPushButton, QGridLayout, QHBoxLayout
from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap
from modules.logging.logger import setup_logger
from modules.Tools.Comms.Voip.modules.Voice.voice_call_twilio import make_call, end_call
import pyaudio
import threading

logger = setup_logger('phone.py')

class PhoneFrame(QWidget):
    def __init__(self, db, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.db = db 
        self.call_active = False
        self.audio_stream = None
        self.audio_thread = None
        self.current_call_sid = None
        logger.info("Initializing PhoneFrame")
        try:
            layout = QVBoxLayout(self)

            self.profile_pic_label = QLabel()
            self.profile_pic_label.setFixedSize(100, 100)
            self.profile_pic_label.setStyleSheet("border: None")
            layout.addWidget(self.profile_pic_label, alignment=Qt.AlignCenter)

            self.number_display = QLabel("")
            self.number_display.setAlignment(Qt.AlignCenter)
            self.number_display.setStyleSheet("color: #ffffff;")
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
                        border-radius: 50px;
                        padding: 10px;
                    }
                """)
                dialpad_layout.addWidget(button, i // 3, i % 3)

            # Call Control Buttons
            call_controls_layout = QHBoxLayout()
            layout.addLayout(call_controls_layout)

            self.call_button = QPushButton("Call")
            self.call_button.setCheckable(True)
            self.call_button.clicked.connect(self.handle_call)
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
            #logger.info(f"Updating profile picture for contact: {contact}")
            if contact[11]:  # Check if there is a profile picture
                pixmap = QPixmap()
                if pixmap.loadFromData(contact[11]):
                    self.profile_pic_label.setPixmap(pixmap.scaled(100, 100, Qt.KeepAspectRatio, Qt.SmoothTransformation))
                    logger.info("Profile picture updated successfully")
                else:
                    logger.warning(f"Failed to load profile picture for contact: {contact[1]}")  # Log contact name instead of data
            else:
                self.profile_pic_label.clear()
                logger.info("No profile picture found for contact")
        except Exception as e:
            logger.error(f"An error occurred while updating the profile picture: {e}", exc_info=True)

    def update_current_contact(self, contact_name):
        try:
            logger.info(f"Updating current contact to: {contact_name}")
            contact = self.db.get_contact_by_name(contact_name)  # Use self.db instead of creating a new instance
            if contact:
                self.update_profile_picture(contact)
                logger.info(f"Current contact updated to: {contact_name}")
            else:
                logger.warning(f"Contact not found: {contact_name}")
        except Exception as e:
            logger.error(f"Failed to update current contact: {e}", exc_info=True)

    def handle_call(self):
        try:
            if self.call_button.isChecked():
                self.call_button.setText("End")
                to_number = self.number_display.text()
                self.current_call_sid = make_call(to_number)
            else:
                self.call_button.setText("Call")
                if self.current_call_sid:
                    end_call(self.current_call_sid)
                    self.current_call_sid = None
        except Exception as e:
            logger.error(f"An error occurred while handling the call: {e}", exc_info=True)

    def start_audio_stream(self):
        try:
            self.audio_stream = pyaudio.PyAudio()
            self.audio_thread = threading.Thread(target=self.audio_stream_thread)
            self.audio_thread.start()
        except Exception as e:
            logger.error(f"An error occurred while starting the audio stream: {e}", exc_info=True)

    def stop_audio_stream(self):
        try:
            if self.audio_stream:
                self.audio_stream.terminate()
            if self.audio_thread:
                self.audio_thread.join()
        except Exception as e:
            logger.error(f"An error occurred while stopping the audio stream: {e}", exc_info=True)

    def audio_stream_thread(self):
        try:
            stream = self.audio_stream.open(format=pyaudio.paInt16,
                                            channels=1,
                                            rate=44100,
                                            input=True,
                                            output=True,
                                            frames_per_buffer=1024)
            while self.call_active:
                data = stream.read(1024)
                stream.write(data, 1024)
            stream.stop_stream()
            stream.close()
        except Exception as e:
            logger.error(f"An error occurred in the audio stream thread: {e}", exc_info=True)