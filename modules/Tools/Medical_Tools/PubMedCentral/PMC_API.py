#modules/Pubmed/PMC_API.py

import aiohttp
import xml.etree.ElementTree as ET
import os
import logging
from dotenv import load_dotenv
import urllib.request
import tarfile
from logging.handlers import RotatingFileHandler

logger = logging.getLogger('PMC_API.py')

log_filename = 'SCOUT.log'
log_max_size = 10 * 1024 * 1024  # 10 MB
log_backup_count = 5

# Create rotating file handler for file logging
rotating_handler = RotatingFileHandler(log_filename, maxBytes=log_max_size, backupCount=log_backup_count, encoding='utf-8')
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
rotating_handler.setFormatter(formatter)

# Create stream handler for console logging
stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)

# Attach handlers to the logger
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


load_dotenv()
API_KEY = os.getenv("NCBI_API_KEY")
 
# Base URL for the PMC OA Web Service API
PMC_BASE_URL = "https://www.ncbi.nlm.nih.gov/pmc/utils/oa/oa.fcgi"

async def search_pmc(pmcid: str):
    url = f"{PMC_BASE_URL}?id={pmcid}"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            xml_response = await response.text()
            if response.status == 200:
                try:
                    root = ET.fromstring(xml_response)
                    link_element = root.find(".//link[@format='tgz']")
                    if link_element is not None:
                        download_url = link_element.get('href')
                        destination_path = os.path.join("Workspace", f"{pmcid}.tar.gz")
                        download_article_package(download_url, destination_path)
                    else:
                        logger.info("No download link found in the XML response.")
                except ET.ParseError:
                    logger.info(f"Failed to parse response as XML. Response: {xml_response}")
            else:
                logger.info(f"Error {response.status}. Raw response: {xml_response}")

def download_article_package(url: str, destination_path: str):
    os.makedirs(os.path.dirname(destination_path), exist_ok=True)
    tmp_path = destination_path + '.tar.gz'
    urllib.request.urlretrieve(url, tmp_path)
    logger.info(f"Compressed article package downloaded to {tmp_path}")
    with tarfile.open(tmp_path, 'r:gz') as file:
        file.extractall(path=os.path.dirname(destination_path))
    logger.info(f"Article package extracted to {os.path.dirname(destination_path)}")
    os.remove(tmp_path)
    logger.info(f"Removed temporary file {tmp_path}")

# Test the function with a known PMCID
#if __name__ == "__main__":
    #import asyncio
    #asyncio.run(search_pmc("PMC7646041"))
