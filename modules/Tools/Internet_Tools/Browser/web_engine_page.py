# modules/Tools/Internet_Tools/web_engine_page.py

from PySide6.QtWebEngineCore import QWebEnginePage
from modules.logging.logger import setup_logger

logger = setup_logger('web_engine_page.py')

class MyWebEnginePage(QWebEnginePage):
    def certificateError(self, certificateError):
        logger.error(f"SSL Certificate Error: {certificateError.errorDescription()}")
        return True  

    def javaScriptConsoleMessage(self, level, message, lineNumber, sourceID):
        if "Updating additional builtin extensions cache" in message or "Found additional builtin extension gallery resources in env" in message:
            logger.debug(f"JavaScript Console: {message} (Source: {sourceID}, Line: {lineNumber})")
        elif "Creation of workbench contribution" in message:
            logger.warning(f"JavaScript Console: {message} (Source: {sourceID}, Line: {lineNumber})")
        elif "INFO" in message:
            logger.info(f"JavaScript Console: {message} (Source: {sourceID}, Line: {lineNumber})")
        else:
            logger.error(f"JavaScript Console: {message} (Source: {sourceID}, Line: {lineNumber})")
    
        if "ax_tree.cc" in message:
            logger.error(f"AXTree Error: {message} (Source: {sourceID}, Line: {lineNumber})")
            logger.error(f"AXTree Error Context: URL - {self.browser_view.url().toString()}, Line - {lineNumber}, Source - {sourceID}")
        # Add more context or actions here if needed

        # Check for CSP errors and log them
        if "Content-Security-Policy" in message and "'\"self\"'" in message:
            logger.error(f"CSP Error: Invalid source expression '\"self\"'. Use 'self' instead.")

        # Check for undefined properties and log them
        if "Cannot read properties of undefined" in message:
            logger.error(f"Undefined Property Error: {message} (Source: {sourceID}, Line: {lineNumber})")

        # Check for Permutive initialization errors and log them
        if "Permutive was not initialized" in message:
            logger.error(f"Permutive Initialization Error: {message} (Source: {sourceID}, Line: {lineNumber})")

        # Check for AbortError and log them
        if "AbortError" in message:
            logger.error(f"AbortError: {message} (Source: {sourceID}, Line: {lineNumber})")

        # Check for loadable state errors and log them
        if "loadableReady() requires state" in message:
            logger.error(f"Loadable State Error: {message} (Source: {sourceID}, Line: {lineNumber})")

        # Check for event parsing errors and log them
        if "Unable to parse event" in message:
            logger.error(f"Parsing Event Error: {message} (Source: {sourceID}, Line: {lineNumber})")

        # Check for fetch errors and log them
        if "Failed to fetch" in message:
            logger.error(f"Fetch Error: {message} (Source: {sourceID}, Line: {lineNumber})")