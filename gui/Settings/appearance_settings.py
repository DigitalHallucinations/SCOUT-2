# gui/Settings/appearance_settings.py

from PySide6 import QtWidgets, QtGui, QtCore

from modules.logging.logger import setup_logger

logger = setup_logger('chat_settings.py')

class AppearanceSettings(QtWidgets.QDialog):
    """
    The `ChatSettings` class is a subclass of `QtWidgets.QDialog` and represents the chat settings window. 
    It initializes the window with the provided `parent` and `user` parameters. 
    It sets the initial provider to 'OpenAI', loads the providers from a JSON file, and creates the widgets for the chat settings window.
    """
    def __init__(self, parent=None, user=None):
        super().__init__(parent)
        self.parent = parent
        self.user = user

        self.setStyleSheet("background-color: #000000; color: white;")

        font_family, font_size, font_color = self.load_font_settings()
        self.parent.set_font_family(font_family)
        self.parent.set_font_size(font_size)
        self.parent.set_font_color(font_color)

        self.font_color_var = font_color

        self.update_window_font(self.parent.font_family, self.parent.font_size, self.font_color_var)

        self.create_appearance_widgets()
        logger.info("ChatSettings widgets created")

    def create_appearance_widgets(self): 
        """
        Creates the various widgets for the chat settings window, including the providers button, fetch models button, 
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
        self.font_size_spinbox.setValue(self.parent.font_size)
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

        self.update_window_font(self.parent.font_family, selected_font_size, self.font_color_var)

        self.save_font_settings(self.parent.font_family, selected_font_size, self.font_color_var)

    def set_font_family(self, font_family):
        self.parent.set_font_family(font_family)

        self.font_style_button.setText(font_family)

        self.update_window_font(font_family, self.parent.font_size, self.font_color_var)

        self.save_font_settings(font_family, self.parent.font_size, self.font_color_var)

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