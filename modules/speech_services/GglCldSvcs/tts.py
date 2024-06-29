# modules/GglCldSvcs/tts.py
# Description: Text to speech module using Google Cloud Text-to-Speech

import pygame
import threading
import os
import re
from datetime import datetime
from google.cloud import texttospeech
from modules.logging.logger import setup_logger

logger = setup_logger('tts.py')

VOICE = texttospeech.VoiceSelectionParams(
    language_code="en-US",
    name="en-US-Wavenet-A"
)

CHUNK_SIZE = 1024
OUTPUT_PATH = "assets/SCOUT/tts_mp3/output.mp3"

_use_tts = False

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

async def text_to_speech(text):
    try:
        if not _use_tts:
            logger.info("TTS is turned off.")
            return

        if contains_code(text):
            logger.info("Skipping TTS as the text contains code.")
            text_without_code = re.sub(r"`[^`]*`", "", text)
            text = text_without_code

        try:
            client = texttospeech.TextToSpeechClient()
        except Exception as e:
            logger.error(f"Failed to initialize TextToSpeechClient: {e}")
            return

        synthesis_input = texttospeech.SynthesisInput(text=text)
        global VOICE
        voice = VOICE

        logger.info(f"Using voice: {voice}")

        audio_config = texttospeech.AudioConfig(
            audio_encoding=texttospeech.AudioEncoding.MP3
        )

        try:
            response = client.synthesize_speech(
                input=synthesis_input, voice=voice, audio_config=audio_config
            )
        except Exception as e:
            logger.error(f"Error during TTS synthesis: {e}")
            return

        base_dir = os.getcwd()
        filename = os.path.join(base_dir, OUTPUT_PATH)
        
        with open(filename, "wb") as out:
            out.write(response.audio_content)
            logger.info(f'Audio content written to file "{filename}"')

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
    logger.info(f"Voice set to: {voice_name}")

def get_voice():
    logger.info(f"Current voice: {VOICE}")
    return VOICE

def get_voices():
    client = texttospeech.TextToSpeechClient()
    voices = []
    try:
        response = client.list_voices()
        for voice in response.voices:
            for language_code in voice.language_codes:
                voices.append({
                    'name': voice.name,
                    'language': language_code,
                    'ssml_gender': texttospeech.SsmlVoiceGender(voice.ssml_gender).name,
                    'natural_sample_rate_hertz': voice.natural_sample_rate_hertz,
                })
        logger.info(f"Found {len(voices)} voices.")
    except Exception as e:
        logger.error(f"Error while getting voices: {e}")
    return voices

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
    
    # Set the desired voice
    set_voice("en-US-Wavenet-A")
    
    # Enable TTS
    set_tts(True)
    
    # Call the text_to_speech function
    await text_to_speech(test_text)

if __name__ == "__main__":
    import asyncio
    asyncio.run(test_tts())
