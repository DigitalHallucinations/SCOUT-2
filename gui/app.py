#gui/app.py

import os
import time
import asyncio
import logging
from logging.handlers import RotatingFileHandler
import ctypes
import tkinter as tk
from tkinter import messagebox

from gui.chat_component import ChatComponent
from modules.chat_history.convo_manager import ConversationManager
from modules.user_accounts.login import LoginComponent
from modules.user_accounts.user_account_db import UserAccountDatabase
from modules.user_accounts.sign_up import SignUpComponent
from gui.Settings import chist_functions as cf
from modules.Personas.persona_manager import PersonaManager

logger = logging.getLogger('app.py')

log_filename = 'SCOUT.log'
log_max_size = 10 * 1024 * 1024 
log_backup_count = 5

rotating_handler = RotatingFileHandler(log_filename, maxBytes=log_max_size, backupCount=log_backup_count, encoding='utf-8')
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
rotating_handler.setFormatter(formatter)

stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)

logger.addHandler(rotating_handler)
logger.addHandler(stream_handler)
logger.setLevel(logging.INFO)

def adjust_logging_level(level):
    """Adjust the logging level.
    
    Parameters:
    - level (str): Desired logging level. Can be 'DEBUG', 'INFO', 'WARNING', 'ERROR', or 'CRITICAL'.
    """
    levels = {
        'DEBUG': logging.DEBUG,
        'INFO': logging.INFO,
        'WARNING': logging.WARNING,
        'ERROR': logging.ERROR,
        'CRITICAL': logging.CRITICAL
    }
    
    logger.setLevel(levels.get(level, logging.WARNING))

# Make application DPI aware to handle high resolution displays properly
try:
    ctypes.windll.shcore.SetProcessDpiAwareness(1)
except AttributeError:
    # The above call may fail on older Windows versions or non-Windows platforms
    pass

class SCOUT(tk.Tk):
    """Initialize the SCOUT application."""
    def __init__(self):
        super().__init__()
        self.configure(bg="#000000")
        self.title("SCOUT")

        # Original geometry
        width, height = 600, 700

        # Get the scaling factor
        scale_factor = self.get_scaling_factor()

        # Increase the size by 10% if scaling factor is higher than 1
        if scale_factor > 1:
            width = int(width * scale_factor * 1)
            height = int(height * scale_factor * 1)

        self.geometry(f"{width}x{height}+0+0")


        self.iconbitmap(default=os.path.join("assets", "SCOUT", "SCOUT_icon.ico"))

        self.user_database = UserAccountDatabase()

        self.user = None

        self.session_id = None

        self.conversation_id = None

        self.login_component = LoginComponent(master=self, 
                                              callback=self.session_manager, 
                                              database=self.user_database, 
                                              signup_callback=self.show_signup_component)
        self.login_component.grab_set()
        self.protocol("WM_DELETE_WINDOW", self.on_closing)     

    # Make application DPI aware to handle high resolution displays properly
    def get_scaling_factor(self):
        """Get the scaling factor for high resolution displays."""
        # Set default scaling to 1 (100%)
        scaling_factor = 1.0

        # Get the scaling factor from Windows
        try:
            user32 = ctypes.windll.user32
            user32.SetProcessDPIAware()
            # The DPI is the pixel scale factor
            dpi = user32.GetDpiForSystem()
            scaling_factor = dpi / 96.0  # 96 dpi is 100%
        except AttributeError:
            # On non-Windows or older Windows, we fall back to the default
            pass

        return scaling_factor
    
    def set_current_user_username(self, username):
        """Set the current user's username."""
        self.current_username = username

    def session_manager(self, user):
        """Manage the user session.
        
        Parameters:
        - user: The user object.
        """
        self.user = user
        if self.user:
            self.session_id = f"{self.user}_{int(time.time())}"
            self.set_current_user_username(self.user)

            # Instantiate PersonaManager with the current user
            self.persona_handler = PersonaManager(self, self.user)
            current_persona = self.persona_handler.current_persona

            self.database = ConversationManager(self.user, current_persona['name'])
            logger.info("Database instantiated successfully.")

            # Initialize conversation_id using the ConversationManager instance
            self.conversation_id = self.database.init_conversation_id()
            logger.info(f"User is set: {self.user}, Session ID: {self.session_id}, Conversation ID: {self.conversation_id}, Current Persona: {current_persona['name'] if current_persona else 'None'}")

            # Release any previous login component if it exists
            if hasattr(self, 'login_component'):
                self.login_component.grab_release()

            # Instantiate ChatComponent with necessary arguments
            scale_factor = self.get_scaling_factor()
            self.chat_component = ChatComponent(
                master=self, persona=current_persona,
                user=self.user, logout_callback=self.reset_to_prelogin_state,
                session_id=self.session_id, conversation_id=self.conversation_id,
                scale_factor=scale_factor
            )
            self.chat_component.pack(fill='both', expand=True)
        else:
            messagebox.showerror("Login Error", "Invalid username or password.")
            self.session_id = None
            self.conversation_id = None

    def show_signup_component(self):
        """Show the sign-up component."""
        self.signup_component = SignUpComponent(master=self, 
                                                callback=self.session_manager, 
                                                database=self.user_database)
        self.signup_component.grab_set()

    def reset_to_prelogin_state(self):
        """Reset the application to the pre-login state."""
        # Check if the frames exist and are not None before destroying them
        if hasattr(self, 'main_frame') and self.main_frame is not None:
            self.main_frame.destroy()
            self.main_frame = None
        
        self.user = None
        self.session_id = None
        self.conversation_id = None
        self.login_component = LoginComponent(master=self, 
                                              callback=self.session_manager, 
                                              database=self.user_database, 
                                              signup_callback=self.show_signup_component)
        self.login_component.grab_set()
        logger.info("Application has been reset to pre-login state.")

    def log_out(self, event):
        """Log out the current user.
        
        Parameters:
        - event: The event that triggered the log out.
        """
        self.user = None
        self.main_frame.destroy()
        self.session_id = None
        self.conversation_id = None
        self.login_component = LoginComponent(master=self, 
                                              callback=self.session_manager, 
                                              database=self.user_database, 
                                              signup_callback=self.show_signup_component)
        self.login_component.grab_set()

    def safe_update(self, command, *args, **kwargs):
        """Safely update the application.
        
        Parameters:
        - command: The command to execute.
        - *args: Additional arguments for the command.
        - **kwargs: Additional keyword arguments for the command.
        """
        if not self.quit_loop:  # Assuming quit_loop is set to True to indicate closing
            self.after(0, command, *args, **kwargs)

    def on_closing(self):
        """Handle the application closing event."""
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            try:
                # Save the chat log first
                if hasattr(self, 'chat_component1'):
                    cf.save_chat_log(self.chat_component1)
            except Exception as e:
                logger.error("Error saving chat log: {}".format(e))
            self.cleanup_on_exit()

    def cleanup_on_exit(self):
        """Clean up resources on application exit."""
        self.user_database.close_connection()     
        
        logger.info("Application closed by the user.")

        self.quit_loop = True
        self.destroy()

    async def async_main(self):
        """Asynchronous main loop of the application."""
        while not self.quit_loop:
            self.update()
            await asyncio.sleep(0.01)

    def run_asyncio_loop(self):
        """Run the asynchronous event loop."""
        self.quit_loop = False
        asyncio.run(self.async_main())

    @staticmethod
    def main():
            """Main entry point of the application."""
            app = SCOUT()
            logger.info("Application started.")
            app.run_asyncio_loop()
