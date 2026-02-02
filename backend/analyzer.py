import cv2
import os
import numpy as np
from moviepy import VideoFileClip
import speech_recognition as sr
import random

def analyze_video_gestures(video_path, output_frames_dir):
    """
    Analyzes video for sudden or erratic movements as a proxy for 'bad gestures'.
    Returns a list of relative paths to frames that were flagged.
    """
    if not os.path.exists(output_frames_dir):
        os.makedirs(output_frames_dir)

    cap = cv2.VideoCapture(video_path)
    ret, frame1 = cap.read()
    if not ret:
        return []

    prev_gray = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)
    frame_count = 0
    flagged_frames = []
    
    # We will only save a max of 5 frames to avoid clutter
    max_frames = 5
    
    while cap.isOpened():
        ret, frame2 = cap.read()
        if not ret:
            break
        
        gray = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)
        diff = cv2.absdiff(prev_gray, gray)
        # Threshold the diff to get binary image of change
        _, thresh = cv2.threshold(diff, 25, 255, cv2.THRESH_BINARY)
        
        # Calculate amount of change
        non_zero_count = np.count_nonzero(thresh)
        total_pixels = frame2.shape[0] * frame2.shape[1]
        
        # Heuristic: If > 15% of pixels changed, it might be a wild gesture
        # This is a very basic heuristic.
        if non_zero_count > (total_pixels * 0.15): 
             if len(flagged_frames) < max_frames:
                frame_name = f"gesture_issue_{len(flagged_frames)}.jpg"
                frame_path = os.path.join(output_frames_dir, frame_name)
                cv2.imwrite(frame_path, frame2)
                # Return relative path for frontend to serve
                flagged_frames.append(f"/static/frames/{frame_name}")
        
        prev_gray = gray
        # Skip 10 frames to speed up processing
        for _ in range(10):
            cap.grab()
        
    cap.release()
    return flagged_frames

def analyze_audio_quality(video_path):
    """
    Extracts audio and analyzes clarity, pauses, and pacing.
    """
    try:
        video = VideoFileClip(video_path)
        audio_path = "temp_audio.wav"
        video.audio.write_audiofile(audio_path, logger=None)
        
        recognizer = sr.Recognizer()
        with sr.AudioFile(audio_path) as source:
            audio_data = recognizer.record(source)
            
        # Use Google Speech Recognition
        text = recognizer.recognize_google(audio_data)
        word_count = len(text.split())
        duration = video.duration # seconds
        if duration > 0:
            wpm = (word_count / duration) * 60
        else:
            wpm = 0
            
        feedback = {
            "transcript": text,
            "wpm": round(wpm, 2),
            "pacing": "Good" if 130 < wpm < 160 else "Too Fast" if wpm >= 160 else "Too Slow",
            "clarity_score": 85 # Placeholder
        }
    except Exception as e:
        print(f"Audio analysis error: {e}")
        feedback = {
            "transcript": "Audio could not be transcribed or was too unclear.",
            "wpm": 0,
            "pacing": "N/A",
            "clarity_score": 0
        }
    
    if os.path.exists("temp_audio.wav"):
        os.remove("temp_audio.wav")
        
    return feedback

def get_motivational_quote():
    quotes = [
        "Speech is power: speech is to persuade, to convert, to compel. - Ralph Waldo Emerson",
        "There are always three speeches, for every one you actually gave. The one you practiced, the one you gave, and the one you wish you gave. - Dale Carnegie",
        "90% of how well the talk will go is determined before you step on the stage. - Somers White",
        "Be sincere; be brief; be seated. - Franklin D. Roosevelt"
    ]
    return random.choice(quotes)
