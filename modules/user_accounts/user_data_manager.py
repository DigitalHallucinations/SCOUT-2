# modules/user_accounts/user_data_manager.py

import os
import json
import re
import logging
from logging.handlers import RotatingFileHandler

logger = logging.getLogger('user_data_manager.py')

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

class UserDataManager:
    def __init__(self, user):
        self.user = user
        self.profile = self.get_profile_text
        self.emr = self.get_emr
        logging.info(f"UDM instantiated with user: {self.user}, {self.profile}")

    def get_profile(self):
        logging.info("Entering get_profile() method")
        try:
            profile_path = os.path.abspath(os.path.join(
                os.path.dirname(__file__), '..', '..', 'modules', 'user_accounts', 'user_profiles',
                f"{self.user}.json"
            ))

            if not os.path.exists(profile_path):
                logging.error(f"Profile file does not exist: {profile_path}")
                return {}

            with open(profile_path, 'r', encoding='utf-8') as file:
                profile = json.load(file)
                logging.info("Profile found")
                return profile

        except Exception as e:
            logging.error(f"Error loading profile: {e}")
            return {}
        
    def format_profile_as_text(self, profile_json):
        logging.info("Formatting profile.")
        profile_lines = []
        for key, value in profile_json.items():
            line = f"{key}: {value}"
            profile_lines.append(line)
        return '\n'.join(profile_lines)
    
    def get_profile_text(self):
        logging.info("Entering get_profile_text() method")
        profile_json = self.get_profile()
        return self.format_profile_as_text(profile_json)
    
    def get_emr(self):
        logging.info("Getting EMR.")
        script_dir = os.path.dirname(os.path.abspath(__file__))

        EMR_filename = f"{self.user}_emr.txt"
        relative_EMR_path = os.path.join(script_dir, '..', '..', 'modules', 'user_accounts', 'user_profiles', EMR_filename)
        
        EMR_path = os.path.abspath(relative_EMR_path)

        logging.info(f"EMR path: {EMR_path}")

        if not os.path.exists(EMR_path):
            logging.error(f"EMR file does not exist: {EMR_path}")
            return ""
        
        try:
            with open(EMR_path, 'r', encoding='utf-8') as file:
                EMR = file.read()
                EMR = EMR.replace("\n", " ")
                EMR = re.sub(r'\s+', ' ', EMR)
                return EMR.strip()
        except Exception as e:
            logging.error(f"Error loading EMR: {e}")
            return ""