# modules/Tools/Intenet_Tools/RSS/rss_feed_reader.py

import feedparser
import logging
from logging.handlers import RotatingFileHandler
from urllib.parse import urlparse

logger = logging.getLogger('rss_feed_reader.py')

log_filename = 'SCOUT.log'
log_max_size = 10 * 1024 * 1024  # 10 MB
log_backup_count = 5

rotating_handler = RotatingFileHandler(log_filename, maxBytes=log_max_size, backupCount=log_backup_count, encoding='utf-8')
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
rotating_handler.setFormatter(formatter)

stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)

logger.addHandler(rotating_handler)
logger.addHandler(stream_handler)
logger.setLevel(logging.INFO)

def adjust_logging_level(level):
    levels = {
        'DEBUG': logging.DEBUG,
        'INFO': logging.INFO,
        'WARNING': logging.WARNING,
        'ERROR': logging.ERROR,
        'CRITICAL': logging.CRITICAL
    }
    logger.setLevel(levels.get(level, logging.WARNING))

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

    def is_valid_feed_url(self, feed_url):
        try:
            parsed_url = urlparse(feed_url)
            return parsed_url.scheme and parsed_url.netloc
        except Exception as e:
            logger.exception(f"Error occurred while validating feed URL: {str(e)}")
            return False

    def add_feed(self, feed_url, category=None):
        logger.info(f"Adding RSS feed: {feed_url}")
        if not self.is_valid_feed_url(feed_url):
            logger.warning(f"Invalid feed URL: {feed_url}")
            raise RSSFeedReaderError(f"Invalid feed URL: {feed_url}. Please provide a valid RSS feed URL.")
        try:
            feed = RSSFeed(feed_url, category)
            self.feeds.append(feed)
            logger.info(f"RSS feed added successfully: {feed_url}")
        except Exception as e:
            logger.exception(f"Error occurred while adding RSS feed: {str(e)}")
            raise RSSFeedReaderError(f"Failed to add RSS feed: {feed_url}. Please check the URL and try again.")

    def remove_entry(self, feed_url, entry_title):
        for feed in self.feeds:
            if feed.url == feed_url:
                feed.entries = [entry for entry in feed.entries if entry.title != entry_title]
                break

    def remove_feed(self, feed_url):
        logger.info(f"Removing RSS feed: {feed_url}")
        try:
            self.feeds = [feed for feed in self.feeds if feed.url != feed_url]
            logger.info(f"RSS feed removed successfully: {feed_url}")
        except Exception as e:
            logger.exception(f"Error occurred while removing RSS feed: {str(e)}")
            raise RSSFeedReaderError(f"Failed to remove RSS feed: {feed_url}. An unexpected error occurred.")

    def get_feeds(self, category=None, enabled=True):
        logger.info("Retrieving RSS feeds")
        if category:
            feeds = [feed for feed in self.feeds if feed.category == category and feed.enabled == enabled]
        else:
            feeds = [feed for feed in self.feeds if feed.enabled == enabled]
        return feeds

    def update_feed(self, feed_url, category=None, enabled=None):
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

    def parse_feed(self, feed_url):
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

    def get_feed_entries(self, feed_url):
        logger.info(f"Retrieving entries from RSS feed: {feed_url}")
        try:
            feed = self.parse_feed(feed_url)
            if feed:
                entries = feed.entries
                logger.info(f"Retrieved {len(entries)} entries from RSS feed: {feed_url}")
                return entries
        except RSSFeedReaderError as e:
            logger.exception(f"Error occurred while retrieving entries from RSS feed: {str(e)}")
            raise e
        except Exception as e:
            logger.exception(f"Error occurred while retrieving entries from RSS feed: {str(e)}")
            raise RSSFeedReaderError(f"Failed to retrieve entries from RSS feed: {feed_url}. An unexpected error occurred.")

    def get_entry_details(self, entry):
        logger.info(f"Retrieving details for entry: {entry.title}")
        try:
            entry_details = {
                'title': entry.title,
                'link': entry.link,
                'published': entry.published,
                'summary': entry.summary
            }
            logger.info(f"Retrieved details for entry: {entry.title}")
            return entry_details
        except AttributeError as e:
            logger.exception(f"Error occurred while retrieving entry details: {str(e)}")
            raise RSSFeedReaderError(f"Failed to retrieve details for entry. The required attributes are missing.")
        except Exception as e:
            logger.exception(f"Error occurred while retrieving entry details: {str(e)}")
            raise RSSFeedReaderError(f"Failed to retrieve details for entry. An unexpected error occurred.")