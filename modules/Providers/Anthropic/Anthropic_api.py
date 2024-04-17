# gui/Anthropic/Anthropic_api.py

import anthropic
import os
from dotenv import load_dotenv
from modules.logging.logger import setup_logger

logger = setup_logger('Anthropic_api.py')


load_dotenv()

Anthropic_API_KEY = os.getenv('Anthropic_API_KEY')
if not Anthropic_API_KEY:
    logger.critical("Anthropic_API_KEY is not set. Please check environment variables.")
    raise EnvironmentError("Anthropic_API_KEY is not set. Please check environment variables.")

class AnthropicAPI:
    def __init__(self):
        self.client = anthropic.Anthropic(
        api_key=Anthropic_API_KEY,
        )

    async def generate_conversation(self, data):
        try:
            response = self.client.messages.create(**data)
            logger.info("response from Anthropic API.")
            return response
         
        except Exception as e:
            logger.error(f"An error occurred while generating conversation: {e}")
            return None    