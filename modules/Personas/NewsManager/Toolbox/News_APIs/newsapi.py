# modules\News\newsapi.py   

import aiohttp
import json
from dotenv import load_dotenv
import os

load_dotenv()  

NEWSAPI_BASE_URL = "https://newsapi.org/v2/"
NEWSAPI_API_KEY = os.getenv("NEWSAPI_API_KEY")  

async def fetch(session, url, params=None):
    headers = {"X-Api-Key": NEWSAPI_API_KEY}
    async with session.get(url, headers=headers, params=params) as response:
        return await response.text()

async def get_everything(q=None, searchIn=None, sources=None, domains=None, excludeDomains=None,
                         from_=None, to=None, language=None, sortBy=None, pageSize=None, page=None):
    params = locals()  
    params = {k: v for k, v in params.items() if v is not None}  
    params['from'] = params.pop('from_', None)  

    url = f"{NEWSAPI_BASE_URL}/everything"
    async with aiohttp.ClientSession() as session:
        result = await fetch(session, url, params=params)
        return json.loads(result)

async def get_top_headlines(country=None, category=None, sources=None, q=None, pageSize=None, page=None, language=None):
    params = locals()  
    params = {k: v for k, v in params.items() if v is not None}  

    url = f"{NEWSAPI_BASE_URL}/top-headlines"
    async with aiohttp.ClientSession() as session:
        result = await fetch(session, url, params=params)
        return json.loads(result)

async def get_sources(category=None, language=None, country=None):
    params = locals()  
    params = {k: v for k, v in params.items() if v is not None} 

    url = f"{NEWSAPI_BASE_URL}/sources"
    async with aiohttp.ClientSession() as session:
        result = await fetch(session, url, params=params)
        return json.loads(result)
