# modules/Providers/OpenAI/function_call_handler.py

import json
import inspect
from datetime import datetime
from modules.logging.logger import setup_logger

logger = setup_logger('function_call_handler.py')

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