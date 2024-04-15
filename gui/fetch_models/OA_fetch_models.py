# guide\OpenAI\OA_gen_response.py

import aiohttp
import os
import logging
from logging.handlers import RotatingFileHandler

logger = logging.getLogger('OA_fetch_models.py') 

log_filename = 'SCOUT.log'
log_max_size = 10 * 1024 * 1024
log_backup_count = 5

rotating_handler = RotatingFileHandler(log_filename, maxBytes=log_max_size, backupCount=log_backup_count, encoding='utf-8')
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
rotating_handler.setFormatter(formatter)

stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)

logger.addHandler(rotating_handler)
logger.addHandler(stream_handler)
logger.setLevel(logging.INFO)

def adjust_logging_level(level):

    levels = {
        'DEBUG': logging.DEBUG,
        'INFO': logging.INFO,
        'WARNING': logging.WARNING,
        'ERROR': logging.ERROR,
        'CRITICAL': logging.CRITICAL
    }
    
    logger.setLevel(levels.get(level, logging.WARNING))

async def fetch_models_openai(chat_log):
    api_key = os.getenv("OPENAI_API_KEY")
    headers = {"Authorization": f"Bearer {api_key}"}
    url = "https://api.openai.com/v1/models"

    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as response:
            if response.status == 200:
                models = await response.json()
                chat_log.configure(state="normal")
                chat_log.insert("end", "Available models:\n", "timestamp")
                for model in models["data"]:
                    chat_log.insert("end", f"{model['id']}\n")
                chat_log.configure(state="disabled")
                chat_log.yview("end")
            else:
                logging.error(f"Error: {response.status}")
                