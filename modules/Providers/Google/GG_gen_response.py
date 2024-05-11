# Google/GG_gen_response.py

import re
from datetime import datetime
#from modules.speech_services.GglCldSvcs import tts
from modules.speech_services.Eleven_Labs.tts import tts, get_tts
from modules.chat_history.convo_manager import ConversationManager
from modules.Providers.Google.genai_api import GenAIAPI
from modules.Tools.Tool_Manager import ToolManager
from modules.logging.logger import setup_logger


logger = setup_logger('GG_gen_response.py')


GG_MODEL = 'gemini-1.5-pro-latest' 

def set_GG_model(model_name):
    global GG_MODEL
    logger.info(f"Changing GG model from {GG_MODEL} to {model_name}")
    GG_MODEL = model_name

def get_GG_model():
    return GG_MODEL

def create_request_body(current_persona, messages, temperature_var, top_p_var, top_k_var, functions = None, safety_settings = None):
    parts = []
    if current_persona.get("content"):
        parts.append({
            "text":  f"SYSTEM MESSAGE: {current_persona["content"]}" + f"    THIS IS THE CHAT HISTORY BETWEEN YOU AND THE USER: {messages}"
        })    
    
    contents = [{
        "parts": parts,
        "role": "user"  
    }]

    Generation_config = {
        "candidate_count": 1,
        "max_output_tokens": 2048,
        "temperature": temperature_var,
        "top_p": top_p_var,
        "top_k": top_k_var
        }

    data = {
        "contents": contents,
        "generation_config": Generation_config,
    }
    if functions:
        data["tools"] = functions

    logger.info("Data object created for HTTP request.")
    return data


async def generate_response(user, current_persona, message, session_id, conversation_id, temperature_var, top_p_var, top_k_var=None, provider_manager=None):  
    logger.info("Starting response generation")
    
    if "name" in current_persona: 
        conversation_history = ConversationManager(user, current_persona["name"], provider_manager)
    else:
        conversation_history = None

    if conversation_id is None:
        raise ValueError("conversation_id cannot be None")

    logger.debug(f"generate_response called with user: {user}, session_id: {session_id}, conversation_id: {conversation_id}, temperature_var: {temperature_var}, top_p_var: {top_p_var}, top_k_var: {top_k_var}")

    if message:
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        conversation_history.add_message(user, conversation_id, "user", message, current_time)
        logger.info("New user message added to conversation history.")

    messages = conversation_history.get_history(user, conversation_id)
    for msg in messages:
        if 'timestamp' in msg:
            del msg['timestamp']
    messages_formatted = format_message_history(messages, user, current_persona.get("name", "Assistant"))
    messages= messages_formatted

    functions = ToolManager.load_functions_from_json(current_persona)

    data = create_request_body(current_persona, messages, temperature_var, top_p_var, top_k_var)

    logger.info("Sending request to Google API.")
    logger.debug(f"Data: {data}")

    genai_api = GenAIAPI(GG_MODEL)
    
    # Call the generate_content method asynchronously
    response_data = await genai_api.generate_content(data)
    
    function_map = ToolManager.load_function_map_from_current_persona(current_persona)

    if "function_call" in response_data:
        try:
            function_response, error_occurred = await ToolManager.handle_function_call(user, conversation_id, response_data, conversation_history, function_map)
            
            if not error_occurred:
                ToolManager.logger.info(f"Function call successful with response: {function_response}")
            else:
                ToolManager.logger.error(f"Error occurred in function call: {function_response}")
        except Exception as e:
            ToolManager.logger.error(f"Exception handling function call: {e}", exc_info=True)


    try:
        if hasattr(response_data, 'candidates') and len(response_data.candidates) > 0:
            detailed_content = response_data.candidates[0].content.parts
            ChatResponse = ""
            for part in detailed_content:
                ChatResponse += part.text + "\n"
            logger.debug(f"Raw detailed_content: {detailed_content}")
            
            separator = ": "  
            persona_prefix = f"{current_persona.get('name', '')}{separator}"
            if ChatResponse.startswith(persona_prefix):
                ChatResponse = ChatResponse[len(persona_prefix):]
            
            logger.debug(f"ChatResponse: {ChatResponse}")

        else:
            logger.warning("Unexpected structure in response_data or candidates list is empty.")
            raise ValueError("Unexpected structure in response_data or candidates list is empty.")
    except Exception as e:
        logger.error(f"Error processing response_data: {e}")
        ChatResponse = "An error occurred while processing the response."
        logger.debug(f"Error response: {ChatResponse}")
        raise

    conversation_history.add_message(user, conversation_id, "assistant", ChatResponse, current_time)
     
    try:
        if get_tts() and not contains_code(ChatResponse):
            await text_to_speech(ChatResponse)
    except Exception as e:
        logger.exception("Error during TTS operation: %s", e)

    logger.info("Exiting generate_response function.")
    return ChatResponse

def contains_code(text: str) -> bool:
    """
    Check if the given text contains code snippets.

    :param text: The text to check.
    :return: True if the text contains code snippets, False otherwise.
    """
    return "<code>" in text

async def text_to_speech(text):
    """
    Convert the given text to speech.

    :param text: The text to convert.
    """
    text_without_code = re.sub(r"`[^`]*`", "", text)
    logger.info("Processing text to speech")
    await tts.text_to_speech(text_without_code)
    

def format_message_history(messages, user_name, assistant_name):
    """
    Format the message history for return to the model to reduce token count.

    :param messages: The list of message dictionaries.
    :param user_name: The name of the user.
    :param assistant_name: The name of the assistant.
    :return: A string representing the formatted message history.
    """
    formatted_messages = []
    for message in messages:
        role = message['role']
        content = message['content']
        display_name = user_name if role == "user" else assistant_name

        if isinstance(content, str) and content.startswith('['):
            try:
                nested_messages = eval(content)
                if isinstance(nested_messages, list):
                    for nested_message in nested_messages:
                        nested_role = nested_message.get('role', 'unknown')
                        nested_display_name = user_name if nested_role == "user" else assistant_name
                        nested_content = nested_message.get('content', '')
                        formatted_messages.append(f"{nested_display_name}: {nested_content}")
            except:
                formatted_messages.append(f"{display_name}: {content}")
        else:
            formatted_messages.append(f"{display_name}: {content}")
    return ', '.join(formatted_messages)
