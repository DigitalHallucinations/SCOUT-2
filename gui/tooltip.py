# gui\components\tooltip.py

import tkinter as tk

class ToolTip:
    def __init__(self, widget, text, delay=500): 
        self.widget = widget
        self.text = text
        self.tooltip = None
        self.id = None
        self.delay = delay
        self.widget.bind("<Enter>", self.schedule)
        self.widget.bind("<Leave>", self.hide)

    def schedule(self, event=None):  
        self.id = self.widget.after(self.delay, self.show)

    def show(self, event=None):
        if self.id:
            self.widget.after_cancel(self.id)
        x, y, _, _ = self.widget.bbox("insert")
        x += self.widget.winfo_rootx() + 25
        y += self.widget.winfo_rooty() + 25
        self.tooltip = tk.Toplevel(self.widget)
        self.tooltip.wm_overrideredirect(True)
        self.tooltip.wm_geometry(f"+{x}+{y}")
        self.tooltip.wm_attributes("-topmost", True)  
        label = tk.Label(self.tooltip, text=self.text, bg="lightyellow", borderwidth=1, relief="solid")
        label.pack()

    def hide(self, event=None):
        if self.id:
            self.widget.after_cancel(self.id)
        if self.tooltip:
            self.tooltip.destroy()
            self.tooltip = None