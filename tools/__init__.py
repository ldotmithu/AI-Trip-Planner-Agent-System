from tools.weather_info import WeatherInfoTool
from tools.attraction_info import GooglePlaceSearchTool,TavilyPlaceSearchTool
from tools.hotel_info import GoogleHotelSearchTool,TavilyHotelSearchTool
from tools.currency_info import CurrencyTools

# --- Initialize Tools ---
weather_tools = WeatherInfoTool().weather_tool_list
google_attraction_tools = GooglePlaceSearchTool().Google_Search_tool_list
tavily_attraction_tools = TavilyPlaceSearchTool().tavily_search_tool_list
google_hotel_tools = GoogleHotelSearchTool().Google_Search_tool_list
tavily_hotel_tools = TavilyHotelSearchTool().tavily_search_tool_list
currency_tools = CurrencyTools().currency_tool_list