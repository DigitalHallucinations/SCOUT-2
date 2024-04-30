# modules/speech_services/Eleven_Labs/tts.py

# Description: Text to speech module using Eleven Labs

import pygame
import threading
import os
import requests
import re
import os
from dotenv import load_dotenv
from modules.logging.logger import setup_logger

logger = setup_logger('tts.py')

CHUNK_SIZE = 1024 
OUTPUT_PATH = "assets/SCOUT/tts_mp3/output.mp3"  

_use_tts = False
VOICE_IDS = []

def play_audio(filename):
    logger.info(f"Playing audio file: {filename}")
    pygame.mixer.init()
    pygame.mixer.music.load(filename)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)
    logger.info("Audio playback finished.")

def contains_code(text: str) -> bool:
    """Check if the given text contains code"""
    logger.debug(f"Checking if text contains code: {text}")
    return "<code>" in text

def get_voices():
    global VOICE_IDS
    load_dotenv()
    XI_API_KEY = os.getenv("XI_API_KEY")
    if XI_API_KEY is None:
        logger.error("API key not found. Please set the XI_API_KEY environment variable.")
        raise ValueError("API key not found. Please set the XI_API_KEY environment variable.")

    url = "https://api.elevenlabs.io/v1/voices"
    headers = {
        "Accept": "application/json",
        "xi-api-key": XI_API_KEY,
        "Content-Type": "application/json"
    }

    logger.info("Fetching voices from Eleven Labs API...")
    response = requests.get(url, headers=headers)
    data = response.json()

    for voice in data['voices']:
        VOICE_IDS.append(voice['voice_id'])

    if VOICE_IDS:
        logger.info(f"Found {len(VOICE_IDS)} voices.")
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
            logger.error("API key not found. Please set the XI_API_KEY environment variable.")
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

        logger.info(f"Sending TTS request to Eleven Labs API with text: {text}")
        response = requests.post(tts_url, headers=headers, json=data, stream=True)

        if response.ok:
            logger.info("TTS response received successfully.")
            with open(OUTPUT_PATH, "wb") as f:
                for chunk in response.iter_content(chunk_size=CHUNK_SIZE):
                    f.write(chunk)
            logger.info(f"Audio stream saved successfully to {OUTPUT_PATH}.")
            threading.Thread(target=play_audio, args=(OUTPUT_PATH,)).start()
        else:
            logger.error(f"Error during TTS: {response.text}")
    except Exception as e:
        logger.error(f"Error during TTS: {e}")

def set_voice(voice_id):
    global VOICE_IDS
    if voice_id in VOICE_IDS:
        VOICE_IDS[0] = voice_id
        logger.info(f"Voice set to: {voice_id}")
    else:
        logger.error(f"Voice ID {voice_id} not found in the list of available voices.")

def get_voice():
    logger.info(f"Current voice ID: {VOICE_IDS[0]}")
    return VOICE_IDS[0]

def set_tts(value):
    global _use_tts
    _use_tts = value
    logger.info(f"TTS set to: {_use_tts}")

def get_tts():
    logger.info(f"TTS status: {_use_tts}")
    return _use_tts

async def tts(text):
    await text_to_speech(text)