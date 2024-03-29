# gui/components/chat_component.py

import asyncio
import logging
import time
import tkinter as tk

from logging.handlers import RotatingFileHandler
from PIL import Image, ImageTk
from .custom_entry import CustomEntry
from modules.Personas.persona_manager import PersonaManager
from gui.Settings import chist_functions as cf
from gui.Settings.chat_settings import ChatSettings
from modules.Avatar.avatar import MediaComponent
from gui.tooltip import ToolTip
import gui.send_message as send_message_module
from modules.speech_services.GglCldSvcs.stt import SpeechToText


logger = logging.getLogger('chat_component.py') 

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

class ChatComponent(tk.Frame):
    """A chat component for the SCOUT application."""
    def __init__(self, master=None, persona=None, user=None, session_id=None, conversation_id=None, logout_callback=None, schedule_async_task=None, scale_factor=1.0):
        """
        Initialize the ChatComponent with necessary parameters and default values.
        Usage: This is the constructor, called when an instance of ChatComponent is created.
        """
        super().__init__(master)
        self.scale_factor = scale_factor
        self.persona = persona
        self.message_entry_visible = True
        self.schedule_async_task = schedule_async_task
        self.session_id = session_id
        self.conversation_id = conversation_id
        self.logout_callback = logout_callback
        self.user = user 
        self.current_provider = "OpenAI"  
        self.switch_provider(self.current_provider)
        self.persona_manager = PersonaManager(self, self.user)
        self.current_persona = self.persona_manager.current_persona
        self.personas = self.persona_manager.personas
        self.typing_indicator_index = None
        self.speech_to_text = SpeechToText()
        self.is_listening = False
        self.message_frame = tk.Frame(self, bg="#000000")
        self.message_frame.pack(side="bottom", fill="x")
        self.prompt = tk.StringVar()
        self.system_name = "SCOUT"
        self.system_name_color = "#00BFFF"
        self.system_name_font = ("Helvetica", 10, "bold")
        self.system_name_tag = "SCOUT"
        self.timestamp_color = "#888888"
        self.timestamp_font = ("Helvetica", 8)
        self.temperature = 0.1  
        self.top_p = 0.9 
        self.top_k = 40  
        self.entry_box = tk.Entry(self)
   
        self.create_widgets()
        logger.info("ChatComponent initialized")
    
    
    def on_persona_selection(self, persona_name):
        """
        Handles the selection of a new persona from the persona menu.
    
        When a user selects a persona from the persona menu, this method updates the current persona,
        saves and clears the chat log, and updates the UI accordingly.
        
        Side Effects:
        - Modifies `self.current_persona` to reflect the newly selected persona.
        - Saves and clears the chat log.
        - Updates the persona button text and system name tag.
        - Shows a message from the selected persona in the chat log.
        
        Thread Safety:
        - This method should be called from the main UI thread.
        
        Usage:
        - Called when a persona is selected from the persona menu.
        
        Dependencies:
        - Relies on `self.personas` for the list of available personas.
        - Calls `cf.save_chat_log` and `cf.clear_chat_log` to manage the chat log.
        - Calls `self.persona_manager.updater` to update the persona manager.
        - Calls `self.show_message` to display a message from the selected persona.
        
        Error Handling:
        - If the selected persona is not found in `self.personas`, no action is taken.
        
        Parameters:
        - persona_name (str): The name of the selected persona.
        
        Returns:
        - None.
        """
        logger.info(f"Current persona_name: {persona_name}")
        cf.save_chat_log(self)

        cf.clear_chat_log(self)

        selected_persona_name = persona_name
        for persona in self.personas:
            if persona["name"] == selected_persona_name:
                self.current_persona = persona 
                break

        self.persona_manager.updater(selected_persona_name)
        self.system_name_tag = f"system_{selected_persona_name}"

        if self.system_name_tag not in self.chat_log.tag_names():
            self.chat_log.tag_configure(self.system_name_tag, foreground=self.system_name_color)

        self.show_message("system", self.current_persona["message"])

        self.persona_button.config(text=selected_persona_name)

    def update_persona_tag(self, system_name_tag, system_name_color):
        """
        Updates the tag configuration for the system messages in the chat log.
    
        This method is called from `on_persona_selection` to update the tag configuration
        when a new persona is selected.
        
        Side Effects:
        - Configures a new tag in the chat log if it doesn't exist.
        
        Thread Safety:
        - This method should be called from the main UI thread.
        
        Usage:
        - Called from `on_persona_selection` method.
        
        Dependencies:
        - Relies on `self.chat_log` to access the chat log widget.
        
        Error Handling:
        - If the tag already exists, no action is taken.
        
        Parameters:
        - system_name_tag (str): The tag associated with the system messages.
        - system_name_color (str): The color for the system messages.        
        
        Returns:
        - None.
        """
        if system_name_tag not in self.chat_log.tag_names():
            self.chat_log.tag_configure(system_name_tag, foreground=system_name_color)

    def update_conversation_id(self, new_conversation_id):
        """
        Updates the conversation ID for the chat component.
    
        This method is called when a new conversation ID is provided, typically after a new session starts.
        
        Side Effects:
        - Modifies `self.conversation_id` to reflect the new conversation ID.
        
        Thread Safety:
        - This method should be called from the main UI thread.
        
        Usage:
        - Called when a new conversation ID is available.
        
        Dependencies:
        - None
        
        Error Handling:
        - None
        
        Parameters:
        - new_conversation_id (str): The new conversation ID to be set.
        
        Returns:
        - None.
        """
        self.conversation_id = new_conversation_id
        logger.info(f"ChatComponent updated with new conversation_id: {new_conversation_id}")

    def create_widgets(self):
        """
        Create and configure the widgets for the chat component.
    
        This method sets up the UI elements of the chat component, including buttons, frames, and icons.
        
        Side Effects:
        - Creates and packs various UI widgets.
        - Calls `self.create_chat_log` and `self.create_message_entry` to set up specific UI components.
        
        Thread Safety:
        - This method should be called from the main UI thread.
        
        Usage:
        - Called from the `__init__` method during chat component initialization.
        
        Dependencies:
        - Relies on various UI libraries (e.g., tkinter, PIL) for widget creation and manipulation.
        - Calls `self.create_chat_log` and `self.create_message_entry` to set up specific UI components.
        
        Error Handling:
        - None
        
        Parameters:
        - None
        
        Returns:
        - None.
        """
        self.configure(bg="#000000")
        icon_size = int(32 * self.scale_factor)
        settings_img = Image.open("assets/SCOUT/icons/settings_icon.png")
        settings_img = settings_img.resize((icon_size, icon_size), Image.Resampling.LANCZOS)
        self.settings_icon = ImageTk.PhotoImage(settings_img)

        buttons_frame = tk.Frame(self, bg="#000000")
        buttons_frame.pack(side="top", fill="x", padx=10, pady=(10, 10))

        self.persona_button = tk.Menubutton(buttons_frame, text=self.personas[0]["name"], relief="flat", bg="#000000", fg="white")
        self.persona_button.pack(side="left", padx=(0, 10))
        ToolTip(self.persona_button, "Change Persona")

        self.persona_menu = tk.Menu(self.persona_button, tearoff=0)
        self.persona_button.configure(menu=self.persona_menu)

        for persona in self.personas:
            self.persona_menu.add_command(label=persona["name"], command=lambda p=persona["name"]: self.on_persona_selection(p))

        self.logout_button = tk.Button(buttons_frame, text="Logout", relief="flat", bg="#000000", fg="white", command=self.on_logout)
        self.logout_button.pack(side="right", padx=(0, 10))

        self.settings_button = tk.Button(buttons_frame, text="", image=self.settings_icon, relief="flat", bg="#000000", command=self.open_settings)
        self.settings_button.pack(side="right")
        ToolTip(self.settings_button, "Settings")


        self.create_chat_log()
        self.create_message_entry()

    def create_message_entry(self):
        """
         Create the message entry widget and associated buttons.
    
        This method sets up the message entry area, including the input field and send/listen buttons.
        
        Side Effects:
        - Creates and packs the message entry widget and associated buttons.
        
        Thread Safety:
        - This method should be called from the main UI thread.
        
        Usage:
        - Called from the `create_widgets` method during chat component setup.
        
        Dependencies:
        - Relies on various UI libraries (e.g., tkinter, PIL) for widget creation and manipulation.
        - Uses `self.toggle_listen` as the command for the listen button.
        - Uses `self.sync_send_message` as the command for the send button.
        
        Error Handling:
        - None
        
        Parameters:
        - None
        
        Returns:
        - None.
        """
        icon_size = int(32 * self.scale_factor)

        send_arrow_img = Image.open("assets/SCOUT/icons/send_arrow.png")
        send_arrow_img = send_arrow_img.resize((icon_size, icon_size), Image.Resampling.LANCZOS)
        self.send_arrow_icon = ImageTk.PhotoImage(send_arrow_img)

        buttons_frame = tk.Frame(self, bg="#000000")
        buttons_frame.pack(side="bottom", fill="x", padx=10, pady=10)

        listen_img = Image.open("assets/SCOUT/icons/listen_icon.png")
        listen_img = listen_img.resize((icon_size, icon_size), Image.Resampling.LANCZOS)
        self.listen_icon = ImageTk.PhotoImage(listen_img)

        listen_img_green = Image.open("assets/SCOUT/icons/listen_icon_green.png")
        listen_img_green = listen_img_green.resize((icon_size, icon_size), Image.Resampling.LANCZOS)
        self.listen_icon_green = ImageTk.PhotoImage(listen_img_green)

        self.listen_button = tk.Button(buttons_frame, image=self.listen_icon, relief="flat", bg="#000000", activebackground="#000000", command=self.toggle_listen)
        self.listen_button.pack(side="left", padx=(0, 10))
        ToolTip(self.listen_button, "Listen")

        self.send_button = tk.Button(buttons_frame, text="", image=self.send_arrow_icon, relief="flat", command=self.sync_send_message, bg="#000000", fg="white", activebackground="#5a6dad", activeforeground="white")
        self.send_button.pack(side="right", padx=10)
        ToolTip(self.send_button, "Send")

        entry_frame = tk.Frame(self, bg="#000000")
        entry_frame.pack(side="bottom", fill="x", padx=10, pady=(10, 0))

        self.message_entry = CustomEntry(entry_frame, height=10, wrap="word", font=("Helvetica", 10), bg="#000000", fg="white", insertbackground="white")
        self.message_entry.pack(fill="x", expand=True)

    def create_chat_log(self):
        """
         Create the chat log widget where messages are displayed.
    
        This method sets up the chat log area, including the text widget and initial system message.
        
        Side Effects:
        - Creates and packs the chat log widget.
        - Displays an initial system message using `self.show_message`.
        - Configures tags for the chat log.
        - Binds the `<<Paste>>` event to `self.paste_func`.
        - Calls `self.show_context_menu` to set up the context menu.
        
        Thread Safety:
        - This method should be called from the main UI thread.
        
        Usage:
        - Called from the `create_widgets` method during chat component setup.
        
        Dependencies:
        - Relies on various UI libraries (e.g., tkinter) for widget creation and manipulation.
        - Uses `self.show_message` to display the initial system message.
        - Uses `self.paste_func` as the event handler for the `<<Paste>>` event.
        - Calls `self.show_context_menu` to set up the context menu.
        
        Error Handling:
        - None
        
        Parameters:
        - None
        
        Returns:
        - None.
        """
        chat_log_container = tk.Frame(self, bg="#000000")
        chat_log_container.pack(side="top", fill="both", expand=True, padx=10, pady=(10, 0))

        self.chat_log = tk.Text(chat_log_container, wrap="word", font=("Helvetica", 10), bg="#000000", fg="#ffffff", padx=10, pady=10)    
        self.show_message("system", self.current_persona["message"])  
        self.chat_log.configure(state="disabled")               
        self.chat_log.tag_configure("SCOUT", foreground="#00BFFF")  
        self.chat_log.tag_configure("timestamp")

        self.chat_log.pack(side="left", fill="both", expand=True)
        self.chat_log.bind("<<Paste>>", self.paste_func)

        self.show_context_menu() 


    def resize_icon(self, icon_path, scale_factor):
        """
        Resize an icon image based on the scale factor.
    
        This method loads an image from the specified path, resizes it based on the scale factor,
        and returns the resized image as a PhotoImage object.
        
        Side Effects:
        - None
        
        Thread Safety:
        - This method should be called from the main UI thread.
        
        Usage:
        - Called from various methods that require resized icons (e.g., `create_widgets`, `create_message_entry`).
        
        Dependencies:
        - Relies on the PIL library for image manipulation.
        
        Error Handling:
        - If the image file cannot be loaded, an exception will be raised by the PIL library.
        
        Parameters:
        - icon_path (str): The path to the icon image file.
        - scale_factor (float): The scale factor to resize the image.
        
        Returns:
        - A PhotoImage object representing the resized image.
        """
        img = Image.open(icon_path)
        img = img.resize((int(img.width * scale_factor), int(img.height * scale_factor)), Image.Resampling.LANCZOS)
        return ImageTk.PhotoImage(img)

    def on_logout(self):
        """
        Handle the logout process.
    
        This method is called when the user clicks the logout button. It initiates the logout process
        by calling the `logout_callback` if provided.
        
        Side Effects:
        - Calls the `logout_callback` if provided.
        
        Thread Safety:
        - This method should be called from the main UI thread.
        
        Usage:
        - Bound to the logout button's command in the `create_widgets` method.
        
        Dependencies:
        - Relies on the `logout_callback` being set to a valid function.
        
        Error Handling:
        - If no `logout_callback` is provided, an error is logged.
        
        Parameters:
        - None
        
        Returns:
        - None.
        """
        logger.info(f"Logout initiated from ChatComponent.")
        if self.logout_callback:
            self.logout_callback()
        else:
            logger.error(f"No logout callback provided.")
            
    def clear_chat_interface(self):
        """
        Clear the chat interface, typically as part of the logout process.
    
        This method clears the chat interface by calling the `log_out` method of the master component,
        if available.
        
        Side Effects:
        - Calls the `log_out` method of the master component, if available.
        
        Thread Safety:
        - This method should be called from the main UI thread.
        
        Usage:
        - Called from the `on_logout` method.
        
        Dependencies:
        - Relies on the master component having a `log_out` method.
        
        Error Handling:
        - None
        
        Parameters:
        - None
        
        Returns:
        - None.
        """
        if hasattr(self.master, 'log_out'):
            self.master.log_out(None)

    def open_settings(self):
        """
        Open the settings window for the chat component.
    
        This method creates an instance of the `ChatSettings` class and displays the settings window.
        
        Side Effects:
        - Creates an instance of the `ChatSettings` class.
        - Calls `withdraw` and `deiconify` on the settings window to display it.
        
        Thread Safety:
        - This method should be called from the main UI thread.
        
        Usage:
        - Bound to the settings button's command in the `create_widgets` method.
        
        Dependencies:
        - Relies on the `ChatSettings` class being defined.
        
        Error Handling:
        - None
        
        Parameters:
        - None
        
        Returns:
        - None.
        """
        self.chat_settings_instance = ChatSettings(master=self, user=self.user)
        self.chat_settings_instance.withdraw()  
        self.chat_settings_instance.deiconify()  

    def show_context_menu(self):
        """
        Show the context menu for the chat log.
    
        This method sets up the context menu for the chat log, which is triggered by a right-click event.
        
        Side Effects:
        - Creates a context menu with a "Copy" command.
        - Binds the right-click event to display the context menu.
        
        Thread Safety:
        - This method should be called from the main UI thread.
        
        Usage:
        - Called from the `create_chat_log` method.
        
        Dependencies:
        - Relies on the `copy_selected` method as the command for the "Copy" menu item.
        
        Error Handling:
        - None
        
        Parameters:
        - None
        
        Returns:
        - None.
        """
        context_menu = tk.Menu(self.chat_log, tearoff=0)
        context_menu.add_command(label="Copy", command=self.copy_selected)
        self.chat_log.bind("<Button-3>", lambda event: context_menu.tk_popup(event.x_root, event.y_root))

    def copy_selected(self):
        """
        Copy the selected text from the chat log to the clipboard.
    
        This method retrieves the selected text from the chat log and copies it to the clipboard.
        
        Side Effects:
        - Clears the clipboard.
        - Appends the selected text to the clipboard.
        
        Thread Safety:
        - This method should be called from the main UI thread.
        
        Usage:
        - Bound to the "Copy" command in the context menu in the `show_context_menu` method.
        
        Dependencies:
        - None
        
        Error Handling:
        - If no text is selected, the method silently does nothing.
        
        Parameters:
        - None
        
        Returns:
        - None.
        """   
        self.clipboard_clear()  
        try:
            selected_text = self.chat_log.get(tk.SEL_FIRST, tk.SEL_LAST)    
            self.clipboard_append(selected_text)    
        except tk.TclError: 
            pass  

    def paste_func(self, event): 
        """
        Handles the paste operation in the message entry widget.
    
        This method is bound to the `<<Paste>>` event in the message entry widget. It retrieves the
        clipboard content and inserts it into the message entry at the current cursor position,
        replacing any selected text.
        
        Side Effects:
        - Retrieves the clipboard content.
        - Inserts the clipboard content into the message entry widget.
        
        Thread Safety:
        - This method should be called from the main UI thread.
        
        Usage:
        - Bound to the `<<Paste>>` event in the `create_chat_log` method.
        
        Dependencies:
        - None
        
        Error Handling:
        - If the clipboard is empty or the paste operation fails, the method silently does nothing.
        
        Parameters:
        - event: The event object containing information about the paste event.
        
        Returns:
        - None.
        """ 
        try:
            clipboard_text = self.clipboard_get()  
            if self.message_entry.tag_ranges(tk.SEL):  
                start = self.message_entry.index(tk.SEL_FIRST)
                end = self.message_entry.index(tk.SEL_LAST)
                self.message_entry.delete(start, end)  
                self.message_entry.insert(start, clipboard_text)  
            else:
                self.message_entry.insert(tk.INSERT, clipboard_text)  
        except tk.TclError:
            pass  

    def show_message(self, role, message):
        """
        Displays a message in the chat log with appropriate formatting.
    
        This method inserts a message into the chat log with the specified role (user or system)
        and applies appropriate formatting based on the role.
        
        Side Effects:
        - Inserts the message into the chat log.
        - Applies formatting tags to the message based on the role.
        - Scrolls the chat log to the end.
        
        Thread Safety:
        - This method should be called from the main UI thread.
        
        Usage:
        - Called from various places in the code where a message needs to be displayed to the user.
        
        Dependencies:
        - Relies on the chat log widget being created and accessible.
        
        Error Handling:
        - None
        
        Parameters:
        - role (str): The role of the message sender ('user' or 'system').
        - message (str): The message text to be displayed.
        
        Returns:
        - None.
        """
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        self.chat_log.configure(state="normal")
        self.chat_log.insert("end", f"{timestamp}\n", "timestamp")

        if role == "user":
            self.chat_log.insert("end", f"{self.user}: ", "You")   
        elif role == "system":
            self.chat_log.insert("end", f"{self.system_name}: ", self.system_name_tag)

        self.chat_log.insert("end", f"{message}\n")
        self.chat_log.configure(state="disabled")
        self.chat_log.yview("end")

    def switch_provider(self, provider):
        """
        Switches the response generation provider for the chat component.
    
        This method updates the `generate_response` function based on the selected provider
        and updates the `current_provider` attribute.
        
        Side Effects:
        - Imports the appropriate response generation module based on the provider.
        - Updates the `generate_response` function.
        - Updates the `current_provider` attribute.
        
        Thread Safety:
        - This method should be called from the main UI thread.
        
        Usage:
        - Called from the `__init__` method and potentially other places where provider switching is needed.
        
        Dependencies:
        - Relies on the response generation modules for each provider being available.
        
        Error Handling:
        - If an unknown provider is specified, a `ValueError` is raised.
        
        Parameters:
        - provider (str): The name of the provider to switch to.
        
        Returns:
        - None.
        """
        if provider == "OpenAI":
            from modules.Providers.OpenAI.OA_gen_response import generate_response
        elif provider == "Mistral":
            from modules.Providers.Mistral.Mistral_gen_response import generate_response    
        elif provider == "Google":
            from modules.Providers.Google.GG_gen_response import generate_response
        elif provider == "HuggingFace":
            from modules.Providers.HuggingFace.HF_gen_response import generate_response  
        elif provider in ["Anthropic"]:
            from modules.Providers.Anthropic.Anthropic_gen_response import generate_response    
        elif provider in ["Local"]:
            logger.warning(f"Provider {provider} is not implemented yet. Reverting to default provider OpenAI.")
            from modules.Providers.OpenAI.OA_gen_response import generate_response
        else:
            raise ValueError(f"Unknown provider: {provider}")

        self.current_provider = provider
        self.send_message = send_message_module.send_message
        self.generate_response = generate_response 

    def toggle_media_component(self):
        """
        Toggles the visibility of the media component.
    
        This method shows or hides the media component based on its current visibility state.
        
        Side Effects:
        - Creates an instance of the `MediaComponent` class if it doesn't exist.
        - Calls `withdraw` or `deiconify` on the media component to hide or show it.
        
        Thread Safety:
        - This method should be called from the main UI thread.
        
        Usage:
        - Called from the `chat_settings.py` module.
        
        Dependencies:
        - Relies on the `MediaComponent` class being defined.
        
        Error Handling:
        - None
        
        Parameters:
        - None
        
        Returns:
        - None.
        """
        if hasattr(self, 'media_component'):
            if self.media_component.winfo_viewable():
                self.media_component.withdraw()
            else:
                self.media_component.deiconify()
        else:
            self.media_component = MediaComponent(self)

    def show_media_component(self):
        """
        Show the media component.
    
        This method creates an instance of the `MediaComponent` class and displays it.
        
        Side Effects:
        - Creates an instance of the `MediaComponent` class.
        
        Thread Safety:
        - This method should be called from the main UI thread.
        
        Usage:
        - Called from the `chat_settings.py` module.
        
        Dependencies:
        - Relies on the `MediaComponent` class being defined.
        
        Error Handling:
        - None
        
        Parameters:
        - None
        
        Returns:
        - None.
        """
        self.master.media_component = MediaComponent(self)        

    def toggle_topmost(self):
        """
        Toggle the 'always on top' state of the chat window.
    
        This method toggles the 'always on top' attribute of the chat window, making it stay
        above other windows or allowing other windows to overlap it.
        
        Side Effects:
        - Modifies the '-topmost' attribute of the chat window.
        
        Thread Safety:
        - This method should be called from the main UI thread.
        
        Usage:
        - Called from the `chat_settings.py` module.
        
        Dependencies:
        - None
        
        Error Handling:
        - None
        
        Parameters:
        - None
        
        Returns:
        - None.
        """
        if self.winfo_ismapped():
            self.winfo_toplevel().attributes("-topmost", not self.winfo_toplevel().attributes("-topmost")) 

    def toggle_listen(self):
        """
        Toggles the speech-to-text listening state.

        When activated, the application starts listening for user speech input and transcribes it to text.
        When deactivated, it stops listening and appends the transcribed text to the message entry.

        Side Effects:
        - Modifies `self.is_listening` to reflect the new listening state.
        - Changes the icon of `self.listen_button` to indicate listening state.
        - Appends transcribed text to `self.message_entry` if stopping listening.

        Thread Safety:
        - This method should be called from the main UI thread.

        Usage:
        - Called when the user clicks the listen button in the UI.

        Dependencies:
        - Relies on `self.speech_to_text` for speech-to-text functionality.

        Error Handling:
        - If speech-to-text service encounters an error, it should be logged and handled gracefully.

        Parameters:
        - None

        Returns:
        - None.
        """
        if self.is_listening:
            logger.info("Stopping speech-to-text listening")
            self.speech_to_text.stop_listening()
            transcript = self.speech_to_text.transcribe('output.wav')

            existing_text = self.message_entry.get('1.0', tk.END)

            updated_text = existing_text.strip() + " " + transcript

            self.message_entry.delete('1.0', tk.END)
            self.message_entry.insert('1.0', updated_text)

            self.listen_button.configure(image=self.listen_icon)
            self.is_listening = False
        else:
            logger.info("Starting speech-to-text listening")
            self.speech_to_text.listen()
            self.listen_button.configure(image=self.listen_icon_green)
            self.is_listening = True

        logger.info(f'Listening state toggled: Now listening: {self.is_listening}')

    def retrieve_session_id(self):
        """
        Retrieve the session ID from the master component.
        Called from: sync_send_message method.
        """
        return self.master.session_id if hasattr(self.master, 'session_id') else None
    
    def retrieve_conversation_id(self):
        """
        Retrieve the session ID from the master component.
    
        This method retrieves the session ID from the master component, if available.
        
        Side Effects:
        - None
        
        Thread Safety:
        - This method should be called from the main UI thread.
        
        Usage:
        - Called from the `sync_send_message` method.
        
        Dependencies:
        - Relies on the master component having a `session_id` attribute.
        
        Error Handling:
        - Returns None if the master component doesn't have a `session_id` attribute.
        
        Parameters:
        - None
        
        Returns:
        - The session ID if available, otherwise None.
        """
        return self.master.conversation_id if hasattr(self.master, 'conversation_id') else None

    def sync_send_message(self):
        """
        Synchronously sends a message by wrapping the asynchronous send_message call.
    
        This method is called when the send button is clicked. It ensures that the session and
        conversation IDs are set before sending the message. It then creates an asynchronous task
        to send the message using the `send_message` function.
        
        Side Effects:
        - Sets the `session_id` and `conversation_id` attributes if they are None.
        - Creates an asynchronous task to send the message.
        
        Thread Safety:
        - This method should be called from the main UI thread.
        
        Usage:
        - Bound to the send button's command in the `create_message_entry` method.
        
        Dependencies:
        - Relies on the `retrieve_session_id` and `retrieve_conversation_id` methods to get the IDs.
        - Relies on the `send_message` function to send the message asynchronously.
        
        Error Handling:
        - None
        
        Parameters:
        - None
        
        Returns:
        - None.
        """
        if self.session_id is None:
            self.session_id = self.retrieve_session_id() 

        if self.conversation_id is None:
            self.conversation_id = self.retrieve_conversation_id()  

        logger.info(f"About to call send_message with user: %s", self.user)
        
        """
        Synchronous wrapper for send_message.
        
        This wrapper interacts with the Generate resonse functions as well as background functions that are triggered by a response.

        """
        asyncio.create_task(self.send_message(self.chat_log, 
                                              self.user, 
                                              self.message_entry, 
                                              self.system_name, 
                                              self.system_name_tag, 
                                              self.typing_indicator_index, 
                                              self.generate_response, 
                                              self.current_persona, 
                                              self.temperature, 
                                              self.top_p, 
                                              self.top_k,
                                              self.session_id,
                                              self.conversation_id))   

     