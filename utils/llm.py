from langchain_groq import ChatGroq
from utils.config import TEMPERATURE,LLM_MODEL_NAME,GROQ_API_KEY
from dotenv import load_dotenv
load_dotenv()

class ModelLoader:
    def __init__(self):
        self.api = GROQ_API_KEY
        self.model = LLM_MODEL_NAME
        self.temp = TEMPERATURE
    
    def load_llm(self):
        groq_model = ChatGroq(
            model=self.model,
            temperature=self.temp,
            api_key=self.api
        )    
        
        return groq_model