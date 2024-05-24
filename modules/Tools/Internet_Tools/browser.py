#modules/Tools/Internet_Tools/browser.py

from PySide6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton, QToolBar, QStatusBar
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWebEngineCore import QWebEnginePage
from PySide6.QtCore import QUrl
from modules.logging.logger import setup_logger

logger = setup_logger('browser.py')

class MyWebEnginePage(QWebEnginePage):
    def certificateError(self, certificateError):
        logger.error(f"SSL Certificate Error: {certificateError.errorDescription()}")
        return True  

    def javaScriptConsoleMessage(self, level, message, lineNumber, sourceID):
        logger.error(f"JavaScript Console: {message} (Source: {sourceID}, Line: {lineNumber})") # Return True to ignore the error and proceed

class Browser(QMainWindow):
    def __init__(self):
        super().__init__()
        logger.info("Initializing Browser")
        #self.setWindowTitle("Browser")
        #self.setGeometry(100, 100, 800, 600)  

        # Create central widget and layout
        central_widget = QWidget()
        central_widget.setStyleSheet("background-color: transparent;")
        main_layout = QVBoxLayout(central_widget)
        self.setCentralWidget(central_widget)

        # Create toolbar for navigation
        self.toolbar = QToolBar()
        self.addToolBar(self.toolbar)

        # Back button
        back_button = QPushButton("<")
        back_button.clicked.connect(self.browser_back)
        self.toolbar.addWidget(back_button)
        logger.info("Back button added")

        # Forward button
        forward_button = QPushButton(">")
        forward_button.clicked.connect(self.browser_forward)
        self.toolbar.addWidget(forward_button)
        logger.info("Forward button added")

        # Reload button
        reload_button = QPushButton("⟳")
        reload_button.clicked.connect(self.browser_reload)
        self.toolbar.addWidget(reload_button)
        logger.info("Reload button added")

        # Stop button
        stop_button = QPushButton("✖")
        stop_button.clicked.connect(self.browser_stop)
        self.toolbar.addWidget(stop_button)
        logger.info("Stop button added")

        # Home button
        home_button = QPushButton("🏠")
        home_button.clicked.connect(self.browser_home)
        self.toolbar.addWidget(home_button)
        logger.info("Home button added")

        # URL bar
        self.url_bar = QLineEdit()
        self.url_bar.returnPressed.connect(self.navigate_to_url)
        self.toolbar.addWidget(self.url_bar)
        logger.info("URL bar added")

        self.content_layout = QHBoxLayout()
        main_layout.addLayout(self.content_layout)

        # Add QWebEngineView
        self.browser_view = QWebEngineView()
        self.browser_view.urlChanged.connect(self.update_url_bar)
        self.browser_view.loadFinished.connect(self.on_load_finished)
        self.browser_view.setPage(MyWebEnginePage(self.browser_view))
        self.content_layout.addWidget(self.browser_view)

        # Add status bar
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.browser_view.loadStarted.connect(lambda: self.status_bar.showMessage("Loading..."))
        self.browser_view.loadFinished.connect(lambda: self.status_bar.showMessage(""))

        self.browser_view.setUrl(QUrl("https://www.google.com"))

    def browser_back(self):
        self.browser_view.back()

    def browser_forward(self):
        self.browser_view.forward()

    def browser_reload(self):
        self.browser_view.reload()

    def browser_stop(self):
        self.browser_view.stop()

    def browser_home(self):
        self.browser_view.setUrl(QUrl("https://www.google.com"))

    def navigate_to_url(self):
        url = self.url_bar.text()
        if not url.startswith("http"):
            url = "http://" + url
        self.browser_view.setUrl(QUrl(url))

    def update_url_bar(self, q):
        self.url_bar.setText(q.toString())

    def on_load_finished(self, success):
        if not success:
            logger.error("Failed to load the page. Check the URL or your internet connection.")
        else:
            logger.info("Page loaded successfully.")

    def handle_ssl_errors(self, reply, errors):
        logger.error(f"SSL errors occurred: {errors}")
        reply.ignoreSslErrors()