# gui/app.py

import os
import time
import asyncio
import keyring
from keyring.errors import PasswordDeleteError

from PySide6 import QtWidgets, QtGui
from PySide6 import QtCore as qtc

from gui.chat_component import ChatComponent
from gui.tool_control_bar import ToolControlBar
from modules.chat_history.convo_manager import ConversationManager
from modules.user_accounts.login import LoginComponent
from modules.user_accounts.user_account_db import UserAccountDatabase
from modules.user_accounts.sign_up import SignUpComponent
from modules.Personas.persona_manager import PersonaManager
from modules.Providers.provider_manager import ProviderManager
from modules.logging.logger import setup_logger
from modules.Background_Services.CognitiveBackgroundServices import CognitiveBackgroundServices
from modules.Personas.FeedManager.Toolbox.Feed_Portal.Feed_Portal import RSSFeedReaderUI
from modules.Tools.Comms.Voip.voip_app import VoIPApp
from modules.Tools.Internet_Tools.Browser.browser import Browser
from modules.Tools.Planning.calendar import Calendar
from modules.Providers.model_manager import ModelManager
from modules.Tools.Code_Execution.code_genius_ui import CodeGeniusUI
# from modules.config import ConfigManager

logger = setup_logger('app.py')

class SCOUT(QtWidgets.QMainWindow):
    """Initialize the SCOUT application."""
    def __init__(self, shutdown_event=None):
        super().__init__()
        self.setStyleSheet("background-color: #000000;")
        self.setWindowFlags(qtc.Qt.FramelessWindowHint)
        width, height = 1200, 800
        self.resize(width, height)
        icon_path = os.path.join("assets", "SCOUT", "SCOUT_icon.ico")
        self.setWindowIcon(QtGui.QIcon(icon_path))
        self.user_database = UserAccountDatabase()
        self.user = None
        self.session_id = None
        self.conversation_id = None
        self.titlebar_color = "#2d2d2d"
        self.is_closing = False  # Flag to control the close process
        self.logout_requested = False  # Flag to indicate if logout is requested

        # Initialize CodeGeniusUI
        self.code_genius_ui = CodeGeniusUI()
        self.code_genius_ui.hide()

        self.feed_portal = RSSFeedReaderUI()
        self.voip_app = VoIPApp()
        self.voip_app.hide()
        self.browser = Browser()
        self.browser.hide()
        self.calendar = Calendar()
        self.calendar.hide()

        logger.info("Creating LoginComponent")
        self.login_component = LoginComponent(
            parent=self,
            callback=self.session_manager,
            database=self.user_database,
            signup_callback=self.show_signup_component
        )
        self.login_component.setModal(True)
        self.login_component.show()

        self.shutdown_event = shutdown_event

    def create_custom_title_bar(self):
        title_bar = QtWidgets.QFrame(self)
        title_bar.setStyleSheet(f"background-color: {self.titlebar_color}; color: white; border-bottom: 2px solid black;")
        title_bar.setFixedHeight(30)

        title_layout = QtWidgets.QHBoxLayout(title_bar)
        title_layout.setContentsMargins(0, 0, 0, 0)
        title_layout.setSpacing(0)

        title_label = QtWidgets.QLabel("SCOUT", title_bar)
        title_label.setAlignment(qtc.Qt.AlignCenter)
        title_label.setStyleSheet("color: white; font-size: 18pt; font-weight: bold; font-family: Consolas;")

        title_layout.addStretch(1)
        title_layout.addWidget(title_label)
        title_layout.addStretch(1)

        self.power_button = QtWidgets.QPushButton(title_bar)
        self.power_button.setIcon(QtGui.QIcon("assets/SCOUT/Icons/power_button_wt.png"))
        self.power_button.setIconSize(qtc.QSize(24, 24))
        self.power_button.setStyleSheet("QPushButton { background-color: transparent; border: none; }")
        self.power_button.clicked.connect(self.on_closing)
        title_layout.addWidget(self.power_button)

        self.power_button.enterEvent = self.on_power_button_hover
        self.power_button.leaveEvent = self.on_power_button_leave

        self.setMenuWidget(title_bar)

        self.draggable = False
        self.drag_position = qtc.QPoint()

        def mousePressEvent(event):
            if event.button() == qtc.Qt.LeftButton:
                self.draggable = True
                self.drag_position = event.globalPos() - self.frameGeometry().topLeft()
                event.accept()

        def mouseMoveEvent(event):
            if event.buttons() == qtc.Qt.LeftButton and self.draggable:
                self.move(event.globalPos() - self.drag_position)
                event.accept()

        def mouseReleaseEvent(event):
            if event.button() == qtc.Qt.LeftButton:
                self.draggable = False

        title_bar.mousePressEvent = mousePressEvent
        title_bar.mouseMoveEvent = mouseMoveEvent
        title_bar.mouseReleaseEvent = mouseReleaseEvent

    def on_power_button_hover(self, event):
        self.power_button.setIcon(QtGui.QIcon("assets/SCOUT/Icons/power_button_rd.png"))

    def on_power_button_leave(self, event):
        self.power_button.setIcon(QtGui.QIcon("assets/SCOUT/Icons/power_button_wt.png"))

    def set_current_user_username(self, username):
        """Set the current user's username."""
        self.current_username = username

    def session_manager(self, user):
        """Manage the user session."""
        logger.info(f"Session manager called with user: {user}")
        self.user = user
        if self.user:
            self.create_custom_title_bar()
            self.session_id = f"{self.user}_{int(time.time())}"
            self.set_current_user_username(self.user)

            self.persona_handler = PersonaManager(self, self.user)
            current_persona = self.persona_handler.current_persona

            self.model_manager = ModelManager()

            self.provider_manager = ProviderManager(self, self.model_manager)

            self.chat_history_database = ConversationManager(self.user, current_persona['name'], self.provider_manager)
            logger.info("Conversation History Database instantiated successfully.")

            self.conversation_id = self.chat_history_database.init_conversation_id()
            logger.info(f"User is set: {self.user}, Session ID: {self.session_id}, Conversation ID: {self.conversation_id}, Current Persona: {current_persona['name'] if current_persona else 'None'}")

            self.database = self.chat_history_database

            if hasattr(self, 'login_component'):
                self.login_component.close()

            persona_name = current_persona['name']
            user_db = f"modules/Personas/{persona_name}/Memory/{persona_name}.db"
            self.cognitive_services = CognitiveBackgroundServices(user_db, self.user, self.provider_manager)

            logger.info("Creating ChatComponent")
            self.chat_component = ChatComponent(
                parent=self,
                persona=current_persona,
                user=self.user,
                session_id=self.session_id,
                conversation_id=self.conversation_id,
                persona_manager=self.persona_handler,
                titlebar_color=self.titlebar_color,
                provider_manager=self.provider_manager,
                cognitive_services=self.cognitive_services,
                conversation_manager=self.chat_history_database,
                model_manager=self.model_manager
            )

            central_widget = QtWidgets.QWidget(self)
            central_layout = QtWidgets.QHBoxLayout(central_widget)
            central_layout.setContentsMargins(0, 0, 0, 0)
            central_layout.setSpacing(0)

            splitter = QtWidgets.QSplitter(qtc.Qt.Horizontal, central_widget)
            splitter.setHandleWidth(1)
            splitter.setStyleSheet("QSplitter::handle { background-color: #000000; }")

            chat_frame = QtWidgets.QFrame(splitter)
            chat_frame.setFrameShape(QtWidgets.QFrame.NoFrame)
            chat_frame.setFrameShadow(QtWidgets.QFrame.Plain)
            chat_frame.setStyleSheet("background-color: #000000;")
            chat_layout = QtWidgets.QVBoxLayout(chat_frame)
            chat_layout.setContentsMargins(0, 0, 0, 0)
            chat_layout.setSpacing(0)
            chat_layout.addWidget(self.chat_component)

            tool_ui_frame = QtWidgets.QFrame(splitter)
            tool_ui_frame.setFrameShape(QtWidgets.QFrame.NoFrame)
            tool_ui_frame.setStyleSheet("background-color: #000000;")
            tool_ui_layout = QtWidgets.QVBoxLayout(tool_ui_frame)
            tool_ui_layout.setContentsMargins(0, 0, 0, 0)
            tool_ui_layout.setSpacing(0)

            tool_control_bar = ToolControlBar(tool_ui_frame, self.voip_app, self.feed_portal, self.browser, self.calendar, self.code_genius_ui)
            tool_ui_layout.addWidget(tool_control_bar)

            tool_ui_layout.addWidget(self.feed_portal)
            tool_ui_layout.addWidget(self.voip_app)
            tool_ui_layout.addWidget(self.browser)
            tool_ui_layout.addWidget(self.calendar)
            tool_ui_layout.addWidget(self.code_genius_ui)

            # Ensure CodeGeniusUI is in front when shown
            self.code_genius_ui.raise_()

            splitter.addWidget(chat_frame)
            splitter.addWidget(tool_ui_frame)
            splitter.setSizes([600, 600])

            central_layout.addWidget(splitter)
            self.setCentralWidget(central_widget)

            self.show()
        else:
            QtWidgets.QMessageBox.critical(self, "Login Error", "Invalid username or password.")
            self.session_id = None
            self.conversation_id = None

    def show_signup_component(self):
        """Show the sign-up component."""
        logger.info("Showing SignUpComponent")
        self.signup_component = SignUpComponent(
            parent=self,
            callback=self.session_manager,
            database=self.user_database
        )
        self.signup_component.setModal(True)
        self.signup_component.show()

    def log_out(self):
        logger.info("Logging out user")
        current_user = self.user
        self.user = None
        self.session_id = None
        self.conversation_id = None

        try:
            keyring.delete_password("SCOUT", current_user)
        except PasswordDeleteError as e:
            logger.debug(f"Caught PasswordDeleteError while deleting password (password still cleared): {str(e)}")

    def on_closing(self, event=None):
        logger.info("Application closing")

        message_box = QtWidgets.QMessageBox(self)
        message_box.setWindowTitle('Quit')
        message_box.setText('Do you want to quit?')
        message_box.setStandardButtons(QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
        message_box.setDefaultButton(QtWidgets.QMessageBox.No)
        message_box.setModal(True)

        # Apply the corrected styles
        self.chat_component.appearance_settings_instance.apply_message_box_style(message_box)

        # Ensure text is visible
        message_box.setStyleSheet("""
            QMessageBox {
                background-color: #2d2d2d;
                color: white;
                font-size: 14px;
            }
            QLabel {
                color: white;
            }
            QPushButton {
                background-color: #4d4d4d;
                color: white;
                font-size: 12px;
                padding: 5px 10px;
            }
            QPushButton:hover {
                background-color: #6d6d6d;
            }
        """)

        # Connect the signal to the slot
        message_box.buttonClicked.connect(self.handle_quit_response)

        message_box.exec()

    def handle_quit_response(self, button):
        if button.text() == '&Yes':
            # Show the logout confirmation dialog
            self.show_logout_confirmation()
        else:
            pass  # Do nothing

    def show_logout_confirmation(self):
        message_box = QtWidgets.QMessageBox(self)
        message_box.setWindowTitle('Log Out')
        message_box.setText('Do you want to log out?')
        message_box.setStandardButtons(QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
        message_box.setDefaultButton(QtWidgets.QMessageBox.No)
        message_box.setModal(True)

        # Apply the corrected styles
        self.chat_component.appearance_settings_instance.apply_message_box_style(message_box)

        # Ensure text is visible
        message_box.setStyleSheet("""
            QMessageBox {
                background-color: #2d2d2d;
                color: white;
                font-size: 14px;
            }
            QLabel {
                color: white;
            }
            QPushButton {
                background-color: #4d4d4d;
                color: white;
                font-size: 12px;
                padding: 5px 10px;
            }
            QPushButton:hover {
                background-color: #6d6d6d;
            }
        """)

        message_box.buttonClicked.connect(self.handle_logout_response)

        message_box.exec()

    def handle_logout_response(self, button):
        if button.text() == '&Yes':
            self.logout_requested = True
        else:
            self.logout_requested = False
        self.cleanup_on_exit()

    def cleanup_on_exit(self):
        self.is_closing = True  # Set the flag to indicate we're closing
        if self.logout_requested:
            self.log_out()
            logger.info("User chose to log out.")
        else:
            logger.info("User chose not to log out.")
        logger.info("Application closed by the user.")
        if self.shutdown_event:
            self.shutdown_event.set()
        self.close()

    def closeEvent(self, event):
        if self.is_closing:
            # If we're already in the process of closing, accept the event
            event.accept()
            super().closeEvent(event)
        else:
            # If not, prompt the user
            event.ignore()
            self.on_closing(event)

    async def async_main(self):
        while True:
            await asyncio.sleep(0.01)
            QtWidgets.QApplication.processEvents()
