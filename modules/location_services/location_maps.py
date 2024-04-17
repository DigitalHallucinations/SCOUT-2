# modules/OpenAI/maps.py

from modules.location_services.ip_api import get_current_location
from modules.location_services.geocode import geocode_location

function_map = {      
        "get_current_location": get_current_location,  
        "geocode_location": geocode_location,
    }

prefix_map = {
        "get_current_location": "Your current location is: ",
        "geocode_location": "The geocoded coordinates are: ",
    }
