# time.md

## File Location
modules/Tools/Base_Tools/time.py

## Overview
This module provides functionality to retrieve current time information in various formats.

## Key Components

### Functions:
1. `async def get_current_info(format_type='timestamp')`
   - Retrieves current time information based on the specified format
   - Parameters:
     - `format_type`: A string specifying the type of information to return (default: 'timestamp')
   - Returns: A string representing the current date or time information

## Dependencies
- datetime
- pytz
- asyncio

## Key Functionalities
1. Provides current time in various formats (time, date, day, month_year, timestamp)
2. Uses America/Chicago timezone

## Usage
This function can be called asynchronously to get current time information in the desired format.

## How the Agent Uses This File
The agent uses this file when it needs to access or provide current time information. It can be used in various scenarios such as:
- Timestamping messages or actions
- Providing the current date or time to users when asked
- Scheduling tasks or reminders based on the current time
- Calculating time differences or durations

The agent can call the `get_current_info()` function with different format types to get the time information in the most appropriate format for the current context or user request.