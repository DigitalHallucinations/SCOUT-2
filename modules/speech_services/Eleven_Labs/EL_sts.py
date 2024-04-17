#modules/speech_services/EL_sts.py

#This file converts one voice to another

import requests  
import json  
import os
from dotenv import load_dotenv
from modules.logging.logger import setup_logger

logger = setup_logger('EL_sts.py')

load_dotenv()

XI_API_KEY = os.getenv("XI_API_KEY")
if XI_API_KEY is None:
    raise ValueError("API key not found. Please set the XI_API_KEY environment variable.")

headers = {
    "Accept": "application/json",
    "xi-api-key": XI_API_KEY
}

CHUNK_SIZE = 1024  
VOICE_ID = "<voice-id>"  
AUDIO_FILE_PATH = "<path>" 
OUTPUT_PATH = "output.mp3"  

sts_url = f"https://api.elevenlabs.io/v1/speech-to-speech/{VOICE_ID}/stream"

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
    logger.info("Audio stream saved successfully.")
else:
    logger.info(response.text)