# modules/Providers/OpenAI/OA_gen_response.py

from .openai_api import OpenAIAPI
from datetime import datetime
from modules.logging.logger import setup_logger
from modules.Providers.OpenAI.CreateRequest import create_request_body
from modules.Tools.ToolManager import load_function_map_from_current_persona, load_functions_from_json, use_tool

logger = setup_logger('OA_gen_response.py')

current_username = None
api = OpenAIAPI()

async def generate_response(user, current_persona, message, session_id, conversation_id, temperature_var, top_p_var, top_k_var, conversation_manager, model_manager, provider_manager=None):
    logger.info(f"generate_response called with user: {user}, session_id: {session_id}, conversation_id: {conversation_id}")

    functions = load_functions_from_json(current_persona)
    function_map = load_function_map_from_current_persona(current_persona)

    if "name" in current_persona:
        conversation_history = conversation_manager
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

    data = create_request_body(model_manager.get_model(), current_persona, 
                           messages, temperature_var, 
                           top_p_var, model_manager.get_max_tokens(), functions 
                           if model_manager.is_model_allowed() else None)

    logger.info(f"Starting response generation for user: {user}, session_id: {session_id}, conversation_id: {conversation_id}")

    logger.info("Data being sent in HTTP request to OpenAI: %s", data)

    response_data = await api.generate_conversation(data)

    if response_data:
        message = response_data["choices"][0]["message"]
        text = message["content"]

        if text is None:
            text = await use_tool(user, conversation_id, message, conversation_history, function_map, functions, current_persona, temperature_var, top_p_var, conversation_manager, model_manager)
            if text is None:
                text = "Gen_response says: Sorry, I couldn't generate a meaningful response. Please try again or provide more context."
                logger.info("Gen_response says: Sorry, I couldn't generate a meaningful response. Please try again or provide more context.")
        
        # Log before calling TTS
        try:
            if provider_manager.get_current_speech_provider() == "Eleven Labs":
                from modules.speech_services.Eleven_Labs.tts import tts, get_tts
            elif provider_manager.get_current_speech_provider() == "Google":
                from modules.speech_services.GglCldSvcs.tts import tts, get_tts

            if get_tts():
                logger.info(f"Attempting to invoke TTS for the text: {text}")
                if contains_code(text):
                    logger.info("Skipping TTS as the text contains code.")
                else:
                    await tts(text)
                    logger.info("TTS successfully invoked.")
            else:
                logger.info("TTS is turned off.")
        except Exception as e:
            logger.error("Error during TTS: %s", e)

        return text
    else:
        return "Sorry, I couldn't generate a response. Please try again."

def contains_code(text: str) -> bool:
    return "<code>" in text
