from typing_extensions import TypedDict,Optional,Any,Dict,List
from pydantic import BaseModel

class TripState(TypedDict):
    user_input: str
    location: Optional[str]
    start_date: Optional[str]
    end_date: Optional[str]
    current_weather: Optional[str]
    current_weather_temp: Optional[float]
    current_weather_condition: Optional[str]
    forecast_weather: Optional[List[Dict[str, Any]]]
    forecast_weather_min_temp: Optional[List[float]] 
    forecast_weather_max_temp: Optional[List[float]] 
    forecast_weather_condition: Optional[List[str]]
    attractive_place: Optional[List[str]]
    hotel_info: Optional[List[str]]
    no_of_traveler: Optional[int] 
    from_currency: Optional[str]
    to_currency: Optional[str]
    rate: Optional[float]
    budget_usd: Optional[float]
    local_currency_budget: Optional[float]
    status: str
    final_plan: str
    messages: List[Dict[str, Any]]  # final summary

class TripRequest(BaseModel):
    user_query: str    