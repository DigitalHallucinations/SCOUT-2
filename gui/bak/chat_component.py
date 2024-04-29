# gui/chat_component.py

import asyncio 
import time
from PySide6 import QtWidgets, QtGui, QtCore
from PySide6.QtCore import QRunnable
import configparser
from gui.Settings import chist_functions as cf
from gui.Settings.chat_settings import ChatSettings
from PySide6.QtWidgets import QMessageBox
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

        font_settings = self.load_appearance_settings()
        (
            self.font_family,
            self.font_size,
            self.font_color,
            self.titlebar_color,
            self.chatlog_frame_bg,
            self.chatlog_font_color,
            self.chatlog_font_family,
            self.chatlog_font_size,
            self.message_entry_frame_bg,
            self.message_entry_font_color,
            self.message_entry_font_family,
            self.message_entry_font_size,
            self.speechbar_frame_bg,
            self.speechbar_font_color,
            self.speechbar_font_family,
            self.speechbar_font_size,
            self.sidebar_frame_bg,
            self.sidebar_font_color,
            self.sidebar_font_family,
            self.sidebar_font_size,
            self.entry_sidebar_frame_bg,
            self.entry_sidebar_font_color,
            self.entry_sidebar_font_family,
            self.entry_sidebar_font_size,
            self.settings_page_main_frame_bg,
            self.settings_page_content_frame_bg,
            self.settings_page_title_label_bg,
            self.settings_page_title_label_font,
            self.settings_page_font_color,
            self.settings_page_font_family,
            self.settings_page_font_size,
            self.settings_page_spinbox_bg
        ) = font_settings

        self.create_widgets()
        logger.info("ChatComponent initialized")
        
    def load_appearance_settings(self, config_file="config.ini"):
        logger.info(f"Loading font settings from {config_file}")
        
        config = configparser.ConfigParser()
        config.read(config_file)

        try:
            font_family = config.get("Font", "family")
            font_size = config.getint("Font", "size")
            font_color = config.get("Font", "color")
            titlebar_color = config.get("Colors", "titlebar")

            chatlog_frame_bg = config.get("ChatlogSettings", "frame_bg")
            chatlog_font_color = config.get("ChatlogSettings", "font_color")
            chatlog_font_family = config.get("ChatlogSettings", "font_family")
            chatlog_font_size = config.getint("ChatlogSettings", "font_size")

            message_entry_frame_bg = config.get("MessageEntrySettings", "frame_bg")
            message_entry_font_color = config.get("MessageEntrySettings", "font_color")
            message_entry_font_family = config.get("MessageEntrySettings", "font_family")
            message_entry_font_size = config.getint("MessageEntrySettings", "font_size")

            speechbar_frame_bg = config.get("SpeechBarSettings", "frame_bg")
            speechbar_font_color = config.get("SpeechBarSettings", "font_color")
            speechbar_font_family = config.get("SpeechBarSettings", "font_family")
            speechbar_font_size = config.getint("SpeechBarSettings", "font_size")

            sidebar_frame_bg = config.get("SideBarSettings", "frame_bg")
            sidebar_font_color = config.get("SideBarSettings", "font_color")
            sidebar_font_family = config.get("SideBarSettings", "font_family")
            sidebar_font_size = config.getint("SideBarSettings", "font_size")

            entry_sidebar_frame_bg = config.get("EntrySideBarSettings", "frame_bg")
            entry_sidebar_font_color = config.get("EntrySideBarSettings", "font_color")
            entry_sidebar_font_family = config.get("EntrySideBarSettings", "font_family")
            entry_sidebar_font_size = config.getint("EntrySideBarSettings", "font_size")

            settings_page_main_frame_bg = config.get("SettingsPageSettings", "main_frame_bg")
            settings_page_content_frame_bg = config.get("SettingsPageSettings", "content_frame_bg")
            settings_page_title_label_bg = config.get("SettingsPageSettings", "title_tab_bg")
            settings_page_title_label_font = config.get("SettingsPageSettings", "title_tab_font")
            settings_page_font_color = config.get("SettingsPageSettings", "font_color")
            settings_page_font_family = config.get("SettingsPageSettings", "font_family")
            settings_page_font_size = config.getint("SettingsPageSettings", "font_size")
            settings_page_spinbox_bg = config.get("SettingsPageSettings", "spinbox_bg")

            logger.info(f"Loaded font settings: Family: {font_family}, Size: {font_size}, Color: {font_color}, Titlebar Color: {titlebar_color}")
        except (configparser.NoSectionError, configparser.NoOptionError):
            logger.warning("No font settings found in config file, using defaults")
            font_family = "Sitka"
            font_size = 15
            font_color = "#ffffff"
            titlebar_color = "#2d2d2d"
            chatlog_frame_bg = "#2d2d2d"
            chatlog_font_color = "#ffffff"
            chatlog_font_family = "Sitka"
            chatlog_font_size = 15
            message_entry_frame_bg = "#2d2d2d"
            message_entry_font_color = "#ffffff"
            message_entry_font_family = "Sitka"
            message_entry_font_size = 15
            speechbar_frame_bg = "#2d2d2d"
            speechbar_font_color = "#ffffff"
            speechbar_font_family = "Sitka"
            speechbar_font_size = 15
            sidebar_frame_bg = "#2d2d2d"
            sidebar_font_color = "#ffffff"
            sidebar_font_family = "Sitka"
            sidebar_font_size = 15
            entry_sidebar_frame_bg = "#000000"
            entry_sidebar_font_color = "#ffffff"
            entry_sidebar_font_family = "Sitka"
            entry_sidebar_font_size = 15
            settings_page_main_frame_bg = "#000000"
            settings_page_content_frame_bg = "#2d2d2d"
            settings_page_title_label_bg = "#2d2d2d"
            settings_page_title_label_font = "Sitka"
            settings_page_font_color = "#ffffff"
            settings_page_font_family = "Sitka"
            settings_page_font_size = 15
            settings_page_spinbox_bg = "#808080"

        return (
            font_family,
            font_size,
            font_color,
            titlebar_color,
            chatlog_frame_bg,
            chatlog_font_color,
            chatlog_font_family,
            chatlog_font_size,
            message_entry_frame_bg,
            message_entry_font_color,
            message_entry_font_family,
            message_entry_font_size,
            speechbar_frame_bg,
            speechbar_font_color,
            speechbar_font_family,
            speechbar_font_size,
            sidebar_frame_bg,
            sidebar_font_color,
            sidebar_font_family,
            sidebar_font_size,
            entry_sidebar_frame_bg,
            entry_sidebar_font_color,
            entry_sidebar_font_family,
            entry_sidebar_font_size,
            settings_page_main_frame_bg,
            settings_page_content_frame_bg,
            settings_page_title_label_bg,
            settings_page_title_label_font,
            settings_page_font_color,
            settings_page_font_family,
            settings_page_font_size,
            settings_page_spinbox_bg
        )
    
    def apply_font_settings(self):
        logger.info("Applying font settings")
        font = QtGui.font = QtGui.QFont(self.font_family, self.font_size, QtGui.QFont.Normal)
        self.setFont(font)
        
        self.chat_log.setFont(QtGui.QFont(self.chatlog_font_family, self.chatlog_font_size))
        self.chat_log.setStyleSheet(f"background-color: {self.chatlog_frame_bg}; color: {self.chatlog_font_color}; font-size: {self.chatlog_font_size}px;")
        
        self.message_entry.setFont(QtGui.QFont(self.message_entry_font_family, self.message_entry_font_size))
        self.message_entry.setStyleSheet(f"background-color: {self.message_entry_frame_bg}; color: {self.message_entry_font_color}; font-size: {self.message_entry_font_size}px;")
        
        self.persona_button.setFont(font)
        self.persona_button.setStyleSheet(f"background-color: #000000; color: {self.font_color}; font-size: {self.font_size}px;")
        self.settings_button.setFont(font)
        
        if hasattr(self, 'microphone_button'):
            self.microphone_button.setFont(font)
        
        if hasattr(self, 'send_button'):
            self.send_button.setFont(font)
        
        self.parent().setWindowTitle(f"SCOUT - {self.user}")

        for widget in self.findChildren(QtWidgets.QWidget):
            widget.setFont(font)
            if isinstance(widget, QtWidgets.QPushButton):
                widget.setStyleSheet(f"background-color: #000000; color: {self.font_color}; font-size: {self.font_size}px;")

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

    def create_widgets(self):
        logger.info("Creating widgets")
        self.setStyleSheet("background-color: #000000;")
        
        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(5)

        content_layout = QtWidgets.QHBoxLayout()
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(0)

        self.create_sidebar(content_layout)

        right_layout = QtWidgets.QVBoxLayout()
        right_layout.setContentsMargins(0, 0, 0, 0)
        right_layout.setSpacing(0)

        self.stacked_widget = QtWidgets.QStackedWidget(self)
        right_layout.addWidget(self.stacked_widget)

        self.create_chat_page()

        self.create_settings_page()

        self.create_speech_bar(right_layout)

        content_layout.addLayout(right_layout)

        main_layout.addLayout(content_layout)

        self.apply_font_settings()

    def create_sidebar(self, main_layout):
        logger.info("Creating sidebar")
        sidebar = QtWidgets.QFrame(self)
        sidebar.setStyleSheet(f"background-color: {self.sidebar_frame_bg}; border-right: 2px solid black;")
        sidebar.setFixedWidth(40)
        sidebar_layout = QtWidgets.QVBoxLayout(sidebar)
        sidebar_layout.setContentsMargins(5, 13, 5, 10)
        sidebar_layout.setSpacing(10)
        self.sidebar = sidebar

        icon_size = QtCore.QSize(32, 32)

        providers_button_frame = QtWidgets.QFrame(sidebar)
        providers_button_frame.setStyleSheet("border: none;")
        providers_button_layout = QtWidgets.QVBoxLayout(providers_button_frame)
        providers_button_layout.setContentsMargins(2, 2, 2, 2)
        providers_button_layout.setSpacing(0)

        self.providers_button = QtWidgets.QPushButton(providers_button_frame)
        self.providers_button.setIcon(QtGui.QIcon("assets/SCOUT/Icons/providers_wt.png"))
        self.providers_button.setIconSize(icon_size)
        self.providers_button.setStyleSheet("QPushButton { background-color: transparent; border: none; }")
        self.providers_button.clicked.connect(self.handle_providers_button)
        providers_button_layout.addWidget(self.providers_button)
        self.providers_button.enterEvent = self.on_providers_button_hover
        self.providers_button.leaveEvent = self.on_providers_button_leave

        ToolTip.setToolTip(self.providers_button, "Providers")

        sidebar_layout.addWidget(providers_button_frame)

        models_button_frame = QtWidgets.QFrame(sidebar)
        models_button_frame.setStyleSheet("border: none;")
        models_button_layout = QtWidgets.QVBoxLayout(models_button_frame)
        models_button_layout.setContentsMargins(2, 2, 2, 2)
        models_button_layout.setSpacing(0)

        self.models_button = QtWidgets.QPushButton(models_button_frame)
        self.models_button.setIcon(QtGui.QIcon("assets/SCOUT/Icons/models_wt.png"))
        self.models_button.setIconSize(icon_size)
        self.models_button.setStyleSheet("QPushButton { background-color: transparent; border: none; }")
        self.models_button.clicked.connect(self.handle_models_button)
        models_button_layout.addWidget(self.models_button)
        self.models_button.enterEvent = self.on_models_button_hover
        self.models_button.leaveEvent = self.on_models_button_leave

        ToolTip.setToolTip(self.models_button, "Models")

        sidebar_layout.addWidget(models_button_frame)

        history_button_frame = QtWidgets.QFrame(sidebar)
        history_button_frame.setStyleSheet("border: none;")
        history_button_layout = QtWidgets.QVBoxLayout(history_button_frame)
        history_button_layout.setContentsMargins(0, 2, 0, 2)
        history_button_layout.setSpacing(0)

        self.history_button = QtWidgets.QPushButton(history_button_frame)
        self.history_button.setIcon(QtGui.QIcon("assets/SCOUT/Icons/history_wt.png"))
        self.history_button.setIconSize(icon_size)
        self.history_button.setStyleSheet("QPushButton { background-color: transparent; border: none; }")
        self.history_button.clicked.connect(self.handle_history_button)
        history_button_layout.addWidget(self.history_button)
        self.history_button.enterEvent = self.on_history_button_hover
        self.history_button.leaveEvent = self.on_history_button_leave

        ToolTip.setToolTip(self.history_button, "History")

        sidebar_layout.addWidget(history_button_frame)

        chat_button_frame = QtWidgets.QFrame(sidebar)
        chat_button_frame.setStyleSheet("border: none;")
        chat_button_layout = QtWidgets.QVBoxLayout(chat_button_frame)
        chat_button_layout.setContentsMargins(2, 2, 2, 2)
        chat_button_layout.setSpacing(0)

        self.chat_button = QtWidgets.QPushButton(chat_button_frame)
        self.chat_button.setIcon(QtGui.QIcon("assets/SCOUT/Icons/chat_wt.png"))
        self.chat_button.setIconSize(icon_size)
        self.chat_button.setStyleSheet("QPushButton { background-color: transparent; border: none; }")
        self.chat_button.clicked.connect(self.show_chat_page)
        chat_button_layout.addWidget(self.chat_button)
        self.chat_button.enterEvent = self.on_chat_button_hover
        self.chat_button.leaveEvent = self.on_chat_button_leave

        ToolTip.setToolTip(self.chat_button, "Chat")

        sidebar_layout.addWidget(chat_button_frame)

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

        settings_button_frame = QtWidgets.QFrame(sidebar)
        settings_button_frame.setStyleSheet("border: none;")
        settings_button_layout = QtWidgets.QVBoxLayout(settings_button_frame)
        settings_button_layout.setContentsMargins(0, 0, 0, 0)
        settings_button_layout.setSpacing(0)

        self.settings_button = QtWidgets.QPushButton(settings_button_frame)
        self.settings_button.setIcon(QtGui.QIcon("assets/SCOUT/Icons/settings_wt.png"))
        self.settings_button.setIconSize(icon_size)
        self.settings_button.setStyleSheet("QPushButton { background-color: transparent; border: none; }")
        self.settings_button.clicked.connect(self.show_settings_page)
        settings_button_layout.addWidget(self.settings_button)
        self.settings_button.enterEvent = self.on_settings_button_hover
        self.settings_button.leaveEvent = self.on_settings_button_leave
        ToolTip.setToolTip(self.settings_button, "Settings")

        sidebar_layout.addWidget(settings_button_frame)

        main_layout.addWidget(sidebar)

    def create_chat_page(self):
        logger.info("Creating chat page")
        self.chat_page = QtWidgets.QWidget()
        self.chat_page.setStyleSheet("background-color: #000000;")
        chat_layout = QtWidgets.QVBoxLayout(self.chat_page)
        chat_layout.setContentsMargins(10, 10, 10, 10)
        chat_layout.setSpacing(5)

        splitter = QtWidgets.QSplitter(QtCore.Qt.Vertical)
        splitter.setStyleSheet("QSplitter::handle { background-color: #000000; }")
        splitter.setHandleWidth(10)
        
        self.create_chat_log(splitter)

        message_entry_layout = QtWidgets.QHBoxLayout()
        message_entry_layout.setContentsMargins(0, 0, 0, 0)
        message_entry_layout.setSpacing(0)

        self.create_message_entry(message_entry_layout)

        self.create_entry_sidebar(message_entry_layout)

        message_entry_frame = QtWidgets.QFrame(self)
        message_entry_frame.setLayout(message_entry_layout)
        splitter.addWidget(message_entry_frame)

        chat_layout.addWidget(splitter)

        self.stacked_widget.addWidget(self.chat_page)

    def create_settings_page(self):
        logger.info("Creating settings page")
        self.settings_page = QtWidgets.QWidget()
        self.settings_page.setStyleSheet(f"background-color: {self.settings_page_main_frame_bg};")
        settings_layout = QtWidgets.QVBoxLayout(self.settings_page)
        settings_layout.setContentsMargins(0, 0, 0, 0)
        settings_layout.setSpacing(0)

        title_label = QtWidgets.QLabel("Settings")
        title_label.setStyleSheet(f"background-color: {self.settings_page_title_label_bg}; color: {self.settings_page_font_color}; font-family: {self.settings_page_title_label_font}; font-size: 24px; font-weight: bold; border: 2px solid black; border-radius: 10px; padding: 5px;")
        title_label.setFixedHeight(40)
        title_label.setAlignment(QtCore.Qt.AlignCenter)
        settings_layout.addWidget(title_label)

        main_frame = QtWidgets.QFrame(self.settings_page)
        main_frame.setStyleSheet(f"background-color: {self.settings_page_main_frame_bg}; 2px solid black;")

        settings_layout.addWidget(main_frame)

        main_frame_layout = QtWidgets.QHBoxLayout(main_frame)
        main_frame_layout.setContentsMargins(5, 5, 5, 5)
        main_frame_layout.setSpacing(5)

        content_frame = QtWidgets.QFrame(main_frame)
        content_frame.setStyleSheet(f"background-color: {self.settings_page_content_frame_bg}; border: 2px solid black; border-radius: 10px;")
        content_frame.setFixedWidth(580)
        content_frame.setFixedHeight(480)  
        main_frame_layout.addWidget(content_frame, alignment=QtCore.Qt.AlignCenter)

        content_layout = QtWidgets.QVBoxLayout(content_frame)
        content_layout.setContentsMargins(10, 10, 10, 10)
        content_layout.setSpacing(20)

        self.chat_settings_instance = ChatSettings(parent=self, user=self.user)
        self.chat_settings_instance.setStyleSheet(f"background-color: {self.settings_page_content_frame_bg}; color: {self.settings_page_font_color}; font-family: {self.settings_page_font_family}; font-size: {self.settings_page_font_size}px;")
        content_layout.addWidget(self.chat_settings_instance)

        content_layout.addStretch(1)

        self.stacked_widget.addWidget(self.settings_page)

    def on_chat_button_hover(self, event):
        self.chat_button.setIcon(QtGui.QIcon("assets/SCOUT/Icons/chat_bl.png"))

    def on_chat_button_leave(self, event):
        self.chat_button.setIcon(QtGui.QIcon("assets/SCOUT/Icons/chat_wt.png"))

    def show_chat_page(self):
        self.stacked_widget.setCurrentWidget(self.chat_page)

    def show_settings_page(self):
        self.stacked_widget.setCurrentWidget(self.settings_page)

    def create_entry_sidebar(self, main_layout):
        logger.info("Creating entry sidebar")
        entry_sidebar = QtWidgets.QFrame(self)
        entry_sidebar.setStyleSheet(f"background-color: {self.entry_sidebar_frame_bg}; border: none;")
        entry_sidebar.setFixedWidth(30)
        entry_sidebar_layout = QtWidgets.QVBoxLayout(entry_sidebar)
        entry_sidebar_layout.setContentsMargins(0, 0, 0, 0)
        entry_sidebar_layout.setSpacing(0)

        self.send_button = QtWidgets.QPushButton(entry_sidebar)
        self.send_button.setIcon(QtGui.QIcon("assets/SCOUT/Icons/send_wt.png"))
        self.send_button.setIconSize(QtCore.QSize(32, 32))
        self.send_button.setFixedSize(QtCore.QSize(32, 32))
        self.send_button.setStyleSheet(f"QPushButton {{ background-color: transparent; border: none; color: {self.entry_sidebar_font_color}; font-family: {self.entry_sidebar_font_family}; font-size: {self.entry_sidebar_font_size}px; }}")
        self.send_button.clicked.connect(self.sync_send_message)
        self.send_button.enterEvent = self.send_button_hover
        self.send_button.leaveEvent = self.send_button_leave
        entry_sidebar_layout.addWidget(self.send_button, alignment=QtCore.Qt.AlignBottom)

        main_layout.addWidget(entry_sidebar)

    
    def create_speech_bar(self, main_layout):
        logger.info("Creating speech bar")
        SpeechBar = QtWidgets.QFrame(self)
        SpeechBar.setStyleSheet(f"background-color: {self.speechbar_frame_bg}; border: none;")
        SpeechBar.setFixedHeight(40)
        buttons_layout = QtWidgets.QHBoxLayout(SpeechBar)
        buttons_layout.setContentsMargins(5, 5, 5, 5)
        buttons_layout.setSpacing(0)

        self.microphone_button = QtWidgets.QPushButton(SpeechBar)
        self.microphone_button.setIcon(QtGui.QIcon("assets/SCOUT/Icons/microphone_wt.png"))
        self.microphone_button.setIconSize(QtCore.QSize(32, 32))
        self.microphone_button.setFixedSize(QtCore.QSize(32, 32))
        self.microphone_button.setStyleSheet(f"QPushButton {{ background-color: transparent; border: none; color: {self.speechbar_font_color}; font-family: {self.speechbar_font_family}; font-size: {self.speechbar_font_size}px; }}")
        self.microphone_button.clicked.connect(self.toggle_listen)
        self.microphone_button.enterEvent = self.on_microphone_button_hover
        self.microphone_button.leaveEvent = self.on_microphone_button_leave
        buttons_layout.addWidget(self.microphone_button, alignment=QtCore.Qt.AlignLeft)

        buttons_layout.addStretch(1)

        main_layout.addWidget(SpeechBar)

    def on_providers_button_hover(self, event):
        self.providers_button.setIcon(QtGui.QIcon("assets/SCOUT/Icons/providers_bl.png"))

    def on_providers_button_leave(self, event):
        self.providers_button.setIcon(QtGui.QIcon("assets/SCOUT/Icons/providers_wt.png"))

    def handle_providers_button(self):
        providers_menu = QtWidgets.QMenu(self)
        for provider in self.llm_providers:
            action = providers_menu.addAction(provider)
            action.triggered.connect(lambda checked, p=provider: self.set_provider(p))
        providers_menu.exec(QtGui.QCursor.pos())

    def on_models_button_hover(self, event):
        self.models_button.setIcon(QtGui.QIcon("assets/SCOUT/Icons/models_bl.png"))

    def on_models_button_leave(self, event):
        self.models_button.setIcon(QtGui.QIcon("assets/SCOUT/Icons/models_wt.png"))

    def handle_models_button(self):
        models_menu = QtWidgets.QMenu(self)
        for model in self.available_models:
            action = models_menu.addAction(model)
            action.triggered.connect(lambda checked, m=model: self.set_model(m))
        models_menu.exec(QtGui.QCursor.pos())

    def on_history_button_hover(self, event):
        self.history_button.setIcon(QtGui.QIcon("assets/SCOUT/Icons/history_bl.png"))

    def on_history_button_leave(self, event):
        self.history_button.setIcon(QtGui.QIcon("assets/SCOUT/Icons/history_wt.png"))

    def handle_history_button(self):
        history_dialog = QtWidgets.QDialog(self)
        history_dialog.setWindowTitle("Chat History")
        history_dialog.exec()

    def on_persona_button_hover(self, event):
        self.persona_button.setIcon(QtGui.QIcon("assets/SCOUT/Icons/agent_bl.png"))

    def on_persona_button_leave(self, event):
        self.persona_button.setIcon(QtGui.QIcon("assets/SCOUT/Icons/agent_wt.png"))

    def on_settings_button_hover(self, event):
        self.settings_button.setIcon(QtGui.QIcon("assets/SCOUT/Icons/settings_bl.png"))

    def on_settings_button_leave(self, event):
        self.settings_button.setIcon(QtGui.QIcon("assets/SCOUT/Icons/settings_wt.png"))
    
    def create_chat_log(self, main_layout):
        logger.info("Creating chat log")
        chat_log_container = QtWidgets.QFrame(self)
        chat_log_container.setStyleSheet(f"""
            QFrame {{
                background-color: {self.chatlog_frame_bg};
                border-radius: 10px;
            }}
        """)
        layout = QtWidgets.QVBoxLayout(chat_log_container)
        layout.setContentsMargins(0, 0, 10, 0)

        self.chat_log = QtWidgets.QTextEdit(chat_log_container)
        self.chat_log.setReadOnly(True)
        self.chat_log.setStyleSheet("""
            QTextEdit {
                background-color: transparent;
                color: #ffffff;
                border: 1px solid #444444;
                border-radius: 10px;
                padding: 10px;
            }
        """)
        self.show_message("system", self.current_persona["message"])
        layout.addWidget(self.chat_log)

        main_layout.addWidget(chat_log_container)

    def create_message_entry(self, main_layout):
        logger.info("Creating message entry")
        entry_frame = QtWidgets.QFrame(self)
        entry_frame.setStyleSheet(f"""
            QFrame {{
                background-color: {self.message_entry_frame_bg};
                border-radius: 10px;
            }}
        """)
        entry_layout = QtWidgets.QVBoxLayout(entry_frame)
        entry_layout.setContentsMargins(10, 0, 0, 0)

        self.message_entry = QtWidgets.QTextEdit(entry_frame)
        self.message_entry.setStyleSheet("""
            QTextEdit {
                background-color: transparent;
                color: white;
                border: 1px solid #444444;
                border-radius: 10px;
                padding: 10px;
            }
        """)
        entry_layout.addWidget(self.message_entry)

        main_layout.addWidget(entry_frame)

    def send_button_hover(self, event):
        self.send_button.setIcon(QtGui.QIcon("assets/SCOUT/Icons/send_bl.png"))
        tooltip_style = f"""
            QToolTip {{
                background-color: {self.entry_sidebar_frame_bg};
                color: {self.entry_sidebar_font_color};
                border: none;
                font-family: {self.entry_sidebar_font_family};
                font-size: {self.entry_sidebar_font_size}px;
            }}
        """
        self.send_button.setStyleSheet(tooltip_style)
        ToolTip.setToolTip(self.send_button, "Send Message")

    def send_button_leave(self, event):
        self.send_button.setIcon(QtGui.QIcon("assets/SCOUT/Icons/send_wt.png"))

    def toggle_listen(self):
        if self.is_listening:
            logger.info("Stopping speech-to-text listening")
            self.speech_to_text.stop_listening()
            
            try:
                transcript = self.speech_to_text.transcribe('output.wav')
                existing_text = self.message_entry.toPlainText()
                updated_text = existing_text.strip() + " " + transcript
                self.message_entry.setPlainText(updated_text)
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
    
    def show_persona_menu(self):
        self.persona_menu.exec_(QtGui.QCursor.pos())

    
              
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

    def toggle_topmost(self):
        logger.info("Toggling topmost")
        if self.isVisible():
            self.parent().setWindowFlags(self.parent().windowFlags() ^ QtCore.Qt.WindowStaysOnTopHint)
            self.parent().show() 

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

        if "```" in message:
            code_blocks = message.split("```")
            for i, block in enumerate(code_blocks):
                if i % 2 == 0:
                    self.chat_log.insertPlainText(block)
                else:
                    language = block.split("\n")[0].strip()
                    code = "\n".join(block.split("\n")[1:])
                    self.insert_code_block(language, code)
                    if i < len(code_blocks) - 1:
                        self.chat_log.insertPlainText("\n")
        else:
            self.chat_log.insertPlainText(f"{message}\n")

        self.chat_log.verticalScrollBar().setValue(self.chat_log.verticalScrollBar().maximum())
        
    def insert_code_block(self, language, code):
        code_block = f"""
        <div style="background-color: #1E1E1E; border: 1px solid #444444; border-radius: 5px; padding: 10px;">
            <div style="color: #888888; font-size: 12px;">{language}</div>
            <pre style="color: #ffffff; font-family: 'Courier New', monospace; font-size: 14px; margin: 0;">{code}</pre>
        </div>
        """
        self.chat_log.insertHtml(code_block)
        self.chat_log.insertPlainText("\n")

   