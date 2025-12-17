import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    
    # Where to save files locally
    STATIC_DIR = "static"
    
    # The domain of your API (Change this when deploying to AWS/DigitalOcean)
    # For local testing, use http://localhost:8000
    BASE_URL = os.getenv("BASE_URL", "http://localhost:8000") 
    
    VOICE_MAPPING = {
        "male": "onyx",
        "female": "shimmer"
    }

settings = Settings()

# Ensure the directory exists when app starts
os.makedirs(settings.STATIC_DIR, exist_ok=True)