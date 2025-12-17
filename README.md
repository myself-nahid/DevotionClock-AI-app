# 🕊️ DevotionClock AI app

A high-performance **FastAPI microservice** that generates personalized daily Christian devotionals with natural-sounding voice narration.

Powered by **OpenAI GPT-4o** for devotional content generation and **OpenAI TTS-1-HD** for high-quality speech synthesis, this service acts as the **Intelligence Engine** for the *Daily Devotional Alarm App*.

---

## 🚀 Features

- **Dynamic Devotional Generation**  
  Creates unique, scripture-based devotionals tailored to user themes and history.

- **High-Fidelity Voice Output**  
  Produces calm, human-like narration using OpenAI’s HD Text-to-Speech model.

- **Smart Audio Stitching**  
  Automatically chunks long scripts and stitches audio to bypass the 4096-character limit using `pydub`.

- **Static Audio Serving**  
  Saves generated MP3 files locally and provides a downloadable URL for mobile clients.

- **Asynchronous Architecture**  
  Fully async FastAPI design for efficient concurrent request handling.

---

## 🛠️ Prerequisites

Ensure the following are installed:

- **Python 3.9+**
- **FFmpeg** (required for audio processing)
  - macOS: `brew install ffmpeg`
  - Windows: Download from https://ffmpeg.org and add to PATH
  - Linux: `sudo apt install ffmpeg`
- **OpenAI API Key** (GPT-4o + TTS access)

---

## 📦 Installation

```bash
git clone https://github.com/your-username/devotional-ai-engine.git
cd devotional-ai-engine
python -m venv venv
```
Activate the virtual environment:
macOS / Linux
```
source venv/bin/activate
```
windows
```
venv\Scripts\activate
```
install dependencies
```
pip install -r requirements.txt
```

## ⚙️ Configuration
Create a .env file in the project root:
```
OPENAI_API_KEY=sk-your-secret-key-here

# Base URL of this API
# Local: http://localhost:8000
# Production: http://your-server-ip-or-domain:8000
BASE_URL=http://localhost:8000
```

## 🏃 Running the Server
Run using Python
```
python -m app.main
```
Or using Uvicorn
```
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```
Server will be available at:
```
http://0.0.0.0:8000
```