#modules/Tools/Internet_Tools/web_scraper.py

import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import json
import csv
import time
from modules.logging.logger import setup_logger

logger = setup_logger('web_scraper.py')

class WebScraper:
    def __init__(self, use_selenium=False, headless=True):
        self.use_selenium = use_selenium
        self.headless = headless
        if self.use_selenium:
            self.setup_selenium()

    def setup_selenium(self):
        logger.info("Setting up Selenium WebDriver")
        chrome_options = Options()
        if self.headless:
            chrome_options.add_argument("--headless")
        self.driver = webdriver.Chrome(options=chrome_options)

    def scrape(self, url, target_elements, method='css', paginate=False, max_pages=None, javascript=False):
        logger.info(f"Scraping URL: {url}")
        scraped_data = []

        if self.use_selenium and javascript:
            self.driver.get(url)
            if paginate:
                scraped_data = self.paginate_selenium(target_elements, method, max_pages)
            else:
                page_source = self.driver.page_source
                scraped_data = self.parse_html(page_source, target_elements, method)
        else:
            response = requests.get(url)
            if response.status_code == 200:
                if paginate:
                    scraped_data = self.paginate_requests(url, target_elements, method, max_pages)
                else:
                    scraped_data = self.parse_html(response.text, target_elements, method)
            else:
                logger.error(f"Failed to retrieve the webpage. Status code: {response.status_code}")

        return scraped_data

    def paginate_requests(self, url, target_elements, method, max_pages):
        logger.info("Paginating using requests")
        scraped_data = []
        page = 1

        while True:
            logger.info(f"Scraping page {page}")
            response = requests.get(f"{url}?page={page}")
            if response.status_code == 200:
                page_data = self.parse_html(response.text, target_elements, method)
                scraped_data.extend(page_data)
                page += 1
                if max_pages and page > max_pages:
                    break
            else:
                logger.warning(f"Failed to retrieve page {page}. Status code: {response.status_code}")
                break

        return scraped_data

    def paginate_selenium(self, target_elements, method, max_pages):
        logger.info("Paginating using Selenium")
        scraped_data = []
        page = 1

        while True:
            logger.info(f"Scraping page {page}")
            page_source = self.driver.page_source
            page_data = self.parse_html(page_source, target_elements, method)
            scraped_data.extend(page_data)
            page += 1
            if max_pages and page > max_pages:
                break

            try:
                next_button = self.driver.find_element_by_css_selector("a[rel='next']")
                next_button.click()
                time.sleep(2)  # Wait for page load
            except:
                logger.info("No more pages to scrape")
                break

        return scraped_data

    def parse_html(self, html, target_elements, method):
        logger.info("Parsing HTML")
        soup = BeautifulSoup(html, 'html.parser')
        scraped_data = []

        for selector in target_elements:
            if method == 'css':
                elements = soup.select(selector)
            elif method == 'xpath':
                elements = soup.xpath(selector)
            else:
                logger.error(f"Invalid method: {method}")
                return []

            for element in elements:
                scraped_data.append(element.get_text(strip=True))

        return scraped_data

    def export_csv(self, data, filename):
        logger.info(f"Exporting data to CSV: {filename}")
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Data'])
            for item in data:
                writer.writerow([item])

    def export_json(self, data, filename):
        logger.info(f"Exporting data to JSON: {filename}")
        with open(filename, 'w', encoding='utf-8') as jsonfile:
            json.dump(data, jsonfile, ensure_ascii=False, indent=4)

    def quit(self):
        if self.use_selenium:
            logger.info("Quitting Selenium WebDriver")
            self.driver.quit()