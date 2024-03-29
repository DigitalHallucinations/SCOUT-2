# gui/Avatar/avatar.py

import os
import tkinter as tk
from PIL import ImageTk, Image
import vlc
import logging
from logging.handlers import RotatingFileHandler

logger = logging.getLogger('avatar.py')

log_filename = 'SCOUT.log'
log_max_size = 10 * 1024 * 1024  # 10 MB
log_backup_count = 5

# Create rotating file handler for file logging
rotating_handler = RotatingFileHandler(log_filename, maxBytes=log_max_size, backupCount=log_backup_count, encoding='utf-8')
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
rotating_handler.setFormatter(formatter)

# Create stream handler for console logging
stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)

# Attach handlers to the logger
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

class MediaComponent(tk.Toplevel):
    def __init__(self, master=None):
        super().__init__(master, bg="#000000")
        self.title("Media Component")
        self.master = master
        self.settings_window = None
        
        img = Image.open(os.path.join("assets", "SCOUT", "SCOUT1.png"))
        self.image = ImageTk.PhotoImage(img)
        self.image_label = tk.Label(self, image=self.image)
        self.image_label.pack()
        self.image_label.bind("<Button-1>", lambda event: self.play_video() if self.master.user else None)

    def play_video(self):
        logger.info("Play video function called")
        video_path = os.path.join("assets", "SCOUT", "avatar_videos", "SCOUT_intro.mp4")
        self.instance = vlc.Instance()

        # Create a new frame for the video player
        self.video_frame = tk.Frame(self)
        self.video_frame.place(x=0, y=0, relwidth=1, relheight=1)

        # Create a new VLC player
        self.player = self.instance.media_player_new()

        # Pass the 'window id' of the video frame to the player, to play in
        if os.name == "nt":  # for Windows
            self.player.set_hwnd(self.video_frame.winfo_id())
        else:  # for Linux
            self.player.set_xwindow(self.video_frame.winfo_id())

        # Stop the player before starting a new video
        self.player.stop()

        self.player.set_mrl(video_path)
        self.player.play()

        # Add an event manager to handle the end of the video
        event_manager = self.player.event_manager()
        event_manager.event_attach(vlc.EventType.MediaPlayerEndReached, self.stop_video)

    def stop_video(self, event=None):
        logger.info("Stop video function called")
        self.player.stop()
        self.player.release()
        self.video_frame.place_forget()  

        if self.winfo_exists():  
            self.image_label = tk.Label(self, image=self.image)
            self.image_label.pack()

        logger.info("Stop video function finished")

