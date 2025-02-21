from fastapi import FastAPI, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from openai import OpenAI

import os
import cv2
import base64
from pytubefix import YouTube
import numpy as np
import tempfile

app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Set up OpenAI API key
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def download_youtube_video(url, temp_dir):
    try:
        yt = YouTube(url)
        stream = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first()
        if not stream:
            raise ValueError("No suitable video stream found") # Raise an exception
        video_path = stream.download(output_path=temp_dir)
        return video_path
    except Exception as e:
        raise ValueError(f"Error downloading video: {str(e)}")

def extract_frames(video_path):
    video = cv2.VideoCapture(video_path)

    base64Frames = []
    while video.isOpened():
        success, frame = video.read()
        if not success:
            break
        _, buffer = cv2.imencode(".jpg", frame)
        base64Frames.append(base64.b64encode(buffer).decode("utf-8"))
    video.release()

    return base64Frames

def extract_keyframes(base64Frames, num_samples=91):
    total_frames = len(base64Frames)
    indices = np.round(np.linspace(0, total_frames - 1, num_samples)).astype(int)
    return [base64Frames[i] for i in indices]

@app.post("/api/search/")
async def search(video_url: str = Form(...), query: str = Form(...)):
    try:
        with tempfile.TemporaryDirectory() as temp_dir:
            video_path = download_youtube_video(video_url, temp_dir)
            base64Frames = extract_frames(video_path)
            base64Keyframes = extract_keyframes(base64Frames)
        
        PROMPT_MESSAGES = [
        {
            "role": "user",
            "content": [
                query,
                *map(lambda x: {"image": x, "resize": 768}, base64Keyframes),
            ],
        },
        ]
        params = {
            "model": "gpt-4o-mini",
            "messages": PROMPT_MESSAGES,
            "max_tokens": 200,
        }

        result = client.chat.completions.create(**params)
        llm_response = result.choices[0].message.content

        return {
            "fullJson": {
                "llmResponse": llm_response
            }
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
