from fastapi import FastAPI, HTTPException
from app.models import DevotionalRequest, DevotionalResponse
from services.llm_generator import generate_devotional_text 
from services.tts_engine import generate_audio_file

app = FastAPI(title="Devotional AI Engine")

@app.post("/generate", response_model=DevotionalResponse)
async def create_devotional(request: DevotionalRequest):
    try:
        # Step 1: Generate Text
        print(f"Generating text for theme: {request.theme}...")
        text_data = await generate_devotional_text(request)
        
        # Step 2: Generate Audio
        # We combine title + scripture + body for the audio generation
        full_spoken_text = f"{text_data['title']}. {text_data['scripture']}. {text_data['content']}"
        
        print("Generating audio (this may take 10-20 seconds)...")
        audio_b64 = await generate_audio_file(full_spoken_text, request.gender_preference)
        
        return DevotionalResponse(
            title=text_data['title'],
            scripture=text_data['scripture'],
            body_text=text_data['content'],
            audio_base64=audio_b64
        )

    except Exception as e:
        print(f"Error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)