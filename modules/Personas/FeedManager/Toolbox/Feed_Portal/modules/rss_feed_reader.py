# Feed portal/rss_feed_reader.py

import feedparser
import chardet
import requests
from urllib.parse import urlparse
from modules.logging.logger import setup_logger
import asyncio

logger = setup_logger('rss_feed_reader')

class RSSFeedReaderError(Exception):
    pass

class RSSFeed:
    def __init__(self, url, category=None, enabled=True):
        self.url = url
        self.category = category
        self.enabled = enabled

class RSSFeedReader:
    def __init__(self):
        self.feeds = []

    async def is_valid_feed_url(self, feed_url):
        try:
            parsed_url = urlparse(feed_url)
            return parsed_url.scheme and parsed_url.netloc
        except Exception as e:
            logger.exception(f"Error occurred while validating feed URL: {str(e)}")
            return False

    async def add_feed(self, feed_url, category=None):
        logger.info(f"Adding RSS feed: {feed_url}")
        if not await self.is_valid_feed_url(feed_url):
            logger.warning(f"Invalid feed URL: {feed_url}")
            raise RSSFeedReaderError(f"Invalid feed URL: {feed_url}. Please provide a valid RSS feed URL.")
        try:
            feed = RSSFeed(feed_url, category)
            self.feeds.append(feed)
            logger.info(f"RSS feed added successfully: {feed_url}")
        except Exception as e:
            logger.exception(f"Error occurred while adding RSS feed: {str(e)}")
            raise RSSFeedReaderError(f"Failed to add RSS feed: {feed_url}. Please check the URL and try again.")

    async def remove_entry(self, feed_url, entry_title):
        for feed in self.feeds:
            if feed.url == feed_url:
                feed.entries = [entry for entry in feed.entries if entry.title != entry_title]
                break

    async def remove_feed(self, feed_url):
        logger.info(f"Removing RSS feed: {feed_url}")
        try:
            self.feeds = [feed for feed in self.feeds if feed.url != feed_url]
            logger.info(f"RSS feed removed successfully: {feed_url}")
        except Exception as e:
            logger.exception(f"Error occurred while removing RSS feed: {str(e)}")
            raise RSSFeedReaderError(f"Failed to remove RSS feed: {feed_url}. An unexpected error occurred.")

    async def get_feeds(self, category=None, enabled=True):
        logger.info("Retrieving RSS feeds")
        if category:
            feeds = [feed for feed in self.feeds if feed.category == category and feed.enabled == enabled]
        else:
            feeds = [feed for feed in self.feeds if feed.enabled == enabled]
        return feeds

    async def update_feed(self, feed_url, category=None, enabled=None):
        logger.info(f"Updating RSS feed: {feed_url}")
        try:
            feed = next((feed for feed in self.feeds if feed.url == feed_url), None)
            if feed:
                if category is not None:
                    feed.category = category
                if enabled is not None:
                    feed.enabled = enabled
                logger.info(f"RSS feed updated successfully: {feed_url}")
            else:
                logger.warning(f"RSS feed not found: {feed_url}")
                raise RSSFeedReaderError(f"RSS feed not found: {feed_url}. Please provide a valid feed URL.")
        except Exception as e:
            logger.exception(f"Error occurred while updating RSS feed: {str(e)}")
            raise RSSFeedReaderError(f"Failed to update RSS feed: {feed_url}. An unexpected error occurred.")

    async def parse_feed(self, feed_url):
        logger.info(f"Parsing RSS feed: {feed_url}")
        try:
            feed = feedparser.parse(feed_url)
            if feed.bozo:
                logger.warning(f"Error parsing RSS feed: {feed.bozo_exception}")
                raise RSSFeedReaderError(f"Failed to parse RSS feed: {feed_url}. Please check the feed format and try again.")
            else:
                logger.info(f"RSS feed parsed successfully: {feed_url}")
                return feed
        except Exception as e:
            logger.exception(f"Error occurred while parsing RSS feed: {str(e)}")
            raise RSSFeedReaderError(f"Failed to parse RSS feed: {feed_url}. An unexpected error occurred.")

    async def get_feed_entries(self, feed_url):
        logger.info(f"Retrieving entries from feed: {feed_url}")
        try:
            response = requests.get(feed_url)
            encoding = chardet.detect(response.content)['encoding']
            content = response.content.decode(encoding)
            feed = feedparser.parse(content)
            if feed.bozo:
                feed_format = feed.version
                if feed_format.startswith('rss'):
                    logger.info(f"Detected RSS feed format: {feed_format}")
                elif feed_format.startswith('atom'):
                    logger.info(f"Detected Atom feed format: {feed_format}")
                elif feed_format.startswith('rdf'):
                    logger.info(f"Detected RDF feed format: {feed_format}")
                else:
                    logger.warning(f"Unknown feed format: {feed_format}")
                    return []
            entries = feed.entries
            logger.info(f"Retrieved {len(entries)} entries from feed: {feed_url}")
            return entries
        except Exception as e:
            logger.exception(f"Error occurred while retrieving entries from feed: {str(e)}")
            return []

    async def get_entry_details(self, entry):
        logger.info(f"Retrieving details for entry: {getattr(entry, 'title', 'N/A')}")
        try:
            entry_details = {
                'title': getattr(entry, 'title', ''),
                'link': getattr(entry, 'link', ''),
                'published': getattr(entry, 'published', ''),
                'summary': getattr(entry, 'summary', '')
            }
            logger.info(f"Retrieved details for entry: {getattr(entry, 'title', 'N/A')}")
            return entry_details
        except Exception as e:
            logger.exception(f"Error occurred while retrieving entry details: {str(e)}")
            raise RSSFeedReaderError(f"Failed to retrieve details for entry. An unexpected error occurred.")

    async def get_categories(self):
        logger.info("Retrieving categories from RSS feeds")
        try:
            categories = set()
            for feed in self.feeds:
                if feed.category:
                    categories.add(feed.category)
            logger.info(f"Retrieved {len(categories)} categories from RSS feeds")
            return list(categories)
        except Exception as e:
            logger.exception(f"Error occurred while retrieving categories: {str(e)}")
            raise RSSFeedReaderError(f"Failed to retrieve categories. An unexpected error occurred.")

    async def sort_entries(self, entries, sorting):
        logger.info(f"Sorting entries based on {sorting['method']} in {sorting['order']} order")
        try:
            if sorting['method'] == 'date':
                entries.sort(key=lambda entry: getattr(entry, 'published_parsed', ''), reverse=(sorting['order'] == 'descending'))
            elif sorting['method'] == 'title':
                entries.sort(key=lambda entry: getattr(entry, 'title', ''), reverse=(sorting['order'] == 'descending'))
            logger.info("Entries sorted successfully")
            return entries
        except Exception as e:
            logger.exception(f"Error occurred while sorting entries: {str(e)}")
            raise RSSFeedReaderError(f"Failed to sort entries. An unexpected error occurred.")

    async def search_feeds_by_keyword(self, keyword):
        matching_feeds = []
        for feed in self.feeds:
            if keyword.lower() in feed.url.lower() or keyword.lower() in feed.category.lower():
                matching_feeds.append(feed)
        return matching_feeds

    async def filter_feeds_by_category(self, category):
        filtered_feeds = [feed for feed in self.feeds if feed.category == category]
        return filtered_feeds