#gui/Settings/chat_settings.py

import asyncio
import json
from datetime import datetime
from PySide6 import QtWidgets, QtGui, QtCore
from google.cloud import texttospeech
from modules.speech_services.GglCldSvcs.tts import set_voice, set_tts, get_tts
from gui.fetch_models.OA_fetch_models import fetch_models_openai
from gui.fetch_models.GG_fetch_models import fetch_models_google, fetch_model_details    
from gui.Settings import chist_functions as cf
from modules.Providers.OpenAI.OA_gen_response import set_OA_model, get_OA_model
from modules.Providers.Mistral.Mistral_gen_response import set_Mistral_model, get_Mistral_model
from modules.Providers.HuggingFace.HF_gen_response import set_hf_model, get_hf_model
from modules.Providers.Google.GG_gen_response import set_GG_model, get_GG_model
from modules.Providers.Anthropic.Anthropic_gen_response import set_Anthropic_model, get_Anthropic_model
from modules.logging.logger import setup_logger

logger = setup_logger('chat_settings.py')

class ChatSettings(QtWidgets.QDialog):
    """
    The `ChatSettings` class is a subclass of `QtWidgets.QDialog` and represents the chat settings window. 
    It initializes the window with the provided `parent` and `user` parameters. 
    It sets the initial provider to 'OpenAI', loads the providers from a JSON file, and creates the widgets for the chat settings window.
    """
    def __init__(self, parent=None, user=None):
        super().__init__(parent)
        self.parent = parent
        self.user = user
        self.llm_providers = []
        self.current_llm_provider = 'Google'
        self.setStyleSheet("background-color: #000000; color: white;")
        self.load_providers()

        font_family, font_size, font_color = self.load_font_settings()
        self.parent.set_font_family(font_family)
        self.parent.set_font_size(font_size)
        self.parent.set_font_color(font_color)

        self.font_color_var = font_color

        self.update_window_font(self.parent.font_family, self.parent.font_size, self.font_color_var)

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
        Sets the current provider, logs the selected provider, switches the provider in the parent window, 
        and populates the models menu based on the selected provider.
        """
        self.current_llm_provider = llm_provider
        logger.info(f"Selected provider: {self.current_llm_provider}")
        self.parent.provider_manager.switch_provider(llm_provider)
        self.populate_models_menu()  

    def create_widgets(self): 
        """
        Creates the various widgets for the chat settings window, including the providers button, fetch models button, 
        topmost button, load chat button, voice button, toggle TTS button, temperature spinbox, top_p spinbox, and top_k spinbox.
        """
        
        self.load_providers()
        self.providers_button = QtWidgets.QPushButton("LLM Providers", self)
        self.providers_button.setStyleSheet("background-color: #000000; color: white;")
        self.providers_menu = QtWidgets.QMenu(self.providers_button)
        self.providers_button.clicked.connect(self.show_providers_menu)

        self.fetch_models_button = QtWidgets.QPushButton("Models", self)
        self.fetch_models_button.setStyleSheet("background-color: #000000; color: white;")
        self.fetch_models_menu = QtWidgets.QMenu(self.fetch_models_button)
        self.fetch_models_button.clicked.connect(self.show_fetch_models_menu)

        self.model_context_menu = QtWidgets.QMenu(self.fetch_models_button)
        self.model_context_menu.addAction("Fetch Details", self.fetch_model_details)

        self.populate_models_menu()

        self.topmost_button = QtWidgets.QPushButton("Top", self)
        self.topmost_button.setStyleSheet("background-color: #000000; color: white;")
        self.topmost_button.clicked.connect(self.parent.toggle_topmost)

        self.load_chat_button = QtWidgets.QPushButton("History", self)
        self.load_chat_button.setStyleSheet("background-color: #000000; color: white;")
        self.load_chat_button.clicked.connect(lambda: cf.load_chat_popup(self.parent))

        self.voice_button = QtWidgets.QPushButton("Voice", self)
        self.voice_button.setStyleSheet("background-color: #000000; color: white;")
        self.voice_menu = QtWidgets.QMenu(self.voice_button)
        self.voice_button.clicked.connect(self.show_voice_menu)

        self.toggle_tts_button = QtWidgets.QPushButton("TTS", self)
        self.toggle_tts_button.setStyleSheet("background-color: #000000; color: white;")
        self.toggle_tts_button.clicked.connect(self.toggle_tts)
        if get_tts():
            self.toggle_tts_button.setStyleSheet("background-color: green; color: white;")
        else:
            self.toggle_tts_button.setStyleSheet("background-color: #000000; color: white;")

        self.populate_voice_menu()

        self.font_style_frame = QtWidgets.QFrame(self)
        self.font_style_frame.setStyleSheet("background-color: #000000;")

        self.font_style_button = QtWidgets.QPushButton("Font Style", self)
        self.font_style_button.setStyleSheet("background-color: #000000; color: white;")
        self.font_style_menu = QtWidgets.QMenu(self.font_style_button)
        self.font_style_button.clicked.connect(self.show_font_style_menu)

        available_fonts = QtGui.QFontDatabase.families()

        self.font_style_menu = QtWidgets.QMenu(self.font_style_button)
        for font_family in available_fonts:
            action = self.font_style_menu.addAction(font_family)
            action.triggered.connect(lambda checked, f=font_family: self.set_font_family(f))  

        self.font_color_frame = QtWidgets.QFrame(self)
        self.font_color_frame.setStyleSheet("background-color: #000000;")

        self.font_color_button = QtWidgets.QPushButton("Font Color", self.font_color_frame)
        self.font_color_button.setStyleSheet("background-color: #000000; color: white;")
        self.font_color_button.clicked.connect(self.choose_font_color)

        self.font_size_frame = QtWidgets.QFrame(self)
        self.font_size_frame.setStyleSheet("background-color: #000000;")
        
        self.font_size_label = QtWidgets.QLabel("Font Size:", self.font_size_frame)
        self.font_size_label.setStyleSheet("color: white;")
        
        self.font_size_spinbox = QtWidgets.QSpinBox(self.font_size_frame)
        self.font_size_spinbox.setRange(8, 24)
        self.font_size_spinbox.setSingleStep(1)
        self.font_size_spinbox.setValue(self.parent.font_size)
        self.font_size_spinbox.setStyleSheet("background-color: #000000; color: white;")
        self.font_size_spinbox.valueChanged.connect(self.update_font_size)

        self.temperature_var = 0.1
        self.temperature_frame = QtWidgets.QFrame(self)
        self.temperature_frame.setStyleSheet("background-color: #000000;")
        self.temperature_label = QtWidgets.QLabel("Temp:", self.temperature_frame)
        self.temperature_label.setStyleSheet("color: white;")
        self.temperature_spinbox = QtWidgets.QDoubleSpinBox(self.temperature_frame)
        self.temperature_spinbox.setRange(0.0, 1.0)
        self.temperature_spinbox.setSingleStep(0.01)
        self.temperature_spinbox.setValue(self.temperature_var)
        self.temperature_spinbox.setStyleSheet("background-color: #000000; color: white;")

        self.top_p_var = 0.9  
        self.top_p_frame = QtWidgets.QFrame(self)
        self.top_p_frame.setStyleSheet("background-color: #000000;")
        self.top_p_label = QtWidgets.QLabel("Top_P:", self.top_p_frame)
        self.top_p_label.setStyleSheet("color: white;")
        self.top_p_spinbox = QtWidgets.QDoubleSpinBox(self.top_p_frame)
        self.top_p_spinbox.setRange(0.0, 1.0)
        self.top_p_spinbox.setSingleStep(0.1)
        self.top_p_spinbox.setValue(self.top_p_var)
        self.top_p_spinbox.setStyleSheet("background-color: #000000; color: white;")

        self.top_k_var = 40
        self.top_k_frame = QtWidgets.QFrame(self)
        self.top_k_frame.setStyleSheet("background-color: #000000;")
        self.top_k_label = QtWidgets.QLabel("Top_K:", self.top_k_frame)
        self.top_k_label.setStyleSheet("color: white;")
        self.top_k_spinbox = QtWidgets.QSpinBox(self.top_k_frame)
        self.top_k_spinbox.setRange(0, 100)
        self.top_k_spinbox.setSingleStep(1)
        self.top_k_spinbox.setValue(self.top_k_var)
        self.top_k_spinbox.setStyleSheet("background-color: #000000; color: white;")

        layout = QtWidgets.QVBoxLayout(self)
        layout.addWidget(self.providers_button)
        layout.addWidget(self.fetch_models_button)
        layout.addWidget(self.topmost_button)
        layout.addWidget(self.load_chat_button)
        layout.addWidget(self.voice_button)
        layout.addWidget(self.toggle_tts_button)
        layout.addWidget(self.font_style_frame)
        layout.addWidget(self.font_style_button)
        layout.addWidget(self.font_color_frame)
        layout.addWidget(self.font_color_button)
        layout.addWidget(self.font_size_frame)
        layout.addWidget(self.font_size_label)
        layout.addWidget(self.font_size_spinbox)
        layout.addWidget(self.temperature_frame)
        layout.addWidget(self.temperature_label)
        layout.addWidget(self.temperature_spinbox)
        layout.addWidget(self.top_p_frame)
        layout.addWidget(self.top_p_label)
        layout.addWidget(self.top_p_spinbox)
        layout.addWidget(self.top_k_frame)
        layout.addWidget(self.top_k_label)
        layout.addWidget(self.top_k_spinbox)

        self.update_window_font(self.parent.font_family, self.parent.font_size, self.font_color_var)        
        self.font_size_spinbox.setValue(self.parent.font_size)  
        self.font_style_button.setText(self.parent.font_family)    


    def save_font_settings(self, font_family, font_size, font_color, config_file="config.ini"):
        logger.info(f"Saving font settings: Family: {font_family}, Size: {font_size}, Color: {font_color}")

        config = QtCore.QSettings(config_file, QtCore.QSettings.IniFormat)

        config.beginGroup("Font")
        config.setValue("family", font_family)
        config.setValue("size", font_size)
        config.setValue("color", font_color)
        config.endGroup()

        logger.info(f"Font settings saved to {config_file}")

    def load_font_settings(self, config_file="config.ini"):
        logger.info(f"Loading font settings from {config_file}")

        config = QtCore.QSettings(config_file, QtCore.QSettings.IniFormat)

        font_family = config.value("Font/family", "Helvetica")
        font_size = config.value("Font/size", 12, type=int)
        font_color = config.value("Font/color", "#ffffff")

        logger.info(f"Loaded font settings: Family: {font_family}, Size: {font_size}, Color: {font_color}")

        return font_family, font_size, font_color

    def update_window_font(self, font_family, font_size, font_color):
        font = QtGui.QFont(font_family, font_size)
        self.setStyleSheet(f"background-color: #000000; color: {font_color};")
        self.setFont(font)

        for widget in self.findChildren(QtWidgets.QWidget):
            widget.setFont(font)
            if isinstance(widget, QtWidgets.QPushButton) or isinstance(widget, QtWidgets.QLabel):
                widget.setStyleSheet(f"background-color: #000000; color: {font_color}; font-size: {font_size}px;")
            elif isinstance(widget, QtWidgets.QDoubleSpinBox) or isinstance(widget, QtWidgets.QSpinBox):
                widget.setStyleSheet(f"background-color: #000000; color: {font_color}; font-size: {font_size}px;")
            elif isinstance(widget, QtWidgets.QMenu):
                widget.setStyleSheet(f"background-color: #000000; color: {font_color}; font-size: {font_size}px;")

    def set_font_size(self):
        selected_font_size = self.font_size_spinbox.value()
        self.parent.set_font_size(selected_font_size)

        self.update_window_font(self.parent.font_family, selected_font_size, self.parent.font_magnification, self.font_color_var)

        self.save_font_settings(self.parent.font_family, selected_font_size, self.parent.font_magnification, self.font_color_var)

    def set_font_family(self, font_family):
        self.parent.set_font_family(font_family)

        self.font_style_button.setText(font_family)

        self.update_window_font(font_family, self.parent.font_size, self.parent.font_magnification, self.font_color_var)

        self.save_font_settings(font_family, self.parent.font_size, self.parent.font_magnification, self.font_color_var)

    def update_font_size(self, value):
        selected_font_size = value
        self.parent.set_font_size(selected_font_size)

        self.update_window_font(self.parent.font_family, selected_font_size, self.font_color_var)

        self.save_font_settings(self.parent.font_family, selected_font_size, self.font_color_var)
    
    def choose_font_color(self):
        color = QtWidgets.QColorDialog.getColor(QtGui.QColor(self.font_color_var), self, "Choose Font Color")
        if color.isValid():
            self.font_color_var = color.name()
            self.update_font_color()

    def update_font_color(self):
        selected_font_color = self.font_color_var
        self.parent.set_font_color(selected_font_color)
        self.update_window_font(self.parent.font_family, self.parent.font_size, selected_font_color)
        self.save_font_settings(self.parent.font_family, self.parent.font_size, selected_font_color)

    def toggle_tts(self):
        """
        The `toggle_tts` method toggles the text-to-speech (TTS) functionality on or off. It updates the state of the TTS button and logs the corresponding action.
        """
        logger.info("Entering toggle_tts")
        if get_tts():
            set_tts(False)
            self.toggle_tts_button.setStyleSheet("background-color: #000000; color: white; font-size: 16px;")
            logger.info("TTS turned off")
        else:
            set_tts(True)
            self.toggle_tts_button.setStyleSheet("background-color: green; color: white; font-size: 16px;")
            logger.info("TTS turned on")
        logger.info("Exiting toggle_tts")

    def populate_voice_menu(self):
        """
        Populates the voice menu with available English voices using the Google Cloud Text-to-Speech API. It retrieves the voices for the specified language codes and adds them as options in the voice menu. 
        """
        logger.info(f"{datetime.now()}: Populating voice menu...")
        client = texttospeech.TextToSpeechClient()
        english_language_codes = ["en-GB", "en-US"]

        self.voice_menu = QtWidgets.QMenu(self.voice_button)
        self.voice_button.setMenu(self.voice_menu)

        for language_code in english_language_codes:
            try:
                logger.info(f"{datetime.now()}: Getting voices for {language_code}...")
                response = client.list_voices(language_code=language_code)
                logger.info(f"{datetime.now()}: Received response for {language_code}.")

                for voice in response.voices:
                    voice_name = voice.name
                    action = self.voice_menu.addAction(voice_name)
                    action.triggered.connect(lambda checked, v=voice_name: self.on_voice_selection(v))
            except Exception as e:
                logger.error(f"{datetime.now()}: Error while getting voices for {language_code}: {e}")

    def on_voice_selection(self, voice_name):
        """
        Called when a voice is selected from the menu, and it sets the selected voice and updates the voice button text.

        """
        logger.info("Voice selection started: %s", voice_name)
        try:
            set_voice(voice_name)
            self.voice_button.setText(voice_name)
            logger.info("Voice selected and applied: %s", voice_name)
        except Exception as e:
            logger.error("Failed to select voice: %s", voice_name, exc_info=True)
    
    def update_chat_component(self):
        """
        Updates the chat component settings based on the values of the temperature, top_p, and top_k spinboxes. 
        It retrieves the values from the corresponding variables and assigns them to the parent window's attributes.
        """
        logger.info("Updating chat component settings")
        try:
            self.parent.temperature = self.temperature_spinbox.value()
            self.parent.top_p = self.top_p_spinbox.value()
            self.parent.top_k = self.top_k_spinbox.value()
            self.parent.font_size = self.font_size_spinbox.value()
            logger.info("Chat component updated - Temp: %f, Top P: %f, Top K: %d",
                        self.parent.temperature, self.parent.top_p, self.parent.top_k)
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
            self.fetch_models_menu.clear()
            self.fetch_models_menu.addAction("OpenAI", self.fetch_models_openai_wrapper)
            self.fetch_models_menu.addAction("Google", self.fetch_models_google_wrapper)

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
                model_menu = QtWidgets.QMenu(model, self.fetch_models_menu)
                model_menu.addAction("Select", lambda m=model: self.set_model_and_update_button(m))
                model_menu.addAction("Details", lambda m=model: self.fetch_model_details(self.parent.chat_log, m))
                self.fetch_models_menu.addMenu(model_menu)
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

            if current_model and current_model == self.fetch_models_button.text():
                logger.info("Model set successfully: %s", current_model)
            else:
                logger.error("Failed to set model. Expected: %s, Found: %s", self.fetch_models_button.text(), current_model)
        except Exception as e:
            logger.error("Error checking current model", exc_info=True)

    def toggle_topmost(self):
        """
         Toggles the topmost state of the chat settings window. 
         It checks if the window is visible and toggles the window flags to enable or disable the stay-on-top behavior. 
         It logs the new topmost state.
        """
        logger.info("Toggling topmost state")
        try:
            if self.isVisible():
                flags = self.windowFlags()
                if flags & QtCore.Qt.WindowStaysOnTopHint:
                    self.setWindowFlags(flags & ~QtCore.Qt.WindowStaysOnTopHint)
                    logger.info("Topmost state changed to: False")
                else:
                    self.setWindowFlags(flags | QtCore.Qt.WindowStaysOnTopHint)
                    logger.info("Topmost state changed to: True")
                self.show()
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
        self.fetch_models_button.setText(model)
        logger.info(f"fetch_models_button text updated to: {model}")
        
        self.check_current_model()

    def fetch_models_google_wrapper(self):
        """
        The `fetch_models_google_wrapper` and `fetch_models_openai_wrapper` methods are wrapper functions that create asynchronous tasks to fetch models from Google and OpenAI, respectively. 
        They pass the chat log from the parent window to the corresponding `fetch_models_*` functions.
        """
        chat_log = self.parent.chat_log  
        asyncio.create_task(fetch_models_google(chat_log))

    def fetch_models_openai_wrapper(self):
        logger.info("Fetching OpenAI models...")
        try:
            chat_log = self.parent.chat_log
            asyncio.create_task(fetch_models_openai(chat_log))
            logger.info("Asynchronous task to fetch OpenAI models started")
        except Exception as e:
            logger.error("Failed to start task for fetching OpenAI models", exc_info=True)
 
    def show_model_context_menu(self, pos):
        """
        The `show_model_context_menu` method shows a context menu for the selected model when right-clicking on a model in the fetch models menu. 
        It identifies the selected model based on the mouse event position and displays the context menu at the mouse position.
        """
        try:
            action = self.fetch_models_menu.actionAt(pos)
            if action:
                self.selected_model = action.text()
                logger.info("Showing context menu for model: %s", self.selected_model)
                self.model_context_menu.popup(self.fetch_models_button.mapToGlobal(pos))
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
            selected_model = self.fetch_models_button.text()
            logger.info("Selected model for details: %s", selected_model)
            asyncio.create_task(fetch_model_details(chat_log, model_name))
            logger.info("Asynchronous task to fetch model details started for: %s", model_name)
        except Exception as e:
            logger.error("Failed to start task for fetching model details for: %s", model_name, exc_info=True)

    def do_nothing(self):
        pass

    def show_providers_menu(self):
        self.providers_menu.clear()
        self.providers_button.setMenu(self.providers_menu)

        for llm_provider in self.llm_providers:       
            action = self.providers_menu.addAction(llm_provider)
            action.triggered.connect(lambda checked, p=llm_provider: self.set_provider(p))
        self.providers_menu.exec(QtGui.QCursor.pos())

    def show_fetch_models_menu(self):
        self.fetch_models_button.setMenu(self.fetch_models_menu)
        self.populate_models_menu()
        self.fetch_models_menu.exec(QtGui.QCursor.pos())

    def show_voice_menu(self):
        self.populate_voice_menu()
        self.voice_menu.exec(QtGui.QCursor.pos())

    def show_font_style_menu(self):
        self.font_style_menu.clear()
        available_fonts = QtGui.QFontDatabase.families()
        for font_family in available_fonts:
            action = self.font_style_menu.addAction(font_family)
            action.triggered.connect(lambda checked, f=font_family: self.set_font_family(f))
        self.font_style_menu.exec(QtGui.QCursor.pos())