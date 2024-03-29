# modules/OpenAI/maps.py

from modules.Time.time import get_current_time, get_current_date
from modules.location_services.ip_api import get_current_location
from modules.location_services.geocode import geocode_location
from modules.News.newsapi import get_everything, get_top_headlines, get_sources

# A dictionary to map function names to actual function objects
function_map = {
        "get_current_time": get_current_time,
        "get_current_date": get_current_date,
        "get_current_location": get_current_location,  
        "geocode_location": geocode_location,
        "get_everything": get_everything,
        "get_top_headlines": get_top_headlines,
        "get_sources": get_sources
    }

prefix_map = {
        "get_current_location": "Your current location is: ",
        "geocode_location": "The geocoded coordinates are: ",
        "get_current_time": "The current time is: ",
        "get_current_date": "Today's date is: ",
        'get_everything': 'Here are the top stories: ',
        'get_top_headlines': 'Here are the top headlines: ',
        'get_sources': 'Here are the sources: '
    }
