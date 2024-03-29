# modules\Personas\NewsMaager\Toolbox\maps.py

from modules.Time.time import get_current_info
from modules.Tools.Base_Tools.Google_search import GoogleSearch
from .News_APIs.hacker_news import get_top_stories, get_new_stories, get_best_stories
from .News_APIs.newsapi import get_everything, get_top_headlines, get_sources

# Create an instance of GoogleSearch
google_search_instance = GoogleSearch()

# A dictionary to map function names to actual function objects
function_map = {

    "get_current_info": get_current_info,
    "get_top_stories": get_top_stories,
    "get_new_stories": get_new_stories,
    "get_best_stories": get_best_stories,
    "get_everything": get_everything,
    "get_top_headlines": get_top_headlines,
    "get_sources": get_sources,
    "google_search": google_search_instance._search
}