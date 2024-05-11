# modules\tooltip.py

from PySide6 import QtWidgets as qtw
from PySide6 import QtCore as qtc
from PySide6 import QtGui as qtg

class ToolTip:
    @staticmethod
    def setToolTip(widget, text):
        widget.setToolTip(text)