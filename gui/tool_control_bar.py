from PySide6 import QtWidgets, QtGui, QtCore as qtc

class ToolControlBar(QtWidgets.QFrame):
    def __init__(self, parent=None, voip_app=None, feed_portal=None):
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

        layout.addStretch(1) 

    def show_feed_portal(self):
        self.feed_portal.show()
        self.voip_app.hide()  

    def show_voip_app(self):
        self.voip_app.show()
        self.feed_portal.hide()  