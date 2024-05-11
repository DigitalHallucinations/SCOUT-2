# modules/settings/filter_sort_settings.py

from PySide6 import QtWidgets as qtw
from PySide6.QtCore import QDate
import json
import os
from datetime import datetime
from modules.Personas.RSSManager.Toolbox.Feed_Portal.tooltip import ToolTip
#from tooltip import ToolTip # not yet implemented
from modules.logging.logger import setup_logger
#from logger import setup_logger

logger = setup_logger('filter_sort_settings')

def load_filter_sort_settings(self): 
    settings_folder = os.path.join("modules", "settings")
    filters_path = os.path.join(settings_folder, "filters.json")
    sorting_path = os.path.join(settings_folder, "sorting.json")

    try:
        with open(filters_path, "r") as f:
            self.filters = json.load(f)
        with open(sorting_path, "r") as f:
            self.sorting = json.load(f)

        if self.filters["date_range"]["start"]:
            self.filters["date_range"]["start"] = datetime.strptime(self.filters["date_range"]["start"], '%Y-%m-%d')
        else:
            self.filters["date_range"]["start"] = None

        if self.filters["date_range"]["end"]:
            self.filters["date_range"]["end"] = datetime.strptime(self.filters["date_range"]["end"], '%Y-%m-%d')
        else:
            self.filters["date_range"]["end"] = None

    except FileNotFoundError:
        os.makedirs(settings_folder, exist_ok=True)
        self.filters = {
            "keywords": [],
            "date_range": {
                "start": None,
                "end": None
            },
            "categories": []
        }
        self.sorting = {
            "method": "date",
            "order": "descending"
        }

def open_filter_settings(self):
    filter_settings_window = qtw.QDialog(self)
    filter_settings_window.setWindowTitle("Filter Settings")
    filter_settings_window.setStyleSheet(f"background-color: {self.window_bg};")

    setup_filter_settings_ui(self, filter_settings_window, self.font_family, self.font_size, self.font_color, self.window_bg, self.spinbox_bg, self.button_bg)

    filter_settings_window.exec()

def setup_filter_settings_ui(self, window, font_family, font_size, font_color, window_bg, spinbox_bg, button_bg):
    font_style = f"{font_family}, {int(font_size * 10)}"

    layout = qtw.QVBoxLayout(window)

    keyword_label = qtw.QLabel("Keywords:", window)
    keyword_label.setStyleSheet(f"color: {font_color}; font: {font_style};")
    layout.addWidget(keyword_label)

    self.keyword_entry = qtw.QLineEdit(window)
    self.keyword_entry.setStyleSheet(f"background-color: {spinbox_bg}; color: {font_color}; font: {font_style};")
    layout.addWidget(self.keyword_entry)

    date_range_label = qtw.QLabel("Date Range:", window)
    date_range_label.setStyleSheet(f"color: {font_color}; font: {font_style};")
    layout.addWidget(date_range_label)

    date_frame = qtw.QFrame(window)
    date_frame.setStyleSheet(f"background-color: {window_bg};")
    date_layout = qtw.QHBoxLayout(date_frame)
    layout.addWidget(date_frame)

    self.start_date_edit = qtw.QDateEdit(date_frame)
    self.start_date_edit.setStyleSheet(f"background-color: {spinbox_bg}; color: {font_color}; font: {font_style};")
    date_layout.addWidget(self.start_date_edit)

    self.end_date_edit = qtw.QDateEdit(date_frame)
    self.end_date_edit.setStyleSheet(f"background-color: {spinbox_bg}; color: {font_color}; font: {font_style};")
    date_layout.addWidget(self.end_date_edit)

    category_label = qtw.QLabel("Categories:", window)
    category_label.setStyleSheet(f"color: {font_color}; font: {font_style};")
    layout.addWidget(category_label)

    self.category_list = qtw.QListWidget(window)
    self.category_list.setStyleSheet(f"background-color: {spinbox_bg}; color: {font_color}; font: {font_style};")
    self.category_list.setSelectionMode(qtw.QAbstractItemView.ExtendedSelection)
    layout.addWidget(self.category_list)

    categories = self.rss_feed_reader.get_categories()
    self.category_list.addItems(categories)

    sort_label = qtw.QLabel("Sort By:", window)
    sort_label.setStyleSheet(f"color: {font_color}; font: {font_style};")
    layout.addWidget(sort_label)

    self.sort_combo = qtw.QComboBox(window)
    self.sort_combo.addItems(["Date", "Title"])
    self.sort_combo.setCurrentText(self.sorting["method"].capitalize())
    self.sort_combo.setStyleSheet(f"background-color: {spinbox_bg}; color: {font_color}; font: {font_style};")
    layout.addWidget(self.sort_combo)

    order_label = qtw.QLabel("Sort Order:", window)
    order_label.setStyleSheet(f"color: {font_color}; font: {font_style};")
    layout.addWidget(order_label)

    self.order_combo = qtw.QComboBox(window)
    self.order_combo.addItems(["Ascending", "Descending"])
    self.order_combo.setCurrentText(self.sorting["order"].capitalize())
    self.order_combo.setStyleSheet(f"background-color: {spinbox_bg}; color: {font_color}; font: {font_style};")
    layout.addWidget(self.order_combo)

    save_button = qtw.QPushButton("Save", window)
    save_button.setStyleSheet(f"background-color: {button_bg}; color: {font_color}; font: {font_style};")
    save_button.clicked.connect(lambda: save_filter_sort_settings(self))
    layout.addWidget(save_button)

def save_filter_sort_settings(self):
    settings_folder = os.path.join("modules", "settings")
    filters_path = os.path.join(settings_folder, "filters.json")
    sorting_path = os.path.join(settings_folder, "sorting.json")

    keywords = self.keyword_entry.text().strip().split(",")

    start_date = self.start_date_edit.date().toString("yyyy-MM-dd")
    end_date = self.end_date_edit.date().toString("yyyy-MM-dd")

    selected_categories = [item.text() for item in self.category_list.selectedItems()]

    self.filters.update({
        "keywords": keywords,
        "date_range": {"start": start_date, "end": end_date},
        "categories": selected_categories
    })

    with open(filters_path, "w") as f:
        json.dump(self.filters, f, indent=4)

    self.sorting.update({
        "method": self.sort_combo.currentText().lower(),
        "order": self.order_combo.currentText().lower()
    })

    with open(sorting_path, "w") as f:
        json.dump(self.sorting, f, indent=4)

    self.refresh_feeds()