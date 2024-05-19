# gui/OpenAI/OA_gen_response.py

import json
import re
import inspect
import importlib.util
import sys
from .openai_api import OpenAIAPI
from modules.speech_services.GglCldSvcs import tts
from datetime import datetime
from modules.chat_history.convo_manager import ConversationManager
from modules.logging.logger import setup_logger

logger = setup_logger('OA_gen_response.py')

MODEL = "gpt-4o"

MODEL_GPT4o = "gpt-4o"
MODEL_GPTo_2024_05_13 = "gpt-4o-2024-05-13"
MODEL_GPT4_0613 = "gpt-4-0613"
MODEL_GPT4_1106_PREVIEW = "gpt-4-1106-preview"
MODEL_GPT4_TURBO_PREVIEW = "gpt-4-turbo-preview"
MODEL_GPT3_5_TURBO_16K_0613 = "gpt-3.5-turbo-16k-0613" 
MODEL_GPT3_5_TURBO_0613 = "gpt-3.5-turbo-0613"
MODEL_GPT3_5_TURBO_1106 = "gpt-3.5-turbo-1106"

# max tokens needs revision
MAX_TOKENS = 4000 
MAX_TOKENS_GPT4 = 4000
MAX_TOKENS_GPT4_0613 = 4000
MAX_TOKENS_GPT3_5_TURBO_16K = 10000
MAX_TOKENS_GPT3_5_TURBO_16K_0613 = 10000

# Model that can use tools. This insures models without the abilty to call tools are not sent tools in the rquest body.
ALLOWED_MODELS = [MODEL_GPT3_5_TURBO_1106, MODEL_GPT4_0613, MODEL_GPT3_5_TURBO_16K_0613, MODEL_GPT3_5_TURBO_0613, MODEL_GPT4_1106_PREVIEW, MODEL_GPT4_TURBO_PREVIEW, MODEL_GPT4o, MODEL_GPTo_2024_05_13]

# Update the FUNCTIONS_JSON_PATH_TEMPLATE and the MAPS_PATH_TEMPLATE to use the dynamic path based on the current_persona
FUNCTIONS_JSON_PATH_TEMPLATE = 'modules/Personas/{}/Toolbox/functions.json'
MAPS_PATH_TEMPLATE = 'modules/Personas/{}/Toolbox/maps.py'

current_username = None
api = OpenAIAPI()

def set_OA_model(model_name):
    global MODEL, MAX_TOKENS
    MODEL = model_name
    if MODEL in ["gpt-3.5-turbo-16k-0613", "gpt-3.5-turbo-16k"]:
        MAX_TOKENS = 4000
    elif MODEL in ["gpt-4-0613", "gpt-4", "gpt-4o", "gpt-4o-2024-05-13"]:
        MAX_TOKENS = 4000
    else:
        MAX_TOKENS = 2000 

def get_OA_model():
    return MODEL

def is_model_allowed():
    return MODEL in ALLOWED_MODELS

def get_required_args(function):
    logger.info("getting required args")
    sig = inspect.signature(function)

    return [param.name for param in sig.parameters.values() 
            if param.default == param.empty and param.name != 'self']

