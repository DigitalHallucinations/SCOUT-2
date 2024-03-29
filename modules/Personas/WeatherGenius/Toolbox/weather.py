# modules/weather/weather.py

import aiohttp
import os

DEBUG_MODE = False  # Set this flag to True to enable debug statements

async def get_current_weather(lat, lon, units='imperial', exclude=None):
    OPENWEATHER_API_KEY = os.environ['OPENWEATHERMAP_API_KEY']
    if DEBUG_MODE:
        print(f"Getting current and forecast weather for location: lat={lat}, lon={lon}, units={units}, exclude={exclude}")

    weather_url = f"https://api.openweathermap.org/data/3.0/onecall?lat={lat}&lon={lon}&units={units}&appid={OPENWEATHER_API_KEY}"

    if exclude:
        weather_url += f'&exclude={exclude}'

    return await get_weather_data(weather_url)

async def get_weather_data(url):
    if DEBUG_MODE:
        print(f"Weather API URL: {url}")

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if DEBUG_MODE:
                print(f"Weather API response status: {response.status}")

            if response.status == 200:
                weather_data = await response.json()
                # Return all the weather data
                return weather_data
            else:
                return f"Error: {response.status}"
