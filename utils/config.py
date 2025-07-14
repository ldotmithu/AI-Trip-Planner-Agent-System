import os
from dotenv import load_dotenv
load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")
GOOGLE_PLACES_API_KEY = os.getenv("GOOGLE_PLACES_API_KEY")
EXCHANGE_RATE_API_KEY = os.getenv("EXCHANGE_RATE_API_KEY")
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")

WEATHER_BASE_URL = "https://api.weatherapi.com/v1"
GOOGLE_PLACES_BASE_URL = "https://maps.googleapis.com/maps/api/place"
EXCHANGE_RATE_BASE_URL = "https://v6.exchangerate-api.com/v6"

LLM_MODEL_NAME = "gemma2-9b-it" 
TEMPERATURE = 0.5

BACKEND_URL = "http://localhost:8000"