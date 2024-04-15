import os
import asyncio
import threading
import tkinter as tk
from tkinter import ttk, messagebox
import json
import configparser
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
#from modules.Personas.RSSManager.Toolbox.RSS.rss_feed_reader import RSSFeedReader, RSSFeedReaderError
from rss_feed_reader import RSSFeedReader, RSSFeedReaderError
import logging
from logging.handlers import RotatingFileHandler

logger = logging.getLogger('RSSFeedReaderUI.py')

log_filename = 'Tools.log'
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
    levels = {
        'DEBUG': logging.DEBUG,
        'INFO': logging.INFO,
        'WARNING': logging.WARNING,
        'ERROR': logging.ERROR,
        'CRITICAL': logging.CRITICAL
    }
    logger.setLevel(levels.get(level, logging.WARNING))

class RSSFeedReaderUI:
    def __init__(self, master):
        self.master = master
        self.master.title("RSS Feed Reader")
        self.rss_feed_reader = RSSFeedReader()
        self.load_feeds()
        self.load_config()
        self.load_settings()
        self.url_cooldown = False 
        self.create_widgets()

    def open_url(self, url):
        if not self.url_cooldown:
            self.url_cooldown = True
            threading.Thread(target=self.open_url_thread, args=(url,)).start()
            self.master.after(5000, self.reset_url_cooldown)  # Start the cooldown timer
        else:
            messagebox.showinfo("Cooldown", "Please wait before clicking the URL again.")

    def open_url_thread(self, url):
        asyncio.run(self.open_url_async(url))

    async def open_url_async(self, url):
        chrome_options = Options()
        chrome_options.add_experimental_option("detach", True)
        driver = webdriver.Chrome(options=chrome_options)
        driver.get(url)

    def reset_url_cooldown(self):
        self.url_cooldown = False

    def load_settings(self):
        config = configparser.ConfigParser()
        config.read("config.ini")

        self.entries_per_feed = config.getint("FeedSettings", "entries_per_feed", fallback=10)
        self.refresh_interval_mins = config.getint("FeedSettings", "refresh_interval_mins", fallback=30)
        self.display_format = config.get("FeedSettings", "display_format", fallback="Simple List")

    def open_settings(self):
        settings_window = tk.Toplevel(self.master)
        settings_window.title("Settings")
        settings_window.configure(bg=self.window_bg)

        font_style = (self.font_family, int(self.font_size * 10))

        style = ttk.Style()
        style.configure("Settings.TLabel", background=self.window_bg, foreground=self.font_color, font=font_style)

        entries_label = ttk.Label(settings_window, text="Entries per Feed:", style="Settings.TLabel")
        entries_label.grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        entries_var = tk.IntVar(value=self.entries_per_feed)
        entries_spinbox = tk.Spinbox(settings_window, from_=1, to=100, textvariable=entries_var, bg=self.spinbox_bg, fg=self.font_color, font=font_style)
        entries_spinbox.grid(row=0, column=1, padx=5, pady=5)

        refresh_label = ttk.Label(settings_window, text="Refresh Interval (mins):", style="Settings.TLabel")
        refresh_label.grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
        refresh_var = tk.IntVar(value=self.refresh_interval_mins)
        refresh_spinbox = tk.Spinbox(settings_window, from_=1, to=1440, textvariable=refresh_var, bg=self.spinbox_bg, fg=self.font_color, font=font_style)
        refresh_spinbox.grid(row=1, column=1, padx=5, pady=5)

        format_label = ttk.Label(settings_window, text="Display Format:", style="Settings.TLabel")
        format_label.grid(row=2, column=0, padx=5, pady=5, sticky=tk.W)
        format_var = tk.StringVar(value=self.display_format)
        format_options = ["Simple List", "Detailed List", "Card View"]
        format_dropdown = tk.OptionMenu(settings_window, format_var, self.display_format, *format_options)
        format_dropdown.configure(bg=self.button_bg, fg=self.font_color, font=font_style)
        format_dropdown.grid(row=2, column=1, padx=5, pady=5)

        save_button = tk.Button(settings_window, text="Save", command=lambda: self.save_settings(entries_var.get(), refresh_var.get(), format_var.get()), bg=self.button_bg, fg=self.font_color, font=font_style)
        save_button.grid(row=3, column=0, columnspan=2, padx=5, pady=5)
    
    def save_settings(self, entries_per_feed, refresh_interval_mins, display_format):
        config = configparser.ConfigParser()
        config.read("config.ini")

        config.set("FeedSettings", "entries_per_feed", str(entries_per_feed))
        config.set("FeedSettings", "refresh_interval_mins", str(refresh_interval_mins))
        config.set("FeedSettings", "display_format", display_format)

        with open("config.ini", "w") as configfile:
            config.write(configfile)

        self.entries_per_feed = entries_per_feed
        self.refresh_interval_mins = refresh_interval_mins
        self.display_format = display_format

        self.refresh_feeds()

    def load_config(self):
        try:
            config_path = os.path.join("C:\\", "SCOUT-2", "config.ini")
            config = configparser.ConfigParser()
            config.read(config_path)

            self.font_family = config.get("Font", "family", fallback="MS Sans Serif")
            self.font_size = config.getfloat("Font", "size", fallback=1.1)
            self.font_color = config.get("Font", "color", fallback="#ffffff")

            self.window_bg = config.get("Colors", "window_bg", fallback="#000000")
            self.spinbox_bg = config.get("Colors", "spinbox_bg", fallback="#808080")
            self.button_bg = config.get("Colors", "button_bg", fallback="#696969")

            style = ttk.Style()
            font_style = (self.font_family, int(self.font_size * 10))

            style.configure("CustomButton.TButton",
                            background=self.button_bg,
                            foreground=self.font_color,
                            font=font_style,
                            borderwidth=0,
                            focusthickness=0,
                            highlightthickness=0)
            style.map("CustomButton.TButton",
                    background=[("active", self.button_bg), ("disabled", self.button_bg)],
                    foreground=[("active", self.font_color), ("disabled", self.font_color)])

        except Exception as e:
            logger.exception("Error occurred while loading configuration.")
            messagebox.showerror("Configuration Error", "Failed to load configuration. Using default values.")
        
    def create_widgets(self):
        try:
            font_style = (self.font_family, int(self.font_size * 10))
            self.master.configure(bg=self.window_bg)

            style = ttk.Style()
            style.configure("TLabel", background=self.window_bg, foreground=self.font_color, font=font_style)
            style.configure("TButton", background=self.button_bg, foreground=self.font_color, font=font_style)

            settings_frame = tk.Frame(self.master, bg=self.window_bg)
            settings_frame.grid(row=0, column=0, columnspan=4, padx=5, pady=5, sticky=tk.E)

            self.settings_button = tk.Button(settings_frame, text="Settings", command=self.open_settings, bg=self.button_bg, fg=self.font_color, font=font_style)
            self.settings_button.pack(side=tk.RIGHT)

            self.feed_url_label = ttk.Label(self.master, text="Feed URL:")
            self.feed_url_label.grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)

            self.feed_url_entry = tk.Entry(self.master, width=40, bg="#C0C0C0", fg="black", font=font_style)
            self.feed_url_entry.grid(row=1, column=1, padx=5, pady=5)

            self.category_label = ttk.Label(self.master, text="Category:")
            self.category_label.grid(row=2, column=0, padx=5, pady=5, sticky=tk.W)

            self.category_entry = tk.Entry(self.master, width=40, bg="#C0C0C0", fg="black", font=font_style)
            self.category_entry.grid(row=2, column=1, padx=5, pady=5)

            self.add_feed_button = tk.Button(self.master, text="Add Feed", command=self.add_feed, bg=self.button_bg, fg=self.font_color, font=font_style)
            self.add_feed_button.grid(row=1, column=2, rowspan=2, padx=5, pady=5)

            self.feeds_listbox = tk.Listbox(self.master, width=70, font=font_style, bg=self.window_bg, fg=self.font_color, exportselection=False, selectmode=tk.SINGLE)
            self.feeds_listbox.grid(row=3, column=0, columnspan=4, padx=5, pady=5)
            self.feeds_listbox.bind("<Button-1>", self.on_feed_click)

            button_frame = tk.Frame(self.master, bg=self.window_bg)
            button_frame.grid(row=4, column=0, columnspan=4, padx=5, pady=5, sticky=tk.E)

            self.start_feed_button = tk.Button(button_frame, text="Start Feed", command=self.start_feed, bg=self.button_bg, fg=self.font_color, font=font_style, state=tk.DISABLED)
            self.start_feed_button.pack(side=tk.RIGHT, padx=(0, 5))

            self.remove_feed_button = tk.Button(button_frame, text="Remove Feed", command=self.remove_feed, bg=self.button_bg, fg=self.font_color, font=font_style, state=tk.DISABLED)
            self.remove_feed_button.pack(side=tk.RIGHT)

            self.entries_listbox = tk.Listbox(self.master, width=70, font=font_style, bg=self.window_bg, fg=self.font_color, exportselection=False, selectmode=tk.SINGLE)
            self.entries_listbox.grid(row=5, column=0, columnspan=4, padx=5, pady=5)
            self.entries_listbox.bind("<Button-1>", self.on_entry_click)

            entry_button_frame = tk.Frame(self.master, bg=self.window_bg)
            entry_button_frame.grid(row=6, column=0, columnspan=4, padx=5, pady=5, sticky=tk.E)

            self.show_entry_button = tk.Button(entry_button_frame, text="Show Entry Details", command=self.show_entry_details, bg=self.button_bg, fg=self.font_color, font=font_style, state=tk.DISABLED)
            self.show_entry_button.pack(side=tk.RIGHT, padx=(0, 5))

            self.remove_entry_button = tk.Button(entry_button_frame, text="Remove Entry", command=self.remove_entry, bg=self.button_bg, fg=self.font_color, font=font_style, state=tk.DISABLED)
            self.remove_entry_button.pack(side=tk.RIGHT)

            self.entry_details_text = tk.Text(self.master, width=70, height=10, font=font_style, bg=self.window_bg, fg=self.font_color, state='disabled', cursor='arrow')
            self.entry_details_text.grid(row=7, column=0, columnspan=4, padx=5, pady=5)
            self.entry_details_text.bind('<Control-c>', self.copy_selection)
            self.entry_details_text.bind('<Button-3>', self.show_text_context_menu)

            self.feed_url_entry.bind('<Button-3>', self.show_context_menu)
            self.category_entry.bind('<Button-3>', self.show_context_menu)

            self.refresh_feeds()
        except Exception as e:
            logger.exception("Error occurred while creating widgets.")
            messagebox.showerror("Widget Creation Error", "Failed to create widgets.")
            
    def on_feed_click(self, event):
        self.start_feed_button.config(state=tk.NORMAL)
        self.remove_feed_button.config(state=tk.NORMAL)

    def on_entry_click(self, event):
        self.show_entry_button.config(state=tk.NORMAL)
        self.remove_entry_button.config(state=tk.NORMAL)

    def remove_entry(self):
        selected_entry = self.entries_listbox.get(tk.ACTIVE)
        if selected_entry:
            feed_url = self.feeds_listbox.get(tk.ACTIVE).split(" - ")[0]
            self.rss_feed_reader.remove_entry(feed_url, selected_entry)
            self.entries_listbox.delete(tk.ACTIVE)
            self.entry_details_text.delete(1.0, tk.END)
            self.show_entry_button.config(state=tk.DISABLED)
            self.remove_entry_button.config(state=tk.DISABLED)
        else:
            messagebox.showerror("Error", "Please select an entry to remove.")

    def on_url_hover(self, event):
        self.entry_details_text.tag_config("url", underline=True)

    def on_url_leave(self, event):
        self.entry_details_text.tag_config("url", underline=False)

    def show_entry_details(self):
        selected_entry = self.entries_listbox.get(tk.ACTIVE)
        if selected_entry:
            feed_url = self.feeds_listbox.get(tk.ACTIVE).split(" - ")[0]
            entries = self.rss_feed_reader.get_feed_entries(feed_url)
            for entry in entries:
                if entry.title == selected_entry:
                    entry_details = self.rss_feed_reader.get_entry_details(entry)
                    self.entry_details_text.configure(state='normal')  # Enable the widget
                    self.entry_details_text.delete(1.0, tk.END)
                    self.entry_details_text.insert(tk.END, f"Title: {entry_details['title']}\n\n")
                    
                    # Insert the "Link:" text
                    self.entry_details_text.insert(tk.END, "Link: ")
                    
                    # Insert the URL with lighter blue text and tag it as "url"
                    url_start = self.entry_details_text.index(tk.END)
                    self.entry_details_text.insert(tk.END, entry_details['link'], "url")
                    url_end = self.entry_details_text.index(tk.END)
                    self.entry_details_text.tag_config("url", foreground="lightblue")
                    
                    # Bind hover events to the URL
                    self.entry_details_text.tag_bind("url", "<Enter>", self.on_url_hover)
                    self.entry_details_text.tag_bind("url", "<Leave>", self.on_url_leave)
                    
                    # Bind a click event to the URL
                    self.entry_details_text.tag_bind("url", "<Button-1>", lambda e: self.open_url(entry_details['link']))
                    
                    # Insert a newline after the URL
                    self.entry_details_text.insert(tk.END, "\n\n")
                    
                    self.entry_details_text.insert(tk.END, f"Published: {entry_details['published']}\n\n")
                    self.entry_details_text.insert(tk.END, f"Summary: {entry_details['summary']}")
                    self.entry_details_text.configure(state='disabled')  # Disable the widget
                    break
        else:
            messagebox.showerror("Error", "Please select an entry to show details.")
            
    def start_feed(self):
        selected_feed = self.feeds_listbox.get(tk.ACTIVE)
        if selected_feed:
            feed_url = selected_feed.split(" - ")[0]
            entries = self.rss_feed_reader.get_feed_entries(feed_url)
            self.entries_listbox.delete(0, tk.END)
            for entry in entries:
                self.entries_listbox.insert(tk.END, entry.title)
        else:
            messagebox.showerror("Error", "Please select a feed to start.")
        
    def add_feed(self):
        try:
            feed_url = self.feed_url_entry.get()
            category = self.category_entry.get()

            if not feed_url:
                messagebox.showerror("Error", "Please enter a feed URL.")
                return

            self.rss_feed_reader.add_feed(feed_url, category)
            self.refresh_feeds()
            self.feed_url_entry.delete(0, tk.END)
            self.category_entry.delete(0, tk.END)
            self.save_feeds()
        except RSSFeedReaderError as e:
            logger.exception("Error occurred while adding feed.")
            messagebox.showerror("Error", str(e))
        except Exception as e:
            logger.exception("Unexpected error occurred while adding feed.")
            messagebox.showerror("Error", "An unexpected error occurred.")

    def remove_feed(self):
        try:
            selected_feed = self.feeds_listbox.get(tk.ACTIVE)

            if not selected_feed:
                messagebox.showerror("Error", "Please select a feed to remove.")
                return

            feed_url = selected_feed.split(" - ")[0]

            self.rss_feed_reader.remove_feed(feed_url)
            self.save_feeds()
            self.refresh_feeds()
        except RSSFeedReaderError as e:
            logger.exception("Error occurred while removing feed.")
            messagebox.showerror("Error", str(e))
        except Exception as e:
            logger.exception("Unexpected error occurred while removing feed.")
            messagebox.showerror("Error", "An unexpected error occurred.")

    def refresh_feeds(self):
        try:
            self.feeds_listbox.delete(0, tk.END)
            self.entries_listbox.delete(0, tk.END)
            self.entry_details_text.delete(1.0, tk.END)

            feeds = self.rss_feed_reader.get_feeds()
            for feed in feeds:
                self.feeds_listbox.insert(tk.END, f"{feed.url} - {feed.category}")

            # Refresh feeds periodically based on the refresh interval
            self.master.after(self.refresh_interval_mins * 60000, self.refresh_feeds)
        except Exception as e:
            logger.exception("Error occurred while refreshing feeds.")
            messagebox.showerror("Error", "An error occurred while refreshing feeds.")

    def load_feeds(self):
        try:
            config_path = os.path.join("C:\\", "SCOUT-2", "feeds.json")
            if os.path.exists(config_path):
                with open(config_path, "r") as file:
                    feed_data = json.load(file)
                    for feed in feed_data:
                        self.rss_feed_reader.add_feed(feed["url"], feed["category"])
        except Exception as e:
            logger.exception("Error occurred while loading feeds.")

    def on_feed_select(self, event):
        try:
            selected_feed = self.feeds_listbox.get(tk.ACTIVE)

            if not selected_feed:
                return

            feed_url = selected_feed.split(" - ")[0]

            entries = self.rss_feed_reader.get_feed_entries(feed_url)
            self.entries_listbox.delete(0, tk.END)

            for entry in entries:
                self.entries_listbox.insert(tk.END, entry.title)

            self.entries_listbox.bind("<<ListboxSelect>>", self.on_entry_select)
        except RSSFeedReaderError as e:
            logger.exception("Error occurred while selecting feed.")
            messagebox.showerror("Error", str(e))
        except Exception as e:
            logger.exception("Unexpected error occurred while selecting feed.")
            messagebox.showerror("Error", "An unexpected error occurred.")

    def on_entry_select(self, event):
        try:
            selected_entry = self.entries_listbox.get(tk.ACTIVE)

            if not selected_entry:
                return

            feed_url = self.feeds_listbox.get(tk.ACTIVE).split(" - ")[0]
            entries = self.rss_feed_reader.get_feed_entries(feed_url)

            for entry in entries:
                if entry.title == selected_entry:
                    entry_details = self.rss_feed_reader.get_entry_details(entry)
                    self.entry_details_text.delete(1.0, tk.END)
                    self.entry_details_text.insert(tk.END, f"Title: {entry_details['title']}\n\n")
                    self.entry_details_text.insert(tk.END, f"Link: {entry_details['link']}\n\n")
                    self.entry_details_text.insert(tk.END, f"Published: {entry_details['published']}\n\n")
                    self.entry_details_text.insert(tk.END, f"Summary: {entry_details['summary']}")
                    break
        except RSSFeedReaderError as e:
            logger.exception("Error occurred while selecting entry.")
            messagebox.showerror("Error", str(e))
        except Exception as e:
            logger.exception("Unexpected error occurred while selecting entry.")
            messagebox.showerror("Error", "An unexpected error occurred.")

    def save_feeds(self):
        try:
            feeds = self.rss_feed_reader.get_feeds()
            feed_data = []
            for feed in feeds:
                feed_data.append({"url": feed.url, "category": feed.category})

            config_path = os.path.join("C:\\", "SCOUT-2", "feeds.json")
            with open(config_path, "w") as file:
                json.dump(feed_data, file)
        except Exception as e:
            logger.exception("Error occurred while saving feeds.")

    def copy_selection(self, event):
        widget = event.widget
        if isinstance(widget, tk.Listbox):
            selection = widget.curselection()
            if selection:
                index = selection[0]
                data = widget.get(index)
                self.master.clipboard_clear()
                self.master.clipboard_append(data)
        elif isinstance(widget, tk.Text):
            try:
                selected_text = widget.get(tk.SEL_FIRST, tk.SEL_LAST)
                self.master.clipboard_clear()
                self.master.clipboard_append(selected_text)
            except tk.TclError:
                pass

    def show_context_menu(self, event):
        widget = event.widget
        if isinstance(widget, tk.Entry):
            menu = tk.Menu(self.master, tearoff=0)
            menu.add_command(label="Paste", command=lambda: widget.event_generate('<<Paste>>'))
            menu.post(event.x_root, event.y_root)            

    def show_text_context_menu(self, event):
        widget = event.widget
        if isinstance(widget, tk.Text):
            menu = tk.Menu(self.master, tearoff=0)
            menu.add_command(label="Copy", command=lambda: self.copy_selection(event))
            menu.post(event.x_root, event.y_root)

if __name__ == "__main__":
    root = tk.Tk()
    app = RSSFeedReaderUI(root)
    root.mainloop()