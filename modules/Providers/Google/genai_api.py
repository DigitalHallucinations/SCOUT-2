import google.generativeai as genai
import os
import logging
from dotenv import load_dotenv
from logging.handlers import RotatingFileHandler

# Setup logging
logger = logging.getLogger('genai_api.py')
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

GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
if not GOOGLE_API_KEY:
    logger.critical("GOOGLE_API_KEY is not set. Please check environment variables.")
    raise EnvironmentError("GOOGLE_API_KEY is not set. Please check environment variables.")

genai.configure(api_key=GOOGLE_API_KEY)

# Gemini_pro Endpoint - https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent

# List available models and check for 'generateContent' support
logger.info("Listing available models:")
for m in genai.list_models():
    if 'generateContent' in m.supported_generation_methods:
        logger.info(m.name)

class GenAIAPI:
    def __init__(self, model='gemini-pro'):
        self.model = genai.GenerativeModel(model)

    async def generate_content(self, data):
        try:
            response_data = self.model.generate_content(**data)
            if response_data:
                logger.info("Response received from GenAI API.")
                return response_data
            else:
                logger.error("No response from GenAI API.")
                return None
        except Exception as e:
            logger.error(f"Error generating response from GenAI API: {e}")
            return None

