# speech_bar.py

# speech_bar.py
from datetime import datetime
from PySide6 import QtWidgets, QtGui, QtCore
from PySide6.QtWidgets import QMessageBox
from gui.tooltip import ToolTip
from modules.speech_services.GglCldSvcs.stt import SpeechToText
from modules.Providers.provider_manager import ProviderManager
from google.cloud import texttospeech
from modules.logging.logger import setup_logger

logger = setup_logger('speech_bar.py')

class SpeechBar(QtWidgets.QFrame):
    def __init__(self, parent=None, model_manager=None, speechbar_frame_bg=None, speechbar_font_color=None, speechbar_font_family=None, speechbar_font_size=None):
        super().__init__(parent)
        self.parent = parent
        self.model_manager = model_manager
        self.speechbar_frame_bg = speechbar_frame_bg
        self.speechbar_font_color = speechbar_font_color
        self.speechbar_font_family = speechbar_font_family
        self.speechbar_font_size = speechbar_font_size
        self.speech_to_text = SpeechToText()
        self.is_listening = False
        self.provider_manager = ProviderManager(self, model_manager)
        self.create_speech_bar()
        self.provider_manager.load_voices()

    def create_speech_bar(self):
        logger.info("Creating speech bar")
        self.setObjectName("SpeechBarFrame")
        self.setStyleSheet(f"""
            QFrame {{
                background-color: {self.speechbar_frame_bg};
                border: none;
                border-radius: 10px;
                margin-left: 5px;
                margin-right: 5px;
            }}
        """)
        self.setFixedHeight(40)
        buttons_layout = QtWidgets.QHBoxLayout(self)
        buttons_layout.setContentsMargins(5, 5, 5, 5)
        buttons_layout.setSpacing(10)

        self.speech_provider_button = QtWidgets.QPushButton("Speech Provider", self)
        self.speech_provider_button.setStyleSheet("background-color: #2d2d2d; color: white;")
        self.speech_provider_menu = QtWidgets.QMenu(self.speech_provider_button)
        self.speech_provider_button.clicked.connect(self.show_speech_provider_menu)
        buttons_layout.addWidget(self.speech_provider_button, alignment=QtCore.Qt.AlignLeft)

        self.voice_button = QtWidgets.QPushButton("Voice", self)
        self.voice_button.setStyleSheet("background-color: #2d2d2d; color: white;")
        self.voice_menu = QtWidgets.QMenu(self.voice_button)
        self.voice_button.clicked.connect(self.show_voice_menu)
        buttons_layout.addWidget(self.voice_button, alignment=QtCore.Qt.AlignLeft)

        buttons_layout.addStretch(1)

        self.toggle_tts_button = QtWidgets.QPushButton(self)
        self.toggle_tts_button.setIcon(QtGui.QIcon("assets/SCOUT/Icons/tts_wt.png"))
        self.toggle_tts_button.setIconSize(QtCore.QSize(32, 32))
        self.toggle_tts_button.setFixedSize(QtCore.QSize(32, 32))
        self.toggle_tts_button.setStyleSheet(f"QPushButton {{ background-color: transparent; border: none; color: {self.speechbar_font_color}; font-family: {self.speechbar_font_family}; font-size: {self.speechbar_font_size}px; }}")
        self.toggle_tts_button.clicked.connect(self.toggle_tts)
        self.toggle_tts_button.enterEvent = self.on_tts_button_hover
        self.toggle_tts_button.leaveEvent = self.on_tts_button_leave
        if self.provider_manager.get_tts():
            self.toggle_tts_button.setIcon(QtGui.QIcon("assets/SCOUT/Icons/tts_gn.png"))
        else:
            self.toggle_tts_button.setIcon(QtGui.QIcon("assets/SCOUT/Icons/tts_wt.png"))
        buttons_layout.addWidget(self.toggle_tts_button, alignment=QtCore.Qt.AlignRight)

        self.microphone_button = QtWidgets.QPushButton(self)
        self.microphone_button.setIcon(QtGui.QIcon("assets/SCOUT/Icons/microphone_wt.png"))
        self.microphone_button.setIconSize(QtCore.QSize(32, 32))
        self.microphone_button.setFixedSize(QtCore.QSize(32, 32))
        self.microphone_button.setStyleSheet(f"QPushButton {{ background-color: transparent; border: none; color: {self.speechbar_font_color}; font-family: {self.speechbar_font_family}; font-size: {self.speechbar_font_size}px; }}")
        self.microphone_button.clicked.connect(self.toggle_listen)
        self.microphone_button.enterEvent = self.on_microphone_button_hover
        self.microphone_button.leaveEvent = self.on_microphone_button_leave
        buttons_layout.addWidget(self.microphone_button, alignment=QtCore.Qt.AlignRight)

        self.populate_voice_menu()

    def show_speech_provider_menu(self):
        self.speech_provider_menu.clear()
        speech_providers = ["Google", "Eleven Labs"]
        for provider in speech_providers:
            action = self.speech_provider_menu.addAction(provider)
            action.triggered.connect(lambda checked, p=provider: self.on_speech_provider_selection(p))
        self.speech_provider_menu.exec(QtGui.QCursor.pos())

    def on_speech_provider_selection(self, speech_provider):
        self.provider_manager.switch_speech_provider(speech_provider)
        self.speech_provider_button.setText(speech_provider)
        self.populate_voice_menu()

    def toggle_tts(self):
        logger.info("Entering toggle_tts")
        if self.provider_manager.get_tts():
            self.provider_manager.set_tts(False)
            self.toggle_tts_button.setIcon(QtGui.QIcon("assets/SCOUT/Icons/tts_wt.png"))
            logger.info("TTS turned off")
        else:
            self.provider_manager.set_tts(True)
            self.toggle_tts_button.setIcon(QtGui.QIcon("assets/SCOUT/Icons/tts_gn.png"))
            logger.info("TTS turned on")
        logger.info("Exiting toggle_tts")

    def populate_voice_menu(self):
        logger.info(f"{datetime.now()}: Populating voice menu...")
        self.voice_menu = QtWidgets.QMenu(self.voice_button)
        self.voice_button.setMenu(self.voice_menu)

        provider = self.provider_manager.get_current_speech_provider()

        if provider == "Google":
            self.populate_google_voice_menu()
        elif provider == "Eleven Labs":
            self.populate_eleven_labs_voice_menu()
        else:
            logger.warning(f"{datetime.now()}: Unsupported provider: {provider}")

    def populate_google_voice_menu(self):
        logger.info(f"{datetime.now()}: Populating Google voice menu...")
        try:
            voices = self.provider_manager.get_voices()
            for voice in voices:
                voice_name = voice['name']
                action = self.voice_menu.addAction(voice_name)
                action.triggered.connect(lambda checked, v=voice: self.on_voice_selection(v))
        except Exception as e:
            logger.error(f"{datetime.now()}: Error while getting voices for Google: {e}")

    def populate_eleven_labs_voice_menu(self):
        logger.info(f"{datetime.now()}: Populating Eleven Labs voice menu...")
        try:
            voices = self.provider_manager.get_voices()
            for voice in voices:
                voice_name = voice['name']
                action = self.voice_menu.addAction(voice_name)
                action.triggered.connect(lambda checked, v=voice: self.on_voice_selection(v))
        except Exception as e:
            logger.error(f"{datetime.now()}: Error while getting voices from Eleven Labs: {e}")

    def show_voice_menu(self):
        self.populate_voice_menu()
        self.voice_menu.exec(QtGui.QCursor.pos())

    def on_voice_selection(self, voice):
        logger.info("Voice selection started: %s", voice)
        try:
            provider = self.provider_manager.get_current_speech_provider()
            if provider == "Eleven Labs":
                if 'voice_id' in voice and 'name' in voice:
                    self.provider_manager.set_voice(voice)
                    voice_name = voice['name']
                else:
                    logger.error("Voice dictionary does not contain 'voice_id' or 'name' key: %s", voice)
                    return
            else:
                self.provider_manager.set_voice(voice)
                voice_name = voice

            self.voice_button.setText(voice_name)
            logger.info("Voice selected and applied: %s", voice_name)
        except Exception as e:
            logger.error("Failed to select voice: %s", e)

    def toggle_listen(self):
        if self.is_listening:
            logger.info("Stopping speech-to-text listening")
            self.speech_to_text.stop_listening()

            try:
                transcript = self.speech_to_text.transcribe('output.wav')
                existing_text = self.parent.message_entry.toPlainText()
                updated_text = existing_text.strip() + " " + transcript
                self.parent.message_entry.setPlainText(updated_text)
            except Exception as e:
                logger.error(f"Error transcribing audio: {str(e)}")
                error_message = str(e)
                QMessageBox.critical(self, "Transcription Error", f"An error occurred during transcription:\n\n{error_message}")

            self.is_listening = False
            self.microphone_button.setIcon(QtGui.QIcon("assets/SCOUT/Icons/microphone_wt.png"))
        else:
            logger.info("Starting speech-to-text listening")
            self.speech_to_text.listen()
            self.is_listening = True
            self.microphone_button.setIcon(QtGui.QIcon("assets/SCOUT/Icons/microphone_gn.png"))

        logger.info(f'Listening state toggled: Now listening: {self.is_listening}')

    def on_microphone_button_hover(self, event):
        if not self.is_listening:
            self.microphone_button.setIcon(QtGui.QIcon("assets/SCOUT/Icons/microphone_bl.png"))
            tooltip_style = f"""
                QToolTip {{
                    background-color: {self.speechbar_frame_bg};
                    color: {self.speechbar_font_color};
                    border: none;
                    font-family: {self.speechbar_font_family};
                    font-size: {self.speechbar_font_size}px;
                }}
            """
            self.microphone_button.setStyleSheet(tooltip_style)
            ToolTip.setToolTip(self.microphone_button, "Speech-to-Text")

    def on_microphone_button_leave(self, event):
        if not self.is_listening:
            self.microphone_button.setIcon(QtGui.QIcon("assets/SCOUT/Icons/microphone_wt.png"))

    def on_tts_button_hover(self, event):
        if self.provider_manager.get_tts():
            self.toggle_tts_button.setIcon(QtGui.QIcon("assets/SCOUT/Icons/tts_bl.png"))
        else:
            self.toggle_tts_button.setIcon(QtGui.QIcon("assets/SCOUT/Icons/tts_bl.png"))
        tooltip_style = f"""
            QToolTip {{
                background-color: {self.speechbar_frame_bg};
                color: {self.speechbar_font_color};
                border: none;
                font-family: {self.speechbar_font_family};
                font-size: {self.speechbar_font_size}px;
            }}
        """
        self.toggle_tts_button.setStyleSheet(tooltip_style)
        ToolTip.setToolTip(self.toggle_tts_button, "Text-to-Speech")

    def on_tts_button_leave(self, event):
        if self.provider_manager.get_tts():
            self.toggle_tts_button.setIcon(QtGui.QIcon("assets/SCOUT/Icons/tts_gn.png"))
        else:
            self.toggle_tts_button.setIcon(QtGui.QIcon("assets/SCOUT/Icons/tts_wt.png"))
