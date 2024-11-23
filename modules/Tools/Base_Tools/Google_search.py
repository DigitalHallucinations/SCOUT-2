# gui.Universal_Tools.Google_search

import os
import requests
from typing import Tuple, Union
from modules.Providers.OpenAI.openai_api import OpenAIAPI
from modules.logging.logger import setup_logger

logger = setup_logger('google_search.py')

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
