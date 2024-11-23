from modules.Tools.Internet_Tools.internet_search import InternetSearch
from modules.Tools.Internet_Tools.webpage_retriever import WebpageRetriever
from modules.Personas.FeedManager.Toolbox.Feed_Portal.modules.rss_feed_reader import RSSFeedReader

internet_search_instance = InternetSearch()
webpage_retriever_instance = WebpageRetriever()
rss_feed_reader_instance = RSSFeedReader()

function_map = {
    "internet_search": internet_search_instance._search,
    "webpage_retriever": webpage_retriever_instance.retrieve_page,
    "rss_feed_reader": {
        "add_feed": rss_feed_reader_instance.add_feed,
        "remove_feed": rss_feed_reader_instance.remove_feed,
        "get_feeds": rss_feed_reader_instance.get_feeds,
        "update_feed": rss_feed_reader_instance.update_feed,
        "get_feed_entries": rss_feed_reader_instance.get_feed_entries,
        "get_entry_details": rss_feed_reader_instance.get_entry_details,
        "remove_entry": rss_feed_reader_instance.remove_entry
    }
}