# gui/sidebar.py

import asyncio
import json
from PySide6 import QtWidgets, QtGui, QtCore
from gui.tooltip import ToolTip
from gui import chist_functions as cf
from gui.fetch_models.OA_fetch_models import fetch_models_openai
from gui.fetch_models.GG_fetch_models import fetch_models_google, fetch_model_details    
from modules.Providers.OpenAI.OA_gen_response import set_OA_model, get_OA_model
from modules.Providers.Mistral.Mistral_gen_response import set_Mistral_model, get_Mistral_model
from modules.Providers.HuggingFace.HF_gen_response import set_hf_model, get_hf_model
from modules.Providers.Google.GG_gen_response import set_GG_model, get_GG_model
from modules.Providers.Anthropic.Anthropic_gen_response import set_Anthropic_model, get_Anthropic_model
from modules.logging.logger import setup_logger

logger = setup_logger('sidebar.py')
class Sidebar(QtWidgets.QFrame):
    def __init__(self, parent=None, personas=None, sidebar_frame_bg=None, font_color=None, font_size=None, font_family=None):
        super().__init__(parent)
        self.personas = personas
        self.sidebar_frame_bg = sidebar_frame_bg
        self.llm_providers = []
        self.current_llm_provider = 'Anthropic'
        self.load_providers()
        self.font_color = font_color
        self.font_size = font_size
        self.font_family = font_family
        self.chat_component = None  
        self.fetch_models_menu = None
        self.create_sidebar()

    def load_providers(self):
        with open('modules/Providers/providers.json') as f:
            self.llm_providers = json.load(f)

    def set_provider(self, llm_provider):
        self.current_llm_provider = llm_provider
        logger.info(f"Selected provider: {self.current_llm_provider}")
        self.chat_component.provider_manager.switch_llm_provider(llm_provider)
        self.chat_component.provider_label.setText(f"Provider: {llm_provider}")
        self.populate_models_menu()     

    def populate_models_menu(self): 
        logger.info("Populating models menu for provider: %s", self.current_llm_provider)
        try:
            self.fetch_models_menu = QtWidgets.QMenu(self.models_button)
            self.models_button.setMenu(self.fetch_models_menu)

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

    def set_model_and_update_button(self, model):
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
        self.chat_component.model_label.setText(f"Model: {model}")
        logger.info(f"fetch_models_button text updated to: {model}")
        
        self.check_current_model()

    def fetch_models_google_wrapper(self):
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
        self.providers_menu = QtWidgets.QMenu(self.providers_button)
        self.providers_button.setMenu(self.providers_menu)

        for llm_provider in self.llm_providers:       
            action = self.providers_menu.addAction(llm_provider)
            action.triggered.connect(lambda checked, p=llm_provider: self.set_provider(p))
        self.providers_menu.exec(QtGui.QCursor.pos())

    def show_fetch_models_menu(self):
        self.fetch_models_button.setMenu(self.fetch_models_menu)
        self.populate_models_menu()
        self.fetch_models_menu.exec(QtGui.QCursor.pos())


    def apply_font_settings(self):
        font = QtGui.QFont(self.font_family, self.font_size, QtGui.QFont.Normal)
        
        self.providers_button.setFont(font)
        self.providers_button.setStyleSheet(f"QPushButton {{ background-color: transparent; border: none; color: {self.font_color}; font-size: {self.font_size}px; }}")
        
        self.models_button.setFont(font)
        self.models_button.setStyleSheet(f"QPushButton {{ background-color: transparent; border: none; color: {self.font_color}; font-size: {self.font_size}px; }}")
        
        self.history_button.setFont(font)
        self.history_button.setStyleSheet(f"QPushButton {{ background-color: transparent; border: none; color: {self.font_color}; font-size: {self.font_size}px; }}")
        
        self.chat_button.setFont(font)
        self.chat_button.setStyleSheet(f"QPushButton {{ background-color: transparent; border: none; color: {self.font_color}; font-size: {self.font_size}px; }}")
        
        self.persona_button.setFont(font)
        self.persona_button.setStyleSheet(f"QPushButton {{ background-color: transparent; border: none; color: {self.font_color}; font-size: {self.font_size}px; }}")
        
        self.settings_button.setFont(font)
        self.settings_button.setStyleSheet(f"QPushButton {{ background-color: transparent; border: none; color: {self.font_color}; font-size: {self.font_size}px; }}")
        
    def create_sidebar(self):
        self.setStyleSheet(f"background-color: {self.sidebar_frame_bg}; border: none;")
        self.setFixedWidth(40)
        sidebar_layout = QtWidgets.QVBoxLayout(self)
        sidebar_layout.setContentsMargins(5, 13, 5, 10)
        sidebar_layout.setSpacing(10)

        icon_size = QtCore.QSize(32, 32)

        providers_button_frame = QtWidgets.QFrame(self)
        providers_button_frame.setObjectName("ProvidersButtonFrame")
        providers_button_frame.setStyleSheet("border: none;")
        providers_button_layout = QtWidgets.QVBoxLayout(providers_button_frame)
        providers_button_layout.setContentsMargins(2, 2, 2, 2)
        providers_button_layout.setSpacing(0)

        self.providers_button = QtWidgets.QPushButton(providers_button_frame)
        self.providers_button.setIcon(QtGui.QIcon("assets/SCOUT/Icons/providers_wt.png"))
        self.providers_button.setIconSize(icon_size)
        self.providers_button.setStyleSheet("QPushButton { background-color: transparent; border: none; }")
        self.providers_button.clicked.connect(self.show_providers_menu)
        providers_button_layout.addWidget(self.providers_button)
        self.providers_button.enterEvent = self.on_providers_button_hover
        self.providers_button.leaveEvent = self.on_providers_button_leave

        sidebar_layout.addWidget(providers_button_frame)

        models_button_frame = QtWidgets.QFrame(self)
        models_button_frame.setObjectName("ModelsButtonFrame")
        models_button_frame.setStyleSheet("border: none;")
        models_button_layout = QtWidgets.QVBoxLayout(models_button_frame)
        models_button_layout.setContentsMargins(2, 2, 2, 2)
        models_button_layout.setSpacing(0)

        self.models_button = QtWidgets.QPushButton(models_button_frame)
        self.models_button.setIcon(QtGui.QIcon("assets/SCOUT/Icons/models_wt.png"))
        self.models_button.setIconSize(icon_size)
        self.models_button.setStyleSheet("QPushButton { background-color: transparent; border: none; }")
        self.models_button.clicked.connect(self.show_fetch_models_menu)
        models_button_layout.addWidget(self.models_button)
        self.models_button.enterEvent = self.on_models_button_hover
        self.models_button.leaveEvent = self.on_models_button_leave

        self.fetch_models_button = QtWidgets.QPushButton(models_button_frame)
        self.fetch_models_button.setStyleSheet("QPushButton { background-color: transparent; border: none; }")
        models_button_layout.addWidget(self.fetch_models_button)

        sidebar_layout.addWidget(models_button_frame)

        history_button_frame = QtWidgets.QFrame(self)
        history_button_frame.setObjectName("HistoryButtonFrame")
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

        sidebar_layout.addWidget(history_button_frame)

        chat_button_frame = QtWidgets.QFrame(self)
        chat_button_frame.setObjectName("ChatButtonFrame")
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

        sidebar_layout.addWidget(chat_button_frame)

        persona_button_frame = QtWidgets.QFrame(self)
        persona_button_frame.setObjectName("PersonaButtonFrame")
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

        self.persona_menu = QtWidgets.QMenu(self.persona_button)
        for persona in self.personas:
            action = self.persona_menu.addAction(persona["name"])
            action.triggered.connect(lambda checked, p=persona["name"]: asyncio.ensure_future(self.on_persona_selection(p)))
        
        sidebar_layout.addWidget(persona_button_frame)

        sidebar_layout.addStretch(1)

        settings_button_frame = QtWidgets.QFrame(self)
        settings_button_frame.setObjectName("SettingsButtonFrame")
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

        sidebar_layout.addWidget(settings_button_frame)

        self.apply_font_settings()

    def on_providers_button_hover(self, event):
        self.providers_button.setIcon(QtGui.QIcon("assets/SCOUT/Icons/providers_bl.png"))
        ToolTip.setToolTip(self, "Providers")

    def on_providers_button_leave(self, event):
        self.providers_button.setIcon(QtGui.QIcon("assets/SCOUT/Icons/providers_wt.png"))

    def on_models_button_hover(self, event):
        self.models_button.setIcon(QtGui.QIcon("assets/SCOUT/Icons/models_bl.png"))
        ToolTip.setToolTip(self, "Models")

    def on_models_button_leave(self, event):
        self.models_button.setIcon(QtGui.QIcon("assets/SCOUT/Icons/models_wt.png"))

    def on_history_button_hover(self, event):
        self.history_button.setIcon(QtGui.QIcon("assets/SCOUT/Icons/history_bl.png"))
        ToolTip.setToolTip(self, "History")

    def on_history_button_leave(self, event):
        self.history_button.setIcon(QtGui.QIcon("assets/SCOUT/Icons/history_wt.png"))

    def handle_history_button(self):
        cf.load_chat_history(self, self.provider_manager)

    def on_chat_button_hover(self, event):
        self.chat_button.setIcon(QtGui.QIcon("assets/SCOUT/Icons/chat_bl.png"))
        ToolTip.setToolTip(self, "Chat")

    def on_chat_button_leave(self, event):
        self.chat_button.setIcon(QtGui.QIcon("assets/SCOUT/Icons/chat_wt.png"))

    def show_chat_page(self):
        self.parent().stacked_widget.setCurrentWidget(self.parent().chat_page)

    def on_persona_button_hover(self, event):
        self.persona_button.setIcon(QtGui.QIcon("assets/SCOUT/Icons/agent_bl.png"))
        ToolTip.setToolTip(self, "Change Persona")
   
    def on_persona_button_leave(self, event):
        self.persona_button.setIcon(QtGui.QIcon("assets/SCOUT/Icons/agent_wt.png"))

    def show_persona_menu(self):
        self.persona_menu.exec_(QtGui.QCursor.pos())

    async def on_persona_selection(self, persona_name):
        await self.parent().on_persona_selection(persona_name)

    def on_settings_button_hover(self, event):
        self.settings_button.setIcon(QtGui.QIcon("assets/SCOUT/Icons/settings_bl.png"))
        ToolTip.setToolTip(self, "Settings")

    def on_settings_button_leave(self, event):
        self.settings_button.setIcon(QtGui.QIcon("assets/SCOUT/Icons/settings_wt.png"))

    def show_settings_page(self):
        self.parent().stacked_widget.setCurrentWidget(self.parent().settings_page)
