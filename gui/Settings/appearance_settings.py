# gui/Settings/appearance_settings.py

from PySide6 import QtWidgets, QtGui, QtCore


from modules.logging.logger import setup_logger


logger = setup_logger('Appearance_settings.py')


class AppearanceSettings(QtWidgets.QDialog):
    """
    The `AppearanceSettings` class is a subclass of `QtWidgets.QDialog` and represents the chat settings window. 
    It initializes the window with the provided `parent` and `user` parameters. 
    It sets the initial provider to 'OpenAI', loads the providers from a JSON file, and creates the widgets for the chat settings window.
    """
    def __init__(self, parent=None, user=None):
        super().__init__(parent)
        self.parent = parent
        self.user = user


        self.setStyleSheet("background-color: #000000; color: white;")


        font_settings = self.load_appearance_settings()
        (
            self.font_family,
            self.font_size,
            self.font_color,
            self.titlebar_color,
            self.chatlog_frame_bg,
            self.chatlog_font_color,
            self.chatlog_font_family,
            self.chatlog_font_size,
            self.message_entry_frame_bg,
            self.message_entry_font_color,
            self.message_entry_font_family,
            self.message_entry_font_size,
            self.speechbar_frame_bg,
            self.speechbar_font_color,
            self.speechbar_font_family,
            self.speechbar_font_size,
            self.sidebar_frame_bg,
            self.sidebar_font_color,
            self.sidebar_font_family,
            self.sidebar_font_size,
            self.entry_sidebar_frame_bg,
            self.entry_sidebar_font_color,
            self.entry_sidebar_font_family,
            self.entry_sidebar_font_size,
            self.settings_page_main_frame_bg,
            self.settings_page_content_frame_bg,
            self.settings_page_title_label_bg,
            self.settings_page_title_label_font,
            self.settings_page_font_color,
            self.settings_page_font_family,
            self.settings_page_font_size,
            self.settings_page_spinbox_bg,
            self.statusbar_frame_bg,
            self.statusbar_font_color,
            self.statusbar_font_family,
            self.statusbar_font_size,
            self.history_frame_bg,
            self.history_font_color,
            self.history_font_family,
            self.history_font_size,
            self.message_box_frame_bg,
            self.message_box_font_color ,
            self.message_box_font_family,
            self.message_box_font_size 
                
        ) = font_settings


        self.font_color_var = self.font_color


        self.update_window_font(self.font_family, self.font_size, self.font_color_var)


        self.create_appearance_widgets()
        logger.info("AppearanceSettings widgets created")


    def create_appearance_widgets(self): 
        """
        Creates the various widgets for the Appearance settings window, including the providers button, fetch models button, 
        load chat button, voice button, toggle TTS button, temperature spinbox, top_p spinbox, and top_k spinbox.
        """
        self.font_style_frame = QtWidgets.QFrame(self)
        self.font_style_frame.setObjectName("FontStyleFrame")
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
        self.font_color_frame.setObjectName("FontColorFrame")
        self.font_color_frame.setStyleSheet("background-color: #000000;")


        self.font_color_button = QtWidgets.QPushButton("Font Color", self.font_color_frame)
        self.font_color_button.setStyleSheet("background-color: #000000; color: white;")
        self.font_color_button.clicked.connect(self.choose_font_color)


        self.font_size_frame = QtWidgets.QFrame(self)
        self.font_size_frame.setObjectName("FontSizeFrame")
        self.font_size_frame.setStyleSheet("background-color: #000000;")
        
        self.font_size_label = QtWidgets.QLabel("Font Size:", self.font_size_frame)
        self.font_size_label.setStyleSheet("color: white;")
        
        self.font_size_spinbox = QtWidgets.QSpinBox(self.font_size_frame)
        self.font_size_spinbox.setRange(8, 24)
        self.font_size_spinbox.setSingleStep(1)
        self.font_size_spinbox.setValue(self.font_size)
        self.font_size_spinbox.setStyleSheet("background-color: #000000; color: white;")
        self.font_size_spinbox.valueChanged.connect(self.update_font_size)


        # LLM Settings


        self.temperature_var = 0.1
        self.temperature_frame = QtWidgets.QFrame(self)
        self.temperature_frame.setObjectName("TemperatureFrame")
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
        self.top_p_frame.setObjectName("TopPFrame")
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
        self.top_k_frame.setObjectName("TopKFrame")
        self.top_k_frame.setStyleSheet("background-color: #000000;")
        self.top_k_label = QtWidgets.QLabel("Top_K:", self.top_k_frame)
        self.top_k_label.setStyleSheet("color: white;")
        self.top_k_spinbox = QtWidgets.QSpinBox(self.top_k_frame)
        self.top_k_spinbox.setRange(0, 100)
        self.top_k_spinbox.setSingleStep(1)
        self.top_k_spinbox.setValue(self.top_k_var)
        self.top_k_spinbox.setStyleSheet("background-color: #000000; color: white;")


        layout = QtWidgets.QVBoxLayout(self)


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


        self.update_window_font(self.font_family, self.font_size, self.font_color_var)        
        self.font_size_spinbox.setValue(self.font_size)  
        self.font_style_button.setText(self.font_family)
    
    def save_font_settings(self, font_family, font_size, font_color, config_file="config.ini"):
        logger.info(f"Saving font settings: Family: {font_family}, Size: {font_size}, Color: {font_color}")


        config = QtCore.QSettings(config_file, QtCore.QSettings.IniFormat)


        config.beginGroup("Font")
        config.setValue("family", font_family)
        config.setValue("size", font_size)
        config.setValue("color", font_color)
        config.endGroup()


        logger.info(f"Font settings saved to {config_file}")


    def load_appearance_settings(self, config_file="config.ini"):
        logger.info(f"Loading font settings from {config_file}")


        config = QtCore.QSettings(config_file, QtCore.QSettings.IniFormat)


        font_family = config.value("Font/family", "Helvetica")
        font_size = config.value("Font/size", 12, type=int)
        font_color = config.value("Font/color", "#ffffff")
        titlebar_color = config.value("TitlebarSettings/color", "#2d2d2d")
        chatlog_frame_bg = config.value("ChatlogSettings/frame_bg", "#2d2d2d")
        chatlog_font_color = config.value("ChatlogSettings/font_color", "#ffffff")
        chatlog_font_family = config.value("ChatlogSettings/font_family", "Sitka")
        chatlog_font_size = config.value("ChatlogSettings/font_size", 15, type=int)
        message_entry_frame_bg = config.value("MessageEntrySettings/frame_bg", "#2d2d2d")
        message_entry_font_color = config.value("MessageEntrySettings/font_color", "#ffffff")
        message_entry_font_family = config.value("MessageEntrySettings/font_family", "Sitka")
        message_entry_font_size = config.value("MessageEntrySettings/font_size", 15, type=int)
        speechbar_frame_bg = config.value("SpeechBarSettings/frame_bg", "#2d2d2d")
        speechbar_font_color = config.value("SpeechBarSettings/font_color", "#ffffff")
        speechbar_font_family = config.value("SpeechBarSettings/font_family", "Sitka")
        speechbar_font_size = config.value("SpeechBarSettings/font_size", 15, type=int)
        sidebar_frame_bg = config.value("SideBarSettings/frame_bg", "#2d2d2d")
        sidebar_font_color = config.value("SideBarSettings/font_color", "#ffffff")
        sidebar_font_family = config.value("SideBarSettings/font_family", "Sitka")
        sidebar_font_size = config.value("SideBarSettings/font_size", 15, type=int)
        entry_sidebar_frame_bg = config.value("EntrySideBarSettings/frame_bg", "#000000")
        entry_sidebar_font_color = config.value("EntrySideBarSettings/font_color", "#ffffff")
        entry_sidebar_font_family = config.value("EntrySideBarSettings/font_family", "Sitka")
        entry_sidebar_font_size = config.value("EntrySideBarSettings/font_size", 15, type=int)
        settings_page_main_frame_bg = config.value("SettingsPageSettings/main_frame_bg", "#000000")
        settings_page_content_frame_bg = config.value("SettingsPageSettings/content_frame_bg", "#2d2d2d")
        settings_page_title_label_bg = config.value("SettingsPageSettings/title_tab_bg", "#2d2d2d")
        settings_page_title_label_font = config.value("SettingsPageSettings/title_tab_font", "Sitka")
        settings_page_font_color = config.value("SettingsPageSettings/font_color", "#ffffff")
        settings_page_font_family = config.value("SettingsPageSettings/font_family", "Sitka")
        settings_page_font_size = config.value("SettingsPageSettings/font_size", 15, type=int)
        settings_page_spinbox_bg = config.value("SettingsPageSettings/spinbox_bg", "#808080")
        statusbar_frame_bg = config.value("StatusBarSettings/frame_bg", "#2d2d2d")
        statusbar_font_color = config.value("StatusBarSettings/font_color", "#ffffff")
        statusbar_font_family = config.value("StatusBarSettings/font_family", "Sitka")
        statusbar_font_size = config.value("StatusBarSettings/font_size", 15, type=int)
        history_frame_bg = config.value("HistorySettings/frame_bg", "#2d2d2d")
        history_font_color = config.value("HistorySettings/font_color", "#ffffff")
        history_font_family = config.value("HistorySettings/font_family", "Sitka")
        history_font_size = config.value("HistorySettings/font_size", 15, type=int)
        message_box_frame_bg = config.value("MessageBoxSettings/frame_bg", "#2d2d2d")
        message_box_font_color = config.value("MessageBoxSettings/font_color", "#ffffff")
        message_box_font_family = config.value("MessageBoxSettings/font_family", "Sitka")
        message_box_font_size = config.value("MessageBoxSettings/font_size", 15, type=int)


        logger.info(f"Loaded font settings: Family: {font_family}, Size: {font_size}, Color: {font_color}")


        return (
            font_family,
            font_size,
            font_color,
            titlebar_color,
            chatlog_frame_bg,
            chatlog_font_color,
            chatlog_font_family,
            chatlog_font_size,
            message_entry_frame_bg,
            message_entry_font_color,
            message_entry_font_family,
            message_entry_font_size,
            speechbar_frame_bg,
            speechbar_font_color,
            speechbar_font_family,
            speechbar_font_size,
            sidebar_frame_bg,
            sidebar_font_color,
            sidebar_font_family,
            sidebar_font_size,
            entry_sidebar_frame_bg,
            entry_sidebar_font_color,
            entry_sidebar_font_family,
            entry_sidebar_font_size,
            settings_page_main_frame_bg,
            settings_page_content_frame_bg,
            settings_page_title_label_bg,
            settings_page_title_label_font,
            settings_page_font_color,
            settings_page_font_family,
            settings_page_font_size,
            settings_page_spinbox_bg,
            statusbar_frame_bg,
            statusbar_font_color,
            statusbar_font_family,
            statusbar_font_size,
            history_frame_bg,
            history_font_color,
            history_font_family,
            history_font_size,
            message_box_frame_bg,
            message_box_font_color,
            message_box_font_family,
            message_box_font_size
        )


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
        self.font_size = selected_font_size


        self.update_window_font(self.font_family, selected_font_size, self.font_color_var)


        self.save_font_settings(self.font_family, selected_font_size, self.font_color_var)


    def set_font_family(self, font_family):
        self.font_family = font_family


        self.font_style_button.setText(font_family)


        self.update_window_font(font_family, self.font_size, self.font_color_var)


        self.save_font_settings(font_family, self.font_size, self.font_color_var)


    def update_font_size(self, value):
        selected_font_size = value
        self.font_size = selected_font_size


        self.update_window_font(self.font_family, selected_font_size, self.font_color_var)


        self.save_font_settings(self.font_family, selected_font_size, self.font_color_var)
    
    def choose_font_color(self):
        color = QtWidgets.QColorDialog.getColor(QtGui.QColor(self.font_color_var), self, "Choose Font Color")
        if color.isValid():
            self.font_color_var = color.name()
            self.update_font_color()


    def update_font_color(self):
        selected_font_color = self.font_color_var
        self.font_color = selected_font_color
        self.update_window_font(self.font_family, self.font_size, selected_font_color)
        self.save_font_settings(self.font_family, self.font_size, selected_font_color)

    def apply_message_box_style(self, message_box):
        message_box.setStyleSheet(f"""
            QMessageBox {{
                background-color: {self.message_box_frame_bg};
                color: {self.message_box_font_color};
                font-family: {self.message_box_font_family};
                font-size: {self.message_box_font_size}pt;
            }}
            QPushButton {{
                background-color: #000000;
                color: {self.message_box_font_color};
                font-family: {self.message_box_font_family};
                font-size: {self.message_box_font_size}pt;
                border: 1px solid {self.message_box_font_color};
                padding: 5px;
            }}
            QPushButton:hover {{
                background-color: #333333;
            }}
        """)

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


    def show_font_style_menu(self):
        self.font_style_menu.clear()
        available_fonts = QtGui.QFontDatabase.families()
        for font_family in available_fonts:
            action = self.font_style_menu.addAction(font_family)
            action.triggered.connect(lambda checked, f=font_family: self.set_font_family(f))
        self.font_style_menu.exec(QtGui.QCursor.pos())