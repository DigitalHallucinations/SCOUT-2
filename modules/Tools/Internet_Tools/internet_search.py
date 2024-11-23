#modules/Tools/Internet_Tools/internet_search.py

import os
import requests
from typing import Tuple, Union
from modules.Providers.OpenAI.openai_api import OpenAIAPI
from bs4 import BeautifulSoup
from modules.logging.logger import setup_logger

logger = setup_logger('internet_search.py')

SERPAPI_KEY = os.getenv("SERPAPI_KEY")

def fetch_page_content(url):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching page content: {e}")
        return None

def extract_page_info(html):
    soup = BeautifulSoup(html, 'html.parser')
    
    title = soup.title.string if soup.title else ""
    main_content = soup.find('div', {'class': 'main-content'})
    content = main_content.get_text(strip=True) if main_content else ""
    
    return {'title': title, 'content': content}

class InternetSearch:
    def __init__(self, api_key=SERPAPI_KEY):
        self.timeout = 10
        self.api_key = api_key
        self.openai_api = OpenAIAPI()

    async def _search(self, query: str, summarize: bool = False) -> Tuple[int, Union[dict, str]]:
        logger.info("Starting search with term: %s", query)

        url = f"https://serpapi.com/search?q={query}&api_key={self.api_key}"
        logger.info("URL: %s", url)

        try:
            response = requests.get(url, timeout=self.timeout)
            logger.info("Response status code: %d", response.status_code)
            response.raise_for_status()
            
            if response.status_code == 200:
                search_results = response.json()
                
                top_result_url = search_results['organic_results'][0]['link']
                page_content = fetch_page_content(top_result_url)
                page_info = extract_page_info(page_content) if page_content else {}
                
                search_results['top_result_info'] = page_info
                
                if summarize:
                    summary = await self._summarize_results(search_results)
                    search_results['summary'] = summary
                
                return response.status_code, search_results
            
            return response.status_code, response.json()
        except requests.HTTPError as http_err:
            logger.error("Error during the request: %s", http_err)
            return response.status_code, str(http_err)
        except Exception as e:
            logger.error("An error occurred: %s", e)
            return -1, str(e)

    async def _summarize_results(self, results: dict) -> str:
        search_results_text = ' '.join([r['snippet'] for r in results['organic_results']])
        top_result_text = results['top_result_info'].get('content', '')
        
        results_text = f"{search_results_text}\n\nTop Result Content:\n{top_result_text}"
        
        logger.debug("Results text to be summarized: %s", results_text)
        chunk_size = 2500
        overlap = 100
        chunks = [results_text[i:i+chunk_size] for i in range(0, len(results_text), chunk_size-overlap)]
        
        logger.debug("Chunks to be summarized: %s", chunks)
        summarized_chunks = []
        
        for chunk in chunks:
            data = {
                "model": "gpt-4-turbo",
                "messages": [{"role": "user", "content": f"Summarize the following: {chunk}"}],
            }
            response_data = await self.openai_api.generate_response(data)
            logger.debug("Model Response for chunk: %s", response_data)
            
            if response_data:
                message = response_data["choices"][0]["message"]
                summarized_chunks.append(message["content"])
        
        return ' '.join(summarized_chunks)