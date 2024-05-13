# modules/Personas/FeedManager/ToolboxFeed_Portal/modules/feed_entry_frame.py

from PySide6 import QtWidgets as qtw

from gui.tooltip import ToolTip
from modules.Personas.FeedManager.Toolbox.Feed_Portal.modules.rss_feed_reader import RSSFeedReaderError
from modules.logging.logger import setup_logger

logger = setup_logger('FeedEntryFrame')

def create_feed_entry_frame(self, layout):
    feed_entry_frame = qtw.QFrame(self)
    feed_entry_frame.setStyleSheet(f"background-color: {self.main_window_color}; border-radius: 10px;")
    feed_entry_layout = qtw.QVBoxLayout(feed_entry_frame)
    feed_entry_layout.setContentsMargins(10, 10, 10, 10)
    layout.addWidget(feed_entry_frame)

    font_style = f"{self.font_family}, {self.font_size}pt"

    self.feed_url_label = qtw.QLabel("Feed URL:", feed_entry_frame)
    self.feed_url_label.setStyleSheet(f"color: {self.font_color}; font: {font_style};")
    feed_entry_layout.addWidget(self.feed_url_label)

    self.feed_url_entry = qtw.QLineEdit(feed_entry_frame)
    self.feed_url_entry.setStyleSheet(f"""
        QLineEdit {{
            background-color: {self.window_bg};
            color: {self.font_color};
            font: {font_style};
            border: 1px solid {self.spinbox_bg};
            padding: 6px;
            border-radius: 4px;
        }}
    """)
    feed_entry_layout.addWidget(self.feed_url_entry)
    ToolTip.setToolTip(self.feed_url_entry, "Enter the URL of the RSS feed")

    self.category_label = qtw.QLabel("Category:", feed_entry_frame)
    self.category_label.setStyleSheet(f"color: {self.font_color}; font: {font_style};")
    feed_entry_layout.addWidget(self.category_label)

    self.category_entry = qtw.QLineEdit(feed_entry_frame)
    self.category_entry.setStyleSheet(f"""
        QLineEdit {{
            background-color: {self.window_bg};
            color: {self.font_color};
            font: {font_style};
            border: 1px solid {self.spinbox_bg};
            padding: 6px;
            border-radius: 4px;
        }}
    """)
    feed_entry_layout.addWidget(self.category_entry)
    ToolTip.setToolTip(self.category_entry, "Enter a category for the RSS feed")

    self.add_feed_button = qtw.QPushButton("Add Feed", feed_entry_frame)
    self.add_feed_button.setStyleSheet(f"""
        QPushButton {{
            background-color: {self.button_bg};
            color: {self.font_color};
            font: {font_style};
            border: none;
            padding: 8px 16px;
            border-radius: 4px;
        }}
        QPushButton:hover {{
            background-color: {self.button_hover_bg};
        }}
        QPushButton:pressed {{
            background-color: {self.button_pressed_bg};
        }}
    """)
    self.add_feed_button.clicked.connect(lambda: add_feed(self))
    feed_entry_layout.addWidget(self.add_feed_button)
    ToolTip.setToolTip(self.add_feed_button, "Add a new RSS feed")

    self.feeds_listbox = qtw.QListWidget(feed_entry_frame)
    self.feeds_listbox.setStyleSheet(f"""
        QListWidget {{
            background-color: {self.window_bg};
            color: {self.font_color};
            font: {font_style};
            border: none;
            padding: 6px;
            border-radius: 4px;
        }}
        QListWidget::item {{
            padding: 6px;
        }}
        QListWidget::item:selected {{
            background-color: {self.button_bg};
            color: {self.font_color};
        }}
    """)
    self.feeds_listbox.itemClicked.connect(self.on_feed_click)
    feed_entry_layout.addWidget(self.feeds_listbox)

    button_frame = qtw.QFrame(feed_entry_frame)
    button_frame.setStyleSheet(f"background-color: {self.window_bg};")
    button_layout = qtw.QHBoxLayout(button_frame)
    button_layout.setContentsMargins(10, 10, 10, 10)
    feed_entry_layout.addWidget(button_frame)

    self.start_feed_button = qtw.QPushButton("Start Feed", button_frame)
    self.start_feed_button.setStyleSheet(f"""
        QPushButton {{
            background-color: {self.button_bg};
            color: {self.font_color};
            font: {font_style};
            border: none;
            padding: 8px 16px;
            border-radius: 4px;
        }}
        QPushButton:hover {{
            background-color: {self.button_hover_bg};
        }}
        QPushButton:pressed {{
            background-color: {self.button_pressed_bg};
        }}
        QPushButton:disabled {{
            background-color: {self.spinbox_bg};
            color: {self.font_color};
        }}
    """)
    self.start_feed_button.clicked.connect(self.start_feed)
    self.start_feed_button.setEnabled(False)
    button_layout.addWidget(self.start_feed_button)
    ToolTip.setToolTip(self.start_feed_button, "Start the selected RSS feed")

    self.remove_feed_button = qtw.QPushButton("Remove Feed", button_frame)
    self.remove_feed_button.setStyleSheet(f"""
        QPushButton {{
            background-color: {self.button_bg};
            color: {self.font_color};
            font: {font_style};
            border: none;
            padding: 8px 16px;
            border-radius: 4px;
        }}
        QPushButton:hover {{
            background-color: {self.button_hover_bg};
        }}
        QPushButton:pressed {{
            background-color: {self.button_pressed_bg};
        }}
        QPushButton:disabled {{
            background-color: {self.spinbox_bg};
            color: {self.font_color};
        }}
    """)
    self.remove_feed_button.clicked.connect(lambda: remove_feed(self))
    self.remove_feed_button.setEnabled(False)
    button_layout.addWidget(self.remove_feed_button)
    ToolTip.setToolTip(self.remove_feed_button, "Remove the selected RSS feed")

def add_feed(self):
    logger.info("Adding a new feed...")
    try:
        feed_url = self.feed_url_entry.text()
        category = self.category_entry.text()

        if not feed_url:
            qtw.QMessageBox.critical(self, "Error", "Please enter a feed URL.")
            return

        self.rss_feed_reader.add_feed(feed_url, category)
        self.refresh_feeds()
        self.feed_url_entry.clear()
        self.category_entry.clear()
        self.save_feeds()
    except RSSFeedReaderError as e:
        logger.exception("Error occurred while adding feed.")
        qtw.QMessageBox.critical(self, "Error", str(e))
    except Exception as e:
        logger.exception("Unexpected error occurred while adding feed.")
        qtw.QMessageBox.critical(self, "Error", "An unexpected error occurred.")

def remove_feed(self):
    try:
        selected_feed = self.feeds_listbox.currentItem().text()

        if not selected_feed:
            qtw.QMessageBox.critical(self, "Error", "Please select a feed to remove.")
            return

        feed_url = selected_feed.split(" - ")[0]

        self.rss_feed_reader.remove_feed(feed_url)
        self.save_feeds()
        self.refresh_feeds()
    except RSSFeedReaderError as e:
        logger.exception("Error occurred while removing feed.")
        qtw.QMessageBox.critical(self, "Error", str(e))
    except Exception as e:
        logger.exception("Unexpected error occurred while removing feed.")
        qtw.QMessageBox.critical(self, "Error", "An unexpected error occurred.")