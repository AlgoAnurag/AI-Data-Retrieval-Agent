import os
from dotenv import load_dotenv

load_dotenv()

SERPAPI_KEY = os.getenv("SERPAPI_KEY")

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
