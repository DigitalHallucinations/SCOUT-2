# modules/OpenAI/maps.py

from modules.Tools.Base_Tools.time import get_current_time, get_current_date
from modules.Tools.location_services.ip_api import get_current_location
from modules.Tools.location_services.geocode import geocode_location
from modules.Personas.NewsManager.Toolbox.News_APIs.hacker_news import get_top_stories, get_new_stories, get_best_stories

# A dictionary to map function names to actual function objects
function_map = {
        "get_current_time": get_current_time,
        "get_current_date": get_current_date,
        "get_current_location": get_current_location,  
        "geocode_location": geocode_location,
        "get_top_stories": get_top_stories,
        "get_new_stories": get_new_stories,
        "get_best_stories": get_best_stories,
    }

prefix_map = {
        "get_current_location": "Your current location is: ",
        "geocode_location": "The geocoded coordinates are: ",
        "get_current_time": "The current time is: ",
        "get_current_date": "Today's date is: ",
        "get_top_stories": "The top stories are: ",
        "get_new_stories": "The new stories are: ",
        "get_best_stories": "The best stories are: ",
    }
