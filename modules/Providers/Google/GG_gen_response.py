# Google/GG_gen_response.py

import re
import logging
from logging.handlers import RotatingFileHandler
from datetime import datetime
from modules.speech_services.GglCldSvcs import tts
from modules.chat_history.convo_manager import ConversationManager
from modules.Providers.Google.genai_api import GenAIAPI
from modules.Tools.Tool_Manager import ToolManager

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

def adjust_logging_level(level):
    """Adjust the logging level.
    
    Parameters:
    - level (str): Desired logging level. Can be 'DEBUG', 'INFO', 'WARNING', 'ERROR', or 'CRITICAL'.
    """
    levels = {
        'DEBUG': logging.DEBUG,
        'INFO': logging.INFO,
        'WARNING': logging.WARNING,
        'ERROR': logging.ERROR,
        'CRITICAL': logging.CRITICAL
    }
    
    logger.setLevel(levels.get(level, logging.WARNING))

"""
 Default model
"""
GG_MODEL = 'gemini-pro' 

def set_GG_model(model_name):
    """
    Set the Gemini model to be used for generating responses.

    :param model_name: The name of the model to use.
    """
    global GG_MODEL
    logger.info(f"Changing GG model from {GG_MODEL} to {model_name}")
    GG_MODEL = model_name

def get_GG_model():
    """
    Get the current Gemini model being used.

    :return: The name of the current model.
    """
    return GG_MODEL

def create_request_body(current_persona, messages, temperature_var, top_p_var, top_k_var, functions = None, safety_settings = None):
    """
    Create the request body for the generative AI model.

    :param current_persona: The current persona of the chatbot.
    :param messages: The chat history messages.
    :param temperature_var: The temperature parameter for the generation.
    :param top_p_var: The top_p parameter for the generation.
    :param top_k_var: The top_k parameter for the generation (optional).
    :return: The request data object.
    """
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


async def generate_response(user, current_persona, message, session_id, conversation_id, temperature_var, top_p_var, top_k_var=None):
    """
    Generates a response using the specified Gemini model.

    :param user: The user for whom the response is being generated.
    :param current_persona: The current persona of the chatbot.
    :param message: The message from the user.
    :param session_id: The session ID for this interaction.
    :param conversation_id: The conversation ID for this interaction.
    :param temperature_var: The temperature parameter for the generation.
    :param top_p_var: The top_p parameter for the generation.
    :param top_k_var: The top_k parameter for the generation (optional).
    :return: The generated text response.
    """
    
    logger.info(f"Starting response generation for user: {user}, session_id: {session_id}, conversation_id: {conversation_id}")
    
    if "name" in current_persona: 
        conversation_history = ConversationManager(user, current_persona["name"])
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

    logger.info(f"Sending request to Google API with data: {data}")
    
    genai_api = GenAIAPI(GG_MODEL)
    
    # Call the generate_content method asynchronously
    response_data = await genai_api.generate_content(data)
    
    function_map = ToolManager.load_function_map_from_current_persona(current_persona)

    if "function_call" in response_data:
        try:
            # Handle the function call using the loaded function map
            function_response, error_occurred = await ToolManager.handle_function_call(user, conversation_id, response_data, conversation_history, function_map)
            
            # Process the function response (e.g., by incorporating it into the chat response or taking further actions based on it)
            if not error_occurred:
                ToolManager.logger.info(f"Function call successful with response: {function_response}")
                # Integrate the function response into the chatbot's response
            else:
                ToolManager.logger.error(f"Error occurred in function call: {function_response}")
        except Exception as e:
            ToolManager.logger.error(f"Exception handling function call: {e}", exc_info=True)
            # Handle exception (e.g., by notifying the user or taking corrective action)


    try:
        if hasattr(response_data, 'candidates') and len(response_data.candidates) > 0:
            # Extract the detailed_content from the first candidate
            detailed_content = response_data.candidates[0].content.parts
            # Initialize an empty string to hold the formatted chat response
            ChatResponse = ""
            # Iterate through each part of the detailed_content
            for part in detailed_content:
                # Append each text part to the ChatResponse string
                ChatResponse += part.text + "\n"
            logger.info(f"Raw detailed_content: {detailed_content}")
            
            # Remove the persona name from the beginning of ChatResponse if present
            separator = ": "  # Define the separator used in the ChatResponse
            persona_prefix = f"{current_persona.get('name', '')}{separator}"
            if ChatResponse.startswith(persona_prefix):
                # Remove the persona name and the separator from the beginning of ChatResponse
                ChatResponse = ChatResponse[len(persona_prefix):]
            
            # Log the formatted ChatResponse without the persona's name at the beginning
            logger.info(f"Formatted ChatResponse: {ChatResponse}")
        else:
            logger.warning("Unexpected structure in response_data or candidates list is empty.")
            raise ValueError("Unexpected structure in response_data or candidates list is empty.")
    except Exception as e:
        logger.error(f"Error processing response_data: {e}")
        ChatResponse = "An error occurred while processing the response."
        logger.info(f"Error response: {ChatResponse}")
        raise

    conversation_history.add_message(user, conversation_id, "assistant", ChatResponse, current_time)
    
    try:
        if tts.get_tts() and not contains_code(ChatResponse):
            await text_to_speech(ChatResponse)
    except Exception as e:
        logger.exception("Error during TTS operation: %s", e)

    logger.info(f"Exiting generate_response function.")
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
        # Extract role and content from each message
        role = message['role']
        content = message['content']
        # Determine the display name based on the role
        display_name = user_name if role == "user" else assistant_name

        # Check if the content needs further processing (e.g., it's a nested message)
        if isinstance(content, str) and content.startswith('['):
            try:
                nested_messages = eval(content)
                if isinstance(nested_messages, list):
                    for nested_message in nested_messages:
                        nested_role = nested_message.get('role', 'unknown')
                        # Use the user_name or assistant_name for nested messages as well
                        nested_display_name = user_name if nested_role == "user" else assistant_name
                        nested_content = nested_message.get('content', '')
                        formatted_messages.append(f"{nested_display_name}: {nested_content}")
            except:
                # Fallback in case of eval errors, directly use the resolved display name
                formatted_messages.append(f"{display_name}: {content}")
        else:
            formatted_messages.append(f"{display_name}: {content}")
    # Join all formatted messages with a comma and space
    return ', '.join(formatted_messages)
