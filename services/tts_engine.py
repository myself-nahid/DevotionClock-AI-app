import io
import uuid
import os
from openai import AsyncOpenAI
from pydub import AudioSegment
from app.config import settings

client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)

def split_text(text, max_chars=4000):
    chunks = []
    while len(text) > max_chars:
        split_index = text.rfind(' ', 0, max_chars)
        if split_index == -1: split_index = max_chars
        chunks.append(text[:split_index])
        text = text[split_index:]
    chunks.append(text)
    return chunks

async def generate_and_save_audio(text_content: str, gender: str) -> tuple[str, float]:
    """
    Generates TTS, saves to disk, returns (filename, duration).
    """
    voice = settings.VOICE_MAPPING.get(gender, "onyx")
    chunks = split_text(text_content)
    
    combined_audio = AudioSegment.empty()

    # 1. Generate and Stitch
    for chunk in chunks:
        if not chunk.strip(): continue
        
        response = await client.audio.speech.create(
            model="tts-1-hd",
            voice=voice,
            input=chunk
        )
        segment = AudioSegment.from_file(io.BytesIO(response.content), format="mp3")
        combined_audio += segment

    # 2. Generate Unique Filename (UUID)
    filename = f"devotional_{uuid.uuid4()}.mp3"
    file_path = os.path.join(settings.STATIC_DIR, filename)

    # 3. Save to Static Folder
    combined_audio.export(file_path, format="mp3")

    # 4. Return filename and duration
    return filename, combined_audio.duration_seconds