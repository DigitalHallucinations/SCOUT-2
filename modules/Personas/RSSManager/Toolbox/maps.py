# modules\Personas\RSSManager\Toolbox\maps.py

from modules.Tools.Internet_Tools.internet_search import InternetSearch
from modules.Tools.Internet_Tools.webpage_retriever import WebpageRetriever
from modules.Personas.RSSManager.Toolbox.Feed_Portal.modules.rss_feed_reader import RSSFeedReader


internet_search_instance = InternetSearch()
webpage_retriever_instance = WebpageRetriever()
rss_feed_reader_instance = RSSFeedReader()


function_map = {
    "internet_search": internet_search_instance._search,
    "webpage_retriever": webpage_retriever_instance.retrieve_page,
    "rss_feed_reader": rss_feed_reader_instance
}