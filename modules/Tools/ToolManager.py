# modules/Providers/OpenAI/ToolManager.py

import json
import inspect
import importlib.util
import sys

from datetime import datetime
from modules.Providers.OpenAI.CreateRequest import create_request_body
from modules.Providers.OpenAI.openai_api import OpenAIAPI
#from modules.speech_services.GglCldSvcs import tts
from modules.speech_services.Eleven_Labs.tts import tts, get_tts
from modules.logging.logger import setup_logger

logger = setup_logger('ToolManager.py')


api = OpenAIAPI()

# Update the FUNCTIONS_JSON_PATH_TEMPLATE and the MAPS_PATH_TEMPLATE to use the dynamic path based on the current_persona
FUNCTIONS_JSON_PATH_TEMPLATE = 'modules/Personas/{}/Toolbox/functions.json'
MAPS_PATH_TEMPLATE = 'modules/Personas/{}/Toolbox/maps.py'

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

async def use_tool(user, conversation_id, message, conversation_history, function_map, functions, current_persona, temperature_var, top_p_var, conversation_manager, model_manager):
    conversation_history = conversation_manager
    
    if message.get("function_call"):
        function_response, error_occurred = await handle_function_call(user, conversation_id, message, conversation_history, function_map)

        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        conversation_history.add_response(user, conversation_id, function_response, current_time)
        logger.info("Function call response added to responses table.")

        formatted_function_response = f"System Message: The function call was executed successfully with the following results: {message['function_call']['name']}: {function_response} If needed, you can make another tool call for further processing or multi-step requests. Provide the answer to the user's question, a summary or ask for further details."

        messages = conversation_history.get_history(user, conversation_id)
        for msg in messages:
            if 'timestamp' in msg:
                del msg['timestamp']

        data = create_request_body(model_manager.get_model(), current_persona, 
                           messages + [{"role": "user", "content": formatted_function_response}], 
                           temperature_var, 
                           top_p_var, model_manager.get_max_tokens(), functions 
                           if model_manager.is_model_allowed() else None)

        response_data = await api.generate_conversation(data)

        if response_data:
            new_message = response_data["choices"][0]["message"]
            new_text = new_message["content"]

            if new_text is None:
                new_prompt = f"System Message: The function call was executed successfully with the following results: {function_response} If needed, you can make another tool call for further processing or multi-step requests. Provide the answer to the user's question, a summary or ask for further details."
                new_text = await call_model_with_new_prompt(new_prompt, current_persona, messages, temperature_var, top_p_var, functions, model_manager)
                if not new_text:
                    new_text = "Tool Manager says: Sorry, I couldn't generate a meaningful response. Please try again or provide more context."

            logger.info("Assistant: %s", new_text)

            if new_text:
                current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                conversation_history.add_message(user, conversation_id, "assistant", new_text, current_time)
                logger.info("Assistant message added to conversation history.")
            try:
                if get_tts():
                    if contains_code(new_text):
                        logger.info("Skipping TTS as the text contains code.")
                    else:
                        await tts(new_text)
            except Exception as e:
                logger.error("Error during TTS: %s", e)

            return new_text
    return None

def get_required_args(function):
    logger.info("getting required args")
    sig = inspect.signature(function)
    return [param.name for param in sig.parameters.values() 
            if param.default == param.empty and param.name != 'self']

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

async def call_model_with_new_prompt(prompt, current_persona, messages, temperature_var, top_p_var, functions, model_manager):
    global api
    data = create_request_body(model_manager.get_model(), current_persona, 
                           messages, temperature_var, 
                           top_p_var, model_manager.get_max_tokens(), functions 
                           if model_manager.is_model_allowed() else None)
    
    response_data = await api.generate_conversation(data)

    if response_data and response_data.get("choices"):
        return response_data["choices"][0]["message"]["content"]
    else:
        return None

def contains_code(text: str) -> bool:
    return "<code>" in text
