#### Medical_Tools_Documentation.md

## ENTREZ_API.py
----------------

This file implements functions to interact with the NCBI Entrez API, specifically for searching PubMed articles.

Key Components:

a) Imports:
   - requests: For making HTTP requests
   - typing: For type hinting
   - json: For JSON parsing
   - setup_logger: Custom logging setup

b) Constants:
   - ENTREZ_API_BASE_URL: Base URL for the Entrez API
   - SEARCH_ENDPOINT: Endpoint for search operations
   - SUMMARY_ENDPOINT: Endpoint for summary operations
   - DATABASE: Set to "pubmed" for PubMed searches
   - RETURN_TYPE: Set to "json" for JSON responses

c) Main Functions:

1. async def search_pubmed(query: str, max_results: int) -> str:
   - Purpose: Search PubMed for articles related to the provided query
   - Parameters:
     * query: The search term
     * max_results: Maximum number of results to return
   - Returns: JSON string containing search results with PMIDs

   Process:
   - Constructs the search URL with parameters
   - Sends a GET request to the Entrez API
   - Extracts PMIDs from the response
   - Fetches summaries for the found PMIDs
   - Returns the results as a JSON string

2. def get_article_summaries(pmids: List[str]) -> List[Dict[str, str]]:
   - Purpose: Fetch summaries for a list of PubMed IDs (PMIDs)
   - Parameters:
     * pmids: List of PMIDs to fetch summaries for
   - Returns: List of dictionaries containing article summaries

   Process:
   - For each PMID, sends a request to the summary endpoint
   - Extracts relevant information (title, authors, source, publication date)
   - Returns a list of formatted article summaries

Error Handling:
- Logs errors for failed requests or JSON parsing issues
- Returns appropriate error messages in case of failures

## PMC_API.py
-------------

This file provides functionality to interact with the PubMed Central (PMC) API for retrieving full-text articles.

Key Components:

a) Imports:
   - aiohttp: For asynchronous HTTP requests
   - xml.etree.ElementTree: For parsing XML responses
   - os, urllib.request, tarfile: For file operations
   - setup_logger: Custom logging setup

b) Constants:
   - PMC_BASE_URL: Base URL for the PMC API

c) Main Functions:

1. async def search_pmc(pmcid: str):
   - Purpose: Search for a specific article in PMC by its PMCID
   - Parameters:
     * pmcid: PubMed Central ID of the article
   - Returns: None (downloads the article package if available)

   Process:
   - Constructs the URL for the PMC API request
   - Sends an asynchronous GET request
   - Parses the XML response to find the download link
   - If a link is found, calls download_article_package()

2. def download_article_package(url: str, destination_path: str):
   - Purpose: Download and extract the article package
   - Parameters:
     * url: URL of the article package
     * destination_path: Where to save the downloaded package
   
   Process:
   - Downloads the compressed article package
   - Extracts the contents to the specified destination
   - Removes the temporary compressed file

3. async def fetch(session, url):
   - Purpose: Helper function to fetch data from a URL
   - Parameters:
     * session: aiohttp ClientSession object
     * url: URL to fetch data from
   - Returns: Text content of the response

Error Handling:
- Logs warnings or errors for various scenarios (parsing errors, download issues)
- Provides informative log messages for each step of the process

Both these modules work together to provide a comprehensive solution for searching and retrieving articles from PubMed and PubMed Central. 
The ENTREZ_API.py focuses on searching and retrieving metadata, while PMC_API.py handles the retrieval of full-text articles when available.
They use asynchronous programming to improve performance when dealing with multiple requests or large datasets.