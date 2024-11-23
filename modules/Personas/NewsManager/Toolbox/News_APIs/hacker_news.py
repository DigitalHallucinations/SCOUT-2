import aiohttp
import json

base_url = "https://hacker-news.firebaseio.com/v0/"

async def fetch(session, url):
    async with session.get(url) as response:
        return await response.text()

async def get_top_stories():
    url = f"{base_url}/topstories.json"
    async with aiohttp.ClientSession() as session:
        result = await fetch(session, url)
        return json.loads(result)

async def get_new_stories():
    url = f"{base_url}/newstories.json"
    async with aiohttp.ClientSession() as session:
        result = await fetch(session, url)
        return json.loads(result)

async def get_best_stories():
    url = f"{base_url}/beststories.json"
    async with aiohttp.ClientSession() as session:
        result = await fetch(session, url)
        return json.loads(result)
