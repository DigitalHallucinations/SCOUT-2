# gui.Universal_Tools.Google_search

import os
import requests
from typing import Tuple, Union
from modules.Providers.OpenAI.openai_api import OpenAIAPI
import logging

from logging.handlers import RotatingFileHandler

logger = logging.getLogger('google_search.py')

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
    """Adjust the logging level.
    
    Parameters:
    - level (str): Desired logging level. Can be 'DEBUG', 'INFO', 'WARNING', 'ERROR', or 'CRITICAL'.
    """
    levels = {
        'DEBUG': logging.DEBUG,
        'INFO': logging.INFO,
        'WARNING': logging.WARNING,
        'ERROR': logging.ERROR,
        'CRITICAL': logging.CRITICAL
    }
    
    logger.setLevel(levels.get(level, logging.WARNING))

SERPAPI_KEY = os.getenv("SERPAPI_KEY")

class GoogleSearch:
    def __init__(self, api_key=SERPAPI_KEY):
        self.timeout = 10
        self.api_key = api_key
        self.openai_api = OpenAIAPI()

    async def _search(self, query: str) -> Tuple[int, Union[dict, str]]:
        """HTTP requests to SerpAPI."""
        
        logger.info("Starting search with term: %s", query)

        url = f"https://serpapi.com/search?q={query}&api_key={self.api_key}"
        logger.info("URL: %s", url)

        try:
            response = requests.get(url, timeout=self.timeout)
            logger.info("Response status code: %d", response.status_code)
            response.raise_for_status()
            return response.status_code, response.json()
        except requests.HTTPError as http_err:
            logger.error("Error during the request: %s", http_err)
            return response.status_code, str(http_err)
        except Exception as e:
            logger.error("An error occurred: %s", e)
            return -1, str(e)
