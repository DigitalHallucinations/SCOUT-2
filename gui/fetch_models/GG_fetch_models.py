#gui/fetch_models/GG_fetch_models.py

import google.generativeai as genai 
from modules.logging.logger import setup_logger

logger = setup_logger('GG_fetch_models.py') 

async def fetch_models_google(chat_log):
    try:
        # Enable editing (if needed)
        chat_log.setReadOnly(False)

        # Insert text into the chat log
        chat_log.append("Available models:\n")
        models = genai.list_models()

        for model in models:
            model_name = model.name
            chat_log.append(f"{model_name}\n")
            logger.info(model_name)

        # Disable editing again (if needed)
        chat_log.setReadOnly(True)

        # Scroll to the bottom of the chat log
        scrollbar = chat_log.verticalScrollBar()
        scrollbar.setValue(scrollbar.maximum())
    except Exception as e:
        logger.error("Error fetching models from Google", exc_info=True)


async def fetch_model_details(chat_log, model_name):
    try:
        # Fetch the model details using the genai API
        model = genai.get_model(model_name)

        # Enable editing in the QTextEdit
        chat_log.setReadOnly(False)

        # Append the model details to the QTextEdit
        chat_log.append(f"Model {model_name} details:\n")
        chat_log.append(f"{model}\n")

        # Log the details
        logger.info(f"Model {model_name} details: {model}")

        # Disable editing in the QTextEdit
        chat_log.setReadOnly(True)

        # Scroll to the bottom of the QTextEdit
        scrollbar = chat_log.verticalScrollBar()
        scrollbar.setValue(scrollbar.maximum())
    except Exception as e:
        logger.error(f"Failed to fetch details for model {model_name}", exc_info=True)
