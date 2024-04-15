import requests
from bs4 import BeautifulSoup
import logging
from logging.handlers import RotatingFileHandler
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

logger = logging.getLogger('webpage_retriever.py')

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

class WebpageRetriever:
    def __init__(self, timeout=10):
        self.timeout = timeout
        chrome_options = Options()
        chrome_options.add_argument("--headless")  # Run Chrome in headless mode
        self.driver = webdriver.Chrome(options=chrome_options)

    async def retrieve_page(self, url: str, capture_screenshot: bool = False) -> dict:
        logger.info(f"Retrieving page content from URL: {url}")

        try:
            response = requests.get(url, timeout=self.timeout)
            response.raise_for_status()

            logger.info(f"Response status code: {response.status_code}")

            soup = BeautifulSoup(response.text, 'html.parser')
            page_content = soup.get_text(separator='\n', strip=True)

            screenshot_base64 = ""
            if capture_screenshot:
                self.driver.get(url)
                screenshot = self.driver.get_screenshot_as_base64()
                screenshot_base64 = f"data:image/png;base64,{screenshot}"

            logger.info(f"Page content retrieved successfully")

            return {
                "content": page_content,
                "screenshot": screenshot_base64
            }

        except requests.exceptions.RequestException as e:
            logger.error(f"Error occurred while retrieving page content: {e}")
            return {
                "content": "",
                "screenshot": ""
            }

    def __del__(self):
        self.driver.quit()