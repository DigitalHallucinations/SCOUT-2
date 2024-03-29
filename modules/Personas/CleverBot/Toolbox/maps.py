# modules\Personas\CleveBot\Toolbox\maps.py

from modules.Time.time import get_current_info
from modules.Tools.Base_Tools.Google_search import GoogleSearch

# Create an instance of GoogleSearch
google_search_instance = GoogleSearch()

# A dictionary to map function names to actual function objects
function_map = {
    "get_current_info": get_current_info,
    "google_search": google_search_instance._search
}