# modules/Search/search_settings.py

import os
import configparser
from PySide6 import QtWidgets as qtw
from PySide6 import QtCore as qtc
from dotenv import load_dotenv, set_key
from modules.Personas.FeedManager.Toolbox.Feed_Portal.Search.feedly_api import FeedlyAPI

class SearchWindow(qtw.QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Search Feeds")
        self.resize(400, 300)
        self.rss_feed_reader = parent.rss_feed_reader

        self.load_config()
        self.setStyleSheet(f"background-color: {self.main_window_color};")
        self.create_widgets()

    def load_config(self):
        settings_folder = "settings"
        config_path = os.path.join(settings_folder, "config.ini")
        config = configparser.ConfigParser()
        config.read(config_path)

        self.font_family = config.get("Font", "family", fallback="Segoe UI")
        self.font_size = config.getfloat("Font", "size", fallback=10)
        self.font_color = config.get("Font", "color", fallback="#ffffff")

        self.main_window_color = config.get("Colors", "main_window_color", fallback="#333333")
        self.window_bg = config.get("Colors", "window_bg", fallback="#2d2d2d")
        self.button_bg = config.get("Colors", "button_bg", fallback="#007acc")
        self.button_hover_bg = config.get("Colors", "button_hover_bg", fallback="#0e639c")
        self.button_pressed_bg = config.get("Colors", "button_pressed_bg", fallback="#005a9e")

    def create_widgets(self):
        font_style = f"{self.font_family}, {self.font_size}pt"

        layout = qtw.QVBoxLayout(self)

        keyword_label = qtw.QLabel("Search by Keyword:", self)
        keyword_label.setStyleSheet(f"color: {self.font_color}; font: {font_style};")
        layout.addWidget(keyword_label)

        keyword_layout = qtw.QHBoxLayout()
        self.keyword_entry = qtw.QLineEdit(self)
        self.keyword_entry.setStyleSheet(f"""
            QLineEdit {{
                background-color: {self.window_bg};
                color: {self.font_color};
                font: {font_style};
                border: 1px solid {self.button_bg};
                padding: 6px;
                border-radius: 4px;
            }}
        """)
        keyword_layout.addWidget(self.keyword_entry)

        self.search_button = qtw.QPushButton("Search", self)
        self.search_button.setStyleSheet(f"""
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
        self.search_button.clicked.connect(self.search_feeds_by_keyword)
        keyword_layout.addWidget(self.search_button)

        layout.addLayout(keyword_layout)

        category_label = qtw.QLabel("Search by Category:", self)
        category_label.setStyleSheet(f"color: {self.font_color}; font: {font_style};")
        layout.addWidget(category_label)

        self.category_combo = qtw.QComboBox(self)
        self.category_combo.setStyleSheet(f"""
            QComboBox {{
                background-color: {self.window_bg};
                color: {self.font_color};
                font: {font_style};
                border: 1px solid {self.button_bg};
                padding: 6px;
                border-radius: 4px;
            }}
            QComboBox QAbstractItemView {{
                background-color: {self.window_bg};
                color: {self.font_color};
                selection-background-color: {self.button_hover_bg};
            }}
        """)
        self.category_combo.currentIndexChanged.connect(self.filter_feeds_by_category)
        layout.addWidget(self.category_combo)

        self.feeds_list = qtw.QListWidget(self)
        self.feeds_list.setStyleSheet(f"""
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
        layout.addWidget(self.feeds_list)

        feedly_search_button = qtw.QPushButton("Search Feedly", self)
        feedly_search_button.setStyleSheet(f"""
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
        feedly_search_button.clicked.connect(self.search_feeds_feedly)
        layout.addWidget(feedly_search_button)

        feedly_token_button = qtw.QPushButton("Add Feedly Access Token", self)
        feedly_token_button.setStyleSheet(f"""
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
        feedly_token_button.clicked.connect(self.add_feedly_token)
        layout.addWidget(feedly_token_button)

    def search_feeds_by_keyword(self):
        keyword = self.keyword_entry.text()
        matching_feeds = self.rss_feed_reader.search_feeds_by_keyword(keyword)
        self.update_feeds_list(matching_feeds)

    def filter_feeds_by_category(self, index):
        category = self.category_combo.itemText(index)
        filtered_feeds = self.rss_feed_reader.filter_feeds_by_category(category)
        self.update_feeds_list(filtered_feeds)

    def update_feeds_list(self, feeds):
        self.feeds_list.clear()
        for feed in feeds:
            self.feeds_list.addItem(f"{feed.url} - {feed.category}")

    def populate_categories(self):
        categories = self.rss_feed_reader.get_categories()
        self.category_combo.clear()
        self.category_combo.addItems(categories)

    def search_feeds_feedly(self):
        query = self.keyword_entry.text()
        if query:
            load_dotenv()
            access_token = os.getenv("FEEDLY_ACCESS_TOKEN")
            if access_token:
                feedly_api = FeedlyAPI(access_token)
                results = feedly_api.search_feeds(query)

                self.feeds_list.clear()
                for result in results:
                    feed_url = result["feedId"]
                    feed_title = result["title"]
                    item = qtw.QListWidgetItem(f"{feed_title} - {feed_url}")
                    item.setData(qtc.Qt.UserRole, feed_url)
                    self.feeds_list.addItem(item)

                self.feeds_list.itemDoubleClicked.connect(self.add_selected_feed)
            else:
                qtw.QMessageBox.warning(self, "Missing Access Token", "Please add your Feedly access token.")

    def add_selected_feed(self, item):
        feed_url = item.data(qtc.Qt.UserRole)
        feed_title = item.text().split(" - ")[0]

        category, ok = qtw.QInputDialog.getText(self, "Feed Category", "Enter a category for the selected feed:")
        if ok and category:
            self.rss_feed_reader.add_feed(feed_url, category)
            self.rss_feed_reader.save_feeds()
            qtw.QMessageBox.information(self, "Feed Added", "The selected feed has been added to the feeds.json file.")

    def add_feedly_token(self):
        dialog = qtw.QDialog(self)
        dialog.setWindowTitle("Feedly Access Token")
        dialog.setStyleSheet(f"""
            QDialog {{
                background-color: {self.window_bg};
                color: {self.font_color};
                font: {self.font_family}, {self.font_size}pt;
            }}
            QLabel {{
                color: {self.font_color};
            }}
            QLineEdit {{
                background-color: {self.window_bg};
                color: {self.font_color};
                border: 1px solid {self.button_bg};
                padding: 6px;
                border-radius: 4px;
            }}
            QPushButton {{
                background-color: {self.button_bg};
                color: {self.font_color};
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

        layout = qtw.QVBoxLayout(dialog)

        label = qtw.QLabel("Enter your Feedly access token:", dialog)
        layout.addWidget(label)

        token_entry = qtw.QLineEdit(dialog)
        layout.addWidget(token_entry)

        button_layout = qtw.QHBoxLayout()
        ok_button = qtw.QPushButton("OK", dialog)
        ok_button.clicked.connect(dialog.accept)
        button_layout.addWidget(ok_button)

        cancel_button = qtw.QPushButton("Cancel", dialog)
        cancel_button.clicked.connect(dialog.reject)
        button_layout.addWidget(cancel_button)

        layout.addLayout(button_layout)

        if dialog.exec() == qtw.QDialog.Accepted:
            token = token_entry.text()
            if token:
                env_file = ".env"
                load_dotenv(env_file)
                set_key(env_file, "FEEDLY_ACCESS_TOKEN", token)
                qtw.QMessageBox.information(self, "Success", "Feedly access token added successfully.")