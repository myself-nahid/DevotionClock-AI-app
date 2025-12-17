import io
import base64
from openai import AsyncOpenAI
from pydub import AudioSegment
from app.config import settings

client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)

def split_text(text, max_chars=4000):
    """
    Simple helper to split text into chunks without cutting words.
    In production, split by sentences (.?!) for better flow.
    """
    chunks = []
    while len(text) > max_chars:
        # Find the last space within the limit
        split_index = text.rfind(' ', 0, max_chars)
        if split_index == -1:
            split_index = max_chars
        chunks.append(text[:split_index])
        text = text[split_index:]
    chunks.append(text)
    return chunks

async def generate_audio_file(text_content: str, gender: str):
    """
    1. Splits text
    2. Calls OpenAI TTS for each chunk
    3. Stitches audio using Pydub
    4. Returns Base64 string of the final MP3
    """
    
    voice = settings.VOICE_MAPPING.get(gender, "onyx")
    chunks = split_text(text_content)
    
    combined_audio = AudioSegment.empty()

    for i, chunk in enumerate(chunks):
        if not chunk.strip(): 
            continue
            
        response = await client.audio.speech.create(
            model="tts-1-hd", # HD is crucial for "Alarm" apps (better dynamic range)
            voice=voice,
            input=chunk
        )
        
        # Load raw bytes into Pydub
        segment_audio = AudioSegment.from_file(io.BytesIO(response.content), format="mp3")
        combined_audio += segment_audio

    # Export combined audio to memory buffer
    buffer = io.BytesIO()
    combined_audio.export(buffer, format="mp3")
    buffer.seek(0)
    
    # Encode to Base64 to send back via JSON
    audio_b64 = base64.b64encode(buffer.read()).decode('utf-8')
    return audio_b64