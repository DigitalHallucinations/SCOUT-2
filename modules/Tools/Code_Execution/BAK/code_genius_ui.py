# modules/Tools/Code_Execution/code_genius_ui.py

import sys
from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QTextEdit, QPushButton, QSplitter, QApplication, QLabel
from PySide6.QtCore import Qt, Slot
from PySide6.QtWebEngineWidgets import QWebEngineView
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from modules.Tools.Code_Execution.python_interpreter import PythonInterpreter
from modules.Tools.Code_Execution.python_highlighter import PythonHighlighter
from modules.logging.logger import setup_logger
from modules.event_system import event_system

logger = setup_logger('code_genius_ui.py')

class CodeExecutionWidget(QWidget):
    def __init__(self, python_interpreter: PythonInterpreter, parent=None):
        super().__init__(parent)
        self.python_interpreter = python_interpreter
        self.setup_ui()
        logger.debug("CodeExecutionWidget initialized")

    def setup_ui(self):
        layout = QVBoxLayout(self)

        self.code_input = QTextEdit()
        self.code_input.setPlaceholderText("Enter Python code here...")
        layout.addWidget(self.code_input)

        self.execute_button = QPushButton("Execute")
        self.execute_button.clicked.connect(self.execute_code)
        layout.addWidget(self.execute_button)

        self.output_area = QTextEdit()
        self.output_area.setReadOnly(True)
        layout.addWidget(self.output_area)

        logger.debug("CodeExecutionWidget UI setup complete")

    def execute_code(self):
        code = self.code_input.toPlainText()
        logger.debug(f"Executing code: {code}")
        self.python_interpreter.run(code)

    @Slot(str, dict)
    def update_output(self, code: str, result: dict):
        if result['success']:
            output = result['result']
            self.output_area.setPlainText(f"Executed Code:\n{code}\n\nOutput:\n{output}")
        else:
            error = result['error']
            self.output_area.setPlainText(f"Error executing code:\n{code}\n\nError:\n{error}")
        logger.debug("UI updated with execution result")

class VisualizationWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
        logger.debug("VisualizationWidget initialized")

    def setup_ui(self):
        layout = QVBoxLayout(self)
        
        self.figure = plt.figure(figsize=(5, 4))
        self.canvas = FigureCanvas(self.figure)
        layout.addWidget(self.canvas)

        self.web_view = QWebEngineView()
        layout.addWidget(self.web_view)

        logger.debug("VisualizationWidget UI setup complete")

    def update_visualization(self, code: str, output: str):
        logger.debug(f"Updating visualization with code: {code}, output: {output}")
        self.figure.clear()
        
        try:
            data = [float(x) for x in output.split()]
            ax = self.figure.add_subplot(111)
            ax.bar(range(len(data)), data)
            ax.set_title("Output Visualization")
            self.canvas.draw()
            logger.debug("Bar chart visualization created")
        except:
            html_content = f"""
            <html>
            <body>
                <h2>Executed Code:</h2>
                <pre>{code}</pre>
                <h2>Output:</h2>
                <pre>{output}</pre>
            </body>
            </html>
            """
            self.web_view.setHtml(html_content)
            logger.debug("Fallback to HTML visualization")


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
        self.label.setStyleSheet("color: white; font-size: 18px;")
        layout.addWidget(self.label)

        # Create and configure the code input area
        self.code_input = QTextEdit(self)
        self.code_input.setPlaceholderText("Enter Python code here...")
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

        # Apply syntax highlighting to the code input area
        self.highlighter = PythonHighlighter(self.code_input.document())

        # Create and configure the code display area
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
        layout.addWidget(self.code_display)

        # Set overall widget style
        self.setStyleSheet("""
            CodeGeniusUI {
                background-color: #1e1e1e;
            }
        """)
        self.setMinimumSize(400, 300)  # Set a minimum size

        logger.debug("CodeGeniusUI UI setup complete with syntax highlighting")

    def on_code_executed(self, code: str, result: dict):
        logger.debug(f"CodeGeniusUI received code execution result: {result}")
        self.show()
        output = f"Executed Code:\n{code}\n\nResult:\n{result['result']}"
        self.code_display.setPlainText(output)
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