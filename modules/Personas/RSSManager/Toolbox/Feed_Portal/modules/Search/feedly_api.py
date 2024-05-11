# modules/Search/feedly_api.py

import requests

class FeedlyAPI:
    def __init__(self, access_token):
       self.access_token = access_token
       self.base_url = "https://cloud.feedly.com/v3"

    def search_feeds(self, query):
        url = f"{self.base_url}/search/feeds"
        headers = {
           "Authorization": f"Bearer {self.access_token}"
        }
        params = {
           "query": query,
           "count": 20  # Adjust the count as needed
        }

        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()

        return response.json()["results"]