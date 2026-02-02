from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import uvicorn
import os
import shutil
from analyzer import (
    analyze_video_gestures,
    analyze_audio_quality,
    get_motivational_quote
)

app = FastAPI()

# -------------------------------
# CORS CONFIGURATION (PERMANENT)
# -------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ],
    allow_credentials=False,   # IMPORTANT: keeps browser stable
    allow_methods=["*"],
    allow_headers=["*"],
)

# -------------------------------
# DIRECTORIES
# -------------------------------
UPLOAD_DIR = "uploads"
FRAMES_DIR = "frames"

os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(FRAMES_DIR, exist_ok=True)

# -------------------------------
# STATIC FILES
# -------------------------------
app.mount("/static", StaticFiles(directory="."), name="static")

# -------------------------------
# ROUTES
# -------------------------------
@app.get("/")
def read_root():
    return {"message": "Rhetoric Backend API is running"}

@app.post("/analyze")
async def analyze_video(file: UploadFile = File(...)):
    if not file.filename:
        raise HTTPException(status_code=400, detail="No file uploaded")

    file_path = os.path.join(UPLOAD_DIR, file.filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # 1. Gesture Analysis
    flagged_frames = analyze_video_gestures(file_path, FRAMES_DIR)

    # 2. Audio Analysis
    audio_analysis = analyze_audio_quality(file_path)

    # 3. Motivational Quote
    quote = get_motivational_quote()

    # 4. Suggested Video
    suggestion_video = "https://www.youtube.com/watch?v=i0a61wFaF8A"

    return {
        "filename": file.filename,
        "flagged_frames": flagged_frames,
        "audio_analysis": audio_analysis,
        "quote": quote,
        "suggestion_video": suggestion_video,
    }

# -------------------------------
# SERVER ENTRY POINT
# -------------------------------
if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
