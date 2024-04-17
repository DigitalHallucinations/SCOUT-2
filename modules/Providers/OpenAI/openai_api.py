#gui\OpenAI\openai_api.py

import aiohttp
from dotenv import load_dotenv
import os
from modules.logging.logger import setup_logger

logger = setup_logger('openai_api.py')

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
if api_key is None:
    raise ValueError("API key not found. Please set the OPENAI_API_KEY environment variable.")

API_ENDPOINT = "https://api.openai.com/v1/chat/completions"

class OpenAIAPI:
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
                    logger.info("Conversation response received from API.")
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

                  