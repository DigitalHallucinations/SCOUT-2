# guide\OpenAI\OA_gen_response.py

import aiohttp
import os
from modules.logging.logger import setup_logger

logger = setup_logger('OA_fetch_models.py') 

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
                logger.error(f"Error: {response.status}")
                