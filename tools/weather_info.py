import requests
from utils.config import WEATHER_API_KEY,WEATHER_BASE_URL
from langchain_community.tools import tool

class WeatherInfoTool:
    def __init__(self):
        self.api = WEATHER_API_KEY
        self.base_url = WEATHER_BASE_URL
        self.weather_tool_list = self.setup_tools()
        
    def setup_tools(self):
        """Get all weather information tools."""
        @tool
        def get_current_weather(location: str):
            """Fetches current weather conditions for a given location."""
            endpoint = f"{self.base_url}/current.json"
            params = {
                "key": self.api,
                "q": location
            }
            try:
                response = requests.get(endpoint, params=params)
                response.raise_for_status()
                data = response.json()
                return {
                    "location": data["location"]["name"],
                    "current_weather_temp": data["current"]["temp_c"],
                    "current_weather_condition": data["current"]["condition"]["text"]
                }
            except Exception as e:
                print(f"Error fetching current weather for {location}: {e}")
                return {"error": f"Could not retrieve current weather for {location}."}
        
        @tool
        def get_forecast_weather(location: str, days: int):
            """Fetches forecast weather conditions for a given location for up to 14 days."""
            endpoint = f"{self.base_url}/forecast.json"
            params = {
                "key": self.api,
                "q": location,
                "days": min(days, 14) # max 14 free if want more pay for it.
            }
            try:
                response = requests.get(endpoint, params=params)
                response.raise_for_status()
                data = response.json()
                forecast = []
                for day_data in data["forecast"]["forecastday"]:
                    forecast.append({
                        "date": day_data["date"], 
                        "min_temp_c": day_data["day"]["mintemp_c"],
                        "max_temp_c": day_data["day"]["maxtemp_c"],
                        "condition": day_data["day"]["condition"]["text"]
                    })
                return {"forecast_weather": forecast}
            except Exception as e:
                print(f"Error fetching forecast weather for {location}: {e}")
                return {"error": f"Could not retrieve forecast weather for {location}."}
        return [get_current_weather, get_forecast_weather]
