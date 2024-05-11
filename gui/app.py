
# gui/app.py

import os
import time
import asyncio
import keyring
from keyring.errors import PasswordDeleteError
from PySide6 import QtWidgets, QtGui
from PySide6 import QtCore as qtc
from PySide6.QtCore import Qt 
from gui.chat_component import ChatComponent
from modules.chat_history.convo_manager import ConversationManager
from modules.user_accounts.login import LoginComponent
from modules.user_accounts.user_account_db import UserAccountDatabase
from modules.user_accounts.sign_up import SignUpComponent
from gui import chist_functions as cf
from modules.Personas.persona_manager import PersonaManager
from modules.Providers.provider_manager import ProviderManager
from modules.logging.logger import setup_logger
from modules.Background_Services.CognitiveBackgroundServices import CognitiveBackgroundServices

logger = setup_logger('app.py')

class SCOUT(QtWidgets.QMainWindow):
    """Initialize the SCOUT application."""
    def __init__(self, shutdown_event=None):
        super().__init__()
        self.setStyleSheet("background-color: #000000;")
        self.setWindowFlags(qtc.Qt.FramelessWindowHint) 

        width, height = 600, 800
        self.resize(width, height)

        icon_path = os.path.join("assets", "SCOUT", "SCOUT_icon.ico")
        self.setWindowIcon(QtGui.QIcon(icon_path))

        self.user_database = UserAccountDatabase()

        self.user = None

        self.session_id = None

        self.conversation_id = None

        self.titlebar_color = "#2d2d2d"  

        logger.info("Creating LoginComponent")
        self.login_component = LoginComponent(parent=self, 
                                            callback=self.session_manager, 
                                            database=self.user_database, 
                                            signup_callback=self.show_signup_component)
        self.login_component.setModal(True)
        self.login_component.show()
        
        self.closeEvent = self.on_closing
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
        """Manage the user session.
        
        Parameters:
        - user: The user object.
        """
        logger.info(f"Session manager called with user: {user}")
        self.user = user
        if self.user:
            self.create_custom_title_bar()  
            self.session_id = f"{self.user}_{int(time.time())}"
            self.set_current_user_username(self.user)

            self.persona_handler = PersonaManager(self, self.user)
            current_persona = self.persona_handler.current_persona

            self.provider_manager = ProviderManager(self)

            self.chat_history_database = ConversationManager(self.user, current_persona['name'], self.provider_manager)
            logger.info("Conversation History Database instantiated successfully.")

            self.conversation_id = self.chat_history_database.init_conversation_id()
            logger.info(f"User is set: {self.user}, Session ID: {self.session_id}, Conversation ID: {self.conversation_id}, Current Persona: {current_persona['name'] if current_persona else 'None'}")

            if hasattr(self, 'login_component'):
                self.login_component.close()

            persona_name = current_persona['name']
            db_file = f"modules/Personas/{persona_name}/Memory/{persona_name}.db"
            self.cognitive_services = CognitiveBackgroundServices(db_file, self.user, self.provider_manager)

            logger.info("Creating ChatComponent")
            self.chat_component = ChatComponent(
                parent=self, persona=current_persona,
                user=self.user, session_id=self.session_id, 
                conversation_id=self.conversation_id,
                persona_manager=self.persona_handler,
                titlebar_color=self.titlebar_color,
                provider_manager=self.provider_manager,
                cognitive_services=self.cognitive_services  
            )
            self.setCentralWidget(self.chat_component)
            self.chat_component.show()
            self.show()    
        else:
            QtWidgets.QMessageBox.critical(self, "Login Error", "Invalid username or password.")
            self.session_id = None
            self.conversation_id = None

    def show_signup_component(self):
        """Show the sign-up component."""
        logger.info("Showing SignUpComponent")
        self.signup_component = SignUpComponent(parent=self, 
                                                callback=self.session_manager, 
                                                database=self.user_database)
        self.signup_component.setModal(True)
        self.signup_component.show()

    def log_out(self, event):
        logger.info("Logging out user")
        current_user = self.user
        self.user = None 
        self.session_id = None
        self.conversation_id = None
        
        try:
            keyring.delete_password("SCOUT", current_user)
        except PasswordDeleteError as e:
            logger.debug(f"Caught PasswordDeleteError while deleting password (password still cleared): {str(e)}")        

    def safe_update(self, command, *args, **kwargs):
        """Safely update the application.
        
        Parameters:
        - command: The command to execute.
        - *args: Additional arguments for the command.
        - **kwargs: Additional keyword arguments for the command.
        """
        if not self.quit_loop:  
            QtWidgets.QApplication.postEvent(self, qtc.QEvent(qtc.QEvent.User), command)
    
    def on_closing(self, event):
        logger.info("Application closing")

        message_box = QtWidgets.QMessageBox(self)
        message_box.setWindowTitle('Quit')
        message_box.setText('Do you want to quit?')
        message_box.setStandardButtons(QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
        message_box.setDefaultButton(QtWidgets.QMessageBox.No)
        message_box.setModal(True)

        self.chat_component.appearance_settings_instance.apply_message_box_style(message_box)

        message_box.accepted.connect(self.cleanup_on_exit(event))  

        message_box.exec()  

    def cleanup_on_exit(self, event):
        self.log_out(event)
        logger.info("Application closed by the user.")
        if self.shutdown_event:
            self.shutdown_event.set()


    async def async_main(self):
        while True:
            await asyncio.sleep(0.01)
            QtWidgets.QApplication.processEvents()