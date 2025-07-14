from models.trip_state import TripState
from langchain_core.prompts import ChatPromptTemplate
import datetime
from tools.weather_info import WeatherInfoTool
from tools.attraction_info import GooglePlaceSearchTool,TavilyPlaceSearchTool
from tools.hotel_info import GoogleHotelSearchTool,TavilyHotelSearchTool
from tools.currency_info import CurrencyTools

def call_tools(state: TripState) -> TripState:
    """
    Agent responsible for deciding which tool to call based on the current state.
    It will try to gather weather, attractions, hotel info, and exchange rates.
    """
    messages = state["messages"]
    
   
    
    
    if state.get("location") and not state.get("current_weather"):
        try:
           
            current_weather_result = WeatherInfoTool().weather_tool_list[0].invoke({"location": state["location"]})
            if current_weather_result and not current_weather_result.get("error"):
                state["current_weather"] = f"Temp: {current_weather_result['current_weather_temp']}°C, Condition: {current_weather_result['current_weather_condition']}"
                state["current_weather_temp"] = current_weather_result["current_weather_temp"]
                state["current_weather_condition"] = current_weather_result["current_weather_condition"]
                state["messages"].append({"role": "system", "content": f"Fetched current weather: {state['current_weather']}"})
            else:
                state["messages"].append({"role": "system", "content": f"Could not fetch current weather for {state['location']}: {current_weather_result.get('error', 'Unknown error')}."})

           
            if state.get("start_date") and state.get("end_date"):
                try:
                    start = datetime.datetime.strptime(state["start_date"], "%Y-%m-%d")
                    end = datetime.datetime.strptime(state["end_date"], "%Y-%m-%d")
                    days_diff = (end - start).days + 1
                    
                    forecast_weather_result = WeatherInfoTool().weather_tool_list[1].invoke({"location": state["location"], "days": days_diff})
                    if forecast_weather_result and not forecast_weather_result.get("error") and forecast_weather_result.get("forecast_weather"):
                        state["forecast_weather"] = forecast_weather_result["forecast_weather"]
                        state["forecast_weather_min_temp"] = [d["min_temp_c"] for d in state["forecast_weather"]]
                        state["forecast_weather_max_temp"] = [d["max_temp_c"] for d in state["forecast_weather"]]
                        state["forecast_weather_condition"] = [d["condition"] for d in state["forecast_weather"]]
                        state["messages"].append({"role": "system", "content": f"Fetched {days_diff}-day weather forecast."})
                    else:
                        state["messages"].append({"role": "system", "content": f"Could not fetch forecast weather for {state['location']}: {forecast_weather_result.get('error', 'Unknown error')}."})
                except ValueError:
                    state["messages"].append({"role": "system", "content": "Invalid date format for forecast. Please use YYYY-MM-DD."})
            
        except Exception as e:
            state["messages"].append({"role": "system", "content": f"Error during weather tool call: {e}"})

    # 2. Attractive Places Information
    if state.get("location") and not state.get("attractive_place"):
        try:
            # Try Google Places first
            attractions_result_google = GooglePlaceSearchTool().Google_Search_tool_list[0].invoke({"location": state["location"]})
            if attractions_result_google and not attractions_result_google.get("error"):
               
                state["attractive_place"] = [attractions_result_google.get("attractive_place", "")] # Store as list of strings
                state["messages"].append({"role": "system", "content": f"Fetched attractive places using Google Places."})
            else:
                state["messages"].append({"role": "system", "content": f"Google Places failed for attractions: {attractions_result_google.get('error', 'Unknown error')}. Trying Tavily."})
                # If Google Places fails, try Tavily
                attractions_result_tavily = TavilyPlaceSearchTool().tavily_search_tool_list[0].invoke({"location": state["location"]})
                if attractions_result_tavily and not attractions_result_tavily.get("error"):
                    state["attractive_place"] = [attractions_result_tavily.get("attractive_place", "")] # Store as list of strings
                    state["messages"].append({"role": "system", "content": f"Fetched attractive places using Tavily."})
                else:
                    state["messages"].append({"role": "system", "content": f"Tavily search also failed for attractions: {attractions_result_tavily.get('error', 'Unknown error')}."})
        except Exception as e:
            state["messages"].append({"role": "system", "content": f"Error during attraction tool call: {e}"})

    # 3. Hotel Information
    if state.get("location") and not state.get("hotel_info"):
        try:
            
            hotel_result_google = GoogleHotelSearchTool().Google_Search_tool_list[0].invoke({"location": state["location"]})
            if hotel_result_google and not hotel_result_google.get("error"):
                state["hotel_info"] = [hotel_result_google.get("hotel_info", "")] # Store as list of strings
                state["messages"].append({"role": "system", "content": f"Fetched hotel info using Google Places."})
            else:
                state["messages"].append({"role": "system", "content": f"Google Places failed for hotels: {hotel_result_google.get('error', 'Unknown error')}. Trying Tavily."})
                # If Google Places fails, try Tavily
                hotel_result_tavily = TavilyHotelSearchTool().tavily_search_tool_list[0].invoke({"location": state["location"]})
                if hotel_result_tavily and not hotel_result_tavily.get("error"):
                    state["hotel_info"] = [hotel_result_tavily.get("hotel_info", "")] # Store as list of strings
                    state["messages"].append({"role": "system", "content": f"Fetched hotel info using Tavily."})
                else:
                    state["messages"].append({"role": "system", "content": f"Tavily search also failed for hotels: {hotel_result_tavily.get('error', 'Unknown error')}."})
        except Exception as e:
            state["messages"].append({"role": "system", "content": f"Error during hotel tool call: {e}"})

    # 4. Currency Exchange Rate
    if state.get("from_currency") and state.get("to_currency") and not state.get("rate"):
        try:
            exchange_rate_result = CurrencyTools().currency_tool_list[0].invoke({
                "from_currency": state["from_currency"],
                "to_currency": state["to_currency"]
            })
            if exchange_rate_result and not exchange_rate_result.get("error"):
                state["rate"] = exchange_rate_result["rate"]
                state["messages"].append({"role": "system", "content": f"Fetched exchange rate {state['from_currency']}/{state['to_currency']}: {state['rate']}."})
                if state.get("budget_usd"):
                    state["local_currency_budget"] = state["budget_usd"] * state["rate"]
                    state["messages"].append({"role": "system", "content": f"Converted budget to local currency: {state['local_currency_budget']:.2f} {state['to_currency']}."})
            else:
                state["messages"].append({"role": "system", "content": f"Could not fetch exchange rate for {state['from_currency']} to {state['to_currency']}: {exchange_rate_result.get('error', 'Unknown error')}."})
        except Exception as e:
            state["messages"].append({"role": "system", "content": f"Error during currency tool call: {e}"})


    state["status"] = "tools_called"
    return state