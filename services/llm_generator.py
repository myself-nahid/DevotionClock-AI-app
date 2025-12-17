import json
from openai import AsyncOpenAI
from app.config import settings

client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)

async def generate_devotional_text(request_data):
    """
    Generates a structured devotional using GPT-4o.
    """
    
    # Dynamic System Prompt
    system_prompt = (
        "You are a warm, empathetic Christian devotional writer. "
        "Your output must be JSON formatted."
    )

    # User Prompt with Constraints
    user_prompt = f"""
    Write a 3-5 minute devotional for {request_data.user_name}.
    Theme: {request_data.theme}
    Avoid these previous topics: {', '.join(request_data.previous_topics)}
    
    Structure the response strictly as this JSON:
    {{
        "title": "Creative Title",
        "scripture": "Book Chapter:Verse (NIV)",
        "content": "The full spoken devotional text..."
    }}
    
    The 'content' should be spoken-word style. Warm, encouraging, and rhythmic.
    Include an opening, the scripture reading, reflection, and a closing prayer.
    Target word count: 400-600 words.
    """

    response = await client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        response_format={"type": "json_object"}
    )

    content = response.choices[0].message.content
    return json.loads(content)