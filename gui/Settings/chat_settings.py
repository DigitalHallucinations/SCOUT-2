#gui/Settings/chat_settings.py

import tkinter as tk
import tkinter.font as tkFont
import tkinter.colorchooser as colorchooser
import configparser
import json
import asyncio
from datetime import datetime
from google.cloud import texttospeech
from modules.speech_services.GglCldSvcs.tts import set_voice, set_tts, get_tts
from gui.fetch_models.OA_fetch_models import fetch_models_openai
from ..fetch_models.GG_fetch_models import fetch_models_google, fetch_model_details    
from gui.Settings import chist_functions as cf
from modules.Providers.OpenAI.OA_gen_response import set_OA_model, get_OA_model
from modules.Providers.Mistral.Mistral_gen_response import set_Mistral_model, get_Mistral_model
from modules.Providers.HuggingFace.HF_gen_response import set_hf_model, get_hf_model
from modules.Providers.Google.GG_gen_response import set_GG_model, get_GG_model
from modules.Providers.Anthropic.Anthropic_gen_response import set_Anthropic_model, get_Anthropic_model
from modules.logging.logger import setup_logger

logger = setup_logger('chat_settings.py')

class ChatSettings(tk.Toplevel):
    """
    The `ChatSettings` class is a subclass of `tk.Toplevel` and represents the chat settings window. 
    It initializes the window with the provided `master` and `user` parameters. 
    It sets the initial provider to 'OpenAI', loads the providers from a JSON file, and creates the widgets for the chat settings window.
    """
    def __init__(self, master=None, user=None):
        super().__init__(master) 
        self.master = master
        self.user = user
        self.llm_providers = []  
        self.current_llm_provider = 'Google'  
        self.title("Chat Settings")
        self.configure(bg="#000000") 
        self.load_providers() 

        font_family, font_size, font_color = self.load_font_settings()
        self.master.set_font_family(font_family)
        self.master.set_font_size(font_size)
        self.master.set_font_color(font_color)

        self.font_color_var = tk.StringVar(value=font_color)

        self.update_window_font(self.master.font_family, self.master.font_size, self.font_color_var.get()) 

        self.create_widgets()
        logger.info("ChatSettings widgets created")
            
    def load_providers(self):
        """
        Loads the available providers from the `providers.json` file.
        """
        with open('modules/Providers/providers.json') as f:
            self.llm_providers = json.load(f)

    def set_provider(self, llm_provider):
        """
        Sets the current provider, logs the selected provider, switches the provider in the master window, 
        and populates the models menu based on the selected provider.
        """
        self.current_llm_provider = llm_provider
        logger.info(f"Selected provider: {self.current_llm_provider}")
        self.master.provider_manager.switch_provider(llm_provider)
        self.populate_models_menu()  

    def create_widgets(self): 
        """
        Creates the various widgets for the chat settings window, including the providers button, fetch models button, 
        topmost button, load chat button, voice button, toggle TTS button, temperature spinbox, top_p spinbox, and top_k spinbox.
        """
        
        self.load_providers()
        self.providers_button = tk.Menubutton(self, text="LLM Providers", relief="raised", bg="#000000", fg="white")
        self.providers_button.pack()

        self.providers_menu = tk.Menu(self.providers_button, tearoff=0)
        self.providers_button.configure(menu=self.providers_menu)
        for llm_provider in self.llm_providers:
            self.providers_menu.add_command(label=llm_provider, command=lambda p=llm_provider: self.set_provider(p))

        self.fetch_models_button = tk.Menubutton(self, text="Models", relief="raised", bg="#000000", fg="white")
        self.fetch_models_button.pack()

        self.fetch_models_menu = tk.Menu(self.fetch_models_button, tearoff=0)
        self.fetch_models_button.configure(menu=self.fetch_models_menu)

        self.model_context_menu = tk.Menu(self.fetch_models_button, tearoff=0)
        self.model_context_menu.add_command(label="Fetch Details", command=self.fetch_model_details)

        self.populate_models_menu()

        self.topmost_button = tk.Button(self, text="Top", bg="#000000", fg="white", command=self.master.toggle_topmost)
        self.topmost_button.pack()

        self.load_chat_button = tk.Button(self, text="History", bg="#000000", fg="white", command=lambda: cf.load_chat_popup(self.master))
        self.load_chat_button.pack()

        self.voice_button = tk.Menubutton(self, text="Voice", relief="raised", bg="#000000", fg="white")
        self.voice_button.pack()

        self.voice_menu = tk.Menu(self.voice_button, tearoff=0)
        self.voice_button.configure(menu=self.voice_menu)

        self.toggle_tts_button = tk.Button(self, text="TTS", command=self.toggle_tts, bg="#000000" if not get_tts() else "green", fg="#ffffff", activebackground="#5a6dad", activeforeground="#ffffff")
        if get_tts():
            self.toggle_tts_button.configure(bg="green")
        else:
            self.toggle_tts_button.configure(bg="#000000")
        self.toggle_tts_button.pack()
   
        self.populate_voice_menu()

        self.font_style_frame = tk.Frame(self, bg="#000000")
        self.font_style_frame.pack()

        self.font_style_button = tk.Menubutton(self, text="Font Style", relief="raised", bg="#000000", fg="white")
        self.font_style_button.pack()

        self.font_style_menu = tk.Menu(self.font_style_button, tearoff=0)
        self.font_style_button.configure(menu=self.font_style_menu)

        available_fonts = list(tkFont.families())

        for font_family in available_fonts:
            self.font_style_menu.add_command(label=font_family, command=lambda f=font_family: self.set_font_family(f))  

        self.font_color_frame = tk.Frame(self, bg="#000000")
        self.font_color_frame.pack()

        self.font_color_button = tk.Button(self.font_color_frame, text="Font Color", command=self.choose_font_color, bg="#000000", fg="white")
        self.font_color_button.pack(side="left")

        self.font_size_frame = tk.Frame(self, bg="#000000")
        self.font_size_frame.pack()
        
        self.font_size_label = tk.Label(self.font_size_frame, text="Font Size:", bg="#000000", fg="white")
        self.font_size_label.pack(side="left")
        
        self.font_size_var = tk.DoubleVar(value=1.0)
        self.font_size_spinbox = tk.Spinbox(self.font_size_frame, from_=1.0, to=1.5, increment=0.1, 
                                            textvariable=self.font_size_var, width=6, 
                                            bg="#000000", fg="white", buttonbackground="#000000", 
                                            command=self.update_font_size, format="%.2f")
        self.font_size_spinbox.pack(side="left")

        self.temperature_var = tk.DoubleVar(value=0.1)
        self.temperature_frame = tk.Frame(self)
        self.temperature_frame.pack()
        self.temperature_label = tk.Label(self.temperature_frame, text="Temp:", bg="#000000", fg="white")
        self.temperature_label.pack(side="left")  
        self.temperature_spinbox = tk.Spinbox(self.temperature_frame, from_=0.0, to=1.0, increment=0.01, textvariable=self.temperature_var, width=6, bg="#000000", fg="white", buttonbackground="#000000", format="%.2f")
        self.temperature_spinbox.pack(side="left")

        self.top_p_var = tk.DoubleVar(value=0.9)  
        self.top_p_frame = tk.Frame(self)
        self.top_p_frame.pack()
        self.top_p_label = tk.Label(self.top_p_frame, text="Top_P:", bg="#000000", fg="white")
        self.top_p_label.pack(side="left")  
        self.top_p_spinbox = tk.Spinbox(self.top_p_frame, from_=0.0, to=1.0, increment=0.1, textvariable=self.top_p_var, width=6, bg="#000000", fg="white", buttonbackground="#000000", format="%.2f")
        self.top_p_spinbox.pack(side="left") 

        self.top_k_var = tk.IntVar(value=40)
        self.top_k_frame = tk.Frame(self)
        self.top_k_frame.pack()
        self.top_k_label = tk.Label(self.top_k_frame, text="Top_K:", bg="#000000", fg="white")
        self.top_k_label.pack(side="left")  
        self.top_k_spinbox = tk.Spinbox(self.top_k_frame, from_=0.0, to=100.0, increment=1, textvariable=self.top_k_var, width=6, bg="#000000", fg="white", buttonbackground="#000000", format="%.2f")
        self.top_k_spinbox.pack(side="left")   

        # Apply loaded font settings to widgets
        self.update_window_font(self.master.font_family, self.master.font_size, self.font_color_var.get())
        self.font_size_var.set(self.master.font_size)  # Update the font size spinbox
        self.font_style_button.config(text=self.master.font_family)  # Update the font style button text


    def save_font_settings(self, font_family, font_size, font_color, config_file="config.ini"):
        logger.info(f"Saving font settings: Family: {font_family}, Size: {font_size}, Color: {font_color}")

        config = configparser.ConfigParser()
        config.read(config_file)

        if not config.has_section("Font"):
            logger.info("Creating new 'Font' section in config file")
            config.add_section("Font")

        config.set("Font", "family", font_family)
        config.set("Font", "size", str(font_size))
        config.set("Font", "color", font_color)

        with open(config_file, "w") as f:
            config.write(f)
            logger.info(f"Font settings saved to {config_file}")

    def load_font_settings(self, config_file="config.ini"):
        logger.info(f"Loading font settings from {config_file}")

        config = configparser.ConfigParser()
        config.read(config_file)

        try:
            font_family = config.get("Font", "family")
            font_size = config.getfloat("Font", "size")
            font_color = config.get("Font", "color")
            logger.info(f"Loaded font settings: Family: {font_family}, Size: {font_size}, Color: {font_color}")
        except (configparser.NoSectionError, configparser.NoOptionError):
            logger.warning("No font settings found in config file, using defaults")
            font_family = "Helvetica"
            font_size = 12.0
            font_color = "#ffffff"
            self.save_font_settings(font_family, font_size, font_color, config_file)

        return font_family, font_size, font_color

    def update_window_font(self, font_family, font_size, font_color):
        for widget in self.winfo_children():
            try:
                widget.configure(font=(font_family, int(font_size * 10), "normal"), fg=font_color)
            except tk.TclError:
                pass

        if hasattr(self, 'font_size_label'):
            self.font_size_label.config(font=(font_family, int(font_size * 10), "normal"), fg=font_color)
        if hasattr(self, 'font_size_spinbox'):
            self.font_size_spinbox.config(font=(font_family, int(font_size * 10), "normal"), fg=font_color)
        if hasattr(self, 'font_color_button'):
            self.font_color_button.config(font=(font_family, int(font_size * 10), "normal"), fg=font_color)
        if hasattr(self, 'temperature_label'):
            self.temperature_label.config(font=(font_family, int(font_size * 10), "normal"), fg=font_color)
        if hasattr(self, 'temperature_spinbox'):
            self.temperature_spinbox.config(font=(font_family, int(font_size * 10), "normal"), fg=font_color)
        if hasattr(self, 'top_p_label'):
            self.top_p_label.config(font=(font_family, int(font_size * 10), "normal"), fg=font_color)
        if hasattr(self, 'top_p_spinbox'):
            self.top_p_spinbox.config(font=(font_family, int(font_size * 10), "normal"), fg=font_color)
        if hasattr(self, 'top_k_label'):
            self.top_k_label.config(font=(font_family, int(font_size * 10), "normal"), fg=font_color)
        if hasattr(self, 'top_k_spinbox'):
            self.top_k_spinbox.config(font=(font_family, int(font_size * 10), "normal"), fg=font_color)
        if hasattr(self, 'providers_button'):
            self.providers_button.config(font=(font_family, int(font_size * 10), "normal"), fg=font_color)
        if hasattr(self, 'fetch_models_button'):
            self.fetch_models_button.config(font=(font_family, int(font_size * 10), "normal"), fg=font_color)
        if hasattr(self, 'topmost_button'):
            self.topmost_button.config(font=(font_family, int(font_size * 10), "normal"), fg=font_color)
        if hasattr(self, 'load_chat_button'):
            self.load_chat_button.config(font=(font_family, int(font_size * 10), "normal"), fg=font_color)
        if hasattr(self, 'voice_button'):
            self.voice_button.config(font=(font_family, int(font_size * 10), "normal"), fg=font_color)
        if hasattr(self, 'toggle_tts_button'):
            self.toggle_tts_button.config(font=(font_family, int(font_size * 10), "normal"), fg=font_color)
        if hasattr(self, 'font_style_button'):
            self.font_style_button.config(font=(font_family, int(font_size * 10), "normal"), fg=font_color)

            
    def set_font_size(self):
        selected_font_size = self.font_size_var.get()
        self.master.set_font_size(selected_font_size)

        for widget in self.winfo_children():
            try:
                widget.config(font=(self.master.font_family, int(selected_font_size * 10), "normal"))
            except tk.TclError:
                pass  # Handle widgets that don't support the 'font' option

        self.font_style_button.config(font=(self.master.font_family, int(selected_font_size * 10), "normal"))
        self.font_size_label.config(font=(self.master.font_family, int(selected_font_size * 10), "normal"))

        self.temperature_label.config(font=(self.master.font_family, int(selected_font_size * 10), "normal"))
        self.top_p_label.config(font=(self.master.font_family, int(selected_font_size * 10), "normal"))
        self.top_k_label.config(font=(self.master.font_family, int(selected_font_size * 10), "normal"))

        self.temperature_spinbox.config(font=(self.master.font_family, int(selected_font_size * 10), "normal"))
        self.top_p_spinbox.config(font=(self.master.font_family, int(selected_font_size * 10), "normal"))
        self.top_k_spinbox.config(font=(self.master.font_family, int(selected_font_size * 10), "normal"))
        self.font_size_spinbox.config(font=(self.master.font_family, int(selected_font_size * 10), "normal"))


        self.update_window_font(self.master.font_family, selected_font_size)
        self.save_font_settings(self.master.font_family, selected_font_size)

    def set_font_family(self, font_family):
        self.master.set_font_family(font_family)

        for widget in self.winfo_children():
            try:
                widget.config(font=(font_family, int(self.master.font_size * 10), "normal"))
            except tk.TclError:
                pass

        self.font_style_button.config(font=(font_family, int(self.master.font_size * 10), "normal"))
        self.font_size_label.config(font=(font_family, int(self.master.font_size * 10), "normal"))

        self.temperature_label.config(font=(font_family, int(self.master.font_size * 10), "normal"))
        self.top_p_label.config(font=(font_family, int(self.master.font_size * 10), "normal"))
        self.top_k_label.config(font=(font_family, int(self.master.font_size * 10), "normal"))

        self.temperature_spinbox.config(font=(font_family, int(self.master.font_size * 10), "normal"))
        self.top_p_spinbox.config(font=(font_family, int(self.master.font_size * 10), "normal"))
        self.top_k_spinbox.config(font=(font_family, int(self.master.font_size * 10), "normal"))
        self.font_size_spinbox.config(font=(font_family, int(self.master.font_size * 10), "normal"))

        self.font_style_button.config(text=font_family)

        self.update_window_font(font_family, self.master.font_size, self.font_color_var.get())

        self.save_font_settings(font_family, self.master.font_size, self.font_color_var.get())

    def update_font_size(self):
        selected_font_size = self.font_size_var.get()
        self.master.set_font_size(selected_font_size)

        for widget in self.winfo_children():
            try:
                widget.config(font=(self.master.font_family, int(selected_font_size * 10), "normal"))
            except tk.TclError:
                pass

        self.font_style_button.config(font=(self.master.font_family, int(selected_font_size * 10), "normal"))
        self.font_size_label.config(font=(self.master.font_family, int(selected_font_size * 10), "normal"))

        self.temperature_label.config(font=(self.master.font_family, int(selected_font_size * 10), "normal"))
        self.top_p_label.config(font=(self.master.font_family, int(selected_font_size * 10), "normal"))
        self.top_k_label.config(font=(self.master.font_family, int(selected_font_size * 10), "normal"))

        self.temperature_spinbox.config(font=(self.master.font_family, int(selected_font_size * 10), "normal"))
        self.top_p_spinbox.config(font=(self.master.font_family, int(selected_font_size * 10), "normal"))
        self.top_k_spinbox.config(font=(self.master.font_family, int(selected_font_size * 10), "normal"))
        self.font_size_spinbox.config(font=(self.master.font_family, int(selected_font_size * 10), "normal"))

        # Update ChatSettings window font
        self.update_window_font(self.master.font_family, selected_font_size, self.font_color_var.get())

        # Save the font settings
        self.save_font_settings(self.master.font_family, selected_font_size, self.font_color_var.get())

    def choose_font_color(self):
        color = colorchooser.askcolor(title="Choose Font Color")[1]
        if color:
            self.font_color_var.set(color)
            self.update_font_color()

    def update_font_color(self):
        selected_font_color = self.font_color_var.get()
        self.master.set_font_color(selected_font_color)
        self.update_window_font(self.master.font_family, self.master.font_size, selected_font_color)
        self.save_font_settings(self.master.font_family, self.master.font_size, selected_font_color)

    def toggle_tts(self):
        """
        The `toggle_tts` method toggles the text-to-speech (TTS) functionality on or off. It updates the state of the TTS button and logs the corresponding action.
        """
        logger.info("Entering toggle_tts")
        if get_tts():
            set_tts(False)
            self.toggle_tts_button.configure(bg="#000000")
            logger.info("TTS turned off")
        else:
            set_tts(True)
            self.toggle_tts_button.configure(bg="green")
            logger.info("TTS turned on")
        logger.info("Exiting toggle_tts")

    def populate_voice_menu(self):
        """
        Populates the voice menu with available English voices using the Google Cloud Text-to-Speech API. It retrieves the voices for the specified language codes and adds them as options in the voice menu. 
        """
        logger.info(f"{datetime.now()}: Populating voice menu...")
        client = texttospeech.TextToSpeechClient()
        english_language_codes = ["en-GB", "en-US"]

        for language_code in english_language_codes:
            try:
                logger.info(f"{datetime.now()}: Getting voices for {language_code}...")
                response = client.list_voices(language_code=language_code)
                logger.info(f"{datetime.now()}: Received response for {language_code}.")

                for voice in response.voices:
                    voice_name = voice.name
                    self.voice_menu.add_command(
                        label=voice_name,
                        command=lambda v=voice_name: self.on_voice_selection(v),
                    )
            except Exception as e:
                logger.error(f"{datetime.now()}: Error while getting voices for {language_code}: {e}")

    def on_voice_selection(self, voice_name):
        """
        Called when a voice is selected from the menu, and it sets the selected voice and updates the voice button text.

        """
        logger.info("Voice selection started: %s", voice_name)
        try:
            set_voice(voice_name)
            self.voice_button.config(text=voice_name)
            logger.info("Voice selected and applied: %s", voice_name)
        except Exception as e:
            logger.error("Failed to select voice: %s", voice_name, exc_info=True)
    
    def update_chat_component(self):
        """
        Updates the chat component settings based on the values of the temperature, top_p, and top_k spinboxes. 
        It retrieves the values from the corresponding variables and assigns them to the master window's attributes.
        """
        logger.info("Updating chat component settings")
        try:
            self.master.temperature = self.temperature_var.get()
            self.master.top_p = self.top_p_var.get()
            self.master.top_k = self.top_k_var.get()
            self.master.font_size = self.font_size_var.get()
            logger.info("Chat component updated - Temp: %f, Top P: %f, Top K: %d",
                        self.master.temperature, self.master.top_p, self.master.top_k)
        except Exception as e:
            logger.error("Failed to update chat component settings", exc_info=True)

    def populate_models_menu(self):
        """
        Populates the models menu based on the selected provider. 
        It clears the existing menu items and adds options for OpenAI and Google models. 
        It then loads the models from the corresponding JSON file based on the current provider. 
        For each model, it creates a submenu with options to select the model and fetch model details.
        The model submenus are added as cascading menus to the fetch models menu.
        """
        logger.info("Populating models menu for provider: %s", self.current_llm_provider)
        try:
            self.fetch_models_menu.delete(0, 'end')
            self.fetch_models_menu.add_command(label="OpenAI", command=self.fetch_models_openai_wrapper)
            self.fetch_models_menu.add_command(label="Google", command=self.fetch_models_google_wrapper)

            models_files = {
                'OpenAI': 'modules/Providers/OpenAI/OA_models.json',
                'Mistral': 'modules/Providers/Mistral/Mistral_models.json',
                'Google': 'modules/Providers/Google/GG_models.json',
                'HuggingFace': 'modules/Providers/HuggingFace/HF_models.json',
                'Anthropic': 'modules/Providers/Anthropic/Anthropic_models.json',
            }

            current_models_file = models_files.get(self.current_llm_provider)
            logger.info("Loading models from file: %s", current_models_file)

            with open(current_models_file) as json_file:
                models = json.load(json_file)['models']
                logger.info("Loaded %d models for provider: %s", len(models), self.current_llm_provider)

            for model in models:
                logger.info("Adding model to menu: %s", model)
                model_menu = tk.Menu(self.fetch_models_menu, tearoff=0)
                model_menu.add_command(label="Select", command=lambda m=model: self.set_model_and_update_button(m))
                model_menu.add_command(label="Details", command=lambda m=model: self.fetch_model_details(self.master.chat_log, m))
                self.fetch_models_menu.add_cascade(label=model, menu=model_menu)
        except Exception as e:
            logger.error("Failed to populate models menu", exc_info=True)

    def check_current_model(self):
        """
        Checks the currently selected model against the model displayed on the fetch models button. 
        It retrieves the current model based on the selected provider using the corresponding `get_*_model` functions. 
        It then compares the current model with the text of the fetch models button and logs the result.
        """
        logger.info("Checking current model against selected model")
        try:
            current_model = None
            if self.current_llm_provider == 'Google':
                current_model = get_GG_model()
                logger.info("Current provider: Google")
            elif self.current_llm_provider == 'Mistral':
                current_model = get_Mistral_model()
                logger.info("Current provider: Mistral")
            elif self.current_llm_provider == 'HuggingFace':
                current_model = get_hf_model()
                logger.info("Current provider: HuggingFace")
            elif self.current_llm_provider == 'OpenAI':
                current_model = get_OA_model()
                logger.info("Current provider: OpenAI")
            elif self.current_llm_provider == 'Anthropic':
                current_model = get_Anthropic_model()
                logger.info("Current provider: OpenAI")    

            if current_model and current_model == self.fetch_models_button.cget("text"):
                logger.info("Model set successfully: %s", current_model)
            else:
                logger.error("Failed to set model. Expected: %s, Found: %s", self.fetch_models_button.cget("text"), current_model)
        except Exception as e:
            logger.error("Error checking current model", exc_info=True)

    def toggle_topmost(self):
        """
         Toggles the topmost state of the chat settings window. 
         It checks if the window is mapped (visible) and toggles the topmost attribute of the window's toplevel (Main Window) widget. 
         It logs the new topmost state.
        """
        logger.info("Toggling topmost state")
        try:
            if self.winfo_ismapped():
                new_state = not self.winfo_toplevel().attributes("-topmost")
                self.winfo_toplevel().attributes("-topmost", new_state)
                logger.info("Topmost state changed to: %s", new_state)
        except Exception as e:
            logger.error("Failed to toggle topmost state", exc_info=True)

    def set_model_and_update_button(self, model):
        """
        Sets the selected model based on the current provider using the corresponding `set_*_model` functions. 
        It updates the text of the fetch models button to display the selected model and calls the `check_current_model` method to verify the model selection.
        """
        logger.info(f"Setting model: {model}")
        if self.current_llm_provider == 'Google':
            set_GG_model(model)
        elif self.current_llm_provider == 'Mistral':
            set_Mistral_model(model)
        elif self.current_llm_provider == 'HuggingFace':
            set_hf_model(model)
        elif self.current_llm_provider == 'OpenAI':
            set_OA_model(model)
        elif self.current_llm_provider == 'Anthropic':
            set_Anthropic_model(model)    
        logger.info(f"Model {model} set successfully for {self.current_llm_provider}")
        
        logger.info("Updating fetch_models_button text")
        self.fetch_models_button.config(text=model)
        logger.info(f"fetch_models_button text updated to: {model}")
        
        self.check_current_model()

    def fetch_models_google_wrapper(self):
        """
        The `fetch_models_google_wrapper` and `fetch_models_openai_wrapper` methods are wrapper functions that create asynchronous tasks to fetch models from Google and OpenAI, respectively. 
        They pass the chat log from the master window to the corresponding `fetch_models_*` functions.
        """
        chat_log = self.master.chat_log  
        asyncio.create_task(fetch_models_google(chat_log))

    def fetch_models_openai_wrapper(self):
        logger.info("Fetching OpenAI models...")
        try:
            chat_log = self.master.chat_log
            asyncio.create_task(fetch_models_openai(chat_log))
            logger.info("Asynchronous task to fetch OpenAI models started")
        except Exception as e:
            logger.error("Failed to start task for fetching OpenAI models", exc_info=True)
 
    def show_model_context_menu(self, event):
        """
        The `show_model_context_menu` method shows a context menu for the selected model when right-clicking on a model in the fetch models menu. 
        It identifies the selected model based on the mouse event coordinates and displays the context menu at the mouse position.
        """
        try:
            self.selected_model = self.fetch_models_menu.identify("label", event.x, event.y)
            if self.selected_model:
                logger.info("Showing context menu for model: %s", self.selected_model)
                self.model_context_menu.tk_popup(event.x_root, event.y_root)
            else:
                logger.info("No model selected for context menu")
        except Exception as e:
            logger.error("Failed to show model context menu", exc_info=True)

    def fetch_model_details(self, chat_log, model_name):
        """
        Fetches the details of a selected model. 
        It retrieves the selected model from the fetch models button and creates an asynchronous task to fetch the model details using the `fetch_model_details` function from the `GG_fetch_models.py` module. 
        It passes the chat log and the model name to the function.
        """
        logger.info("Fetching details for model: %s", model_name)
        try:
            selected_model = self.fetch_models_button.cget("text")
            logger.info("Selected model for details: %s", selected_model)
            asyncio.create_task(fetch_model_details(chat_log, model_name))
            logger.info("Asynchronous task to fetch model details started for: %s", model_name)
        except Exception as e:
            logger.error("Failed to start task for fetching model details for: %s", model_name, exc_info=True)

    def show(self):
        """
        Makes the chat settings window visible by calling the `deiconify` method.
        """
        self.deiconify()

    def hide(self):
        """
        Hides the chat settings window by calling the `withdraw` method.
        """
        self.withdraw()

    def do_nothing(self):
        pass