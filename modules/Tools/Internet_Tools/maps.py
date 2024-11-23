# modules/Tools/Intenet_Tools/maps.py

from modules.Tools.Base_Tools.time import get_current_info
from modules.Tools.Internet_Tools.internet_search import InternetSearch
from modules.Tools.Internet_Tools.webpage_retriever import WebpageRetriever
from modules.Tools.Internet_Tools.web_scraper import WebScraper

internet_search_instance = InternetSearch()
webpage_retriever_instance = WebpageRetriever()
web_scraper_instance = WebScraper()

function_map = {
    "get_current_info": get_current_info,
    "internet_search": internet_search_instance._search,
    "webpage_retriever": webpage_retriever_instance.retrieve_page,
    "web_scraper": web_scraper_instance.scrape
}