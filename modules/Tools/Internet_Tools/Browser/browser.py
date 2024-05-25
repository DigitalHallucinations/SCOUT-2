# modules/Tools/Internet_Tools/browser.py

import re

from PySide6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton, QToolBar, QStatusBar, QTabWidget, QTabBar, QLabel, QMenu, QFileDialog
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWebEngineCore import QWebEnginePage
from PySide6.QtCore import QUrl, QSize, Qt
from PySide6.QtGui import QIcon, QPixmap

from modules.Tools.Internet_Tools.Browser.browser_db import BrowserDatabase
from modules.logging.logger import setup_logger


logger = setup_logger('browser.py')


class MyWebEnginePage(QWebEnginePage):
    def certificateError(self, certificateError):
        logger.error(f"SSL Certificate Error: {certificateError.errorDescription()}")
        return True  


    def javaScriptConsoleMessage(self, level, message, lineNumber, sourceID):
        logger.error(f"JavaScript Console: {message} (Source: {sourceID}, Line: {lineNumber})") 


class CustomTabBar(QTabBar):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMovable(True)
        self.setTabsClosable(True)
        self.setElideMode(Qt.ElideRight)
        self.setSelectionBehaviorOnRemove(QTabBar.SelectPreviousTab)


class Browser(QMainWindow):
    def __init__(self):
        super().__init__()
        logger.info("Initializing Browser")

        # Initialize the BrowserDatabase
        self.db = BrowserDatabase()

        self.home_page = "https://www.google.com"
        self.bookmarks = []
        self.history = []

        icon_size = QSize(22, 22)


        # Create central widget and layout
        central_widget = QWidget()
        central_widget.setStyleSheet("background-color: transparent;")
        main_layout = QVBoxLayout(central_widget)
        self.setCentralWidget(central_widget)


        # Create toolbar for navigation
        self.toolbar = QToolBar()
        self.addToolBar(self.toolbar)


        # Back Icon
        back_img = QPixmap("assets/SCOUT/Icons/Browser_icons/back_wt.png")
        back_img = back_img.scaled(icon_size.width(), icon_size.height())


        # Back button
        back_button = QPushButton(self)
        back_button.setIcon(QIcon(back_img))
        back_button.setIconSize(icon_size)
        back_button.setStyleSheet("QPushButton { background-color: transparent; border: none; }")
        back_button.clicked.connect(self.browser_back)
        self.toolbar.addWidget(back_button)
        logger.info("Back button added")


        def on_back_button_hover(event):
            hover_img = QPixmap("assets/SCOUT/Icons/Browser_icons/back_bl.png")
            hover_img = hover_img.scaled(icon_size.width(), icon_size.height())
            back_button.setIcon(QIcon(hover_img))


        def on_back_button_leave(event):
            back_button.setIcon(QIcon(back_img))


        back_button.enterEvent = lambda event: on_back_button_hover(event)
        back_button.leaveEvent = lambda event: on_back_button_leave(event)


        # Forward Icon
        forward_img = QPixmap("assets/SCOUT/Icons/Browser_icons/forward_wt.png")
        forward_img = forward_img.scaled(icon_size.width(), icon_size.height())


        # Forward button
        forward_button = QPushButton(self)
        forward_button.setIcon(QIcon(forward_img))
        forward_button.setIconSize(icon_size)
        forward_button.setStyleSheet("QPushButton { background-color: transparent; border: none; }")
        forward_button.clicked.connect(self.browser_forward)
        self.toolbar.addWidget(forward_button)
        logger.info("Forward button added")


        def on_forward_button_hover(event):
            hover_img = QPixmap("assets/SCOUT/Icons/Browser_icons/forward_bl.png")
            hover_img = hover_img.scaled(icon_size.width(), icon_size.height())
            forward_button.setIcon(QIcon(hover_img))


        def on_forward_button_leave(event):
            forward_button.setIcon(QIcon(forward_img))


        forward_button.enterEvent = lambda event: on_forward_button_hover(event)
        forward_button.leaveEvent = lambda event: on_forward_button_leave(event)


        # Reload Icon
        reload_img = QPixmap("assets/SCOUT/Icons/Browser_icons/reload_wt.png")
        reload_img = reload_img.scaled(icon_size.width(), icon_size.height())


        # Reload button
        reload_button = QPushButton(self)
        reload_button.setIcon(QIcon(reload_img))
        reload_button.setIconSize(icon_size)
        reload_button.setStyleSheet("QPushButton { background-color: transparent; border: none; }")
        reload_button.clicked.connect(self.browser_reload)
        self.toolbar.addWidget(reload_button)
        logger.info("Reload button added")


        def on_reload_button_hover(event):
            hover_img = QPixmap("assets/SCOUT/Icons/Browser_icons/reload_bl.png")
            hover_img = hover_img.scaled(icon_size.width(), icon_size.height())
            reload_button.setIcon(QIcon(hover_img))


        def on_reload_button_leave(event):
            reload_button.setIcon(QIcon(reload_img))


        reload_button.enterEvent = lambda event: on_reload_button_hover(event)
        reload_button.leaveEvent = lambda event: on_reload_button_leave(event)


        # Home Icon
        home_img_path = "assets/SCOUT/Icons/Browser_icons/home_wt.png"
        home_img = QPixmap(home_img_path)
        if home_img.isNull():
            logger.error(f"Failed to load image: {home_img_path}")
        else:
            home_img = home_img.scaled(icon_size.width(), icon_size.height())


        # Home button
        home_button = QPushButton(self)
        home_button.setIcon(QIcon(home_img))
        home_button.setIconSize(icon_size)
        home_button.setStyleSheet("QPushButton { background-color: transparent; border: none; }")
        home_button.clicked.connect(self.browser_home)
        self.toolbar.addWidget(home_button)
        logger.info("Home button added")


        def on_home_button_hover(event):
            hover_img_path = "assets/SCOUT/Icons/Browser_icons/home_bl.png"
            hover_img = QPixmap(hover_img_path)
            if hover_img.isNull():
                logger.error(f"Failed to load image: {hover_img_path}")
            else:
                hover_img = hover_img.scaled(icon_size.width(), icon_size.height())
                home_button.setIcon(QIcon(hover_img))


        def on_home_button_leave(event):
            home_button.setIcon(QIcon(home_img))


        home_button.enterEvent = lambda event: on_home_button_hover(event)
        home_button.leaveEvent = lambda event: on_home_button_leave(event)


        # URL bar
        self.url_bar = QLineEdit()
        self.url_bar.returnPressed.connect(self.navigate_to_url)
        self.url_bar.setStyleSheet("""
            QLineEdit {
                color: #ffffff;
                background-color: #2d2d2d;
                border: none;
                border-radius: 10px;
                padding: 5px;
            }
        """)
        self.toolbar.addWidget(self.url_bar)
        logger.info("URL bar added")


        # Add tab button
        self.add_tab_button = QPushButton(self)
        self.add_tab_button.setIcon(QIcon("assets/SCOUT/Icons/Browser_icons/add_tab_wt.png"))
        self.add_tab_button.setIconSize(QSize(22, 22))
        self.add_tab_button.setStyleSheet("QPushButton { background-color: transparent; border: none; }")
        self.add_tab_button.clicked.connect(self.add_new_tab)
        self.toolbar.addWidget(self.add_tab_button)


        def on_home_button_hover(event):
            hover_img_path = "assets/SCOUT/Icons/Browser_icons/home_bl.png"
            hover_img = QPixmap(hover_img_path)
            if hover_img.isNull():
                logger.error(f"Failed to load image: {hover_img_path}")
            else:
                hover_img = hover_img.scaled(icon_size.width(), icon_size.height())
                home_button.setIcon(QIcon(hover_img))


        def on_home_button_leave(event):
            home_button.setIcon(QIcon(home_img))


        home_button.enterEvent = lambda event: on_home_button_hover(event)
        home_button.leaveEvent = lambda event: on_home_button_leave(event)


        # Bookmarks Bar
        self.bookmarks_toolbar = QToolBar("Bookmarks")
        self.addToolBar(Qt.TopToolBarArea, self.bookmarks_toolbar)
        self.insertToolBarBreak(self.bookmarks_toolbar)  # Ensure the bookmarks toolbar is below the main toolbar


        # Bookmark Icon
        bookmark_img = QPixmap("assets/SCOUT/Icons/Browser_icons/bookmark_wt.png")
        bookmark_img = bookmark_img.scaled(icon_size.width(), icon_size.height())


        # Bookmark button
        bookmark_button = QPushButton(self)
        bookmark_button.setIcon(QIcon(bookmark_img))
        bookmark_button.setIconSize(icon_size)
        bookmark_button.setStyleSheet("QPushButton { background-color: transparent; border: none; }")
        bookmark_button.clicked.connect(self.add_bookmark)
        self.bookmarks_toolbar.addWidget(bookmark_button)  # Add bookmark button to bookmarks toolbar
        logger.info("Bookmark button added")


        def on_bookmark_button_hover(event):
            hover_img = QPixmap("assets/SCOUT/Icons/Browser_icons/bookmark_bl.png")
            hover_img = hover_img.scaled(icon_size.width(), icon_size.height())
            bookmark_button.setIcon(QIcon(hover_img))


        def on_bookmark_button_leave(event):
            bookmark_button.setIcon(QIcon(bookmark_img))


        bookmark_button.enterEvent = lambda event: on_bookmark_button_hover(event)
        bookmark_button.leaveEvent = lambda event: on_bookmark_button_leave(event)


        self.content_layout = QHBoxLayout()
        main_layout.addLayout(self.content_layout)


        # Create tab widget
        self.tabs = QTabWidget()
        self.tabs.setTabBar(CustomTabBar(self.tabs))
        self.tabs.setTabsClosable(True)
        self.tabs.tabCloseRequested.connect(self.close_tab)
        self.content_layout.addWidget(self.tabs)


        # Add initial tab
        self.add_new_tab("Home")
        self.browser_home()


        # Add status bar
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.tabs.currentWidget().loadStarted.connect(lambda: self.status_bar.showMessage("Loading..."))
        self.tabs.currentWidget().loadFinished.connect(lambda: self.status_bar.showMessage(""))

        self.browser_view.page().profile().downloadRequested.connect(self.on_download_requested)

        # Load bookmarks from the database
        self.load_bookmarks()

    def on_download_requested(self, download):
        download_path = QFileDialog.getSaveFileName(self, "Save File", download.path())[0]
        if download_path:
            download.setPath(download_path)
            download.accept()
            logger.info(f"Download started: {download_path}")
        else:
            download.cancel()
            logger.info("Download canceled")

    def show_context_menu(self, pos):
        context_menu = QMenu(self)
        back_action = context_menu.addAction("Back")
        forward_action = context_menu.addAction("Forward")
        reload_action = context_menu.addAction("Reload")
        context_menu.addSeparator()
        bookmark_action = context_menu.addAction("Bookmark")


        action = context_menu.exec_(self.browser_view.mapToGlobal(pos))


        if action == back_action:
            self.browser_back()
        elif action == forward_action:
            self.browser_forward()
        elif action == reload_action:
            self.browser_reload()
        elif action == bookmark_action:
            self.add_bookmark()


    def add_new_tab(self, qurl=None, label="Blank"):
        self.browser_view = QWebEngineView()
        
        self.browser_view.urlChanged.connect(self.update_url_bar)
        self.browser_view.loadFinished.connect(self.on_load_finished)
        self.browser_view.setPage(MyWebEnginePage(self.browser_view))
        
        i = self.tabs.addTab(self.browser_view, label)
        self.tabs.setCurrentIndex(i)

        if qurl:
            if isinstance(qurl, str):
                qurl = QUrl(qurl)
            self.browser_view.setUrl(qurl)
        else:
            self.browser_home()

        # Add history entry to the database
        self.db.add_history(qurl.toString(), label)

    def close_tab(self, i):
        if self.tabs.count() > 1:
            self.tabs.removeTab(i)


    def browser_back(self):
        self.tabs.currentWidget().back()


    def browser_forward(self):
        self.tabs.currentWidget().forward()


    def browser_reload(self):
        self.tabs.currentWidget().reload()


    def browser_home(self):
        self.tabs.currentWidget().setUrl(QUrl(self.home_page))


    def navigate_to_url(self):
        url = self.url_bar.text()
        if not url.startswith("http"):
            url = "http://" + url
        self.tabs.currentWidget().setUrl(QUrl(url))


    def update_url_bar(self, q):
        self.url_bar.setText(q.toString())
        self.tabs.setTabText(self.tabs.currentIndex(), q.toString())

    def on_load_finished(self, success):
        if not success:
            logger.error("Failed to load the page. Check the URL or your internet connection.")
        else:
            logger.info("Page loaded successfully.")
            current_url = self.tabs.currentWidget().url().toString()
            current_title = self.tabs.tabText(self.tabs.currentIndex())
            self.db.add_history(current_url, current_title)

    def handle_ssl_errors(self, reply, errors):
        logger.error(f"SSL errors occurred: {errors}")
        reply.ignoreSslErrors()

    def add_bookmark(self):
        current_url = self.tabs.currentWidget().url().toString()
        if current_url not in self.bookmarks:
            self.bookmarks.append(current_url)
            bookmark_name = self.extract_site_name(current_url)
            bookmark_label = QLabel(bookmark_name)
            bookmark_label.setStyleSheet("color: #FFFFFF;")
            bookmark_label.mousePressEvent = lambda event: self.tabs.currentWidget().setUrl(QUrl(current_url))
            bookmark_label.enterEvent = lambda event: bookmark_label.setStyleSheet("color: #5077E0;")
            bookmark_label.leaveEvent = lambda event: bookmark_label.setStyleSheet("color: #FFFFFF;")
            self.bookmarks_toolbar.addWidget(bookmark_label)
            logger.info(f"Added bookmark: {current_url}")

            self.db.add_bookmark(current_url, bookmark_name)
        else:
            logger.info(f"Bookmark already exists: {current_url}")

    def extract_site_name(self, url):
        match = re.search(r'://(www\.)?([^/]+)', url)
        if match:
            return match.group(2).split('.')[0].capitalize()
        return "Unknown"
    
    def load_bookmarks(self):
        bookmarks = self.db.get_all_bookmarks()
        for bookmark in bookmarks:
            url, title = bookmark[1], bookmark[2]
            bookmark_label = QLabel(title)
            bookmark_label.setStyleSheet("color: #FFFFFF;")
            bookmark_label.mousePressEvent = lambda event, url=url: self.tabs.currentWidget().setUrl(QUrl(url))
            bookmark_label.enterEvent = lambda event, label=bookmark_label: label.setStyleSheet("color: #5077E0;")
            bookmark_label.leaveEvent = lambda event, label=bookmark_label: label.setStyleSheet("color: #FFFFFF;")
            self.bookmarks_toolbar.addWidget(bookmark_label)
            self.bookmarks.append(url)
            logger.info(f"Loaded bookmark: {url}")

    def load_history(self):
        history = self.db.get_all_history()
        for entry in history:
            url, title = entry[1], entry[2]
            self.history.append(url)
            logger.info(f"Loaded history entry: {url}")