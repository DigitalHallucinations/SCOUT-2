# modules/Providers/Anthropic/Anthropic_gen_response.py

import json
import re
from .Anthropic_api import AnthropicAPI
from modules.speech_services.GglCldSvcs import tts
from datetime import datetime
from modules.chat_history.convo_manager import ConversationManager
from modules.logging.logger import setup_logger

logger = setup_logger('Anthropic_gen_response.py')
 
api = AnthropicAPI()

MODEL = "claude-3-opus-20240229"

MODEL_CLAUDE_3_OPUS = "claude-3-opus-20240229"
MODEL_CLAUDE_3_SONNET = "claude-3-sonnet-20240229" 
MODEL_CLAUDE_3_HAIKU = "claude-3-haiku-20240307"
MODEL_CLAUDE_3_SONNET = 4096
MODEL_CLAUDE_3_OPUS = 4096
MODEL_CLAUDE_3_HAIKU = 4096
MAX_TOKENS = 4096 

FUNCTIONS_JSON_PATH_TEMPLATE = 'modules/Personas/{}/Toolbox/functions.json'

current_username = None

def set_Anthropic_model(model_name):
    """
    Used in chat_settings.py sets the Anthropic Model
    """
    global MODEL, MAX_TOKENS
    MODEL = model_name
    if MODEL in ["claude-3-opus-20240229"]:
        MAX_TOKENS = 4096
    elif MODEL in ["claude-3-sonnet-20240229"]:
        MAX_TOKENS = 4096
    elif MODEL in ["claude-3-haiku-20240307"]:
        MAX_TOKENS = 4096    
    else:
        MAX_TOKENS = 2000 

def get_Anthropic_model():
    """
    Used in chat_settings.py
    retrieves the current model in use
    """
    return MODEL

def create_request_body(current_persona, messages, temperature_var, top_p_var, top_k_var, funtions=None):
    logger.info("Creating request body.")
    logger.info({MODEL})
    logger.info({MAX_TOKENS})
    logger.info({temperature_var})
    logger.info({top_p_var})

    if isinstance(current_persona["content"], str):
        system_content = current_persona["content"]
    else:
        system_content = json.dumps(current_persona["content"]) if current_persona["content"] else ""
    
    data = {
        "model": MODEL,
        "system": system_content,  
        "max_tokens": MAX_TOKENS,
        "temperature": temperature_var,
        "messages": messages
    }

    logger.info("request body created.")
    return data

async def generate_response(user, current_persona, message, session_id, conversation_id, temperature_var, top_p_var, top_k_var):
    """
    Generates a response using the specified Anthropic model.

    :param user: The user for whom the response is being generated.
    :param current_persona: The current persona of the chatbot.
    :param message: The message from the user.
    :param session_id: The session ID for this interaction.
    :param conversation_id: The conversation ID for this interaction.
    :param temperature_var: The temperature parameter for the generation.
    :param top_p_var: The top_p parameter for the generation.
    :return: The generated text response.
    """
    logger.info(f"generate_response called with user: {user}, current persona: {current_persona["name"]}, session_id: {session_id}, conversation_id: {conversation_id}")
    
    functions = None

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


    data = create_request_body(current_persona, 
                              messages, 
                              temperature_var, 
                              top_p_var,
                              functions 
                              )
      
    logger.info(f"Starting response generation for user: {user}, session_id: {session_id}, conversation_id: {conversation_id}")

    #logger.info("Data being sent in HTTP request to AnthropicAPI: %s", data) 
    logger.info("Data being sent in HTTP request to AnthropicAPI.") 

    response_data = await api.generate_conversation(data)

    if response_data:
        #logger.info(f"response from Anthropic API: {response_data}")
        logger.info("response from Anthropic API.")
        content_blocks = response_data.content 
        text = ''
        if not content_blocks:
            logger.error("No content blocks found in the response from Anthropic API.")
            text = "Sorry, I couldn't generate a response. The API response was not in the expected format."
        else:
            for block in content_blocks:
                if block.type == 'text':
                    text_block = block.text 
                    if text_block:
                        text += text_block + '\n\n'
                    else:
                        logger.warning("A text block was found without any text content.")
                else:
                    logger.warning(f"A content block of type '{block.type}' was found, which is not handled by this method.")
            
        #logger.info(f"Extracted response: {text}")
        logger.info("Extracted response")

        if text:  
            current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')  
            conversation_history.add_message(user, conversation_id, "assistant", text, current_time)
            logger.info("Assistant message added to conversation history.")

        try:
                if tts.get_tts():
                    if contains_code(text):
                        logger.info("Skipping TTS as the text contains code.")
                    else:
                        await text_to_speech(text)
        except Exception as e:
                logger.error("Error during TTS: %s", e)

        return text
    else:
        return "Sorry, I couldn't generate a response. Please try again."

def contains_code(text: str) -> bool:
    """Check if the given text contains code"""
    return "<code>" in text

async def text_to_speech(text):
    """
    Convert the given text to speech.

    :param text: The text to convert.
    """
    logger.info("Using TTS")  
    text_without_code = re.sub(r"`[^`]*`", "", text)
    await tts.text_to_speech(text_without_code)

