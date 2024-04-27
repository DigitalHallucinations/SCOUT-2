# gui/tooltip.py

from PySide6.QtWidgets import QToolTip
from PySide6.QtGui import QPalette, QColor, QFont
import configparser

class ToolTip:
    def __init__(self):
        self.config = configparser.ConfigParser()
        self.config.read('config.ini')
        palette = QPalette()
        palette.setColor(QPalette.ToolTipBase, QColor(self.config.get('MessageBoxSettings', 'window_bg')))
        palette.setColor(QPalette.ToolTipText, QColor(self.config.get('MessageBoxSettings', 'font_color')))
        QToolTip.setPalette(palette)
        font = QFont()
        font.setFamily(self.config.get('MessageBoxSettings', 'font_family'))
        font.setPointSize(int(self.config.get('MessageBoxSettings', 'font_size')))
        QToolTip.setFont(font)

    @staticmethod
    def setToolTip(widget, text):
        widget.setToolTip(text)