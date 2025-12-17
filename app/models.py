from pydantic import BaseModel
from typing import Optional, List

class DevotionalRequest(BaseModel):
    theme: str
    user_name: str
    gender_preference: str
    previous_topics: Optional[List[str]] = []

class DevotionalResponse(BaseModel):
    title: str
    scripture: str
    body_text: str
    audio_url: str  
    duration_seconds: float 