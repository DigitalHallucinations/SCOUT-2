# modules/Personas/FeedManager/Toolbox/Feed_Portal/Feed_Portal.py

import os
import threading
import json
import configparser
import feedparser
import webbrowser
import asyncio

from PySide6 import QtWidgets as qtw
from PySide6 import QtCore as qtc
from PySide6.QtGui import QDesktopServices

from modules.Personas.FeedManager.Toolbox.Feed_Portal.modules.rss_feed_reader import RSSFeedReader, RSSFeedReaderError
from modules.Personas.FeedManager.Toolbox.Feed_Portal.Search.search_window import SearchWindow
from modules.Personas.FeedManager.Toolbox.Feed_Portal.modules.entries_frame import create_entries_frame
from modules.Personas.FeedManager.Toolbox.Feed_Portal.settings import settings, filter_sort_settings
from modules.Personas.FeedManager.Toolbox.Feed_Portal.modules.header_frame import create_header_frame
from modules.Personas.FeedManager.Toolbox.Feed_Portal.modules.feed_entry_frame import create_feed_entry_frame
from modules.logging.logger import setup_logger

logger = setup_logger('RSSFeedReaderUI')

class RSSFeedReaderUI(qtw.QFrame):
    def __init__(self):
        super().__init__()
        logger.info("Initializing RSS Feed Reader...")
        self.setWindowTitle("Feed Portal")
        self.rss_feed_reader = RSSFeedReader()
        logger.info("Loading feeds and configuration...")
        asyncio.create_task(self.load_feeds())
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

            self.main_window_color = config.get("Colors", "main_window_color", fallback="#000000")
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

        try:
            central_widget = qtw.QWidget(self)
            central_widget.setStyleSheet("background-color: transparent;")
            layout = qtw.QVBoxLayout(central_widget)
            self.setLayout(layout)

            create_header_frame(self, layout)
            create_feed_entry_frame(self, layout)
            create_entries_frame(self, layout)

            asyncio.create_task(self.refresh_feeds())
        except Exception as e:
            logger.exception("Error occurred while creating widgets.")
            qtw.QMessageBox.critical(self, "Widget Creation Error", "Failed to create widgets.")

    def open_search_window(self):
        search_window = SearchWindow(self)
        search_window.populate_categories()
        search_window.exec_()        

    async def remove_entry(self):
        selected_entry = self.entries_listbox.currentItem().text()
        if selected_entry:
            feed_url = self.feeds_listbox.currentItem().text().split(" - ")[0]
            await self.rss_feed_reader.remove_entry(feed_url, selected_entry)
            self.entries_listbox.takeItem(self.entries_listbox.currentRow())
            self.entry_details_text.clear()
            self.show_entry_button.setEnabled(False)
            self.remove_entry_button.setEnabled(False)
        else:
            qtw.QMessageBox.critical(self, "Error", "Please select an entry to remove.")

    async def show_entry_details(self):
       selected_entry = None
       if self.display_format == "Simple List":
           selected_entry = self.entries_listbox.currentItem().text()
       elif self.display_format == "Detailed List":
           selected_entry = self.entries_detailed_list.currentItem().text(0)
       elif self.display_format == "Card View":
           selected_entry = self.entries_card_view.currentItem().text().split("<br>")[0].replace("<b>", "").replace("</b>", "")

       if selected_entry:
           feed_url = self.feeds_listbox.currentItem().text().split(" - ")[0]
           entries = await self.rss_feed_reader.get_feed_entries(feed_url)
           for entry in entries:
               if entry.title == selected_entry:
                   entry_details = await self.rss_feed_reader.get_entry_details(entry)
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

    async def start_feed(self):
        selected_feed = self.feeds_listbox.currentItem().text()
        if selected_feed:
            feed_url = selected_feed.split(" - ")[0]
            entries = await self.rss_feed_reader.get_feed_entries(feed_url)
            entries = await self.rss_feed_reader.sort_entries(entries, self.sorting)

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

    async def refresh_feeds(self):
        logger.info("Refreshing feeds...")
        try:
            self.feeds_listbox.clear()
            self.entries_listbox.clear()
            self.entry_details_text.clear()

            feeds = await self.rss_feed_reader.get_feeds()
            for feed in feeds:
                self.feeds_listbox.addItem(f"{feed.url} - {feed.category}")

            qtc.QTimer.singleShot(self.refresh_interval_mins * 60000, lambda: asyncio.create_task(self.refresh_feeds()))
        except Exception as e:
            logger.exception("Error occurred while refreshing feeds.")
            qtw.QMessageBox.critical(self, "Error", "An error occurred while refreshing feeds.")

    async def load_feeds(self):
        logger.info("Loading feeds...")
        try:
            config_path = os.path.join("modules", "Personas", "FeedManager", "Toolbox", "Feed_Portal", "feeds.json")

            if os.path.exists(config_path):
                with open(config_path, "r") as file:
                    feed_data = json.load(file)
                    self.loaded_entries = {}
                    for category, data in feed_data.items():
                        for feed in data["feeds"]:
                            await self.rss_feed_reader.add_feed(feed["url"], category)
                            entries = data["entries"].get(feed["url"], [])
                            self.loaded_entries[feed["url"]] = []
                            for entry_details in entries:
                                entry = feedparser.FeedParserDict(entry_details)
                                self.loaded_entries[feed["url"]].append(entry)
        except Exception as e:
            logger.exception("Error occurred while loading feeds.")

    async def on_feed_select(self, item):
        try:
            selected_feed = item.text()

            if not selected_feed:
                return

            feed_url = selected_feed.split(" - ")[0]

            entries = await self.rss_feed_reader.get_feed_entries(feed_url)
            entries = await self.rss_feed_reader.sort_entries(entries, self.sorting)
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

    async def on_entry_select(self, item):
        try:
            selected_entry = item.text()

            if not selected_entry:
                return

            feed_url = self.feeds_listbox.currentItem().text().split(" - ")[0]
            entries = await self.rss_feed_reader.get_feed_entries(feed_url)

            for entry in entries:
                if entry.title == selected_entry:
                    entry_details = await self.rss_feed_reader.get_entry_details(entry)
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

    async def save_feeds(self):
        logger.info("Saving feeds...")
        try:
            feeds = await self.rss_feed_reader.get_feeds()
            feed_data = {}

            for feed in feeds:
                category = feed.category
                if category not in feed_data:
                    feed_data[category] = {"feeds": [], "entries": {}}

                feed_data[category]["feeds"].append({"url": feed.url})

                try:
                    entries = await self.rss_feed_reader.get_feed_entries(feed.url)
                    feed_data[category]["entries"][feed.url] = []

                    for entry in entries:
                        try:
                            entry_details = await self.rss_feed_reader.get_entry_details(entry)
                            feed_data[category]["entries"][feed.url].append(entry_details)
                        except RSSFeedReaderError as e:
                            logger.warning(f"Skipping entry due to missing details: {str(e)}")
                except RSSFeedReaderError as e:
                    logger.warning(f"Skipping feed due to parsing error: {str(e)}")
                    continue

            script_dir = os.path.dirname(os.path.abspath(__file__))
            config_path = os.path.join(script_dir, "modules/Personas/FeedManager/Toolbox/Feed_Portal/feeds.json")
            with open(config_path, "w") as file:
                json.dump(feed_data, file, indent=2)
        except Exception as e:
            logger.exception("Error occurred while saving feeds.")

    def closeEvent(self, event):
        #self.save_feeds()
        logger.info("RSS Feed Reader closed.")
        event.accept()