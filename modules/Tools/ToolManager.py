# modules/Providers/OpenAI/ToolManager.py

import asyncio
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
from modules.event_system import event_system

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
    logger.info(f"use_tool called for user: {user}, conversation_id: {conversation_id}")
    logger.debug(f"Full message: {message}")
    
    if message.get("function_call"):
        logger.info(f"Function call detected: {message['function_call']['name']}")
        function_response, error_occurred = await handle_function_call(user, conversation_id, message, conversation_history, function_map)

        logger.info(f"Function call response: {function_response}")
        logger.info(f"Error occurred: {error_occurred}")

        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        conversation_history.add_response(user, conversation_id, function_response, current_time)
        logger.info("Function call response added to responses table.")

        formatted_function_response = f"System Message: The function call was executed successfully with the following results: {message['function_call']['name']}: {function_response} If needed, you can make another tool call for further processing or multi-step requests. Provide the answer to the user's question, a summary or ask for further details."

        logger.debug(f"Formatted function response: {formatted_function_response}")

        messages = conversation_history.get_history(user, conversation_id)
        logger.debug(f"Conversation history: {messages}")

        new_text = await call_model_with_new_prompt(formatted_function_response, current_persona, messages, temperature_var, top_p_var, functions, model_manager)
        
        logger.info(f"Model response: {new_text}")

        if new_text is None:
            logger.warning("Model returned None response")
            new_text = "Tool Manager says: Sorry, I couldn't generate a meaningful response. Please try again or provide more context."

        logger.info("Assistant: %s", new_text)

        if new_text:
            current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            conversation_history.add_message(user, conversation_id, "assistant", new_text, current_time)
            logger.info("Assistant message added to conversation history.")

        return new_text
    return None

async def handle_function_call(user, conversation_id, message, conversation_history, function_map):
    logger.info(f"handle_function_call for user: {user}, conversation_id: {conversation_id}")
    logger.debug(f"Full message: {message}")
    
    function_name = message["function_call"]["name"]
    function_args_json = message["function_call"].get("arguments", "{}")

    try:
        function_args = json.loads(function_args_json)
        logger.info(f"Function name: {function_name}")
        logger.debug(f"Function args: {function_args}")
    except json.JSONDecodeError as e:
        logger.error(f"Error decoding JSON: {e}")
        return f"Error: Invalid JSON in function arguments: {e}", True

    if function_name in function_map:
        required_args = get_required_args(function_map[function_name])
        logger.info(f"Required args for {function_name}: {required_args}")
        logger.info(f"Provided args: {list(function_args.keys())}")
        missing_args = set(required_args) - set(function_args.keys())

        if missing_args:
            logger.error(f"Not all required arguments provided for {function_name}. Missing: {', '.join(missing_args)}")
            return f"Error: Not all required arguments provided for {function_name}. Missing: {', '.join(missing_args)}", True

        try:
            logger.info(f"Calling function {function_name} with arguments {function_args}")
            if asyncio.iscoroutinefunction(function_map[function_name]):
                function_response = await function_map[function_name](**function_args)
            else:
                function_response = function_map[function_name](**function_args)
            logger.info(f"Function response: {function_response}")
            
            # Publish event for code execution
            if function_name == "execute_python":
                event_system.publish("code_executed", function_args['command'], function_response)
                logger.info("Published code_executed event")
            
            return function_response, False
        except Exception as e:
            logger.error(f"Exception during function call {function_name}: {e}", exc_info=True)
            return f"Error: Exception during function call {function_name}: {e}", True

    logger.error(f"Function {function_name} not found in function map.")
    return None, True


async def call_model_with_new_prompt(prompt, current_persona, messages, temperature_var, top_p_var, functions, model_manager):
    logger.info("call_model_with_new_prompt called")
    logger.info(f"Prompt: {prompt}")
    logger.debug(f"Messages: {messages}")
    
    data = create_request_body(model_manager.get_model(), current_persona, 
                           messages + [{"role": "user", "content": prompt}], 
                           temperature_var, 
                           top_p_var, model_manager.get_max_tokens(), functions 
                           if model_manager.is_model_allowed() else None)
    
    logger.debug(f"Request data: {data}")
    
    response_data = await api.generate_conversation(data)
    
    logger.debug(f"Response data: {response_data}")

    if response_data and response_data.get("choices"):
        return response_data["choices"][0]["message"]["content"]
    else:
        logger.error(f"Failed to get valid response from model. Response data: {response_data}")
        return None
