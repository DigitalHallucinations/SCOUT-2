import logging
from logging.handlers import RotatingFileHandler
import os
import re
from dotenv import load_dotenv
from modules.speech_services.GglCldSvcs import tts
from datetime import datetime
from modules.chat_history.convo_manager import ConversationManager
import google.generativeai as palm

load_dotenv()

logger = logging.getLogger('GG_gen_response.py')

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

logger.info("Application start")
logger.info("Logging system initialized")

def adjust_logging_level(level):
    old_level = logging.getLevelName(logger.level)
    levels = {
        'DEBUG': logging.DEBUG,
        'INFO': logging.INFO,
        'WARNING': logging.WARNING,
        'ERROR': logging.ERROR,
        'CRITICAL': logging.CRITICAL
    }
    new_level = levels.get(level, logging.WARNING)
    logger.setLevel(new_level)
    logger.info(f"Logging level changed from {old_level} to {level}")

GG_MODEL = "models/chat-bison-001"
PALM_API_KEY = os.getenv("PALM_API_KEY")

if not PALM_API_KEY:
    logger.critical("PALM_API_KEY is not set. Please check environment variables.")

palm.configure(api_key=PALM_API_KEY)
logger.info(f"PALM API configured with model: {GG_MODEL}")

ENABLE_NLP = False

def set_GG_model(model_name):
    global GG_MODEL
    logger.info(f"Changing GG model from {GG_MODEL} to {model_name}")
    GG_MODEL = model_name

def get_GG_model():
    return GG_MODEL

def create_data_object(current_persona, messages, temperature_var, top_p_var, top_k_var):
    context = current_persona.get("content")
    data = {
        "model": GG_MODEL,
        "context": context,  # context is the persona
        "messages": messages,
        "temperature": temperature_var,
        "top_p": top_p_var,
        "top_k": top_k_var,
    }
    logger.debug("Data object created for HTTP request")
    return data

async def generate_response(user, current_persona, message, session_id, conversation_id, temperature_var, top_p_var, top_k_var=None):
    logger.info(f"Starting response generation for user: {user}, session_id: {session_id}, conversation_id: {conversation_id}")
    
    if "name" in current_persona: 
        conversation_history = ConversationManager(user, current_persona["name"])
    else:
        conversation_history = None

    if conversation_id is None:
        raise ValueError("conversation_id cannot be None")

    if message:
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        conversation_history.add_message(user, conversation_id, "user", message, current_time)
        logger.info("New user message added to conversation history.")

    messages = conversation_history.get_history(user, conversation_id)
    for msg in messages:
        if 'timestamp' in msg:
            del msg['timestamp']
        if 'role' in msg:
            msg['author'] = '0' if msg['role'] == 'user' else '1'
            del msg['role']

    data = create_data_object(current_persona, messages, temperature_var, top_p_var, top_k_var)

    logger.info(f"Sending request to Google API with data: {data}")
    
    try:
        response_data = palm.chat(**data)
        logger.info(f"Received response data from Google API: {response_data}")   

        # Assuming response_data has a 'candidates' attribute that is a list
        if hasattr(response_data, 'candidates') and len(response_data.candidates) > 0:
            ChatResponse = response_data.candidates[0].get("content", "Unknown response content")
            
        else:
            logger.warning("Unexpected structure in response_data or candidates list is empty.")
            raise ValueError("Unexpected structure in response_data or candidates list is empty.")
        
    except Exception as e:
        logger.exception("Error processing response_data: %s", e)
        ChatResponse = "An error occurred while processing the response."
        logger.info(f"Error response: {ChatResponse}")

    
    conversation_history.add_message(user, conversation_id, "assistant", ChatResponse, current_time)
    try:
        if tts.get_tts() and not contains_code(ChatResponse):
            await text_to_speech(ChatResponse)
    except Exception as e:
        logger.exception("Error during TTS operation: %s", e)

    return ChatResponse

def contains_code(text: str) -> bool:
    return "<code>" in text

async def text_to_speech(text):
    text_without_code = re.sub(r"`[^`]*`", "", text)
    logger.debug("Processing text to speech")
    await tts.text_to_speech(text_without_code)
