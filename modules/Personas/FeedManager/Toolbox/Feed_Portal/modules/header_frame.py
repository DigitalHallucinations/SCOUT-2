# modules/Personas/FeedManager/Toolbox/Feed_Portal/header_frame.py

from PySide6 import QtWidgets as qtw
from PySide6 import QtCore as qtc
from PySide6 import QtGui as qtg

from modules.Personas.FeedManager.Toolbox.Feed_Portal.settings import settings, filter_sort_settings
from gui.tooltip import ToolTip

def create_header_frame(self, layout):
    header_frame = qtw.QFrame(self)
    header_frame.setStyleSheet(f"background-color: {self.window_bg}; border-radius: 10px;")
    header_layout = qtw.QHBoxLayout(header_frame)
    header_layout.setContentsMargins(10, 10, 10, 10)
    header_layout.setSpacing(5)  
    header_layout.addStretch(1)  
    layout.addWidget(header_frame)

    icon_size = 32

    filter_sort_button = qtw.QPushButton(header_frame)
    filter_sort_button.setIcon(qtg.QIcon("assets/SCOUT/Icons/filter_wt.png"))
    filter_sort_button.setIconSize(qtc.QSize(icon_size, icon_size))
    filter_sort_button.setStyleSheet("QPushButton { background-color: transparent; border: none; }")
    filter_sort_button.clicked.connect(lambda: filter_sort_settings.open_filter_settings(self))
    header_layout.addWidget(filter_sort_button)

    def on_filter_sort_button_hover(event):
        filter_sort_button.setIcon(qtg.QIcon("assets/SCOUT/Icons/filter_bl.png"))
        ToolTip.setToolTip(filter_sort_button, "Open Filter/Sort Settings")

    def on_filter_sort_button_leave(event):
        filter_sort_button.setIcon(qtg.QIcon("assets/SCOUT/Icons/filter_wt.png"))

    filter_sort_button.enterEvent = lambda event: on_filter_sort_button_hover(event)
    filter_sort_button.leaveEvent = lambda event: on_filter_sort_button_leave(event)

    self.search_button = qtw.QPushButton(header_frame)
    self.search_button.setIcon(qtg.QIcon("assets/SCOUT/Icons/search_wt.png"))
    self.search_button.setIconSize(qtc.QSize(icon_size, icon_size))
    self.search_button.setStyleSheet("QPushButton { background-color: transparent; border: none; }")
    self.search_button.clicked.connect(self.open_search_window)
    header_layout.addWidget(self.search_button)

    def on_search_button_hover(event):
        self.search_button.setIcon(qtg.QIcon("assets/SCOUT/Icons/search_bl.png"))
        ToolTip.setToolTip(self.search_button, "Open Search Window")

    def on_search_button_leave(event):
        self.search_button.setIcon(qtg.QIcon("assets/SCOUT/Icons/search_wt.png"))

    self.search_button.enterEvent = lambda event: on_search_button_hover(event)
    self.search_button.leaveEvent = lambda event: on_search_button_leave(event)

    settings_img = qtg.QPixmap("assets/SCOUT/Icons/settings_wt.png")
    settings_img = settings_img.scaled(icon_size, icon_size)

    self.settings_button = qtw.QPushButton(header_frame)
    self.settings_button.setIcon(qtg.QIcon(settings_img))
    self.settings_button.setIconSize(qtc.QSize(icon_size, icon_size))
    self.settings_button.setStyleSheet("QPushButton { background-color: transparent; border: none; }")
    self.settings_button.clicked.connect(lambda: settings.open_settings(self))
    header_layout.addWidget(self.settings_button)

    def on_settings_button_hover(event):
        hover_img = qtg.QPixmap("assets/SCOUT/Icons/settings_bl.png")
        hover_img = hover_img.scaled(icon_size, icon_size)
        self.settings_button.setIcon(qtg.QIcon(hover_img))
        ToolTip.setToolTip(self.settings_button, "Open Settings")

    def on_settings_button_leave(event):
        self.settings_button.setIcon(qtg.QIcon(settings_img))

    self.settings_button.enterEvent = lambda event: on_settings_button_hover(event)
    self.settings_button.leaveEvent = lambda event: on_settings_button_leave(event)