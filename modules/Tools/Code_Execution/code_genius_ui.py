# modules/Tools/Code_Execution/code_genius_ui.py

import sys
import threading
from PySide6 import QtGui, QtWidgets
from PySide6.QtWidgets import QWidget, QVBoxLayout, QTextEdit, QPushButton, QSplitter, QApplication, QLabel, QHBoxLayout
from PySide6.QtCore import Qt, Slot, QSize, Signal, QObject
from modules.Tools.Code_Execution.python_interpreter import PythonInterpreter
from modules.Tools.Code_Execution.python_highlighter import PythonHighlighter
from modules.logging.logger import setup_logger
from modules.event_system import event_system

logger = setup_logger('code_genius_ui.py')

icon_size = 24  # Define the icon size

class CodeExecutionThread(QObject):
    execution_finished = Signal(dict)

    def __init__(self, code, interpreter):
        super().__init__()
        self.code = code
        self.interpreter = interpreter
        self._is_running = True
        self.thread = threading.Thread(target=self.run_code)
        self.thread.daemon = True

    def run_code(self):
        logger.debug(f"Executing code in thread: {self.code}")
        result = self.interpreter.run(self.code)
        if self._is_running:
            self.execution_finished.emit(result)
        else:
            self.execution_finished.emit({"success": False, "result": None, "error": "Execution stopped"})
        logger.debug("Code execution thread finished")

    def start(self):
        self.thread.start()

    def stop(self):
        self._is_running = False
        logger.debug("Stopping code execution thread")

class CodeExecutionWidget(QWidget):
    def __init__(self, python_interpreter: PythonInterpreter, parent=None):
        super().__init__(parent)
        self.python_interpreter = python_interpreter
        self.execution_thread = None
        self.setup_ui()
        logger.debug("CodeExecutionWidget initialized")

    def setup_ui(self):
        layout = QVBoxLayout(self)

        self.code_input = QTextEdit()
        self.code_input.setPlaceholderText("Enter Python code here...")
        self.highlighter = PythonHighlighter(self.code_input.document())
        self.code_input.setStyleSheet("""
            QTextEdit {
                background-color: #1e1e1e;
                color: #d4d4d4;
                border: 1px solid #3e3e3e;
                font-family: 'Consolas', 'Courier New', monospace;
                font-size: 14px;
            }
        """)
        layout.addWidget(self.code_input)

        # Add the toolbar
        self.toolbar = QHBoxLayout()
        self.toolbar_widget = QWidget()
        self.toolbar_widget.setLayout(self.toolbar)
        self.toolbar_widget.setStyleSheet("background-color: ##1e1e1e;")
        self.add_toolbar_buttons()
        layout.addWidget(self.toolbar_widget)

        self.setLayout(layout)

        logger.debug("CodeExecutionWidget UI setup complete")

    def add_toolbar_buttons(self):
        # Run button
        run_img = QtGui.QPixmap("assets/SCOUT/Icons/play_wt.png")
        run_img = run_img.scaled(icon_size, icon_size)

        self.run_button = QtWidgets.QPushButton(self)
        self.run_button.setIcon(QtGui.QIcon(run_img))
        self.run_button.setIconSize(QSize(icon_size, icon_size))
        self.run_button.setStyleSheet("QPushButton { background-color: transparent; border: none; }")
        self.run_button.clicked.connect(self.execute_code)
        self.toolbar.addWidget(self.run_button)

        def on_run_button_hover(event):
            hover_img = QtGui.QPixmap("assets/SCOUT/Icons/play_bl.png")
            hover_img = hover_img.scaled(icon_size, icon_size)
            self.run_button.setIcon(QtGui.QIcon(hover_img))

        def on_run_button_leave(event):
            self.run_button.setIcon(QtGui.QIcon(run_img))

        self.run_button.enterEvent = lambda event: on_run_button_hover(event)
        self.run_button.leaveEvent = lambda event: on_run_button_leave(event)

        # Stop button
        stop_img = QtGui.QPixmap("assets/SCOUT/Icons/stop_wt.png")
        stop_img = stop_img.scaled(icon_size, icon_size)

        self.stop_button = QtWidgets.QPushButton(self)
        self.stop_button.setIcon(QtGui.QIcon(stop_img))
        self.stop_button.setIconSize(QSize(icon_size, icon_size))
        self.stop_button.setStyleSheet("QPushButton { background-color: transparent; border: none; }")
        self.stop_button.clicked.connect(self.stop_execution)
        self.toolbar.addWidget(self.stop_button)

        def on_stop_button_hover(event):
            hover_img = QtGui.QPixmap("assets/SCOUT/Icons/stop_rd.png")
            hover_img = hover_img.scaled(icon_size, icon_size)
            self.stop_button.setIcon(QtGui.QIcon(hover_img))

        def on_stop_button_leave(event):
            self.stop_button.setIcon(QtGui.QIcon(stop_img))

        self.stop_button.enterEvent = lambda event: on_stop_button_hover(event)
        self.stop_button.leaveEvent = lambda event: on_stop_button_leave(event)

        self.toolbar.addStretch(1)

    def execute_code(self):
        code = self.code_input.toPlainText()
        logger.debug(f"Starting execution thread for code: {code}")
        self.execution_thread = CodeExecutionThread(code, self.python_interpreter)
        self.execution_thread.execution_finished.connect(self.on_execution_finished)
        self.execution_thread.start()

    def stop_execution(self):
        if self.execution_thread:
            logger.debug("Stopping execution thread")
            self.execution_thread.stop()
            self.execution_thread = None

    @Slot(dict)
    def on_execution_finished(self, result: dict):
        event_system.publish("code_executed", self.code_input.toPlainText(), result)
        self.execution_thread = None

class CodeGeniusUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setup_ui()
        event_system.subscribe("code_executed", self.on_code_executed)
        logger.debug("CodeGeniusUI initialized and subscribed to code_executed event")

    def setup_ui(self):
        layout = QVBoxLayout(self)

        # Add CodeGeniusUI Title bar
        self.label = QLabel("CodeGenius UI")
        self.label.setStyleSheet("color: white; background-color: #1e1e1e; font-size: 18px;")
        layout.addWidget(self.label)

        # Create a splitter
        splitter = QSplitter(Qt.Vertical)

        # Create the code input area with highlighting and toolbar
        self.code_input_widget = CodeExecutionWidget(PythonInterpreter())
        splitter.addWidget(self.code_input_widget)

        # Create the code display area
        self.code_display = QTextEdit(self)
        self.code_display.setReadOnly(True)
        self.code_display.setStyleSheet("""
            QTextEdit {
                background-color: #2d2d2d;
                color: white;
                border: 1px solid #3e3e3e;
                font-family: 'Consolas', 'Courier New', monospace;
                font-size: 14px;
            }
        """)
        splitter.addWidget(self.code_display)

        layout.addWidget(splitter)

        self.setLayout(layout)

        # Set overall widget style
        self.setStyleSheet("""
            CodeGeniusUI {
                background-color: #1e1e1e;
            }
        """)
        self.setMinimumSize(400, 300)  # Set a minimum size

        logger.debug("CodeGeniusUI UI setup complete")

    def on_code_executed(self, code: str, result: dict):
        logger.debug(f"CodeGeniusUI received code execution result: {result}")
        self.show()
        self.code_display.setPlainText(f"Executed Code:\n{code}\n")
        output = result['result'] if result['success'] else result['error']
        self.code_display.append(f"Output:\n{output}")
        logger.info("CodeGeniusUI updated with execution result")

    def show(self):
        super().show()
        logger.info("CodeGeniusUI shown")
        # Force an update
        self.repaint()

    def hide(self):
        super().hide()
        logger.info("CodeGeniusUI hidden")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CodeGeniusUI()
    window.show()
    sys.exit(app.exec())
