# modules/location_services/geocode.py

import aiohttp
import os

DEBUG_MODE = False  # Set this flag to True to enable debug statements

async def geocode_location(location):
    """Get the coordinates of a location by its name using OpenWeather's Geocoding API"""
    OPENWEATHER_API_KEY = os.environ['OPENWEATHERMAP_API_KEY']
    BASE_URL = "http://api.openweathermap.org/geo/1.0/direct"

    params = {
        'q': location,
        'limit': 1,  # only the first location is needed
        'appid': OPENWEATHER_API_KEY,
    }

    if DEBUG_MODE:
        print(f"Geocoding location: {location}")

    async with aiohttp.ClientSession() as session:
        async with session.get(BASE_URL, params=params) as response:
            if DEBUG_MODE:
                print(f"Geocoding API response status: {response.status}")

            if response.status == 200:
                data = await response.json()
                # Extract the latitude and longitude from the response
                if data:  # if any location found
                    lat = data[0]['lat']
                    lon = data[0]['lon']
                    if DEBUG_MODE:
                        print(f"Geocoded Location: {location}, Lat: {lat}, Lon: {lon}")
                    return {'lat': lat, 'lon': lon, 'city': location}
                else:
                    return {'error': f"No location found for {location}"}
            else:
                return {'error': f"Error: {response.status}"}
