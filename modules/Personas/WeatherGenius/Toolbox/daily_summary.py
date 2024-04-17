# modules/weather/get_daily_weather_summary.py

import aiohttp
import os

DEBUG_MODE = False  
async def get_daily_weather_summary(lat, lon, date, units='imperial', lang=None, tz=None):
    OPENWEATHER_API_KEY = os.environ['OPENWEATHERMAP_API_KEY']
    if DEBUG_MODE:
        print(f"Getting daily aggregated weather for location: lat={lat}, lon={lon}, date={date}, units={units}, lang={lang}, tz={tz}")

    weather_url = f"https://api.openweathermap.org/data/3.0/onecall/day_summary?lat={lat}&lon={lon}&date={date}&units={units}&appid={OPENWEATHER_API_KEY}"

    if lang:
        weather_url += f'&lang={lang}'
    if tz:
        weather_url += f'&tz={tz}'

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
