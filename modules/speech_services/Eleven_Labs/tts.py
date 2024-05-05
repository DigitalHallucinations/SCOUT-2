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
#from logger import setup_logger
logger = setup_logger('11_tts.py')

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

    voices = []
    for voice in data['voices']:
        voice_data = {
            'voice_id': voice['voice_id'],
            'name': voice['name']
        }
        voices.append(voice_data)

    if voices:
        logger.info(f"Found {len(voices)} voices.")
        return voices
    else:
        logger.error("No voices found. Please check your Eleven Labs API key.")
        return [] 
    
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

        if not VOICE_IDS:
            logger.error("No voice IDs found. Please make sure voices are loaded.")
            return

        voice_id = VOICE_IDS[0]['voice_id']
        tts_url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}/stream"
       
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

        logger.info(f"Eleven Labs API response status code: {response.status_code}")
        logger.info(f"Eleven Labs API response headers: {response.headers}")

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
        
def set_voice(voice):
    global VOICE_IDS
    for i, v in enumerate(VOICE_IDS):
        if v['name'] == voice['name'] and v['voice_id'] == voice['voice_id']:
            new_voice = {
                'voice_id': voice['voice_id'],
                'name': voice['name']
            }
            VOICE_IDS[i] = new_voice
            logger.info(f"Voice set to: {voice['name']} with voice ID: {voice['voice_id']}")
            return
    logger.error(f"Voice name {voice['name']} not found in the list of available voices.")

def load_voices():
    global VOICE_IDS
    VOICE_IDS = get_voices()
    if VOICE_IDS:
        logger.info(f"Loaded {len(VOICE_IDS)} voices.")
    else:
        logger.warning("No voices loaded.")

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

async def test_tts():
    test_text = "Hello World!"
    
    # Load the voices
    load_voices()
    
    # Set the desired voice
    test_voice = {'voice_id': 'iP95p4xoKVk53GoZ742B', 'name': 'Chris'}
    set_voice(test_voice)
    
    # Enable TTS
    set_tts(True)
    
    # Call the text_to_speech function
    await text_to_speech(test_text)

if __name__ == "__main__":
    import asyncio
    asyncio.run(test_tts())