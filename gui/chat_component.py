# gui/chat_component.py


import asyncio 
import time
from PySide6 import QtWidgets, QtGui, QtCore
from PySide6.QtCore import QRunnable
from gui import chist_functions as cf
from gui.Settings.appearance_settings import AppearanceSettings
from gui.sidebar import Sidebar
from gui.tooltip import ToolTip
import gui.send_message as send_message_module
from modules.logging.logger import setup_logger
from gui.speech_bar import SpeechBar

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
    def __init__(self, parent=None, persona=None, user=None, session_id=None, conversation_id=None, logout_callback=None, schedule_async_task=None, persona_manager=None, titlebar_color=None, provider_manager=None, cognitive_services=None, conversation_manager=None):
        super().__init__(parent)
        logger.info("Initializing ChatComponent")
        self.persona = persona
        self.message_entry_visible = True
        self.schedule_async_task = schedule_async_task
        self.session_id = session_id
        self.conversation_id = conversation_id
        self.logout_callback = logout_callback
        self.user = user 
        self.provider_manager = provider_manager
        self.cognitive_services = cognitive_services  
        self.send_message = send_message_module.send_message
        self.persona_manager = persona_manager
        self.current_persona = self.persona_manager.current_persona
        self.personas = self.persona_manager.personas
        self.conversation_manager = conversation_manager
        
        self.system_name = "SCOUT"
        self.system_name_color = "#00BFFF"
        self.user_name_color = "#00ff7f"
        self.system_name_tag = "SCOUT"
        self.timestamp_color = "#ffff7f"
        self.temperature = 0.1  
        self.top_p = 0.9 
        self.top_k = 40  

        self.appearance_settings_instance = AppearanceSettings(parent=self, user=self.user)
        self.create_widgets()
        logger.info("ChatComponent initialized")

    def apply_font_settings(self):
        logger.info("Applying font settings")
        font = QtGui.QFont(self.appearance_settings_instance.font_family, self.appearance_settings_instance.font_size, QtGui.QFont.Normal)
        self.setFont(font)
        
        self.chat_log.setFont(QtGui.QFont(self.appearance_settings_instance.chatlog_font_family, self.appearance_settings_instance.chatlog_font_size))
        self.chat_log.setStyleSheet(f"background-color: {self.appearance_settings_instance.chatlog_frame_bg}; color: {self.appearance_settings_instance.chatlog_font_color}; font-size: {self.appearance_settings_instance.chatlog_font_size}px;")
        
        self.message_entry.setFont(QtGui.QFont(self.appearance_settings_instance.message_entry_font_family, self.appearance_settings_instance.message_entry_font_size))
        self.message_entry.setStyleSheet(f"background-color: {self.appearance_settings_instance.message_entry_frame_bg}; color: {self.appearance_settings_instance.message_entry_font_color}; font-size: {self.appearance_settings_instance.message_entry_font_size}px;")
        
        if hasattr(self, 'send_button'):
            self.send_button.setFont(font)
        
        self.parent().setWindowTitle(f"SCOUT - {self.user}")

        for widget in self.findChildren(QtWidgets.QWidget):
            widget.setFont(font)
            if isinstance(widget, QtWidgets.QPushButton):
                widget.setStyleSheet(f"background-color: #000000; color: {self.appearance_settings_instance.font_color}; font-size: {self.appearance_settings_instance.font_size}px;") 
                
    async def on_persona_selection(self, persona_name):
        logger.info(f"Persona selected: {persona_name}")

        await cf.clear_chat_log(self, self.provider_manager, self.cognitive_services)

        selected_persona_name = persona_name
        for persona in self.personas:
            if persona["name"] == selected_persona_name:
                self.current_persona = persona
                break

        self.current_persona = self.persona_manager.personalize_persona(self.current_persona, self.user)
        self.persona_manager.updater(selected_persona_name, self.user)
        self.system_name_tag = f"system_{selected_persona_name}"
        self.system_name = selected_persona_name

        self.chat_log.setTextColor(QtGui.QColor(self.appearance_settings_instance.chatlog_font_color))
        self.chat_log.setFontWeight(QtGui.QFont.Bold)
        self.chat_log.insertPlainText(self.system_name + ": ")
        self.chat_log.setTextColor(QtGui.QColor(self.appearance_settings_instance.chatlog_font_color))
        self.chat_log.setFontWeight(QtGui.QFont.Normal)

        self.show_message("system", self.current_persona["message"])

        self.update_status_bar()

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

        left_layout = QtWidgets.QVBoxLayout()
        left_layout.setContentsMargins(0, 0, 0, 0)
        left_layout.setSpacing(5)

        self.sidebar = self.create_sidebar()
        left_layout.addWidget(self.sidebar)

        content_layout.addLayout(left_layout)

        right_layout = QtWidgets.QVBoxLayout()
        right_layout.setContentsMargins(0, 0, 0, 0)
        right_layout.setSpacing(5)

        self.stacked_widget = QtWidgets.QStackedWidget(self)
        right_layout.addWidget(self.stacked_widget)

        self.create_chat_page()

        self.create_appearance_settings_page()

        self.speech_bar = SpeechBar(
            parent=self,
            speechbar_frame_bg=self.appearance_settings_instance.speechbar_frame_bg,
            speechbar_font_color=self.appearance_settings_instance.speechbar_font_color,
            speechbar_font_family=self.appearance_settings_instance.speechbar_font_family,
            speechbar_font_size=self.appearance_settings_instance.speechbar_font_size
        )
        right_layout.addWidget(self.speech_bar) 

        content_layout.addLayout(right_layout)

        main_layout.addLayout(content_layout)

        status_bar_frame = QtWidgets.QFrame(self)
        status_bar_frame.setObjectName("StatusBarFrame")
        self.create_status_bar(status_bar_frame)
        main_layout.addWidget(status_bar_frame)

        self.apply_font_settings()
        self.update_status_bar()

    def create_sidebar(self):
        logger.info("Creating sidebar")
        sidebar = Sidebar(self, self.personas, self.appearance_settings_instance.sidebar_frame_bg, self.appearance_settings_instance.sidebar_font_color, self.appearance_settings_instance.sidebar_font_size, self.appearance_settings_instance.sidebar_font_family)
        sidebar.chat_component = self  
        return sidebar 

    def create_status_bar(self, status_bar_frame):
        status_bar_frame.setStyleSheet(f"background-color: {self.appearance_settings_instance.statusbar_frame_bg}; border: none;")
        status_bar_frame.setFixedHeight(30)
        status_bar_layout = QtWidgets.QHBoxLayout(status_bar_frame)
        status_bar_layout.setContentsMargins(5, 0, 5, 0)
        status_bar_layout.setSpacing(10)

        self.provider_label = QtWidgets.QLabel(status_bar_frame)
        self.provider_label.setStyleSheet(f"color: {self.appearance_settings_instance.statusbar_font_color}; font-family: {self.appearance_settings_instance.statusbar_font_family}; font-size: {self.appearance_settings_instance.statusbar_font_size}px;")
        status_bar_layout.addWidget(self.provider_label)

        self.model_label = QtWidgets.QLabel(status_bar_frame)
        self.model_label.setStyleSheet(f"color: {self.appearance_settings_instance.statusbar_font_color}; font-family: {self.appearance_settings_instance.statusbar_font_family}; font-size: {self.appearance_settings_instance.statusbar_font_size}px;")
        status_bar_layout.addWidget(self.model_label)

        status_bar_layout.addStretch(1)

        self.username_label = QtWidgets.QLabel(status_bar_frame)
        self.username_label.setStyleSheet(f"color: {self.appearance_settings_instance.statusbar_font_color}; font-family: {self.appearance_settings_instance.statusbar_font_family}; font-size: {self.appearance_settings_instance.statusbar_font_size}px;")
        status_bar_layout.addWidget(self.username_label) 
        
    def update_status_bar(self):
        provider = self.provider_manager.get_current_llm_provider()
        model = self.provider_manager.get_current_model()

        self.provider_label.setText(f"Provider: {provider}")
        self.model_label.setText(f"Model: {model}")
        self.username_label.setText(f"User: {self.user}")        

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

    def create_appearance_settings_page(self):
        logger.info("Creating settings page")
        self.settings_page = QtWidgets.QWidget()
        self.settings_page.setStyleSheet(f"background-color: {self.appearance_settings_instance.settings_page_main_frame_bg};")
        settings_layout = QtWidgets.QVBoxLayout(self.settings_page)
        settings_layout.setContentsMargins(0, 0, 0, 0)
        settings_layout.setSpacing(0)

        title_label = QtWidgets.QLabel("Settings")
        title_label.setStyleSheet(f"background-color: {self.appearance_settings_instance.settings_page_title_label_bg}; color: {self.appearance_settings_instance.settings_page_font_color}; font-family: {self.appearance_settings_instance.settings_page_title_label_font}; font-size: 24px; font-weight: bold; border: 2px solid black; border-radius: 10px; padding: 5px;")
        title_label.setFixedHeight(40)
        title_label.setAlignment(QtCore.Qt.AlignCenter)
        settings_layout.addWidget(title_label)

        main_frame = QtWidgets.QFrame(self.settings_page)
        main_frame.setObjectName("SettingsPageMainFrame")
        main_frame.setStyleSheet(f"background-color: {self.appearance_settings_instance.settings_page_main_frame_bg}; border: 2px solid black;")

        settings_layout.addWidget(main_frame)

        main_frame_layout = QtWidgets.QHBoxLayout(main_frame)
        main_frame_layout.setContentsMargins(5, 5, 5, 5)
        main_frame_layout.setSpacing(5)

        content_frame = QtWidgets.QFrame(main_frame)
        content_frame.setObjectName("SettingsPageContentFrame")
        content_frame.setStyleSheet(f"background-color: {self.appearance_settings_instance.settings_page_content_frame_bg}; border: 2px solid black; border-radius: 10px;")
        content_frame.setFixedWidth(580)
        content_frame.setFixedHeight(480)  
        main_frame_layout.addWidget(content_frame, alignment=QtCore.Qt.AlignCenter)

        content_layout = QtWidgets.QVBoxLayout(content_frame)
        content_layout.setContentsMargins(10, 10, 10, 10)
        content_layout.setSpacing(20)

        self.appearance_settings_instance.setStyleSheet(f"background-color: {self.appearance_settings_instance.settings_page_content_frame_bg}; color: {self.appearance_settings_instance.settings_page_font_color}; font-family: {self.appearance_settings_instance.settings_page_font_family}; font-size: {self.appearance_settings_instance.settings_page_font_size}px;")
        content_layout.addWidget(self.appearance_settings_instance)

        content_layout.addStretch(1)

        self.stacked_widget.addWidget(self.settings_page)

    def show_chat_page(self):
        self.stacked_widget.setCurrentWidget(self.chat_page)

    def show_settings_page(self):
        self.stacked_widget.setCurrentWidget(self.settings_page)

    def create_entry_sidebar(self, main_layout):
        logger.info("Creating entry sidebar")
        entry_sidebar = QtWidgets.QFrame(self)
        entry_sidebar.setObjectName("EntrySidebarFrame")
        entry_sidebar.setStyleSheet(f"background-color: {self.appearance_settings_instance.entry_sidebar_frame_bg}; border: none;")
        entry_sidebar.setFixedWidth(30)
        entry_sidebar_layout = QtWidgets.QVBoxLayout(entry_sidebar)
        entry_sidebar_layout.setContentsMargins(0, 0, 0, 0)
        entry_sidebar_layout.setSpacing(0)

        self.send_button = QtWidgets.QPushButton(entry_sidebar)
        self.send_button.setIcon(QtGui.QIcon("assets/SCOUT/Icons/send_wt.png"))
        self.send_button.setIconSize(QtCore.QSize(32, 32))
        self.send_button.setFixedSize(QtCore.QSize(32, 32))
        self.send_button.setStyleSheet(f"QPushButton {{ background-color: transparent; border: none; color: {self.appearance_settings_instance.entry_sidebar_font_color}; font-family: {self.appearance_settings_instance.entry_sidebar_font_family}; font-size: {self.appearance_settings_instance.entry_sidebar_font_size}px; }}")
        self.send_button.clicked.connect(self.sync_send_message)
        self.send_button.enterEvent = self.send_button_hover
        self.send_button.leaveEvent = self.send_button_leave
        entry_sidebar_layout.addWidget(self.send_button, alignment=QtCore.Qt.AlignBottom)

        main_layout.addWidget(entry_sidebar) 

    def create_chat_log(self, main_layout):
        logger.info("Creating chat log")
        chat_log_container = QtWidgets.QFrame(self)
        chat_log_container.setObjectName("ChatLogContainer")
        chat_log_container.setStyleSheet(f"""
            QFrame {{
                background-color: {self.appearance_settings_instance.chatlog_frame_bg};
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
        entry_frame.setObjectName("MessageEntryFrame")
        entry_frame.setStyleSheet(f"""
            QFrame {{
                background-color: {self.appearance_settings_instance.message_entry_frame_bg};
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
                background-color: {self.appearance_settings_instance.entry_sidebar_frame_bg};
                color: {self.appearance_settings_instance.entry_sidebar_font_color};
                border: none;
                font-family: {self.appearance_settings_instance.entry_sidebar_font_family};
                font-size: {self.appearance_settings_instance.entry_sidebar_font_size}px;
            }}
            """
        self.send_button.setStyleSheet(tooltip_style)
        ToolTip.setToolTip(self.send_button, "Send Message")

    def send_button_leave(self, event):
        self.send_button.setIcon(QtGui.QIcon("assets/SCOUT/Icons/send_wt.png"))

    def show_persona_menu(self):
        self.persona_menu.exec_(QtGui.QCursor.pos())

    def set_font_size(self, font_size):
        self.parent.font_size = font_size
        self.apply_font_settings()
    
    def set_font_family(self, font_family):
        self.parent.font_family = font_family
        self.apply_font_settings()

    def set_font_color(self, font_color):
        self.parent.font_color = font_color
        self.apply_font_settings()

    def on_logout(self):
        logger.info(f"Logout initiated from ChatComponent.")
        if hasattr(self.parent(), 'log_out'):
            self.parent().log_out(None)
        else:
            logger.error(f"No log_out method found in parent.")

    def open_settings(self):
        logger.info("Opening settings")
        self.appearance_settings_instance = AppearanceSettings(parent=self, user=self.user)
        self.appearance_settings_instance.hide()  
        self.appearance_settings_instance.show()  
 
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
        timestamp = time.strftime("%I:%M %p", time.localtime()).lower()

        cursor = self.chat_log.textCursor()
        cursor.movePosition(QtGui.QTextCursor.End)

        timestamp_format = QtGui.QTextCharFormat()
        timestamp_format.setForeground(QtGui.QColor(self.timestamp_color))
        cursor.setCharFormat(timestamp_format)
        cursor.insertText(f"{timestamp}\n")

        if role == "user":
            user_format = QtGui.QTextCharFormat()
            user_format.setForeground(QtGui.QColor(self.user_name_color))  
            user_format.setFontWeight(QtGui.QFont.Bold)
            cursor.setCharFormat(user_format)
            cursor.insertText(f"{self.user}: ")

            cursor.setCharFormat(QtGui.QTextCharFormat())
            cursor.insertText(f"{message}\n\n")
        elif role == "system":
            system_format = QtGui.QTextCharFormat()
            system_format.setForeground(QtGui.QColor(self.system_name_color))
            system_format.setFontWeight(QtGui.QFont.Bold)
            cursor.setCharFormat(system_format)
            cursor.insertText(f"{self.system_name}: ")

            cursor.setCharFormat(QtGui.QTextCharFormat())
            cursor.insertText(f"{message}\n\n")

        self.chat_log.setTextCursor(cursor)
        self.chat_log.verticalScrollBar().setValue(self.chat_log.verticalScrollBar().maximum())