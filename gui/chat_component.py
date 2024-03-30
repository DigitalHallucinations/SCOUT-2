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
from modules.Providers.provider_manager import ProviderManager


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

    levels = {
        'DEBUG': logging.DEBUG,
        'INFO': logging.INFO,
        'WARNING': logging.WARNING,
        'ERROR': logging.ERROR,
        'CRITICAL': logging.CRITICAL
    }
    
    logger.setLevel(levels.get(level, logging.WARNING))

class ChatComponent(tk.Frame):
    def __init__(self, master=None, persona=None, user=None, session_id=None, conversation_id=None, logout_callback=None, schedule_async_task=None, scale_factor=1.0):

        super().__init__(master)
        self.scale_factor = scale_factor
        self.persona = persona
        self.message_entry_visible = True
        self.schedule_async_task = schedule_async_task
        self.session_id = session_id
        self.conversation_id = conversation_id
        self.logout_callback = logout_callback
        self.user = user 
        self.provider_manager = ProviderManager(self)
        self.current_provider = self.provider_manager.current_provider
        self.send_message = send_message_module.send_message
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
       
        if system_name_tag not in self.chat_log.tag_names():
            self.chat_log.tag_configure(system_name_tag, foreground=system_name_color)

    def update_conversation_id(self, new_conversation_id):

        self.conversation_id = new_conversation_id
        logger.info(f"ChatComponent updated with new conversation_id: {new_conversation_id}")

    def create_widgets(self):

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

        img = Image.open(icon_path)
        img = img.resize((int(img.width * scale_factor), int(img.height * scale_factor)), Image.Resampling.LANCZOS)
        return ImageTk.PhotoImage(img)

    def on_logout(self):

        logger.info(f"Logout initiated from ChatComponent.")
        if self.logout_callback:
            self.logout_callback()
        else:
            logger.error(f"No logout callback provided.")
            
    def clear_chat_interface(self):
  
        if hasattr(self.master, 'log_out'):
            self.master.log_out(None)

    def open_settings(self):
 
        self.chat_settings_instance = ChatSettings(master=self, user=self.user)
        self.chat_settings_instance.withdraw()  
        self.chat_settings_instance.deiconify()  

    def show_context_menu(self):

        context_menu = tk.Menu(self.chat_log, tearoff=0)
        context_menu.add_command(label="Copy", command=self.copy_selected)
        self.chat_log.bind("<Button-3>", lambda event: context_menu.tk_popup(event.x_root, event.y_root))

    def copy_selected(self):

        self.clipboard_clear()  
        try:
            selected_text = self.chat_log.get(tk.SEL_FIRST, tk.SEL_LAST)    
            self.clipboard_append(selected_text)    
        except tk.TclError: 
            pass  

    def paste_func(self, event): 

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

    def toggle_media_component(self):
 
        if hasattr(self, 'media_component'):
            if self.media_component.winfo_viewable():
                self.media_component.withdraw()
            else:
                self.media_component.deiconify()
        else:
            self.media_component = MediaComponent(self)

    def show_media_component(self):

        self.master.media_component = MediaComponent(self)        

    def toggle_topmost(self):
  
        if self.winfo_ismapped():
            self.winfo_toplevel().attributes("-topmost", not self.winfo_toplevel().attributes("-topmost")) 

    def toggle_listen(self):

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

        return self.master.session_id if hasattr(self.master, 'session_id') else None
    
    def retrieve_conversation_id(self):

        return self.master.conversation_id if hasattr(self.master, 'conversation_id') else None

    def sync_send_message(self):

        if self.session_id is None:
            self.session_id = self.retrieve_session_id() 

        if self.conversation_id is None:
            self.conversation_id = self.retrieve_conversation_id()  

        logger.info(f"About to call send_message with user: %s", self.user)
        

        asyncio.create_task(self.send_message(self.chat_log, 
                                              self.user, 
                                              self.message_entry, 
                                              self.system_name, 
                                              self.system_name_tag, 
                                              self.typing_indicator_index, 
                                              self.provider_manager.generate_response, 
                                              self.current_persona, 
                                              self.temperature, 
                                              self.top_p, 
                                              self.top_k,
                                              self.session_id,
                                              self.conversation_id))