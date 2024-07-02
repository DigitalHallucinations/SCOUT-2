# modules\Personas\CodeGenius\Toolbox\maps.py

from modules.Tools.Base_Tools.time import get_current_info
from modules.Tools.Base_Tools.Google_search import GoogleSearch
from modules.Tools.Base_Tools.TerminalCommand import TerminalCommand
from modules.Tools.Code_Execution.python_interpreter import PythonInterpreter

# Create an instance of PythonInterpreter
python_interpreter = PythonInterpreter()

# Create an instance of GoogleSearch
google_search_instance = GoogleSearch()

# A dictionary to map function names to actual function objects
function_map = {
    "get_current_info": get_current_info,
    "google_search": google_search_instance._search,
    "execute_python": python_interpreter.run,
    "terminal_command": TerminalCommand
}
