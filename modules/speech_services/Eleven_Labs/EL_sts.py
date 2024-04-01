#modules/speech_services/EL_sts.py
#This file converts one voice to another

import requests  
import json  
import logging
from logging.handlers import RotatingFileHandler
import os
from dotenv import load_dotenv

logger = logging.getLogger('EL_sts.py')

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


load_dotenv()

XI_API_KEY = os.getenv("XI_API_KEY")
if XI_API_KEY is None:
    raise ValueError("API key not found. Please set the XI_API_KEY environment variable.")

headers = {
    "Accept": "application/json",
    "xi-api-key": XI_API_KEY
}

CHUNK_SIZE = 1024  # Size of chunks to read/write at a time
VOICE_ID = "<voice-id>"  # ID of the voice model to use
AUDIO_FILE_PATH = "<path>"  # Path to the input audio file
OUTPUT_PATH = "output.mp3"  # Path to save the output audio file

sts_url = f"https://api.elevenlabs.io/v1/speech-to-speech/{VOICE_ID}/stream"

# Note: voice settings are converted to a JSON string
data = {
    "model_id": "eleven_english_sts_v2",
    "voice_settings": json.dumps({
        "stability": 0.5,
        "similarity_boost": 0.8,
        "style": 0.0,
        "use_speaker_boost": True
    })
}

files = {
    "audio": open(AUDIO_FILE_PATH, "rb")
}

response = requests.post(sts_url, headers=headers, data=data, files=files, stream=True)

if response.ok:
    with open(OUTPUT_PATH, "wb") as f:
        for chunk in response.iter_content(chunk_size=CHUNK_SIZE):
            f.write(chunk)
    logging.info("Audio stream saved successfully.")
else:
    logging.info(response.text)