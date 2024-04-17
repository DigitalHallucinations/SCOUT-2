# gui\components\custom_entry.py

import tkinter as tk
from modules.logging.logger import setup_logger

logger = setup_logger('custom_entry.py')

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