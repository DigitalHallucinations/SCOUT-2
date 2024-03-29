#modules/Pubmed/ENTREZ_API.py

import requests
from typing import List, Dict
import json
import logging
from logging.handlers import RotatingFileHandler

logger = logging.getLogger('ENTREZ_API.py')

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
 


# Constants for the Entrez API
ENTREZ_API_BASE_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"
SEARCH_ENDPOINT = "/esearch.fcgi"
SUMMARY_ENDPOINT = "/esummary.fcgi"
DATABASE = "pubmed"
RETURN_TYPE = "json"

async def search_pubmed(query: str, max_results: int) -> str:
    """Search PubMed for articles related to the provided query and return results with PMIDs as a JSON string."""
    search_url = f"{ENTREZ_API_BASE_URL}{SEARCH_ENDPOINT}"
    logger.info(f"Initiating PubMed search with query: {query}")
    
    search_params = {
        "db": DATABASE,
        "term": query,
        "retmode": RETURN_TYPE,
        "retmax": max_results
    }
    
    response = requests.get(search_url, params=search_params)
    logger.info( f"Received response for query: {query}")
    data = response.json()
    
    # Extract the list of PubMed IDs from the search results
    pmids = data.get("esearchresult", {}).get("idlist", [])
    
    # Fetch a list of article summaries with PMIDs
    summaries_with_pmids = get_article_summaries(pmids)
    
    # Convert the list of summaries to a JSON string
    return json.dumps(summaries_with_pmids, ensure_ascii=False)

def get_article_summaries(pmids: List[str]) -> List[Dict[str, str]]:
    """Fetches summaries with PMIDs for a list of PubMed IDs."""
    summary_url = f"{ENTREZ_API_BASE_URL}{SUMMARY_ENDPOINT}"
    logger.info( f"Fetching article details with PMIDs for: {pmids}")
    summaries = []
    
    for pmid in pmids:
        summary_params = {
            "db": DATABASE,
            "id": pmid,
            "retmode": RETURN_TYPE
        }
        
        response = requests.get(summary_url, params=summary_params)
        article_data = response.json()
        
        article_summary = {
            "pmid": pmid,  # Adding the PMID
            "title": article_data.get("result", {}).get(pmid, {}).get("title", ""),
            "authors": ", ".join([author.get("name", "") for author in article_data.get("result", {}).get(pmid, {}).get("authors", [])]),
            "source": article_data.get("result", {}).get(pmid, {}).get("source", ""),
            "pubdate": article_data.get("result", {}).get(pmid, {}).get("pubdate", "")
        }
        
        summaries.append(article_summary)
    
    return summaries

