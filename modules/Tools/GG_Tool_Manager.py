# modules/Tools/Tool_Manager.py

import json
import logging
import inspect
from logging.handlers import RotatingFileHandler
from datetime import datetime
import importlib.util
import sys

logger = logging.getLogger('Tool_Manager')

log_filename = 'SCOUT.log'
log_max_size = 10 * 1024 * 1024  # 10 MB
log_backup_count = 5

# Create rotating file handler for file logging
rotating_handler = RotatingFileHandler(log_filename, maxBytes=log_max_size, backupCount=log_backup_count, encoding='utf-8')
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
rotating_handler.setFormatter(formatter)

# Create stream handler for console logging
stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)

# Attach handlers to the logger
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

class ToolManager:
    FUNCTIONS_JSON_PATH_TEMPLATE = 'modules/Personas/{}/Toolbox/functions.json'
    MAPS_PATH_TEMPLATE = 'modules/Personas/{}/Toolbox/maps.py'

    @staticmethod
    def get_required_args(function):
        sig = inspect.signature(function)
        return [param.name for param in sig.parameters.values() 
                if param.default == param.empty and param.name != 'self']

    @staticmethod
    def load_function_map_from_current_persona(current_persona):
        """
    Dynamically imports the function_map module based on the current persona's name.
    
    Parameters:
    - current_persona (dict): The current persona dictionary, expected to have a "name" key.
    
    Returns:
    - A reference to the function_map variable from the dynamically imported module.
    """
        persona_name = current_persona["name"]
        maps_path = ToolManager.MAPS_PATH_TEMPLATE.format(persona_name)
        module_name = f'persona_{persona_name}_maps'

        spec = importlib.util.spec_from_file_location(module_name, maps_path)
        module = importlib.util.module_from_spec(spec)
        sys.modules[module_name] = module
        spec.loader.exec_module(module)
        
        return module.function_map

    @staticmethod
    def load_functions_from_json(current_persona):
        """
    Dynamically loads functions definitions from a JSON file based on the current persona's name.
    
    Parameters:
    - current_persona (dict): The current persona dictionary, expected to have a "name" key.
    
    Returns:
    - The functions definitions as a Python dictionary.
    """
        persona_name = current_persona["name"]
        functions_json_path = ToolManager.FUNCTIONS_JSON_PATH_TEMPLATE.format(persona_name)
        
        try:
            with open(functions_json_path, 'r') as file:
                functions = json.load(file)
                logger.info("Functions loaded from file: %s", functions_json_path)
                return functions
        except FileNotFoundError:
            logger.error(f"Functions JSON file not found for persona: {persona_name}")
        except json.JSONDecodeError as e:
            logger.error(f"Error decoding JSON from {functions_json_path}: {e}")

        return {}

    @staticmethod
    async def handle_function_call(user, conversation_id, message, conversation_history, function_map):
       
       
        entry_time = datetime.now()
        logger.debug(f"Entering handle_function_call at {entry_time.isoformat()}")
        
        function_name = message["function_call"]["name"]
        function_args_json = message["function_call"].get("arguments", "{}")

        try:
            function_args = json.loads(function_args_json)
        except json.JSONDecodeError as e:
            logger.error(f"Error decoding JSON: {e}")
            function_args = {}

        conversation_history.add_function_call(user, conversation_id, function_name, function_args_json, datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

        if function_name in function_map:
            required_args = ToolManager.get_required_args(function_map[function_name])
            missing_args = set(required_args) - set(function_args.keys())

            if missing_args:
                logger.error(f"Not all required arguments provided for {function_name}. Missing: {', '.join(missing_args)}")
                return f"Error: Not all required arguments provided for {function_name}. Missing: {', '.join(missing_args)}", True

            try:
                function_response = await function_map[function_name](**function_args)
            except Exception as e:
                logger.error(f"Exception during function call {function_name}: {e}", exc_info=True)
                return f"Error: Exception during function call {function_name}: {e}", True

            exit_time = datetime.now()
            logger.debug(f"Exiting handle_function_call at {exit_time.isoformat()}, duration: {(exit_time-entry_time).total_seconds()} seconds")
            
            if not isinstance(function_response, str):
                function_response = str(function_response)

            return function_response, False

        logger.error(f"Function {function_name} not found in function map.")
        return None, True