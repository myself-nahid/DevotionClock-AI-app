import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    # Voice presets mapping
    VOICE_MAPPING = {
        "male": "onyx",
        "female": "shimmer"
    }
    # Path to save temp files
    TEMP_DIR = "temp_audio"

settings = Settings()

# Ensure temp dir exists
os.makedirs(settings.TEMP_DIR, exist_ok=True)