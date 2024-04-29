# gui/sidebar.py

from PySide6 import QtWidgets, QtGui, QtCore
from gui.tooltip import ToolTip

class Sidebar(QtWidgets.QFrame):
    def __init__(self, parent=None, personas=None, sidebar_frame_bg=None, font_color=None, font_size=None, font_family=None):
        super().__init__(parent)
        self.personas = personas
        self.sidebar_frame_bg = sidebar_frame_bg
        self.font_color = font_color
        self.font_size = font_size
        self.font_family = font_family
        self.create_sidebar()

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
        self.setStyleSheet(f"background-color: {self.sidebar_frame_bg}; border-right: 2px solid black;")
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
        self.providers_button.clicked.connect(self.handle_providers_button)
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
        self.models_button.clicked.connect(self.handle_models_button)
        models_button_layout.addWidget(self.models_button)
        self.models_button.enterEvent = self.on_models_button_hover
        self.models_button.leaveEvent = self.on_models_button_leave

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
            action.triggered.connect(lambda checked, p=persona["name"]: self.on_persona_selection(p))

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

    def handle_providers_button(self):
        providers_menu = QtWidgets.QMenu(self)
        for provider in self.llm_providers:
            action = providers_menu.addAction(provider)
            action.triggered.connect(lambda checked, p=provider: self.set_provider(p))
        providers_menu.exec(QtGui.QCursor.pos())

    def on_models_button_hover(self, event):
        self.models_button.setIcon(QtGui.QIcon("assets/SCOUT/Icons/models_bl.png"))
        ToolTip.setToolTip(self, "Models")

    def on_models_button_leave(self, event):
        self.models_button.setIcon(QtGui.QIcon("assets/SCOUT/Icons/models_wt.png"))

    def handle_models_button(self):
        models_menu = QtWidgets.QMenu(self)
        for model in self.available_models:
            action = models_menu.addAction(model)
            action.triggered.connect(lambda checked, m=model: self.set_model(m))
        models_menu.exec(QtGui.QCursor.pos())

    def on_history_button_hover(self, event):
        self.history_button.setIcon(QtGui.QIcon("assets/SCOUT/Icons/history_bl.png"))
        ToolTip.setToolTip(self, "History")

    def on_history_button_leave(self, event):
        self.history_button.setIcon(QtGui.QIcon("assets/SCOUT/Icons/history_wt.png"))

    def handle_history_button(self):
        history_dialog = QtWidgets.QDialog(self)
        history_dialog.setWindowTitle("Chat History")
        history_dialog.exec()

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

    def on_persona_selection(self, persona_name):
        self.parent().on_persona_selection(persona_name)

    def on_settings_button_hover(self, event):
        self.settings_button.setIcon(QtGui.QIcon("assets/SCOUT/Icons/settings_bl.png"))
        ToolTip.setToolTip(self, "Settings")

    def on_settings_button_leave(self, event):
        self.settings_button.setIcon(QtGui.QIcon("assets/SCOUT/Icons/settings_wt.png"))

    def show_settings_page(self):
        self.parent().stacked_widget.setCurrentWidget(self.parent().settings_page)