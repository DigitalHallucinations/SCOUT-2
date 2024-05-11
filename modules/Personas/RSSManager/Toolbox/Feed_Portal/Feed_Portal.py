# Feed portal/RSSFeedReaderUI.py

import os
import threading
import json
import configparser
import feedparser
import webbrowser

from PySide6 import QtWidgets as qtw
from PySide6 import QtCore as qtc
from PySide6 import QtGui as qtg
from PySide6.QtGui import QDesktopServices

from modules.Personas.RSSManager.Toolbox.Feed_Portal.rss_feed_reader import RSSFeedReader, RSSFeedReaderError
from modules.Personas.RSSManager.Toolbox.Feed_Portal.Search.search_window import SearchWindow
from gui.tooltip import ToolTip
from modules.Personas.RSSManager.Toolbox.Feed_Portal.settings import settings, filter_sort_settings
from modules.logging.logger import setup_logger

import os

logger = setup_logger('RSSFeedReaderUI')

class RSSFeedReaderUI(qtw.QFrame):
    def __init__(self):
        super().__init__()
        logger.info("Initializing RSS Feed Reader...")
        self.setWindowTitle("Feed Portal")
        self.rss_feed_reader = RSSFeedReader()
        logger.info("Loading feeds and configuration...")
        self.load_feeds()
        self.load_config()
        settings.load_settings(self)  
        filter_sort_settings.load_filter_sort_settings(self)
        self.url_cooldown = False

        self.create_widgets()

    def open_url(self, url):
        logger.info("Opening url...")
        if not self.url_cooldown:
            self.url_cooldown = True
            threading.Thread(target=self.open_url_thread, args=(url.toString(),)).start()
            qtc.QTimer.singleShot(5000, self.reset_url_cooldown)
        else:
            qtw.QMessageBox.information(self, "Cooldown", "Please wait before clicking the URL again.")
    
    def open_url_thread(self, url):
        webbrowser.open(url)

    def reset_url_cooldown(self):
        self.url_cooldown = False

    def load_config(self):
        logger.info("Loading configuration from config.ini...")
        try:
            settings_folder = "settings"
            config_path = os.path.join(settings_folder, "config.ini")
            config = configparser.ConfigParser()
            config.read(config_path)

            self.font_family = config.get("Font", "family", fallback="Segoe UI")
            self.font_size = config.getfloat("Font", "size", fallback=10)
            self.font_color = config.get("Font", "color", fallback="#ffffff")

            self.main_window_color = config.get("Colors", "main_window_color", fallback="#1e1e1e")
            self.window_bg = config.get("Colors", "window_bg", fallback="#2d2d2d")
            self.spinbox_bg = config.get("Colors", "spinbox_bg", fallback="#3c3c3c")
            self.button_bg = config.get("Colors", "button_bg", fallback="#007acc")
            self.button_hover_bg = config.get("Colors", "button_hover_bg", fallback="#0e639c")
            self.button_pressed_bg = config.get("Colors", "button_pressed_bg", fallback="#005a9e")

        except Exception as e:
            logger.exception("Error occurred while loading configuration.")
            qtw.QMessageBox.critical(self, "Configuration Error", "Failed to load configuration. Using default values.")
            
    def create_widgets(self):
        logger.info("Creating UI widgets...")

        icon_size = 32
        settings_img = qtg.QPixmap("assets/icons/settings_icon.png")
        settings_img = settings_img.scaled(icon_size, icon_size)

        try:
            font_style = f"{self.font_family}, {self.font_size}pt"

            central_widget = qtw.QWidget(self)
            central_widget.setStyleSheet(f"background-color: {self.main_window_color};")
            layout = qtw.QVBoxLayout(central_widget)
            self.setLayout(layout)

            settings_frame = qtw.QFrame(central_widget)
            settings_frame.setStyleSheet(f"background-color: {self.window_bg};")
            settings_layout = qtw.QHBoxLayout(settings_frame)
            settings_layout.setContentsMargins(10, 10, 10, 10)
            layout.addWidget(settings_frame)

            filter_sort_button = qtw.QPushButton("Filter/Sort", settings_frame)
            filter_sort_button.setStyleSheet(f"""
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
            filter_sort_button.clicked.connect(lambda: filter_sort_settings.open_filter_settings(self))
            settings_layout.addWidget(filter_sort_button)
            ToolTip.setToolTip(filter_sort_button, "Open Filter/Sort Settings")

            self.search_button = qtw.QPushButton("Search", settings_frame)
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
            self.search_button.clicked.connect(self.open_search_window)
            settings_layout.addWidget(self.search_button)
            ToolTip.setToolTip(self.search_button, "Open Search Window")

            self.settings_button = qtw.QPushButton(settings_frame)
            self.settings_button.setIcon(settings_img)
            self.settings_button.setStyleSheet(f"""
                QPushButton {{
                    background-color: {self.window_bg};
                    color: {self.font_color};
                    font: {font_style};
                    border: none;
                    padding: 8px;
                    border-radius: 4px;
                }}
                QPushButton:hover {{
                    background-color: {self.button_hover_bg};
                }}
                QPushButton:pressed {{
                    background-color: {self.button_pressed_bg};
                }}
            """)
            self.settings_button.clicked.connect(lambda: settings.open_settings(self))
            settings_layout.addWidget(self.settings_button)
            ToolTip.setToolTip(self.settings_button, "Open Settings")

            self.feed_url_label = qtw.QLabel("Feed URL:", central_widget)
            self.feed_url_label.setStyleSheet(f"color: {self.font_color}; font: {font_style};")
            layout.addWidget(self.feed_url_label)

            self.feed_url_entry = qtw.QLineEdit(central_widget)
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
            layout.addWidget(self.feed_url_entry)
            ToolTip.setToolTip(self.feed_url_entry, "Enter the URL of the RSS feed")

            self.category_label = qtw.QLabel("Category:", central_widget)
            self.category_label.setStyleSheet(f"color: {self.font_color}; font: {font_style};")
            layout.addWidget(self.category_label)

            self.category_entry = qtw.QLineEdit(central_widget)
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
            layout.addWidget(self.category_entry)
            ToolTip.setToolTip(self.category_entry, "Enter a category for the RSS feed")

            self.add_feed_button = qtw.QPushButton("Add Feed", central_widget)
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
            self.add_feed_button.clicked.connect(self.add_feed)
            layout.addWidget(self.add_feed_button)
            ToolTip.setToolTip(self.add_feed_button, "Add a new RSS feed")

            self.feeds_listbox = qtw.QListWidget(central_widget)
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
            layout.addWidget(self.feeds_listbox)

            button_frame = qtw.QFrame(central_widget)
            button_frame.setStyleSheet(f"background-color: {self.window_bg};")
            button_layout = qtw.QHBoxLayout(button_frame)
            button_layout.setContentsMargins(10, 10, 10, 10)
            layout.addWidget(button_frame)

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
            self.remove_feed_button.clicked.connect(self.remove_feed)
            self.remove_feed_button.setEnabled(False)
            button_layout.addWidget(self.remove_feed_button)
            ToolTip.setToolTip(self.remove_feed_button, "Remove the selected RSS feed")

            self.entries_listbox = qtw.QListWidget(central_widget)
            self.entries_listbox.setStyleSheet(f"""
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
            self.entries_listbox.itemClicked.connect(self.on_entry_click)
            layout.addWidget(self.entries_listbox)

            self.entries_detailed_list = qtw.QTreeWidget(central_widget)
            self.entries_detailed_list.setStyleSheet(f"""
                QTreeWidget {{
                    background-color: {self.window_bg};
                    color: {self.font_color};
                    font: {font_style};
                    border: none;
                    padding: 6px;
                    border-radius: 4px;
                }}
                QTreeWidget::item {{
                    padding: 6px;
                }}
                QTreeWidget::item:selected {{
                    background-color: {self.button_bg};
                    color: {self.font_color};
                }}
            """)
            self.entries_detailed_list.setHeaderLabels(["Title", "Published"])
            self.entries_detailed_list.itemClicked.connect(self.on_entry_click)
            layout.addWidget(self.entries_detailed_list)
            self.entries_detailed_list.hide()

            self.entries_card_view = qtw.QListWidget(central_widget)
            self.entries_card_view.setStyleSheet(f"""
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
                    border: 1px solid {self.spinbox_bg};
                    border-radius: 4px;
                    margin-bottom: 6px;
                }}
                QListWidget::item:selected {{
                    background-color: {self.button_bg};
                    color: {self.font_color};
                }}
            """)
            self.entries_card_view.itemClicked.connect(self.on_entry_click)
            layout.addWidget(self.entries_card_view)
            self.entries_card_view.hide()

            entry_button_frame = qtw.QFrame(central_widget)
            entry_button_frame.setStyleSheet(f"background-color: {self.window_bg};")
            entry_button_layout = qtw.QHBoxLayout(entry_button_frame)
            entry_button_layout.setContentsMargins(10, 10, 10, 10)
            layout.addWidget(entry_button_frame)

            self.show_entry_button = qtw.QPushButton("Show Entry Details", entry_button_frame)
            self.show_entry_button.setStyleSheet(f"""
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
            self.show_entry_button.clicked.connect(self.show_entry_details)
            self.show_entry_button.setEnabled(False)
            entry_button_layout.addWidget(self.show_entry_button)
            ToolTip.setToolTip(self.show_entry_button, "Show details of the selected entry")

            self.remove_entry_button = qtw.QPushButton("Remove Entry", entry_button_frame)
            self.remove_entry_button.setStyleSheet(f"""
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
            self.remove_entry_button.clicked.connect(self.remove_entry)
            self.remove_entry_button.setEnabled(False)
            entry_button_layout.addWidget(self.remove_entry_button)
            ToolTip.setToolTip(self.remove_entry_button, "Remove the selected entry")

            self.entry_details_text = qtw.QTextBrowser(central_widget)
            self.entry_details_text.setStyleSheet(f"""
                QTextBrowser {{
                    background-color: {self.window_bg};
                    color: {self.font_color};
                    font: {font_style};
                    border: none;
                    padding: 10px;
                    border-radius: 4px;
                }}
                QTextBrowser a {{
                    color: {self.button_bg};
                    text-decoration: none;
                }}
                QTextBrowser a:hover {{
                    text-decoration: underline;
                }}
            """)
            self.entry_details_text.setReadOnly(True)
            self.entry_details_text.setOpenExternalLinks(True)
            self.entry_details_text.setTextInteractionFlags(qtc.Qt.TextBrowserInteraction | qtc.Qt.LinksAccessibleByMouse)
            self.entry_details_text.viewport().setCursor(qtg.QCursor(qtc.Qt.PointingHandCursor))
            layout.addWidget(self.entry_details_text)

            self.refresh_feeds()
        except Exception as e:
            logger.exception("Error occurred while creating widgets.")
            qtw.QMessageBox.critical(self, "Widget Creation Error", "Failed to create widgets.")

    def open_search_window(self):
        search_window = SearchWindow(self)
        search_window.populate_categories()
        search_window.exec_()

    def on_feed_click(self, item):
        self.start_feed_button.setEnabled(True)
        self.remove_feed_button.setEnabled(True)

    def on_entry_click(self, item):
        self.show_entry_button.setEnabled(True)
        self.remove_entry_button.setEnabled(True)

        selected_entry = None
        if self.display_format == "Simple List":
            selected_entry = self.entries_listbox.currentItem().text()
        elif self.display_format == "Detailed List":
            selected_entry = self.entries_detailed_list.currentItem().text(0)
        elif self.display_format == "Card View":
            selected_entry = self.entries_card_view.currentItem().text().split("<br>")[0].replace("<b>", "").replace("</b>", "")

        if selected_entry:
            feed_url = self.feeds_listbox.currentItem().text().split(" - ")[0]
            entries = self.rss_feed_reader.get_feed_entries(feed_url)
            for entry in entries:
                if entry.title == selected_entry:
                    entry_details = self.rss_feed_reader.get_entry_details(entry)
                    self.entry_details_text.clear()
                    self.entry_details_text.append(f"<h3>{entry_details['title']}</h3>")

                    url_link = f"<a href=\"{entry_details['link']}\">{entry_details['link']}</a>"
                    self.entry_details_text.append(f"<p><strong>Link:</strong> {url_link}</p>")

                    self.entry_details_text.append(f"<p><strong>Published:</strong> {entry_details['published']}</p>")
                    self.entry_details_text.append(f"<p><strong>Summary:</strong> {entry_details['summary']}</p>")

                    self.entry_details_text.setOpenExternalLinks(False)
                    self.entry_details_text.anchorClicked.connect(self.open_url)

                    break

    def remove_entry(self):
        selected_entry = self.entries_listbox.currentItem().text()
        if selected_entry:
            feed_url = self.feeds_listbox.currentItem().text().split(" - ")[0]
            self.rss_feed_reader.remove_entry(feed_url, selected_entry)
            self.entries_listbox.takeItem(self.entries_listbox.currentRow())
            self.entry_details_text.clear()
            self.show_entry_button.setEnabled(False)
            self.remove_entry_button.setEnabled(False)
        else:
            qtw.QMessageBox.critical(self, "Error", "Please select an entry to remove.")

    def show_entry_details(self):
        selected_entry = None
        if self.display_format == "Simple List":
            selected_entry = self.entries_listbox.currentItem().text()
        elif self.display_format == "Detailed List":
            selected_entry = self.entries_detailed_list.currentItem().text(0)
        elif self.display_format == "Card View":
            selected_entry = self.entries_card_view.currentItem().text().split("<br>")[0].replace("<b>", "").replace("</b>", "")

        if selected_entry:
            feed_url = self.feeds_listbox.currentItem().text().split(" - ")[0]
            entries = self.rss_feed_reader.get_feed_entries(feed_url)
            for entry in entries:
                if entry.title == selected_entry:
                    entry_details = self.rss_feed_reader.get_entry_details(entry)
                    self.entry_details_text.clear()
                    self.entry_details_text.append(f"<h3>{entry_details['title']}</h3>")

                    url_link = f"<a href=\"{entry_details['link']}\">{entry_details['link']}</a>"
                    self.entry_details_text.append(f"<p><strong>Link:</strong> {url_link}</p>")

                    self.entry_details_text.append(f"<p><strong>Published:</strong> {entry_details['published']}</p>")
                    self.entry_details_text.append(f"<p><strong>Summary:</strong> {entry_details['summary']}</p>")

                    self.entry_details_text.setOpenExternalLinks(False)
                    self.entry_details_text.anchorClicked.connect(self.open_url)

                    break
        else:
            qtw.QMessageBox.critical(self, "Error", "Please select an entry to show details.")
            
    def open_url_in_browser(self, url):
        QDesktopServices.openUrl(url)

    def start_feed(self):
        selected_feed = self.feeds_listbox.currentItem().text()
        if selected_feed:
            feed_url = selected_feed.split(" - ")[0]
            entries = self.rss_feed_reader.get_feed_entries(feed_url)
            entries = self.rss_feed_reader.sort_entries(entries, self.sorting)

            if self.display_format == "Simple List":
                self.entries_listbox.clear()
                for entry in entries:
                    self.entries_listbox.addItem(entry.title)
                self.entries_listbox.show()
                self.entries_detailed_list.hide()
                self.entries_card_view.hide()
            elif self.display_format == "Detailed List":
                self.entries_detailed_list.clear()
                for entry in entries:
                    item = qtw.QTreeWidgetItem(self.entries_detailed_list)
                    item.setText(0, entry.title)
                    item.setText(1, entry.published)
                self.entries_listbox.hide()
                self.entries_detailed_list.show()
                self.entries_card_view.hide()
            elif self.display_format == "Card View":
                self.entries_card_view.clear()
                for entry in entries:
                    item = qtw.QListWidgetItem(self.entries_card_view)
                    item.setText(f"<b>{entry.title}</b><br>{entry.published}")
                self.entries_listbox.hide()
                self.entries_detailed_list.hide()
                self.entries_card_view.show()
        else:
            qtw.QMessageBox.critical(self, "Error", "Please select a feed to start.")
            
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

    def refresh_feeds(self):
        logger.info("Refreshing feeds...")
        try:
            self.feeds_listbox.clear()
            self.entries_listbox.clear()
            self.entry_details_text.clear()

            feeds = self.rss_feed_reader.get_feeds()
            for feed in feeds:
                self.feeds_listbox.addItem(f"{feed.url} - {feed.category}")

            qtc.QTimer.singleShot(self.refresh_interval_mins * 60000, self.refresh_feeds)
        except Exception as e:
            logger.exception("Error occurred while refreshing feeds.")
            qtw.QMessageBox.critical(self, "Error", "An error occurred while refreshing feeds.")

    def load_feeds(self):
        logger.info("Loading feeds...")
        try:
            script_dir = os.path.dirname(os.path.abspath(__file__))
            config_path = os.path.join(script_dir, "feeds.json")

            if os.path.exists(config_path):
                with open(config_path, "r") as file:
                    feed_data = json.load(file)
                    self.loaded_entries = {}
                    for category, data in feed_data.items():
                        for feed in data["feeds"]:
                            self.rss_feed_reader.add_feed(feed["url"], category)
                            entries = data["entries"].get(feed["url"], [])
                            self.loaded_entries[feed["url"]] = []
                            for entry_details in entries:
                                entry = feedparser.FeedParserDict(entry_details)
                                self.loaded_entries[feed["url"]].append(entry)
        except Exception as e:
            logger.exception("Error occurred while loading feeds.")

    def on_feed_select(self, item):
        try:
            selected_feed = item.text()

            if not selected_feed:
                return

            feed_url = selected_feed.split(" - ")[0]

            entries = self.rss_feed_reader.get_feed_entries(feed_url)
            entries = self.rss_feed_reader.sort_entries(entries, self.sorting)
            self.entries_listbox.clear()

            for entry in entries:
                self.entries_listbox.addItem(entry.title)

            self.entries_listbox.itemClicked.connect(self.on_entry_select)
        except RSSFeedReaderError as e:
            logger.exception("Error occurred while selecting feed.")
            qtw.QMessageBox.critical(self, "Error", str(e))
        except Exception as e:
            logger.exception("Unexpected error occurred while selecting feed.")
            qtw.QMessageBox.critical(self, "Error", "An unexpected error occurred.")

    def on_entry_select(self, item):
        try:
            selected_entry = item.text()

            if not selected_entry:
                return

            feed_url = self.feeds_listbox.currentItem().text().split(" - ")[0]
            entries = self.rss_feed_reader.get_feed_entries(feed_url)

            for entry in entries:
                if entry.title == selected_entry:
                    entry_details = self.rss_feed_reader.get_entry_details(entry)
                    self.entry_details_text.clear()
                    self.entry_details_text.append(f"<h3>{entry_details['title']}</h3>")
                    self.entry_details_text.append(f"<p><strong>Link:</strong> {entry_details['link']}</p>")
                    self.entry_details_text.append(f"<p><strong>Published:</strong> {entry_details['published']}</p>")
                    self.entry_details_text.append(f"<p><strong>Summary:</strong> {entry_details['summary']}</p>")
                    break
        except RSSFeedReaderError as e:
            logger.exception("Error occurred while selecting entry.")
            qtw.QMessageBox.critical(self, "Error", str(e))
        except Exception as e:
            logger.exception("Unexpected error occurred while selecting entry.")
            qtw.QMessageBox.critical(self, "Error", "An unexpected error occurred.")

    def save_feeds(self):
        logger.info("Saving feeds...")
        try:
            feeds = self.rss_feed_reader.get_feeds()
            feed_data = {}

            for feed in feeds:
                category = feed.category
                if category not in feed_data:
                    feed_data[category] = {"feeds": [], "entries": {}}

                feed_data[category]["feeds"].append({"url": feed.url})

                try:
                    entries = self.rss_feed_reader.get_feed_entries(feed.url)
                    feed_data[category]["entries"][feed.url] = []

                    for entry in entries:
                        try:
                            entry_details = self.rss_feed_reader.get_entry_details(entry)
                            feed_data[category]["entries"][feed.url].append(entry_details)
                        except RSSFeedReaderError as e:
                            logger.warning(f"Skipping entry due to missing details: {str(e)}")
                except RSSFeedReaderError as e:
                    logger.warning(f"Skipping feed due to parsing error: {str(e)}")
                    continue

            script_dir = os.path.dirname(os.path.abspath(__file__))
            config_path = os.path.join(script_dir, "feeds.json")
            with open(config_path, "w") as file:
                json.dump(feed_data, file, indent=2)
        except Exception as e:
            logger.exception("Error occurred while saving feeds.")

    def closeEvent(self, event):
        #self.save_feeds()
        logger.info("RSS Feed Reader closed.")
        event.accept()

