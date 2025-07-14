# AI Trip Planner ✈️

Plan your next adventure effortlessly with the power of AI! This project leverages Large Language Models (LLMs) and various external tools to generate personalized trip itineraries, including weather forecasts, attractions, hotel suggestions, and currency conversions.

## ✨ Features

* **Intelligent Trip Planning:** Understands natural language requests for trip details (location, dates, travelers, budget, currency conversion).
* **Real-time Weather:** Fetches current and forecast weather conditions for your destination.
* **Attraction Discovery:** Recommends top tourist attractions using Google Places and Tavily Search.
* **Hotel Suggestions:** Provides accommodation options based on your destination and preferences.
* **Currency Conversion:** Calculates budget in local currency based on live exchange rates.
* **Interactive Frontend:** A user-friendly Streamlit interface for seamless interaction.
* **Robust Backend:** A FastAPI backend orchestrates the AI workflow and serves the API.

## 🚀 Technologies Used

**Backend (Python - FastAPI)**
* **FastAPI**: A modern, fast (high-performance) web framework for building APIs.
* **LangChain**: Framework for developing applications powered by language models.
* **LangGraph**: A library for building robust and stateful multi-actor applications with LLMs, ideal for orchestrating complex workflows.
* **LangChain Community / LangChain Google Community**: Integrations for various tools.
* **Groq**: High-performance LLM inference for fast processing.
* **Pydantic**: Data validation and settings management.
* **Requests**: HTTP library for making API calls to external services.
* **python-dotenv**: For loading environment variables.

**Frontend (Python - Streamlit)**
* **Streamlit**: A simple and powerful framework for creating beautiful web applications for machine learning and data science.

**External APIs**
* **WeatherAPI**: For current and forecast weather data.
* **Google Places API**: For searching local businesses and points of interest (attractions, hotels).
* **Tavily Search API**: A search engine optimized for AI agents, used as a fallback or alternative for information retrieval.
* **ExchangeRate-API**: For real-time currency exchange rates.

## ⚙️ Setup Instructions

Follow these steps to get the project up and running on your local machine.

### 1. Clone the Repository

```bash
git clone https://github.com/ldotmithu/AI-Trip-Planner-Agent-System.git
cd AI-Trip-Planner-Agent-System 
```
### 2. Create and Activate Virtual Environment
- It's highly recommended to use a virtual environment to manage dependencies.

```bash
python -m venv venv
# activate 
venv\Scripts\activate
```
### 3. Install Dependencies
```bash
pip install -r requirements.txt
```
### 4. Configure Environment Variables [Must]
``` bash 
# .env (or wherever your config.py reads from)

# WeatherAPI (e.g., from weatherapi.com)
WEATHER_API_KEY="your_weather_api_key_here"
WEATHER_BASE_URL="[http://api.weatherapi.com/v1](http://api.weatherapi.com/v1)"

# Google Places API (e.g., from Google Cloud Console)
GOOGLE_PLACES_API_KEY="your_google_places_api_key_here"
GOOGLE_PLACES_BASE_URL="[https://maps.googleapis.com/maps/api/place](https://maps.googleapis.com/maps/api/place)" # This might not be directly used if using langchain_google_community

# Tavily Search API (e.g., from tavily.com)
TAVILY_API_KEY="your_tavily_api_key_here"

# ExchangeRate-API (e.g., from exchangerate-api.com)
EXCHANGE_RATE_API_KEY="your_exchange_rate_api_key_here"
EXCHANGE_RATE_BASE_URL="[https://v6.exchangerate-api.com/v6](https://v6.exchangerate-api.com/v6)"

# Groq API (e.g., from groq.com)
GROQ_API_KEY="your_groq_api_key_here"
LLM_MODEL_NAME="llama3-8b-8192" # Or any other Groq model you prefer
TEMPERATURE=0.7 # LLM temperature
```

### ▶️ How to Run

1. Run the Backend AP
```
    uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
```
- This will start the FastAPI server, typically accessible at http://localhost:8000. The --reload flag enables live reloading during development.

2. Run the Streamlit Frontend
```
streamlit run frontend/main.py
```
- This will open the Streamlit application in your default web browser, typically at http://localhost:8501.


