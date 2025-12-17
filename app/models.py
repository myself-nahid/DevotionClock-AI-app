from pydantic import BaseModel
from typing import Optional, List

class DevotionalRequest(BaseModel):
    theme: str                # e.g., "Faith Over Fear"
    user_name: str            # e.g., "John"
    gender_preference: str    # "male" or "female"
    previous_topics: Optional[List[str]] = [] # To ensure uniqueness

class DevotionalResponse(BaseModel):
    title: str
    scripture: str
    body_text: str
    audio_base64: str         # Returning base64 is easiest for the backend to handle immediately
    # In a larger scale app, might return an S3 URL instead of base64