# modules\Personas\Toolbox\WeatherGenius\maps.py

from modules.Time.time import get_current_info
from modules.Tools.Base_Tools.Google_search import GoogleSearch
from modules.Personas.WeatherGenius.Toolbox.weather import get_current_weather
from modules.Personas.WeatherGenius.Toolbox.historical_weather import get_historical_weather
from modules.Personas.WeatherGenius.Toolbox.daily_summary import get_daily_weather_summary


# Create an instance of GoogleSearch
google_search_instance = GoogleSearch()

# A dictionary to map function names to actual function objects
function_map = {
    "get_current_weather": get_current_weather,
    "get_historical_weather": get_historical_weather,
    "get_daily_weather_summary": get_daily_weather_summary,
    "get_current_info": get_current_info,
    "google_search": google_search_instance._search
}