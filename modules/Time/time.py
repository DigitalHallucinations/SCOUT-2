# modules/Time/time.py

import datetime
import pytz
import asyncio

async def get_current_info(format_type='timestamp'):
    """
    Get current time information based on the specified format.
    
    Parameters:
    - format_type: A string that specifies the type of information to return. 
      Options are 'time', 'date', 'day', 'month_year', 'timestamp'. Default is 'timestamp'.
    
    Returns:
    - A string representing the current date or time information based on the format_type.
    """
    await asyncio.sleep(0)  
    now = datetime.datetime.now(pytz.timezone('America/Chicago'))
    format_options = {
        'time': "%H:%M:%S",
        'date': "%Y-%m-%d",
        'day': "%A",
        'month_year': "%B %Y",
        'timestamp': "%Y-%m-%d %H:%M:%S"
    }
    return now.strftime(format_options.get(format_type, "%Y-%m-%d %H:%M:%S"))
