#modules/Personas/FeedManager/Toolbox/Feed_Portal/modules/entries_frame.py


from PySide6 import QtWidgets as qtw
from PySide6 import QtCore as qtc
from PySide6 import QtGui as qtg

from gui.tooltip import ToolTip

def create_entries_frame(self, layout):
    entries_frame = qtw.QFrame(self)
    entries_frame.setStyleSheet(f"background-color: {self.main_window_color}; border-radius: 10px;")
    entries_layout = qtw.QVBoxLayout(entries_frame)
    entries_layout.setContentsMargins(10, 10, 10, 10)
    layout.addWidget(entries_frame)

    font_style = f"{self.font_family}, {self.font_size}pt"

    self.entries_listbox = qtw.QListWidget(entries_frame)
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
    entries_layout.addWidget(self.entries_listbox)

    self.entries_detailed_list = qtw.QTreeWidget(entries_frame)
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
    entries_layout.addWidget(self.entries_detailed_list)
    self.entries_detailed_list.hide()

    self.entries_card_view = qtw.QListWidget(entries_frame)
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
    entries_layout.addWidget(self.entries_card_view)
    self.entries_card_view.hide()

    entry_button_frame = qtw.QFrame(entries_frame)
    entry_button_frame.setStyleSheet(f"background-color: {self.window_bg};")
    entry_button_layout = qtw.QHBoxLayout(entry_button_frame)
    entry_button_layout.setContentsMargins(10, 10, 10, 10)
    entries_layout.addWidget(entry_button_frame)

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

    self.entry_details_text = qtw.QTextBrowser(entries_frame)
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
    entries_layout.addWidget(self.entry_details_text)