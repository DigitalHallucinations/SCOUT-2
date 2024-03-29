# gui\components\custom_entry.py

import tkinter as tk
import logging
from logging.handlers import RotatingFileHandler


logger = logging.getLogger('custom_entry.py')

log_filename = 'SCOUT.log'
log_max_size = 10 * 1024 * 1024  # 10 MB
log_backup_count = 5

rotating_handler = RotatingFileHandler(log_filename, maxBytes=log_max_size, backupCount=log_backup_count, encoding='utf-8')
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
rotating_handler.setFormatter(formatter)

stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)

logger.addHandler(rotating_handler)
logger.addHandler(stream_handler)
logger.setLevel(logging.INFO)

def adjust_logging_level(level):
    """Adjust the logging level.
    
    Parameters:
    - level (str): Desired logging level. Can be 'DEBUG', 'INFO', 'WARNING', 'ERROR', or 'CRITICAL'.
    """
    levels = {
        'DEBUG': logging.DEBUG,
        'INFO': logging.INFO,
        'WARNING': logging.WARNING,
        'ERROR': logging.ERROR,
        'CRITICAL': logging.CRITICAL
    }
    
    logger.setLevel(levels.get(level, logging.WARNING))
class CustomEntry(tk.Text):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.bind("<Button-3>", self.show_context_menu)

    def show_context_menu(self, event):
        context_menu = tk.Menu(self, tearoff=0)
        context_menu.add_command(label="Cut", command=self.cut)
        context_menu.add_command(label="Copy", command=self.copy)
        context_menu.add_command(label="Paste", command=self.paste_func) 
        context_menu.add_command(label="Delete", command=self.delete_selected) 
        context_menu.tk.call("tk_popup", context_menu, event.x_root, event.y_root)  

    def cut(self):
        try:
            self.clipboard_clear()
            self.clipboard_append(self.selection_get())
            self.delete_selected()
        except tk.TclError:
            logger.error(f"Error cutting text in the custom entry widget.")

    def copy(self):
        try:
            self.clipboard_clear()
            self.clipboard_append(self.selection_get())
        except tk.TclError:
            logger.error(f"Error copying text in the custom entry widget.")

    def paste_func(self):
        try:
            clipboard_text = self.clipboard_get() 
            if self.tag_ranges(tk.SEL):  
                start = self.index(tk.SEL_FIRST)
                end = self.index(tk.SEL_LAST)
                self.delete(start, end)  
                self.insert(start, clipboard_text)  
            else:
                self.insert(tk.INSERT, clipboard_text)
        except tk.TclError:
            logger.error("Error pasting text in the custom entry widget.")

    def delete_selected(self):
        try:
            start = self.index(tk.SEL_FIRST)
            end = self.index(tk.SEL_LAST)
            self.delete(start, end)
        except tk.TclError:
            logger.error(f"Error deleting selected text in the custom entry widget.")