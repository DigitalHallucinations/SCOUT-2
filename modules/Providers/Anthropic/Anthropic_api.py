# gui/Anthropic/Anthropic_api.py

import anthropic
import os
import logging
from dotenv import load_dotenv
from logging.handlers import RotatingFileHandler

logger = logging.getLogger('Anthropic_api.py')
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