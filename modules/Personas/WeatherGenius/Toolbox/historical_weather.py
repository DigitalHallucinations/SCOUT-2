# modules/weather/get_historical_weather.py

import aiohttp
import os

DEBUG_MODE = False  

async def get_historical_weather(lat, lon, dt, units='imperial', lang=None):
    OPENWEATHER_API_KEY = os.environ['OPENWEATHERMAP_API_KEY']
    if DEBUG_MODE:
        print(f"Getting historical weather for location: lat={lat}, lon={lon}, dt={dt}, units={units}, lang={lang}")

    weather_url = f"https://api.openweathermap.org/data/3.0/onecall/timemachine?lat={lat}&lon={lon}&dt={dt}&units={units}&appid={OPENWEATHER_API_KEY}"

    if lang:
        weather_url += f'&lang={lang}'

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
                return weather_data
            else:
                return f"Error: {response.status}"
