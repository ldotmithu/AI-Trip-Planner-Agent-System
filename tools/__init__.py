from tools.weather_info import WeatherInfoTool
from tools.attraction_info import GooglePlaceSearchTool,TavilyPlaceSearchTool
from tools.hotel_info import GoogleHotelSearchTool,TavilyHotelSearchTool
from tools.currency_info import CurrencyTools

# --- Initialize Tools ---


class InitializeTools:
    def __init__(self):
        self.weather_tools = WeatherInfoTool().weather_tool_list
        self.google_attraction_tools = GooglePlaceSearchTool().Google_Search_tool_list
        self.tavily_attraction_tools = TavilyPlaceSearchTool().tavily_search_tool_list
        self.google_hotel_tools = GoogleHotelSearchTool().Google_Search_tool_list
        self.tavily_hotel_tools = TavilyHotelSearchTool().tavily_search_tool_list
        self.currency_tools = CurrencyTools().currency_tool_list
    
    def alltools(self):
        all_tools = (
            self.weather_tools + 
            self.google_attraction_tools + 
            self.tavily_attraction_tools + 
            self.google_hotel_tools + 
            self.tavily_hotel_tools + 
            self.currency_tools
        )
        return all_tools