from crewai.tools import tool
from langchain_community.tools import DuckDuckGoSearchResults
import re
import requests

@tool("fetch_prayer_times")
def fetch_prayer_times(city: str, date: str):
    """
    Fetches Islamic prayer times for a specific city (Makkah or Madinah) 
    on a given date (format: YYYY-MM-DD). Use this to align rituals with prayers.
    """
    # Coordinates for holy cities
    coords = {
        "makkah": {"lat": 21.4225, "lon": 39.8262},
        "madinah": {"lat": 24.4672, "lon": 39.6112}
    }
    
    city_lower = city.lower()
    if city_lower not in coords:
        return "City not supported. Please use 'Makkah' or 'Madinah'."

    lat = coords[city_lower]["lat"]
    lon = coords[city_lower]["lon"]
    
    # Using AlAdhan API (A standard for prayer times)
    url = f"https://api.aladhan.com/v1/timings/{date}?latitude={lat}&longitude={lon}&method=4"
    
    try:
        response = requests.get(url).json()
        timings = response['data']['timings']
        return f"Prayer Times for {city} on {date}: {timings}"
    except Exception as e:
        return f"Error fetching prayer times: {str(e)}"
