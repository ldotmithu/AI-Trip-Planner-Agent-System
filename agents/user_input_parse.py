from models.trip_state import TripState
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from utils.llm import ModelLoader
from langchain_groq import ChatGroq
from utils.config import TEMPERATURE,LLM_MODEL_NAME,GROQ_API_KEY
from tools import InitializeTools
import re , json
from dotenv import load_dotenv
load_dotenv()

obj= InitializeTools()
all_tools = obj.alltools()

model_loader = ModelLoader()
llm = model_loader.load_llm()
llm_with_tools = llm.bind_tools(all_tools)


def parse_user_input(state: TripState) -> TripState:
    """
    Parses user input to extract location, dates, number of travelers, and budget.
    This node acts as an initial information extraction step.
    """
    user_input = state.get("user_input", "")
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", """You are a helpful assistant. Extract the following information from the user's trip request:
        - **location**: The destination city (e.g., Paris, Tokyo)
        - **start_date**: The start date of the trip in YYYY-MM-DD format (if provided).
        - **end_date**: The end date of the trip in YYYY-MM-DD format (if provided).
        - **no_of_traveler**: The number of travelers (integer, if provided).
        - **budget_usd**: The budget in USD (float, if provided).
        - **from_currency**: The currency the user wants to convert from (3-letter ISO code, if specified, e.g., "USD").
        - **to_currency**: The currency the user wants to convert to (3-letter ISO code, if specified, e.g., "EUR").
        
        If information is not explicitly provided, leave it as 'null'.
        Respond with a JSON object containing these keys.
        Example: {{"location": "Paris", "start_date": "2025-07-10", "end_date": "2025-07-15", "no_of_traveler": 2, "budget_usd": 2000.0, "from_currency": "USD", "to_currency": "EUR"}}
        """),
        ("human", "{user_input}")
    ])
    
    chain = prompt | llm | StrOutputParser()
    
    try:
        extracted_info_str = chain.invoke({"user_input": user_input})
        print(f"Extracted info raw: {extracted_info_str}")
        
        # --- MODIFIED: More robust JSON extraction ---
        json_content = extracted_info_str.strip()
        
        # Attempt to find JSON within markdown code blocks first
        match = re.search(r'```(?:json)?\s*(.*?)\s*```', json_content, re.DOTALL)
        if match:
            json_content = match.group(1).strip()
        
        # Clean up any residual backticks or unexpected characters that might interfere with parsing
        json_content = json_content.replace("```", "").strip()

        print(f"JSON content after stripping: {json_content}")
        extracted_info = json.loads(json_content) 
        # --- END MODIFIED ---
        
        # Update state with extracted info
        return {
            **state,
            "location": extracted_info.get("location"),
            "start_date": extracted_info.get("start_date"),
            "end_date": extracted_info.get("end_date"),
            "no_of_traveler": extracted_info.get("no_of_traveler"),
            "budget_usd": extracted_info.get("budget_usd"),
            "from_currency": extracted_info.get("from_currency"),
            "to_currency": extracted_info.get("to_currency"),
            "status": "parsed_input",
            "messages": state.get("messages", []) + [{"role": "system", "content": "Parsed user input."}]
        }
    except json.JSONDecodeError as e:
        print(f"Error parsing LLM output JSON: {e} - Raw output: {extracted_info_str}")
        return {
            **state,
            "status": "parsing_error",
            "messages": state.get("messages", []) + [{"role": "system", "content": f"Error parsing LLM's structured output: {e}. Raw output: ```json\\n{extracted_info_str}\\n```"}]
        }
    except Exception as e:
        print(f"Unexpected error parsing user input: {e}")
        return {
            **state,
            "status": "parsing_error",
            "messages": state.get("messages", []) + [{"role": "system", "content": f"An unexpected error occurred during input parsing: {e}. Please try again with a clearer request."}]
        }