#gui/fetch_models/GG_fetch_models.py

import logging
from logging.handlers import RotatingFileHandler
import google.generativeai as genai 

logger = logging.getLogger('GG_fetch_models.py') 

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

async def fetch_models_google(chat_log):
    models = genai.list_models() 

    chat_log.configure(state="normal")
    chat_log.insert("end", "Available models:\n", "timestamp")
    for model in models:
        model_name = model.name
        chat_log.insert("end", f"{model.name}\n")
        logger.info(model_name)
    chat_log.configure(state="disabled")
    chat_log.yview("end")

async def fetch_model_details(chat_log, model_name):
    model = genai.get_model(model_name)  

    chat_log.configure(state="normal")
    chat_log.insert("end", f"Model {model_name} details:\n", "timestamp")
    chat_log.insert("end", f"{model}\n")
    logger.info(f"Model {model_name} details:")
    chat_log.configure(state="disabled")
    chat_log.yview("end")