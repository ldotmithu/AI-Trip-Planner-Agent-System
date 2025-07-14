import requests
from utils.config import EXCHANGE_RATE_API_KEY,EXCHANGE_RATE_BASE_URL
from langchain_community.tools import tool

class CurrencyTools:
    def __init__(self):
        self.api_key = EXCHANGE_RATE_API_KEY
        self.base_url = EXCHANGE_RATE_BASE_URL
        self.currency_tool_list = self.setup_tools() # Call setup_tools to initialize the list
        
    def setup_tools(self):
        """ Defines and returns a list of currency exchange tools. """
        @tool
        def get_exchange_rate(from_currency: str, to_currency: str):
            """
            Fetches the current exchange rate between two currencies (e.g., USD to EUR).
            Currency codes should be 3-letter ISO 4217 codes (e.g., USD, EUR, JPY).
            """
            endpoint = f"{self.base_url}/{self.api_key}/pair/{from_currency.upper()}/{to_currency.upper()}" # Convert to uppercase
            try:
                response = requests.get(endpoint)
                response.raise_for_status()
                data = response.json()
                if data.get("result") == "success":
                    return {
                        "from_currency": from_currency.upper(),
                        "to_currency": to_currency.upper(),
                        "rate": data["conversion_rate"]
                    }
                else:
                    print(f"ExchangeRate-API error: {data.get('error-type', 'Unknown error')}")
                    return {"error": f"Could not retrieve exchange rate for {from_currency} to {to_currency}."}
            except Exception as e:
                print(f"Error fetching exchange rate: {e}")
                return {"error": f"Failed to get exchange rate: {e}"}
        return [get_exchange_rate]