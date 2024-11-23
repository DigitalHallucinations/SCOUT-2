# modules\Personas\SCOUT\Toolbox\maps.py

from modules.Tools.Base_Tools.time import get_current_info
from modules.Tools.Base_Tools.Google_search import GoogleSearch
from modules.Tools.Planning.calendar import Calendar

# Create an instance of GoogleSearch
google_search_instance = GoogleSearch()

# Create an instance of Calendar
calendar_instance = Calendar()

# A dictionary to map function names to actual function objects
function_map = {
    "get_current_info": get_current_info,
    "google_search": google_search_instance._search,
    "Calendar": calendar_instance.handle_action
}