# modules/EL_tts.py
# Description: Text to speech module using Eleven Labs

import pygame
import threading
import logging
import os
import requests
import re
from logging.handlers import RotatingFileHandler
import os
from dotenv import load_dotenv

logger = logging.getLogger('EL_tts.py')

log_filename = 'SCOUT.log'
log_max_size = 10 * 1024 * 1024  # 10 MB
log_backup_count = 5

rotating_handler = RotatingFileHandler(log_filename, maxBytes=log_max_size, backupCount=log_backup_count, encoding='utf-8')
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
rotating_handler.setFormatter(formatter)

logger = logging.getLogger('')
for handler in logger.handlers[:]:
    logger.removeHandler(handler)

logger.addHandler(rotating_handler)
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

CHUNK_SIZE = 1024  # Size of chunks to read/write at a time
OUTPUT_PATH = "assets/SCOUT/tts_mp3/output.mp3"  

_use_tts = False
VOICE_IDS = []

def play_audio(filename):
    pygame.mixer.init()
    pygame.mixer.music.load(filename)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)

def contains_code(text: str) -> bool:
    """Check if the given text contains code"""
    return "<code>" in text

def get_voices():
    global VOICE_IDS
    load_dotenv()
    XI_API_KEY = os.getenv("XI_API_KEY")
    if XI_API_KEY is None:
        raise ValueError("API key not found. Please set the XI_API_KEY environment variable.")

    url = "https://api.elevenlabs.io/v1/voices"
    headers = {
        "Accept": "application/json",
        "xi-api-key": XI_API_KEY,
        "Content-Type": "application/json"
    }

    response = requests.get(url, headers=headers)
    data = response.json()

    for voice in data['voices']:
        VOICE_IDS.append(voice['voice_id'])

    if VOICE_IDS:
        set_voice(VOICE_IDS[0])
    else:
        logger.error("No voices found. Please check your Eleven Labs API key.")

async def text_to_speech(text):
    try:
        if not _use_tts:
            logger.info("TTS is turned off.")
            return

        if contains_code(text):
            logger.info("Skipping TTS as the text contains code.")
            text_without_code = re.sub(r"`[^`]*`", "", text)
            text = text_without_code

        load_dotenv()
        XI_API_KEY = os.getenv("XI_API_KEY")
        if XI_API_KEY is None:
            raise ValueError("API key not found. Please set the XI_API_KEY environment variable.")

        tts_url = f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_IDS[0]}/stream"

        headers = {
            "Accept": "application/json",
            "xi-api-key": XI_API_KEY
        }

        data = {
            "text": text,
            "model_id": "eleven_multilingual_v2",
            "voice_settings": {
                "stability": 0.5,
                "similarity_boost": 0.8,
                "style": 0.0,
                "use_speaker_boost": True
            }
        }

        response = requests.post(tts_url, headers=headers, json=data, stream=True)

        if response.ok:
            with open(OUTPUT_PATH, "wb") as f:
                for chunk in response.iter_content(chunk_size=CHUNK_SIZE):
                    f.write(chunk)
            logger.info("Audio stream saved successfully.")
            threading.Thread(target=play_audio, args=(OUTPUT_PATH,)).start()
        else:
            logger.error(f"Error during TTS: {response.text}")
    except Exception as e:
        logger.error(f"Error during TTS: {e}")

def set_voice(voice_id):
    global VOICE_IDS
    if voice_id in VOICE_IDS:
        VOICE_IDS[0] = voice_id
    else:
        logger.error(f"Voice ID {voice_id} not found in the list of available voices.")

def get_voice():
    return VOICE_IDS[0]

def set_tts(value):
    global _use_tts
    _use_tts = value
    logger.info("TTS set to: %s", _use_tts)

def get_tts():
    return _use_tts