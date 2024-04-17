import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from modules.logging.logger import setup_logger

logger = setup_logger('webpage_retriever.py')

class WebpageRetriever:
    def __init__(self, timeout=10):
        self.timeout = timeout
        chrome_options = Options()
        chrome_options.add_argument("--headless")  
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