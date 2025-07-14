
import json , re
import datetime 
from models.trip_state import TripState
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from utils.llm import ModelLoader

model_loader = ModelLoader()
llm = model_loader.load_llm()

def generate_response(state: TripState) -> TripState:
    """
    Generates a comprehensive trip plan summary based on the gathered information.
    """
    location = state.get("location", "the specified location")
    
    response_parts = [
        f"# Bonjour! Your Paris Trip Plan 🇫🇷", 
        f"Get ready for an amazing trip to **{location}**! Based on the information you provided, here's a plan to make the most of your time in the City of Lights:\n"
    ]

    
    if state.get("start_date") and state.get("end_date"):
        try:
            start_dt = datetime.datetime.strptime(state["start_date"], "%Y-%m-%d").strftime("%B %dth")
            end_dt = datetime.datetime.strptime(state["end_date"], "%Y-%m-%d").strftime("%B %dth, %Y")
            response_parts.append(f"## 🗓️ Trip Dates")
            response_parts.append(f"**From**: {start_dt} **To**: {end_dt}\n")
        except ValueError:
            response_parts.append(f"## 🗓️ Trip Dates")
            response_parts.append(f"**Dates**: {state['start_date']} to {state['end_date']} (Date format error, please use YYYY-MM-DD)\n")


    if state.get("current_weather") or state.get("forecast_weather"):
        response_parts.append(f"## ☁️ Weather Outlook")

        if state.get("current_weather_temp") is not None and state.get("current_weather_condition"):
            response_parts.append(f"- **Current Weather**: {state['current_weather_temp']}°C, {state['current_weather_condition']}.")

        if state.get("forecast_weather"):
           
            min_temps = state.get("forecast_weather_min_temp", [])
            max_temps = state.get("forecast_weather_max_temp", [])
            conditions = state.get("forecast_weather_condition", [])

            if min_temps and max_temps and conditions:
                avg_min = sum(min_temps) / len(min_temps)
                avg_max = sum(max_temps) / len(max_temps)
                
                
                from collections import Counter
                common_conditions = Counter(conditions).most_common(2) 
                
                weather_summary = f"Throughout your trip, expect daily temperatures generally ranging from **{min(min_temps):.1f}°C to {max(max_temps):.1f}°C**."
                
                if len(common_conditions) == 1:
                    weather_summary += f" The weather will mostly be **{common_conditions[0][0].lower()}**."
                elif len(common_conditions) > 1:
                    weather_summary += f" You'll see a mix of **{common_conditions[0][0].lower()}** and **{common_conditions[1][0].lower()}** conditions."
                
                response_parts.append(f"- **Forecast Summary**: {weather_summary} Pack layers suitable for varying temperatures and an umbrella for occasional showers.")

                
                response_parts.append("\n### Detailed Daily Forecast:")
                response_parts.append("| Date | Min Temp (°C) | Max Temp (°C) | Condition |")
                response_parts.append("|---|---|---|---|")
                for day in state["forecast_weather"]:
                    response_parts.append(
                        f"| {day['date']} | {day['min_temp_c']} | {day['max_temp_c']} | {day['condition']} |"
                    )
            else:
                response_parts.append("- Could not retrieve a detailed weather forecast for your trip dates.")
        response_parts.append("\n") 
    # Budget and Currency Information
    if state.get("budget_usd"):
        response_parts.append(f"## 💰 Budget & Currency")
        budget_str = f"You've got **${state['budget_usd']:.2f} USD**"
        if state.get("local_currency_budget") and state.get("to_currency"):
            budget_str += f" (**{state['local_currency_budget']:.2f} {state['to_currency']}**)"
        budget_str += " to spend, which is a great starting point for a fantastic Parisian adventure!"
        response_parts.append(f"- {budget_str}")
    if state.get("from_currency") and state.get("to_currency") and state.get("rate"):
        response_parts.append(f"- **Exchange Rate**: 1 {state['from_currency']} = {state['rate']:.4f} {state['to_currency']}.")
    response_parts.append("\n")

    # Number of Travelers
    if state.get("no_of_traveler"):
        response_parts.append(f"## 👨‍👩‍👧‍👦 Travelers")
        traveler_text = "It looks like you're traveling solo."
        if state['no_of_traveler'] == 2:
            traveler_text = "It looks like you're traveling with one other person."
        elif state['no_of_traveler'] > 2:
            traveler_text = f"You're planning a trip for **{state['no_of_traveler']} people**."
        response_parts.append(f"- {traveler_text}\n")


    # 2. Attractions Summary (Refined parsing and presentation)
    if state.get("attractive_place"):
        response_parts.append(f"## 🗺️ Top Attractions")
        attractions_info_raw = state["attractive_place"][0] 
        parsed_attractions = []
        
        
        if isinstance(attractions_info_raw, str):
            
            attraction_entries = re.split(r'\d+\.\s*', attractions_info_raw)
            for entry in attraction_entries:
                if entry.strip():
                    lines = entry.strip().split('\n')
                    name = lines[0].strip() if lines else "Unknown Attraction"
                    parsed_attractions.append(name)
        
        if parsed_attractions:
            response_parts.append("Here are some of the must-see attractions based on your list. Remember to check opening hours and ticket prices in advance:\n")
            for attraction_name in parsed_attractions[:8]: 
                response_parts.append(f"- **{attraction_name.split('Address:')[0].strip()}**") # Take only the name before address
            response_parts.append("\n")
        else:
            response_parts.append("Could not retrieve specific attractive places, but Paris has countless beautiful spots to discover!\n")

    # 3. Hotel Information Summary (Refined parsing and presentation)
    if state.get("hotel_info"):
        response_parts.append(f"## 🏨 Accommodation Suggestions")
        hotel_info_raw = state["hotel_info"][0] # Get the raw string output
        parsed_hotels = []

        if isinstance(hotel_info_raw, str):
            hotel_entries = re.split(r'\d+\.\s*', hotel_info_raw)
            for entry in hotel_entries:
                if entry.strip():
                    lines = entry.strip().split('\n')
                    name = lines[0].strip() if lines else "Unknown Hotel"
                    parsed_hotels.append(name)

        if parsed_hotels:
            response_parts.append("I've selected some hotel options based on location, ratings, and your potential budget. Remember, prices fluctuate, so double-check before booking!\n")
            for hotel_name in parsed_hotels[:5]: # Limit to top 5
                response_parts.append(f"- **{hotel_name.split('Address:')[0].strip()}**") 
            response_parts.append("\n")
        else:
            response_parts.append("Could not retrieve specific hotel information, but many great options are available in Paris!\n")


    
    response_parts.append("## 🚶‍♀️ Getting Around")
    response_parts.append("- **Metro**: Efficient and affordable.")
    response_parts.append("- **Bus**: A good option for exploring neighborhoods.")
    response_parts.append("- **Walking**: The best way to experience Paris!\n")

    response_parts.append("## 🍽️ Food & Culture")
    response_parts.append("- **Boulangerie**: Indulge in fresh pastries and bread.")
    response_parts.append("- **Crêperies**: Enjoy delicious crepes.")
    response_parts.append("- **Cafés**: Experience the Parisian café culture.")
    response_parts.append("- **Brasseries**: Traditional French cuisine.")
    response_parts.append("- **Pro-tip**: Learn a few basic French phrases for a more immersive experience!\n")

    response_parts.append("## ✅ Important Reminders")
    response_parts.append("- **Passport and Visa**: Make sure your documents are in order.")
    response_parts.append("- **Travel Insurance**: Protect yourself against unexpected events.\n")

    response_parts.append("## 💡 Let me know if you'd like help with:")
    response_parts.append("- Restaurant recommendations")
    response_parts.append("- Day-by-day itinerary suggestions")
    response_parts.append("- Hidden gem spots")
    response_parts.append("- Transportation tips")
    response_parts.append("- Cultural insights\n")

    response_parts.append("Let's plan your dream Paris trip! ✨") 

    final_summary_content = "\n".join(response_parts)
    
    summary_prompt = ChatPromptTemplate.from_messages([
        ("system", """You are a friendly, enthusiastic, and helpful trip planning assistant.
        Refine the provided trip plan content to make it engaging, well-organized, and slightly more conversational.
        Ensure all key information (dates, weather, budget, travelers, attractions, hotels, practical tips) is clearly presented using Markdown headings and bullet points.
        Maintain a positive and helpful tone. Do NOT add new factual information. ONLY reformat and refine the provided raw content.
        """),
        ("human", "Here's the raw information gathered:\n{raw_info}")
    ])
    
    final_summary_chain = summary_prompt | llm | StrOutputParser()
    
    try:
        final_summary = final_summary_chain.invoke({"raw_info": final_summary_content})
        
        return {
            **state,
            "messages": state.get("messages", []) + [{"role": "assistant", "content": final_summary}],
            "status": "completed",
            "final_plan": final_summary
        }
    except Exception as e:
        print(f"Error generating final response with LLM: {e}")
        return {
            **state,
            "messages": state.get("messages", []) + [{"role": "assistant", "content": f"I encountered an error while finalizing your trip plan: {e}. Here's the raw information I gathered:\n{final_summary_content}"}],
            "status": "error",
            "final_plan": f"Could not generate a detailed plan. Error: {e}. Here's the raw information gathered so far:\n{final_summary_content}"
        }