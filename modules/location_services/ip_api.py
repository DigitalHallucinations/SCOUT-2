#modules/location_services/ip_api.py

import aiohttp
import os

IP_API_URL = "http://ip-api.com/json"

async def get_current_location():
    """Get the current location using the IP-API service."""
    async with aiohttp.ClientSession() as session:
        async with session.get(IP_API_URL) as response:
            if response.status == 200:
                data = await response.json()
                if 'status' in data and data['status'] == 'fail':
                    return {'error': "Could not get current location from IP-API"}
                return data
            else:
                return {'error': f"Error: {response.status}"}