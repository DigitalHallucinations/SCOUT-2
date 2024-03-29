#gui\Mistral\Mistral_api.py

import aiohttp
from dotenv import load_dotenv
import os
import logging

from logging.handlers import RotatingFileHandler

logger = logging.getLogger('Mistral_api.py')

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

load_dotenv()

api_key = os.getenv("Mistral_API_KEY")
if api_key is None:
    raise ValueError("API key not found. Please set the Mistral_API_KEY environment variable.")

API_ENDPOINT = "https://api.mistral.ai/v1/chat/completions"

class MistralAPI:
    def __init__(self):
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}",
        }

    async def generate_conversation(self, data):
        """
        Used by OA_gen_response.py for communication of user interactions with the OpenAI API.
        """
        async with aiohttp.ClientSession() as session:
            async with session.post(API_ENDPOINT, headers=self.headers, json=data) as response:
                if response.status == 200:
                    response_data = await response.json()
                    logger.info(f"Conversation response received from API. {response}")
                    return response_data
                else:
                    error_message = await response.text()
                    logger.erroe("Error generating conversation from API: %s: %s", response.status, error_message)
                    return None

    async def generate_cognitive_background_service(self, data):
        """
        Used by ConitiveBackgroundServices.py for communication of system background interactions with the OpenAI API.
        """
        async with aiohttp.ClientSession() as session:
            async with session.post(API_ENDPOINT, headers=self.headers, json=data) as response:
                if response.status == 200:
                    response_data = await response.json()
                    logger.info("CBS response received from API.")
                    return response_data
                else:
                    error_message = await response.text()
                    logger.erroe("Error generating CBS response from API: %s: %s", response.status, error_message)
                    return None

                  