def load_function_map_from_current_persona(current_persona):
    persona_name = current_persona["name"]  
    maps_path = MAPS_PATH_TEMPLATE.format(persona_name)  
    module_name = f'persona_{persona_name}_maps' 

    spec = importlib.util.spec_from_file_location(module_name, maps_path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module  
    spec.loader.exec_module(module)
    
    return module.function_map

def load_functions_from_json(current_persona):
    persona_name = current_persona["name"]  
    functions_json_path = FUNCTIONS_JSON_PATH_TEMPLATE.format(persona_name)  
    
    try:
        with open(functions_json_path, 'r') as file:
            functions = json.load(file)
            logger.info("Functions loaded from file: %s")
            return functions
    except FileNotFoundError:
        logger.info(f"Functions JSON file not found for persona: {persona_name}")
    except json.JSONDecodeError as e:
        logger.info(f"Error decoding JSON from {functions_json_path}: {e}")

    return {}  

def create_request_body(current_persona, messages, temperature_var, top_p_var, functions=None):
    logger.info("Creating request body.")
    logger.info(f"Model: {MODEL}")
    logger.info(f"Max Tokens: {MAX_TOKENS}")
    logger.info(f"Temperature: {temperature_var}")
    logger.info(f"Messages: {messages}")    

    data = {
        "model": MODEL,
        "messages": [{"role": "system", "content": current_persona["content"]}] + messages,
        "temperature": temperature_var,
        "max_tokens": MAX_TOKENS,
        "top_p": top_p_var
    }
    if functions:
        data["functions"] = functions
        data["function_call"] = "auto"
        
    logger.info("Request body created.")    
    return data

async def handle_function_call(user, conversation_id, message, conversation_history, function_map):
    entry_time = datetime.now()
    logger.info(f"Entering handle_function_call at {entry_time.isoformat()}")
    
    logger.info(f"Raw function call: {message}")    
    function_name = message["function_call"]["name"]
    function_args_json = message["function_call"].get("arguments", "{}")

    try:
        function_args = json.loads(function_args_json)
        logger.info(f"Decoded args: {function_args}")  
    except json.JSONDecodeError as e:
        logger.error(f"Error decoding JSON: {e}")
        function_args = {}  

    logger.info(f"Function name: {function_name}")
    logger.info(f"Function args: {function_args}")

    if function_name in function_map:
        required_args = get_required_args(function_map[function_name])  
        logger.info(f"Required args for {function_name}: {required_args}")  
        missing_args = set(required_args) - set(function_args.keys())

        if missing_args:
            logger.error(f"Not all required arguments provided for {function_name}. Missing: {', '.join(missing_args)}")
            return f"Error: Not all required arguments provided for {function_name}. Missing: {', '.join(missing_args)}", True

        try:
            logger.info(f"Calling function {function_name} with arguments {function_args}")
            function_response = await function_map[function_name](**function_args)
            logger.info(f"Function response: {function_response}")
        except Exception as e:
            logger.error(f"Exception during function call {function_name}: {e}", exc_info=True)
            return f"Error: Exception during function call {function_name}: {e}", True

        exit_time = datetime.now()
        logger.info(f"Exiting handle_function_call at {exit_time.isoformat()}, duration: {(exit_time-entry_time).total_seconds()} seconds")
        
        if not isinstance(function_response, str):
            function_response = str(function_response)

        return function_response, False

    logger.error(f"Function {function_name} not found in function map.")
    return None, True

async def use_tool(user, conversation_id, message, conversation_history, function_map, functions, current_persona, temperature_var, top_p_var):
    if message.get("function_call"):
        function_response, error_occurred = await handle_function_call(user, conversation_id, message, conversation_history, function_map)

        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        conversation_history.add_response(user, conversation_id, function_response, current_time)
        logger.info("Function call response added to responses table.")

        formatted_function_response = f"System Message: The function call was executed successfully with the following results: {message['function_call']['name']}: {function_response} If needed, you can make another tool call for further proccesing or multi-step requests. Provide the answer to the users question, a summary or ask for further details."

        messages = conversation_history.get_history(user, conversation_id)
        for msg in messages:
            if 'timestamp' in msg:
                del msg['timestamp']

        data = create_request_body(current_persona, 
                           messages + [{"role": "user", "content": formatted_function_response}], 
                           temperature_var, 
                           top_p_var, functions 
                           if is_model_allowed() else None)

        response_data = await api.generate_conversation(data)

        if response_data:
            new_message = response_data["choices"][0]["message"]
            new_text = new_message["content"]

            if new_text is None:
                new_prompt = f"System Message: The function call was executed successfully with the following results: {function_response} If needed, you can make another tool call for further proccesing or multi-step requests. Provide the answer to the users question, a summary or ask for further details."
                new_text = await call_model_with_new_prompt(new_prompt, current_persona, temperature_var, top_p_var, function_map, functions)
                if not new_text:
                    new_text = "Sorry, I couldn't generate a meaningful response. Please try again or provide more context."

            logger.info("Assistant: %s", new_text)
            
            if new_text:
                current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                conversation_history.add_message(user, conversation_id, "assistant", new_text, current_time)                    
                logger.info("Assistant message added to conversation history.")
            try:
                if tts.get_tts():
                    if contains_code(new_text):
                        logger.info("Skipping TTS as the text contains code.")
                else:
                    await tts.text_to_speech(new_text)
            except Exception as e:
                logger.error("Error during TTS: %s", e)

            return new_text
    return None

async def generate_response(user, current_persona, message, session_id, conversation_id, temperature_var, top_p_var, top_k_var, provider_manager=None):
    logger.info(f"generate_response called with user: {user}, session_id: {session_id}, conversation_id: {conversation_id}")

    functions = load_functions_from_json(current_persona)
    function_map = load_function_map_from_current_persona(current_persona)

    if "name" in current_persona: 
        conversation_history = ConversationManager(user, current_persona["name"], provider_manager)
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
                           messages, temperature_var, 
                           top_p_var, functions 
                           if is_model_allowed() else None)
    
    logger.info(f"Starting response generation for user: {user}, session_id: {session_id}, conversation_id: {conversation_id}")

    logger.info("Data being sent in HTTP request to OpenAI: %s", data) 

    response_data = await api.generate_conversation(data)

    if response_data:
        message = response_data["choices"][0]["message"]
        text = message["content"]  

        if text is None:
            text = await use_tool(user, conversation_id, message, conversation_history, function_map, functions, current_persona, temperature_var, top_p_var)
            if text is None:
                text = "Sorry, I couldn't generate a meaningful response. Please try again or provide more context."

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

async def call_model_with_new_prompt(prompt, current_persona, temperature_var, top_p_var, functions):
    global api
    data = create_request_body(current_persona, [{"role": "user", "content": prompt}], temperature_var, top_p_var, functions)    
    response_data = await api.generate_conversation(data)
    
    if response_data and response_data.get("choices"):
        return response_data["choices"][0]["message"]["content"]
    else:
        return None

def contains_code(text: str) -> bool:
    return "<code>" in text

async def text_to_speech(text):
    logger.info("Skipping TTS as the text contains code.")  
    text_without_code = re.sub(r"`[^`]*`", "", text)
    await tts.text_to_speech(text_without_code)