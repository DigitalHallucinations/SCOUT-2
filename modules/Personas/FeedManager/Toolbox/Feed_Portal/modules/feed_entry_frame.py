# modules/Personas/FeedManager/Toolbox/Feed_Portal/modules/feed_entry_frame.py

import asyncio
from PySide6 import QtWidgets as qtw
from PySide6 import QtCore as qtc
from PySide6 import QtGui as qtg
from gui.tooltip import ToolTip
from modules.Personas.FeedManager.Toolbox.Feed_Portal.modules.rss_feed_reader import RSSFeedReaderError
from modules.logging.logger import setup_logger

logger = setup_logger('FeedEntryFrame')

def create_feed_entry_frame(self, layout):
    feed_entry_frame = qtw.QFrame(self)
    feed_entry_frame.setStyleSheet(f"background-color: {self.main_window_color}; border-radius: 10px;")
    feed_entry_layout = qtw.QVBoxLayout(feed_entry_frame)
    feed_entry_layout.setContentsMargins(5, 5, 5, 5)
    layout.addWidget(feed_entry_frame)

    font_style = f"{self.font_family}, {self.font_size}pt"
    icon_size = 32

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

    category_frame = qtw.QFrame(feed_entry_frame)
    category_frame.setStyleSheet("background-color: transparent;")
    category_layout = qtw.QHBoxLayout(category_frame)
    category_layout.setContentsMargins(0, 0, 0, 0)
    feed_entry_layout.addWidget(category_frame)

    self.category_entry = qtw.QLineEdit(category_frame)
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
    category_layout.addWidget(self.category_entry)
    ToolTip.setToolTip(self.category_entry, "Enter a category for the RSS feed")

    self.add_feed_button = qtw.QPushButton(category_frame)
    self.add_feed_button.setIcon(qtg.QIcon("assets/SCOUT/Icons/add_file_wt.png"))
    self.add_feed_button.setIconSize(qtc.QSize(icon_size, icon_size))
    self.add_feed_button.setStyleSheet("QPushButton { background-color: transparent; border: none; }")
    self.add_feed_button.clicked.connect(lambda: asyncio.create_task(self.rss_feed_reader.add_feed(self.feed_url_entry.text(), self.category_entry.text())))
    category_layout.addWidget(self.add_feed_button)
    ToolTip.setToolTip(self.add_feed_button, "Add a new RSS feed")

    def on_add_feed_button_hover(event):
        self.add_feed_button.setIcon(qtg.QIcon("assets/SCOUT/Icons/add_file_bl.png"))

    def on_add_feed_button_leave(event):
        self.add_feed_button.setIcon(qtg.QIcon("assets/SCOUT/Icons/add_file_wt.png"))

    self.add_feed_button.enterEvent = lambda event: on_add_feed_button_hover(event)
    self.add_feed_button.leaveEvent = lambda event: on_add_feed_button_leave(event)

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
            white-space: normal;
            word-wrap: break-word;
        }}
        QListWidget::item:selected {{
            background-color: {self.button_bg};
            color: {self.font_color};
        }}
        QListWidget::item:hover {{
            background-color: {self.button_hover_bg};
        }}
        QListWidget::horizontalScrollBar {{
            height: 0px;
        }}
    """)
    self.feeds_listbox.setHorizontalScrollBarPolicy(qtc.Qt.ScrollBarAlwaysOff)
    self.feeds_listbox.setWordWrap(True)
    self.feeds_listbox.setContextMenuPolicy(qtc.Qt.CustomContextMenu)
    self.feeds_listbox.customContextMenuRequested.connect(lambda pos: show_feed_context_menu(self, pos))
    feed_entry_layout.addWidget(self.feeds_listbox)

async def add_feed(self):
       logger.info("Adding a new feed...")
       try:
           feed_url = self.feed_url_entry.text()
           category = self.category_entry.text()

           if not feed_url:
               qtw.QMessageBox.critical(self, "Error", "Please enter a feed URL.")
               return

           await self.rss_feed_reader.add_feed(feed_url, category)
           await self.refresh_feeds()
           self.feed_url_entry.clear()
           self.category_entry.clear()
           await self.save_feeds()
       except RSSFeedReaderError as e:
           logger.exception("Error occurred while adding feed.")
           qtw.QMessageBox.critical(self, "Error", str(e))
       except Exception as e:
           logger.exception("Unexpected error occurred while adding feed.")
           qtw.QMessageBox.critical(self, "Error", "An unexpected error occurred.")

def show_feed_context_menu(self, pos):
    item = self.feeds_listbox.itemAt(pos)
    if item:
        menu = qtw.QMenu(self)
        start_action = menu.addAction("Start Feed")
        remove_action = menu.addAction("Remove Feed")

        action = menu.exec_(self.feeds_listbox.mapToGlobal(pos))

        if action == start_action:
            asyncio.create_task(self.start_feed())
        elif action == remove_action:
            asyncio.create_task(remove_feed(self))

async def remove_feed(self):
    try:
        selected_feed = self.feeds_listbox.currentItem().text()

        if not selected_feed:
            qtw.QMessageBox.critical(self, "Error", "Please select a feed to remove.")
            return

        feed_url = selected_feed.split(" - ")[0]

        await self.rss_feed_reader.remove_feed(feed_url)
        await self.save_feeds()
        await self.refresh_feeds()
    except RSSFeedReaderError as e:
        logger.exception("Error occurred while removing feed.")
        qtw.QMessageBox.critical(self, "Error", str(e))
    except Exception as e:
        logger.exception("Unexpected error occurred while removing feed.")
        qtw.QMessageBox.critical(self, "Error", "An unexpected error occurred.")