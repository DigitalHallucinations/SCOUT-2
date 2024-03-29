# guide\Google\GG_fetch_models.py

import os
import google.generativeai as palm
import logging

logger = logging.getLogger()

async def fetch_models_google(chat_log):
    palm.configure(api_key=os.getenv("PALM_API_KEY"))

    models = palm.list_models()
    
    chat_log.configure(state="normal")
    chat_log.insert("end", "Available models:\n", "timestamp")
    for model in models:
        model_name = model.name
        chat_log.insert("end", f"{model.name}\n")
        logger.info(model_name)
    chat_log.configure(state="disabled")
    chat_log.yview("end")

async def fetch_model_details(chat_log, model_name):
    palm.configure(api_key=os.getenv("PALM_API_KEY"))

    model = palm.get_model(model_name)

    chat_log.configure(state="normal")
    chat_log.insert("end", f"Model {model_name} details:\n", "timestamp")
    chat_log.insert("end", f"{model}\n")
    logger.info(f"Model {model_name} details:")
    chat_log.configure(state="disabled")
    chat_log.yview("end")



