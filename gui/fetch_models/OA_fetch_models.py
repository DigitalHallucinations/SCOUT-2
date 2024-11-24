import aiohttp
import os
from modules.logging.logger import setup_logger

logger = setup_logger('OA_fetch_models.py')

async def fetch_models_openai(chat_log):
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        logger.error("OpenAI API key is not set. Please configure the environment variable 'OPENAI_API_KEY'.")
        return

    headers = {"Authorization": f"Bearer {api_key}"}
    url = "https://api.openai.com/v1/models"

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers) as response:
                if response.status == 200:
                    models = await response.json()

                    # Enable editing in the QTextEdit
                    chat_log.setReadOnly(False)

                    # Append available models to the QTextEdit
                    chat_log.append("Available models:\n")
                    for model in models["data"]:
                        chat_log.append(f"{model['id']}\n")

                    # Disable editing in the QTextEdit
                    chat_log.setReadOnly(True)

                    # Scroll to the bottom of the QTextEdit
                    scrollbar = chat_log.verticalScrollBar()
                    scrollbar.setValue(scrollbar.maximum())
                else:
                    logger.error(f"Error fetching OpenAI models: HTTP {response.status}")
    except Exception as e:
        logger.error("An error occurred while fetching OpenAI models", exc_info=True)

                