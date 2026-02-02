from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import uvicorn
import os
import shutil
from typing import List
from analyzer import analyze_video_gestures, analyze_audio_quality, get_motivational_quote

app = FastAPI()

# CORS configuration
origins = [
    "http://localhost:5173",  # Vite default port
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Ensure upload directory exists
UPLOAD_DIR = "uploads"
FRAMES_DIR = "frames"
os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(FRAMES_DIR, exist_ok=True)

# Mount static files for serving extracted frames
app.mount("/static", StaticFiles(directory="."), name="static")

@app.get("/")
def read_root():
    return {"message": "Rhetoric Backend API is running"}

@app.post("/analyze")
async def analyze_video(file: UploadFile = File(...)):
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    # 1. Analyze Gestures
    # We save frames to 'frames' directory which is served under /static/frames
    frames_output_dir = os.path.join(FRAMES_DIR)
    flagged_frames = analyze_video_gestures(file_path, frames_output_dir)
    
    # 2. Analyze Audio
    audio_analysis = analyze_audio_quality(file_path)
    
    # 3. Get Quote
    quote = get_motivational_quote()
    
    # 4. Suggestion Video (Static for now, can be randomized)
    suggestion_video = "https://www.youtube.com/watch?v=i0a61wFaF8A" # Julian Treasure: How to speak so that people want to listen
    
    return {
        "filename": file.filename,
        "flagged_frames": flagged_frames,
        "audio_analysis": audio_analysis,
        "quote": quote,
        "suggestion_video": suggestion_video
    }

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
