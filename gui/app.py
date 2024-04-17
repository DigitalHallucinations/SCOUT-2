#gui/app.py

import os
import time
import asyncio
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
from modules.logging.logger import setup_logger

logger = setup_logger('app.py')

try:
    ctypes.windll.shcore.SetProcessDpiAwareness(1)
except AttributeError:
    pass

class SCOUT(tk.Tk):
    """Initialize the SCOUT application."""
    def __init__(self):
        super().__init__()
        self.configure(bg="#000000")
        self.title("SCOUT")

        width, height = 600, 700

        scale_factor = self.get_scaling_factor()

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

    def get_scaling_factor(self):
        """Get the scaling factor for high resolution displays."""
        scaling_factor = 1.0

        try:
            user32 = ctypes.windll.user32
            user32.SetProcessDPIAware()
            dpi = user32.GetDpiForSystem()
            scaling_factor = dpi / 96.0  
        except AttributeError:
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

            self.persona_handler = PersonaManager(self, self.user)
            current_persona = self.persona_handler.current_persona

            self.database = ConversationManager(self.user, current_persona['name'])
            logger.info("Database instantiated successfully.")

            self.conversation_id = self.database.init_conversation_id()
            logger.info(f"User is set: {self.user}, Session ID: {self.session_id}, Conversation ID: {self.conversation_id}, Current Persona: {current_persona['name'] if current_persona else 'None'}")

            if hasattr(self, 'login_component'):
                self.login_component.grab_release()

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
        if not self.quit_loop:  
            self.after(0, command, *args, **kwargs)

    def on_closing(self):
        """Handle the application closing event."""
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            try:
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
