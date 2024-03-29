# modules\GglCldSvcs\tts.py
# Description: Text to speech module

import pygame 
import threading
import logging
import os
import re

from datetime import datetime
from google.cloud import texttospeech
import logging

from logging.handlers import RotatingFileHandler

log_filename = 'SCOUT.log'
log_max_size = 10 * 1024 * 1024  # 10 MB
log_backup_count = 5

# Create a rotating file handler with UTF-8 encoding
rotating_handler = RotatingFileHandler(log_filename, maxBytes=log_max_size, backupCount=log_backup_count, encoding='utf-8')
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
rotating_handler.setFormatter(formatter)

# Remove existing handlers if present
logger = logging.getLogger('')
for handler in logger.handlers[:]:
    logger.removeHandler(handler)

# Add the rotating file handler to the logger
logger.addHandler(rotating_handler)
logger.setLevel(logging.INFO)  # Set the default logging level

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

VOICE = texttospeech.VoiceSelectionParams(
    language_code="en-US",
    name="en-US-Wavenet-A"
)

_use_tts = False

def play_audio(filename):
    pygame.mixer.init()

    pygame.mixer.music.load(filename)

    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)  

def contains_code(text: str) -> bool:
    """Check if the given text contains code"""
    return "<code>" in text

async def text_to_speech(text):
    try:
        if not _use_tts:
            logger.info("TTS is turned off.")
            return

        if contains_code(text):
            logger.info("Skipping TTS as the text contains code.")
            text_without_code = re.sub(r"`[^`]*`", "", text)
            text = text_without_code

        client = texttospeech.TextToSpeechClient()

        synthesis_input = texttospeech.SynthesisInput(text=text)

        global VOICE
        voice = VOICE

        logger.info(f"Using voice: {voice}")  

        audio_config = texttospeech.AudioConfig(
            audio_encoding=texttospeech.AudioEncoding.MP3
        )

        response = client.synthesize_speech(
            input=synthesis_input, voice=voice, audio_config=audio_config
        )

       
        base_dir = os.getcwd()  
        filename = os.path.join(base_dir, "assets", "SCOUT", "tts_mp3", f"output_{datetime.now().strftime('%Y%m%d%H%M%S')}.mp3")
        
        with open(filename, "wb") as out:
            out.write(response.audio_content)
            print(f'Audio content written to file "{filename}"')

        threading.Thread(target=play_audio, args=(filename,)).start()
    except Exception as e:
        logger.error(f"Error during TTS: {e}")

def set_voice(voice_name):
    global VOICE
    language_code = voice_name.split('-')[0] + '-' + voice_name.split('-')[1]
    VOICE = texttospeech.VoiceSelectionParams(
        language_code=language_code,
        name=voice_name,
    )

def get_voice():
    return VOICE

def set_tts(value):
    global _use_tts
    _use_tts = value
    logger.info("TTS set to: %s", _use_tts)

def get_tts():
    return _use_tts
