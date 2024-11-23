# modules/Providers/Google/genai_api.py

import google.generativeai as genai
import os
from dotenv import load_dotenv
from modules.logging.logger import setup_logger

logger = setup_logger('genai_api.py')

load_dotenv()

GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
if not GOOGLE_API_KEY:
    logger.critical("GOOGLE_API_KEY is not set. Google GenAI functionality will be disabled.")
else:
    genai.configure(api_key=GOOGLE_API_KEY)

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