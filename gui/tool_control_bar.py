# gui/tool_control_bar.py

from PySide6 import QtWidgets, QtGui
from PySide6 import QtCore as qtc

class ToolControlBar(QtWidgets.QFrame):
    def __init__(self, parent=None, voip_app=None, feed_portal=None, browser=None, calendar=None, code_genius_ui=None):
        super().__init__(parent)
        self.setFixedHeight(30)
        self.setStyleSheet("""
            QFrame {
                background-color: #2d2d2d;
                border-radius: 10px;
            }
        """)

        layout = QtWidgets.QHBoxLayout(self)
        layout.setContentsMargins(5, 0, 0, 0)
        layout.setSpacing(10)  

        self.voip_app = voip_app
        self.feed_portal = feed_portal
        self.browser = browser
        self.calendar = calendar
        self.code_genius_ui = code_genius_ui

        icon_size = 20

        # Phone Icon
        phone_img = QtGui.QPixmap("assets/SCOUT/Icons/Voip_icons/phone_wt.png")
        phone_img = phone_img.scaled(icon_size, icon_size)

        phone_button = QtWidgets.QPushButton(self)
        phone_button.setIcon(QtGui.QIcon(phone_img))
        phone_button.setIconSize(qtc.QSize(icon_size, icon_size))
        phone_button.setStyleSheet("QPushButton { background-color: transparent; border: none; }")
        phone_button.clicked.connect(self.show_voip_app)
        layout.addWidget(phone_button)

        def on_phone_button_hover(event):
            hover_img = QtGui.QPixmap("assets/SCOUT/Icons/Voip_icons/phone_bl.png")
            hover_img = hover_img.scaled(icon_size, icon_size)
            phone_button.setIcon(QtGui.QIcon(hover_img))

        def on_phone_button_leave(event):
            phone_button.setIcon(QtGui.QIcon(phone_img))

        phone_button.enterEvent = lambda event: on_phone_button_hover(event)
        phone_button.leaveEvent = lambda event: on_phone_button_leave(event)

        # RSS Icon
        rss_img = QtGui.QPixmap("assets/SCOUT/Icons/Voip_icons/rss_wt.png")
        rss_img = rss_img.scaled(icon_size, icon_size)

        rss_button = QtWidgets.QPushButton(self)
        rss_button.setIcon(QtGui.QIcon(rss_img))
        rss_button.setIconSize(qtc.QSize(icon_size, icon_size))
        rss_button.setStyleSheet("QPushButton { background-color: transparent; border: none; }")
        rss_button.clicked.connect(self.show_feed_portal)
        layout.addWidget(rss_button)

        def on_rss_button_hover(event):
            hover_img = QtGui.QPixmap("assets/SCOUT/Icons/Voip_icons/rss_bl.png")
            hover_img = hover_img.scaled(icon_size, icon_size)
            rss_button.setIcon(QtGui.QIcon(hover_img))

        def on_rss_button_leave(event):
            rss_button.setIcon(QtGui.QIcon(rss_img))

        rss_button.enterEvent = lambda event: on_rss_button_hover(event)
        rss_button.leaveEvent = lambda event: on_rss_button_leave(event)

        # Browser Icon
        browser_img = QtGui.QPixmap("assets/SCOUT/Icons/browser_wt.png")
        browser_img = browser_img.scaled(icon_size, icon_size)

        browser_button = QtWidgets.QPushButton(self)
        browser_button.setIcon(QtGui.QIcon(browser_img))
        browser_button.setIconSize(qtc.QSize(icon_size, icon_size))
        browser_button.setStyleSheet("QPushButton { background-color: transparent; border: none; }")
        browser_button.clicked.connect(self.show_browser)
        layout.addWidget(browser_button)

        def on_browser_button_hover(event):
            hover_img = QtGui.QPixmap("assets/SCOUT/Icons/browser_bl.png")
            hover_img = hover_img.scaled(icon_size, icon_size)
            browser_button.setIcon(QtGui.QIcon(hover_img))

        def on_browser_button_leave(event):
            browser_button.setIcon(QtGui.QIcon(browser_img))

        browser_button.enterEvent = lambda event: on_browser_button_hover(event)
        browser_button.leaveEvent = lambda event: on_browser_button_leave(event)

        # Calendar Icon
        calendar_img = QtGui.QPixmap("assets/SCOUT/Icons/calendar_wt.png")
        calendar_img = calendar_img.scaled(icon_size, icon_size)

        calendar_button = QtWidgets.QPushButton(self)
        calendar_button.setIcon(QtGui.QIcon(calendar_img))
        calendar_button.setIconSize(qtc.QSize(icon_size, icon_size))
        calendar_button.setStyleSheet("QPushButton { background-color: transparent; border: none; }")
        calendar_button.clicked.connect(self.show_calendar)
        layout.addWidget(calendar_button)

        def on_calendar_button_hover(event):
            hover_img = QtGui.QPixmap("assets/SCOUT/Icons/calendar_bl.png")
            hover_img = hover_img.scaled(icon_size, icon_size)
            calendar_button.setIcon(QtGui.QIcon(hover_img))

        def on_calendar_button_leave(event):
            calendar_button.setIcon(QtGui.QIcon(calendar_img))

        calendar_button.enterEvent = lambda event: on_calendar_button_hover(event)
        calendar_button.leaveEvent = lambda event: on_calendar_button_leave(event)

        # CodeGenius Icon
        code_genius_img = QtGui.QPixmap("assets/SCOUT/Icons/code_genius_wt.png")
        code_genius_img = code_genius_img.scaled(icon_size, icon_size)

        code_genius_button = QtWidgets.QPushButton(self)
        code_genius_button.setIcon(QtGui.QIcon(code_genius_img))
        code_genius_button.setIconSize(qtc.QSize(icon_size, icon_size))
        code_genius_button.setStyleSheet("QPushButton { background-color: transparent; border: none; }")
        code_genius_button.clicked.connect(self.show_code_genius_ui)
        layout.addWidget(code_genius_button)

        def on_code_genius_button_hover(event):
            hover_img = QtGui.QPixmap("assets/SCOUT/Icons/code_genius_bl.png")
            hover_img = hover_img.scaled(icon_size, icon_size)
            code_genius_button.setIcon(QtGui.QIcon(hover_img))

        def on_code_genius_button_leave(event):
            code_genius_button.setIcon(QtGui.QIcon(code_genius_img))

        code_genius_button.enterEvent = lambda event: on_code_genius_button_hover(event)
        code_genius_button.leaveEvent = lambda event: on_code_genius_button_leave(event)

        layout.addStretch(1)

    def show_feed_portal(self):
        self.feed_portal.show()
        self.voip_app.hide()
        self.browser.hide()
        self.calendar.hide()
        self.code_genius_ui.hide()

    def show_voip_app(self):
        self.voip_app.show()
        self.feed_portal.hide()
        self.browser.hide()
        self.calendar.hide()
        self.code_genius_ui.hide()

    def show_browser(self):
        self.browser.show()
        self.voip_app.hide()
        self.feed_portal.hide()
        self.calendar.hide()
        self.code_genius_ui.hide()

    def show_calendar(self):
        self.calendar.show()
        self.browser.hide()
        self.voip_app.hide()
        self.feed_portal.hide()
        self.code_genius_ui.hide()

    def show_code_genius_ui(self):
        self.code_genius_ui.show()
        self.calendar.hide()
        self.browser.hide()
        self.voip_app.hide()
        self.feed_portal.hide()