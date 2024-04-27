# gui/chat_component.py

import asyncio 
import time
from PySide6 import QtWidgets, QtGui, QtCore
from PySide6.QtCore import QRunnable
import configparser
from PIL import Image, ImageQt
from gui.Settings import chist_functions as cf
from gui.Settings.chat_settings import ChatSettings

from gui.tooltip import ToolTip
import gui.send_message as send_message_module
from modules.speech_services.GglCldSvcs.stt import SpeechToText
from modules.Providers.provider_manager import ProviderManager
from modules.logging.logger import setup_logger

logger = setup_logger('chat_component.py') 

class SendMessageTask(QRunnable):
    def __init__(self, chat_component, user, message, session_id, conversation_id):
        super().__init__()
        self.chat_component = chat_component
        self.user = user
        self.message = message
        self.session_id = session_id
        self.conversation_id = conversation_id

    def run(self):
        asyncio.run(send_message_module.send_message(self.chat_component, self.user, self.message, self.session_id, self.conversation_id))

class ChatComponent(QtWidgets.QWidget):
    def __init__(self, parent=None, persona=None, user=None, session_id=None, conversation_id=None, logout_callback=None, schedule_async_task=None, persona_manager=None, titlebar_color=None):
        super().__init__(parent)
        logger.info("Initializing ChatComponent")
        self.persona = persona
        self.message_entry_visible = True
        self.schedule_async_task = schedule_async_task
        self.session_id = session_id
        self.conversation_id = conversation_id
        self.logout_callback = logout_callback
        self.user = user 
        self.provider_manager = ProviderManager(self)
        self.send_message = send_message_module.send_message
        self.persona_manager = persona_manager
        self.current_persona = self.persona_manager.current_persona
        self.personas = self.persona_manager.personas
        self.typing_indicator_index = None
        self.speech_to_text = SpeechToText()
        self.is_listening = False
        self.message_frame = QtWidgets.QFrame(self)
        self.message_frame.setStyleSheet("background-color: #000000;")
        self.prompt = QtCore.QStringListModel()
        self.system_name = "SCOUT"
        self.system_name_color = "#00BFFF"
        self.system_name_tag = "SCOUT"
        self.timestamp_color = "#888888"
        self.temperature = 0.1  
        self.top_p = 0.9 
        self.top_k = 40  

        font_settings = self.load_font_settings()
        self.font_family, self.font_size, self.font_color, self.sidebar_color, self.titlebar_color = font_settings

        self.create_widgets()
        logger.info("ChatComponent initialized")
            
    def load_font_settings(self, config_file="config.ini"):
        logger.info(f"Loading font settings from {config_file}")
        
        config = configparser.ConfigParser()
        config.read(config_file)

        try:
            font_family = config.get("Font", "family")
            font_size = config.getint("Font", "size")
            font_color = config.get("Font", "color")
            sidebar_color = config.get("Colors", "sidebar_bg")
            titlebar_color = config.get("Colors", "titlebar")
            logger.info(f"Loaded font settings: Family: {font_family}, Size: {font_size}, Color: {font_color}, Titlebar Color: {titlebar_color}")
        except (configparser.NoSectionError, configparser.NoOptionError):
            logger.warning("No font settings found in config file, using defaults")
            font_family = "Helvetica"
            font_size = 12
            font_color = "#ffffff"
            titlebar_color = "#2d2d2d"

        return font_family, font_size, font_color, sidebar_color, titlebar_color
    
    async def on_persona_selection(self, persona_name):
        logger.info(f"Current persona_name: {persona_name}")

        await cf.clear_chat_log(self)

        selected_persona_name = persona_name
        for persona in self.personas:
            if persona["name"] == selected_persona_name:
                self.current_persona = persona 
                break

        self.persona_manager.updater(selected_persona_name)
        self.system_name_tag = f"system_{selected_persona_name}"

        if self.system_name_tag not in self.chat_log.toPlainText():
            self.chat_log.setTextColor(QtGui.QColor(self.system_name_color))
            self.chat_log.setFontWeight(QtGui.QFont.Bold)
            self.chat_log.insertPlainText(self.system_name_tag + ": ")
            self.chat_log.setTextColor(QtGui.QColor(self.font_color))
            self.chat_log.setFontWeight(QtGui.QFont.Normal)

        self.show_message("system", self.current_persona["message"])

    def update_persona_tag(self, system_name_tag, system_name_color):
        if system_name_tag not in self.chat_log.toPlainText():
            self.chat_log.setTextColor(QtGui.QColor(system_name_color))
            self.chat_log.setFontWeight(QtGui.QFont.Bold)
            self.chat_log.insertPlainText(system_name_tag + ": ")
            self.chat_log.setTextColor(QtGui.QColor(self.font_color))
            self.chat_log.setFontWeight(QtGui.QFont.Normal)

    def update_conversation_id(self, new_conversation_id):
        self.conversation_id = new_conversation_id
        logger.info(f"ChatComponent updated with new conversation_id: {new_conversation_id}")

    def apply_font_settings(self):
        logger.info("Applying font settings")
        font = QtGui.font = QtGui.QFont(self.font_family, self.font_size, QtGui.QFont.Normal)
        self.setFont(font)
        self.chat_log.setFont(font)
        self.chat_log.setStyleSheet(f"background-color: #000000; color: {self.font_color}; font-size: {self.font_size}px;")
        self.message_entry.setFont(font)
        self.message_entry.setStyleSheet(f"background-color: #000000; color: {self.font_color}; font-size: {self.font_size}px;")
        self.persona_button.setFont(font)
        self.persona_button.setStyleSheet(f"background-color: #000000; color: {self.font_color}; font-size: {self.font_size}px;")
        self.settings_button.setFont(font)
        self.listen_button.setFont(font)
        self.send_button.setFont(font)
        self.parent().setWindowTitle(f"SCOUT - {self.user}")

        for widget in self.findChildren(QtWidgets.QWidget):
            widget.setFont(font)
            if isinstance(widget, QtWidgets.QPushButton):
                widget.setStyleSheet(f"background-color: #000000; color: {self.font_color}; font-size: {self.font_size}px;")
            elif isinstance(widget, QtWidgets.QTextEdit):
                widget.setStyleSheet(f"background-color: #000000; color: {self.font_color}; font-size: {self.font_size}px;")

    def create_widgets(self):
        logger.info("Creating widgets")
        self.setStyleSheet("background-color: #000000;")

        main_layout = QtWidgets.QHBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(5)

        # Create sidebar
        sidebar = QtWidgets.QFrame(self)
        sidebar.setStyleSheet(f"background-color: {self.sidebar_color}; border-top: 1px solid black;")
        sidebar.setFixedWidth(40)
        sidebar_layout = QtWidgets.QVBoxLayout(sidebar)
        sidebar_layout.setContentsMargins(5, 13, 5, 10)
        sidebar_layout.setSpacing(10)
        self.sidebar = sidebar

        icon_size = QtCore.QSize(32, 32)

        # Persona button frame
        persona_button_frame = QtWidgets.QFrame(sidebar)
        persona_button_frame.setStyleSheet("border: none;")
        persona_button_layout = QtWidgets.QVBoxLayout(persona_button_frame)
        persona_button_layout.setContentsMargins(2, 2, 2, 2)
        persona_button_layout.setSpacing(0)

        self.persona_button = QtWidgets.QPushButton(persona_button_frame)
        self.persona_button.setIcon(QtGui.QIcon("assets/SCOUT/Icons/agent_wt.png"))
        self.persona_button.setIconSize(icon_size)
        self.persona_button.setStyleSheet("QPushButton { background-color: transparent; border: none; }")
        self.persona_button.clicked.connect(self.show_persona_menu)
        persona_button_layout.addWidget(self.persona_button)
        self.persona_button.enterEvent = self.on_persona_button_hover
        self.persona_button.leaveEvent = self.on_persona_button_leave

        ToolTip.setToolTip(self.persona_button, "Change Persona")

        self.persona_menu = QtWidgets.QMenu(self.persona_button)
        for persona in self.personas:
            action = self.persona_menu.addAction(persona["name"])
            action.triggered.connect(lambda checked, p=persona["name"]: asyncio.ensure_future(self.on_persona_selection(p)))

        sidebar_layout.addWidget(persona_button_frame)

        sidebar_layout.addStretch(1)

        # Settings button frame
        settings_button_frame = QtWidgets.QFrame(sidebar)
        settings_button_frame.setStyleSheet("border: none;")
        settings_button_layout = QtWidgets.QVBoxLayout(settings_button_frame)
        settings_button_layout.setContentsMargins(0, 0, 0, 0)
        settings_button_layout.setSpacing(0)

        self.settings_button = QtWidgets.QPushButton(settings_button_frame)
        self.settings_button.setIcon(QtGui.QIcon("assets/SCOUT/Icons/settings_wt.png"))
        self.settings_button.setIconSize(icon_size)
        self.settings_button.setStyleSheet("QPushButton { background-color: transparent; border: none; }")
        self.settings_button.clicked.connect(self.toggle_settings_frame)
        settings_button_layout.addWidget(self.settings_button)
        self.settings_button.enterEvent = self.on_settings_button_hover
        self.settings_button.leaveEvent = self.on_settings_button_leave
        ToolTip.setToolTip(self.settings_button, "Settings")

        sidebar_layout.addWidget(settings_button_frame)

        main_layout.addWidget(sidebar)

        # Create chat area
        chat_area = QtWidgets.QFrame(self)
        chat_area.setStyleSheet("background-color: #000000;")
        chat_layout = QtWidgets.QVBoxLayout(chat_area)
        chat_layout.setContentsMargins(10, 10, 10, 10)
        chat_layout.setSpacing(10)

        self.create_chat_log(chat_layout)
        self.create_message_entry(chat_layout)

        main_layout.addWidget(chat_area)

        # Create settings frame
        self.settings_frame = QtWidgets.QFrame(self)
        self.settings_frame.setStyleSheet("background-color: #222222; border: 1px solid white;")
        self.settings_frame.setFixedWidth(200)
        self.settings_frame.setVisible(False)
        settings_layout = QtWidgets.QVBoxLayout(self.settings_frame)
        settings_layout.setContentsMargins(10, 10, 10, 10)
        settings_layout.setSpacing(10)

        # Add settings widgets to the settings frame
        self.chat_settings_instance = ChatSettings(parent=self, user=self.user)
        self.chat_settings_instance.setStyleSheet("border: none;")
        settings_layout.addWidget(self.chat_settings_instance)

        main_layout.addWidget(self.settings_frame)

        self.apply_font_settings()

    def on_persona_button_hover(self, event):
        self.persona_button.setIcon(QtGui.QIcon("assets/SCOUT/Icons/agent_bl.png"))

    def on_persona_button_leave(self, event):
        self.persona_button.setIcon(QtGui.QIcon("assets/SCOUT/Icons/agent_wt.png"))

    def on_settings_button_hover(self, event):
        self.settings_button.setIcon(QtGui.QIcon("assets/SCOUT/Icons/settings_bl.png"))

    def on_settings_button_leave(self, event):
        self.settings_button.setIcon(QtGui.QIcon("assets/SCOUT/Icons/settings_wt.png"))
    
    def show_persona_menu(self):
        self.persona_menu.exec_(QtGui.QCursor.pos())

    def show_settings_frame(self):
        self.settings_frame.setVisible(True)
        animation = QtCore.QPropertyAnimation(self.settings_frame, b"geometry")
        animation.setDuration(500)  
        animation.setStartValue(QtCore.QRect(-200, 0, 200, self.height()))
        animation.setEndValue(QtCore.QRect(self.sidebar.width() + 5, 0, 200, self.height()))  # Add spacing
        animation.start()

    def hide_settings_frame(self):
        animation = QtCore.QPropertyAnimation(self.settings_frame, b"geometry")
        animation.setDuration(300)
        animation.setStartValue(QtCore.QRect(self.sidebar.width() + 5, 0, 200, self.height()))  # Add spacing
        animation.setEndValue(QtCore.QRect(-200, 0, 200, self.height()))
        animation.finished.connect(self.clear_settings_frame)
        animation.start()
        self.settings_frame.setVisible(False)

    def toggle_settings_frame(self):
        if self.settings_frame.isVisible():
            self.hide_settings_frame()
        else:
            self.show_settings_frame()

    def clear_settings_frame(self):
        self.settings_frame.setVisible(False)
        layout = self.settings_frame.layout()
        if layout is not None:
            while layout.count():
                item = layout.takeAt(0)
                widget = item.widget()
                if widget is not None:
                    widget.deleteLater()
                else:
                    self.clear_layout(item.layout())
            QtWidgets.QWidget().setLayout(layout)

    def clear_layout(self, layout):
        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()
            else:
                self.clear_layout(item.layout())

    def create_chat_log(self, main_layout):
        logger.info("Creating chat log")
        chat_log_container = QtWidgets.QFrame(self)
        chat_log_container.setStyleSheet("background-color: #000000;")
        layout = QtWidgets.QVBoxLayout(chat_log_container)
        layout.setContentsMargins(10, 10, 10, 0)

        self.chat_log = QtWidgets.QTextEdit(chat_log_container)
        self.chat_log.setReadOnly(True)
        self.chat_log.setStyleSheet("background-color: #000000; color: #ffffff;")
        self.show_message("system", self.current_persona["message"])
        self.chat_log.setTextInteractionFlags(QtCore.Qt.TextSelectableByMouse | QtCore.Qt.TextSelectableByKeyboard)
        self.chat_log.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.chat_log.customContextMenuRequested.connect(self.show_context_menu)

        layout.addWidget(self.chat_log)

        main_layout.addWidget(chat_log_container)

    def create_message_entry(self, main_layout):
        logger.info("Creating message entry")
        icon_size = 64

        send_arrow_img = Image.open("assets/SCOUT/icons/send_arrow.png")
        send_arrow_img = send_arrow_img.resize((icon_size, icon_size), Image.LANCZOS)
        self.send_arrow_icon = ImageQt.toqpixmap(send_arrow_img)

        buttons_frame = QtWidgets.QFrame(self)
        buttons_frame.setStyleSheet("background-color: #000000;")
        buttons_layout = QtWidgets.QHBoxLayout(buttons_frame)
        buttons_layout.setContentsMargins(10, 10, 10, 10)

        listen_img = Image.open("assets/SCOUT/icons/listen_icon.png")
        listen_img = listen_img.resize((icon_size, icon_size), Image.LANCZOS)
        self.listen_icon = ImageQt.toqpixmap(listen_img)

        listen_img_green = Image.open("assets/SCOUT/icons/listen_icon_green.png")
        listen_img_green = listen_img_green.resize((icon_size, icon_size), Image.LANCZOS)
        self.listen_icon_green = ImageQt.toqpixmap(listen_img_green)

        self.listen_button = QtWidgets.QPushButton(buttons_frame)
        self.listen_button.setIcon(QtGui.QIcon(self.listen_icon))
        self.listen_button.setStyleSheet("background-color: #000000;")
        self.listen_button.clicked.connect(self.toggle_listen)
        buttons_layout.addWidget(self.listen_button)
        ToolTip.setToolTip(self.listen_button, "Listen")

        self.send_button = QtWidgets.QPushButton(buttons_frame)
        self.send_button.setIcon(QtGui.QIcon(self.send_arrow_icon))
        self.send_button.setStyleSheet("background-color: #000000; color: white;")
        self.send_button.clicked.connect(self.sync_send_message)
        buttons_layout.addWidget(self.send_button)
        ToolTip.setToolTip(self.send_button, "Send")

        entry_frame = QtWidgets.QFrame(self)
        entry_frame.setStyleSheet("background-color: #000000;")
        entry_layout = QtWidgets.QVBoxLayout(entry_frame)
        entry_layout.setContentsMargins(10, 10, 10, 0)

        self.message_entry = QtWidgets.QTextEdit(entry_frame)
        self.message_entry.setStyleSheet("background-color: #000000; color: white;")
        entry_layout.addWidget(self.message_entry)
        
        main_layout.addWidget(buttons_frame)
        main_layout.addWidget(entry_frame)
        
    def set_font_size(self, font_size):
        self.font_size = font_size
        self.apply_font_settings()
    
    def set_font_family(self, font_family):
        """Sets the font family for the chat log."""
        self.font_family = font_family
        self.apply_font_settings()

    def set_font_color(self, font_color):
        self.font_color = font_color
        self.apply_font_settings()

    def on_logout(self):
        logger.info(f"Logout initiated from ChatComponent.")
        if hasattr(self.parent(), 'log_out'):
            self.parent().log_out(None)
        else:
            logger.error(f"No log_out method found in parent.")

    def open_settings(self):
        logger.info("Opening settings")
        self.chat_settings_instance = ChatSettings(parent=self, user=self.user)
        self.chat_settings_instance.hide()  
        self.chat_settings_instance.show()  

    def show_context_menu(self, pos):
        logger.info("Showing context menu")
        context_menu = QtWidgets.QMenu(self.chat_log)
        copy_action = context_menu.addAction("Copy")
        copy_action.triggered.connect(self.copy_selected)
        context_menu.exec(self.chat_log.mapToGlobal(pos))

    def copy_selected(self):
        logger.info("Copying selected text")
        QtWidgets.QApplication.clipboard().setText(self.chat_log.textCursor().selectedText())

    def toggle_topmost(self):
        logger.info("Toggling topmost")
        if self.isVisible():
            self.parent().setWindowFlags(self.parent().windowFlags() ^ QtCore.Qt.WindowStaysOnTopHint)
            self.parent().show() 

    def toggle_listen(self):
        if self.is_listening:
            logger.info("Stopping speech-to-text listening")
            self.speech_to_text.stop_listening()
            transcript = self.speech_to_text.transcribe('output.wav')

            existing_text = self.message_entry.toPlainText()

            updated_text = existing_text.strip() + " " + transcript

            self.message_entry.setPlainText(updated_text)

            self.listen_button.setIcon(QtGui.QIcon(self.listen_icon))
            self.is_listening = False
        else:
            logger.info("Starting speech-to-text listening")
            self.speech_to_text.listen()
            self.listen_button.setIcon(QtGui.QIcon(self.listen_icon_green))
            self.is_listening = True

        logger.info(f'Listening state toggled: Now listening: {self.is_listening}')

    def retrieve_session_id(self):
        logger.info("Retrieving session ID")
        return self.parent().session_id if hasattr(self.parent(), 'session_id') else None
    
    def retrieve_conversation_id(self):
        logger.info("Retrieving conversation ID")
        return self.parent().conversation_id if hasattr(self.parent(), 'conversation_id') else None
    
    def sync_send_message(self):
        logger.info("Sending message")
        if self.session_id is None:
            self.session_id = self.retrieve_session_id() 

        if self.conversation_id is None:
            self.conversation_id = self.retrieve_conversation_id()  

        logger.info(f"About to call send_message with user: %s", self.user)

        message = self.message_entry.toPlainText().strip()
        asyncio.ensure_future(send_message_module.send_message(self, self.user, message, self.session_id, self.conversation_id))
        self.message_entry.clear()

    def show_message(self, role, message):
        QtCore.QMetaObject.invokeMethod(self, "_show_message", QtCore.Qt.QueuedConnection, QtCore.Q_ARG(str, role), QtCore.Q_ARG(str, message))

    @QtCore.Slot(str, str)

    def _show_message(self, role, message):
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        self.chat_log.setTextColor(QtGui.QColor(self.timestamp_color))
        self.chat_log.insertPlainText(f"{timestamp}\n")

        if role == "user":
            self.chat_log.setTextColor(QtGui.QColor(self.font_color))
            self.chat_log.insertPlainText(f"{self.user}: ")   
        elif role == "system":
            self.chat_log.setTextColor(QtGui.QColor(self.system_name_color))
            self.chat_log.setFontWeight(QtGui.QFont.Bold)
            self.chat_log.insertPlainText(f"{self.system_name}: ")
            self.chat_log.setTextColor(QtGui.QColor(self.font_color))
            self.chat_log.setFontWeight(QtGui.QFont.Normal)

        self.chat_log.insertPlainText(f"{message}\n")
        self.chat_log.verticalScrollBar().setValue(self.chat_log.verticalScrollBar().maximum())