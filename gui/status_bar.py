# gui/status_bar.py

from PySide6 import QtWidgets, QtGui

class StatusBar(QtWidgets.QFrame):
    def __init__(self, parent=None, appearance_settings_instance=None, provider_manager=None, user=None):
        super().__init__(parent)
        self.appearance_settings_instance = appearance_settings_instance
        self.provider_manager = provider_manager
        self.user = user
        self.init_ui()

    def init_ui(self):
        self.setStyleSheet(f"background-color: {self.appearance_settings_instance.statusbar_frame_bg}; border: none;")
        self.setFixedHeight(30)
        status_bar_layout = QtWidgets.QHBoxLayout(self)
        status_bar_layout.setContentsMargins(5, 0, 5, 0)
        status_bar_layout.setSpacing(10)

        self.provider_label = QtWidgets.QLabel(self)
        self.provider_label.setStyleSheet(f"color: {self.appearance_settings_instance.statusbar_font_color}; font-family: {self.appearance_settings_instance.statusbar_font_family}; font-size: {self.appearance_settings_instance.statusbar_font_size}px;")
        status_bar_layout.addWidget(self.provider_label)

        self.model_label = QtWidgets.QLabel(self)
        self.model_label.setStyleSheet(f"color: {self.appearance_settings_instance.statusbar_font_color}; font-family: {self.appearance_settings_instance.statusbar_font_family}; font-size: {self.appearance_settings_instance.statusbar_font_size}px;")
        status_bar_layout.addWidget(self.model_label)

        status_bar_layout.addStretch(1)

        self.username_label = QtWidgets.QLabel(self)
        self.username_label.setStyleSheet(f"color: {self.appearance_settings_instance.statusbar_font_color}; font-family: {self.appearance_settings_instance.statusbar_font_family}; font-size: {self.appearance_settings_instance.statusbar_font_size}px;")
        status_bar_layout.addWidget(self.username_label)

    def update_status_bar(self):
        provider = self.provider_manager.get_current_llm_provider()
        model = self.provider_manager.get_current_model()

        self.provider_label.setText(f"Provider: {provider}")
        self.model_label.setText(f"Model: {model}")
        self.username_label.setText(f"User: {self.user}")

    def create_status_bar(self, status_bar_frame):
        status_bar_frame.setStyleSheet(f"background-color: {self.appearance_settings_instance.statusbar_frame_bg}; border: none;")
        status_bar_frame.setFixedHeight(30)
        status_bar_layout = QtWidgets.QHBoxLayout(status_bar_frame)
        status_bar_layout.setContentsMargins(5, 0, 5, 0)
        status_bar_layout.setSpacing(10)

        self.provider_label = QtWidgets.QLabel(status_bar_frame)
        self.provider_label.setStyleSheet(f"color: {self.appearance_settings_instance.statusbar_font_color}; font-family: {self.appearance_settings_instance.statusbar_font_family}; font-size: {self.appearance_settings_instance.statusbar_font_size}px;")
        status_bar_layout.addWidget(self.provider_label)

        self.model_label = QtWidgets.QLabel(status_bar_frame)
        self.model_label.setStyleSheet(f"color: {self.appearance_settings_instance.statusbar_font_color}; font-family: {self.appearance_settings_instance.statusbar_font_family}; font-size: {self.appearance_settings_instance.statusbar_font_size}px;")
        status_bar_layout.addWidget(self.model_label)

        status_bar_layout.addStretch(1)

        self.username_label = QtWidgets.QLabel(status_bar_frame)
        self.username_label.setStyleSheet(f"color: {self.appearance_settings_instance.statusbar_font_color}; font-family: {self.appearance_settings_instance.statusbar_font_family}; font-size: {self.appearance_settings_instance.statusbar_font_size}px;")
        status_bar_layout.addWidget(self.username_label) 
        
    def update_status_bar(self):
        provider = self.provider_manager.get_current_llm_provider()
        model = self.provider_manager.get_current_model()

        self.provider_label.setText(f"Provider: {provider}")
        self.model_label.setText(f"Model: {model}")
        self.username_label.setText(f"User: {self.user}")    