#modules/Personas/FeedManager/Toolbox/Feed_Portal/modules/entries_frame.py


from PySide6 import QtWidgets as qtw
from PySide6 import QtCore as qtc
from PySide6 import QtGui as qtg

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
            white-space: normal;
        }}
        QListWidget::item {{
            padding: 6px;
            word-wrap: break-word;
        }}
        QListWidget::item:selected {{
            background-color: {self.button_bg};
            color: {self.font_color};
        }}
    """)
    self.entries_listbox.setContextMenuPolicy(qtc.Qt.CustomContextMenu)
    self.entries_listbox.customContextMenuRequested.connect(lambda pos: show_context_menu(self, pos))
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
            word-wrap: break-word;
        }}
        QTreeWidget::item:selected {{
            background-color: {self.button_bg};
            color: {self.font_color};
        }}
    """)
    self.entries_detailed_list.setHeaderLabels(["Title", "Published"])
    self.entries_listbox.customContextMenuRequested.connect(lambda pos: show_context_menu(self, pos))    
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
            word-wrap: break-word;
            border-radius: 4px;
            margin-bottom: 6px;
        }}
        QListWidget::item:selected {{
            background-color: {self.button_bg};
            color: {self.font_color};
        }}
    """)
    self.entries_listbox.customContextMenuRequested.connect(lambda pos: show_context_menu(self, pos))
    entries_layout.addWidget(self.entries_card_view)
    self.entries_card_view.hide()

    self.entry_details_text = qtw.QTextBrowser(entries_frame)
    self.entry_details_text.setStyleSheet(f"""
        QTextBrowser {{
            background-color: {self.window_bg};
            color: {self.font_color};
            font: {font_style};
            word-wrap: break-word;
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

def show_context_menu(self, pos):
    if not self.entries_listbox.selectedItems():
        return

    menu = qtw.QMenu(self)

    show_details_action = qtg.QAction("Show Details", self)
    show_details_action.triggered.connect(self.show_entry_details)
    menu.addAction(show_details_action)

    remove_entry_action = qtg.QAction("Remove Entry", self)
    remove_entry_action.triggered.connect(self.remove_entry)
    menu.addAction(remove_entry_action)

    menu.exec(self.entries_listbox.mapToGlobal(pos))

