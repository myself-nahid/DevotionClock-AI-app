from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from app.models import DevotionalRequest, DevotionalResponse
from services.llm_generator import generate_devotional_text
from services.tts_engine import generate_and_save_audio
from app.config import settings

app = FastAPI()

# --- IMPORTANT: Mount the static folder ---
# This makes files in /static accessible via http://localhost:8000/static/filename.mp3
app.mount("/static", StaticFiles(directory=settings.STATIC_DIR), name="static")

@app.post("/generate", response_model=DevotionalResponse)
async def create_devotional(request: DevotionalRequest):
    try:
        # 1. Generate Text
        print(f"Generating Text for {request.user_name}...")
        text_data = await generate_devotional_text(request)
        
        # 2. Prepare text for speech
        full_spoken_text = f"{text_data['title']}. {text_data['scripture']}. {text_data['content']}"
        
        # 3. Generate and Save Audio
        print("Generating Audio File...")
        filename, duration = await generate_and_save_audio(full_spoken_text, request.gender_preference)
        
        # 4. Construct Full URL
        full_audio_url = f"{settings.BASE_URL}/static/{filename}"

        print(f"Done! Audio available at: {full_audio_url}")

        return DevotionalResponse(
            title=text_data['title'],
            scripture=text_data['scripture'],
            body_text=text_data['content'],
            audio_url=full_audio_url,
            duration_seconds=duration
        )

    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    # Reload=True is for development only
    uvicorn.run(app, host="0.0.0.0", port=8000)