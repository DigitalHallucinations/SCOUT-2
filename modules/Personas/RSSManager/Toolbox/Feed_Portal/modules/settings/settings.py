# modules/settings/settings.py

from PySide6 import QtWidgets as qtw
import configparser
import os
from modules.tooltip import ToolTip
from modules.logging.logger import setup_logger

logger = setup_logger('settings')

def load_settings(self):
    """Loads settings from the config.ini file."""
    logger.info("Loading settings from config.ini...")
    settings_folder = os.path.join("modules", "settings")
    config_path = os.path.join(settings_folder, "config.ini")
    config = configparser.ConfigParser()
    config.read(config_path)

    self.entries_per_feed = config.getint("FeedSettings", "entries_per_feed", fallback=10)
    self.refresh_interval_mins = config.getint("FeedSettings", "refresh_interval_mins", fallback=30)
    self.display_format = config.get("FeedSettings", "display_format", fallback="Simple List")

def load_config(self):
    logger.info("Loading configuration from config.ini...")
    try:
        settings_folder = os.path.join("modules", "settings")
        config_path = os.path.join(settings_folder, "config.ini")
        config = configparser.ConfigParser()
        config.read(config_path)

        self.font_family = config.get("Font", "family", fallback="MS Sans Serif")
        self.font_size = config.getfloat("Font", "size", fallback=1.1)
        self.font_color = config.get("Font", "color", fallback="#ffffff")

        self.main_window_color = config.get("Colors", "main_window_color", fallback="#333333")
        self.window_bg = config.get("Colors", "window_bg", fallback="#000000")
        self.spinbox_bg = config.get("Colors", "spinbox_bg", fallback="#808080")
        self.button_bg = config.get("Colors", "button_bg", fallback="#696969")

    except Exception as e:
        logger.exception("Error occurred while loading configuration.")
        qtw.QMessageBox.critical(self, "Configuration Error", "Failed to load configuration. Using default values.")

def open_settings(self):
    """Opens a new window for adjusting settings."""
    logger.info("Opening settings window...")
    settings_window = qtw.QDialog(self)
    settings_window.setWindowTitle("Settings")
    settings_window.setStyleSheet(f"background-color: {self.window_bg};")
    settings_window.setFixedSize(400, 200)

    font_style = f"{self.font_family}, {int(self.font_size * 10)}"

    layout = qtw.QVBoxLayout(settings_window)

    entries_label = qtw.QLabel("Entries per Feed:", settings_window)
    entries_label.setStyleSheet(f"color: {self.font_color}; font: {font_style};")
    layout.addWidget(entries_label)

    entries_spinbox = qtw.QSpinBox(settings_window)
    entries_spinbox.setRange(1, 100)
    entries_spinbox.setValue(self.entries_per_feed)
    entries_spinbox.setStyleSheet(f"background-color: {self.spinbox_bg}; color: {self.font_color}; font: {font_style};")
    layout.addWidget(entries_spinbox)
    ToolTip.setToolTip(entries_spinbox, "Set the number of entries per feed")

    refresh_label = qtw.QLabel("Refresh Interval (mins):", settings_window)
    refresh_label.setStyleSheet(f"color: {self.font_color}; font: {font_style};")
    layout.addWidget(refresh_label)

    refresh_spinbox = qtw.QSpinBox(settings_window)
    refresh_spinbox.setRange(1, 1440)
    refresh_spinbox.setValue(self.refresh_interval_mins)
    refresh_spinbox.setStyleSheet(f"background-color: {self.spinbox_bg}; color: {self.font_color}; font: {font_style};")
    layout.addWidget(refresh_spinbox)
    ToolTip.setToolTip(refresh_spinbox, "Set the refresh interval in minutes")

    format_label = qtw.QLabel("Display Format:", settings_window)
    format_label.setStyleSheet(f"color: {self.font_color}; font: {font_style};")
    layout.addWidget(format_label)

    format_combo = qtw.QComboBox(settings_window)
    format_combo.addItems(["Simple List", "Detailed List", "Card View"])
    format_combo.setCurrentText(self.display_format)
    format_combo.setStyleSheet(f"background-color: {self.button_bg}; color: {self.font_color}; font: {font_style};")
    layout.addWidget(format_combo)
    ToolTip.setToolTip(format_combo, "Select the display format for entries")

    save_button = qtw.QPushButton("Save", settings_window)
    save_button.setStyleSheet(f"background-color: {self.button_bg}; color: {self.font_color}; font: {font_style};")
    save_button.clicked.connect(lambda: save_settings(self, entries_spinbox.value(), refresh_spinbox.value(), format_combo.currentText()))
    layout.addWidget(save_button)
    ToolTip.setToolTip(save_button, "Save the settings")

    settings_window.exec()

def save_settings(self, entries_per_feed, refresh_interval_mins, display_format):
    """Saves the current settings to the config.ini file."""
    logger.info("Saving settings to config.ini...")
    settings_folder = "settings"
    config_path = os.path.join(settings_folder, "config.ini")

    config = configparser.ConfigParser()
    config.read(config_path)

    if not config.has_section("FeedSettings"):
        config.add_section("FeedSettings")

    config.set("FeedSettings", "entries_per_feed", str(entries_per_feed))
    config.set("FeedSettings", "refresh_interval_mins", str(refresh_interval_mins))
    config.set("FeedSettings", "display_format", display_format)

    os.makedirs(settings_folder, exist_ok=True)
    with open(config_path, "w") as configfile:
        config.write(configfile)

    self.entries_per_feed = entries_per_feed
    self.refresh_interval_mins = refresh_interval_mins
    self.display_format = display_format

    self.refresh_feeds()