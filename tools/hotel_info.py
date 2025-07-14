import requests
from utils.config import GOOGLE_PLACES_API_KEY,GOOGLE_PLACES_BASE_URL,TAVILY_API_KEY
from langchain_google_community import GooglePlacesTool, GooglePlacesAPIWrapper
from langchain_tavily import TavilySearch
from langchain_community.tools import tool

class GoogleHotelSearchTool: # Corrected class name as it was duplicated
    def __init__(self):
        self.places_wrapper = GooglePlacesAPIWrapper(gplaces_api_key=GOOGLE_PLACES_API_KEY) # Corrected arg name
        self.places_tool = GooglePlacesTool(api_wrapper=self.places_wrapper)
        self.Google_Search_tool_list = self.setup_tools()
        
    def _run_Google_Search(self, query: str):
        try:
            result = self.places_tool.run(query)
            return result
        except Exception as e:
            print(f"Error running Google Places Search for '{query}': {e}")
            raise e
        
    def setup_tools(self):
        """Get all hotel information tools."""
        @tool
        def Google_Search_hotel(location: str) -> str:
            """
            Searches for top hotels, resorts, and accommodations in the specified location using GooglePlaces API.
            """
            # Changed query from "restaurants and eateries" to "hotels"
            response = self._run_Google_Search(f"top hotels and accommodations in {location}")
            return {"hotel_info": response} # Changed key to "hotel_info"
        
        return [Google_Search_hotel]

class TavilyHotelSearchTool: # Renamed to avoid confusion and properly target hotels
    def __init__(self):
        self.api = TAVILY_API_KEY
        self.tavily_search_tool_list = self.setup_tools()
        
    def _run_tavily_search(self, query: str) -> str:
        tavily_tool = TavilySearch(api_key=self.api, topic="general", include_answer="advanced") # Pass API key
        try:
            result = tavily_tool.invoke({"query": query})
            if isinstance(result, dict) and result.get("answer"):
                return result["answer"]
            return str(result)
        except Exception as e:
            print(f"Tavily search failed for '{query}': {e}")
            return f"Tavily search failed: {e}"
        
    def setup_tools(self):
        """Get all hotel information tools."""
        @tool
        def tavily_search_hotel(location: str):
            """
            Searches for top hotels, resorts, and accommodations in the specified location using TavilySearch.
            """
            # Changed query from "restaurants and eateries" to "hotels"
            response = self._run_tavily_search(f"top hotels and accommodations in {location}")
            return {"hotel_info": response} # Changed key to "hotel_info"
            
        return [tavily_search_hotel]