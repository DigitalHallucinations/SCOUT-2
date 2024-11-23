#modules/Pubmed/ENTREZ_API.py

import requests
from typing import List, Dict
import json
from modules.logging.logger import setup_logger

logger = setup_logger('ENTREZ_API.py')

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
    
    pmids = data.get("esearchresult", {}).get("idlist", [])
    
    summaries_with_pmids = get_article_summaries(pmids)
    
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
            "pmid": pmid,  
            "title": article_data.get("result", {}).get(pmid, {}).get("title", ""),
            "authors": ", ".join([author.get("name", "") for author in article_data.get("result", {}).get(pmid, {}).get("authors", [])]),
            "source": article_data.get("result", {}).get(pmid, {}).get("source", ""),
            "pubdate": article_data.get("result", {}).get(pmid, {}).get("pubdate", "")
        }
        
        summaries.append(article_summary)
    
    return summaries

