# modules/Tools/Code_Execution/Python_interpreter_maps.py

from modules.Tools.Base_Tools.time import get_current_info
from modules.Tools.Base_Tools.Google_search import GoogleSearch
from modules.Tools.Base_Tools.TerminalCommand import TerminalCommand
from modules.Tools.Code_Execution.python_interpreter import PythonInterpreter
from modules.logging.logger import setup_logger

logger = setup_logger('Python_interpreter_maps')

# Create instances
python_interpreter = PythonInterpreter()
google_search_instance = GoogleSearch()

# A dictionary to map function names to actual function objects
function_map = {
    "get_current_info": get_current_info,
    "google_search": google_search_instance._search,
    "execute_python": python_interpreter.run,
    "terminal_command": TerminalCommand
}

"""
# Function descriptions
function_descriptions = [
    {
        "name": "execute_python",
        "description": "Execute Python code and return the result",
        "parameters": {
          "type": "object",
          "properties": {
            "code": {
              "type": "string",
              "description": "The Python code to execute"
            }
          },
          "required": ["code"]
        }
    }
    # Add descriptions for other functions here if needed
]
"""