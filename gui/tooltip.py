# gui/tooltip.py

from PySide6.QtWidgets import QToolTip
from PySide6.QtGui import QPalette, QColor, QFont
import configparser

class ToolTip:
    def __init__(self):
        self.config = configparser.ConfigParser()
        self.config.read('config.ini')

    @staticmethod
    def setToolTip(widget, text):
        widget.setToolTip(text)