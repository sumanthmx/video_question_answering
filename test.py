from IPython.display import display, Image, Audio

import cv2  # We're using OpenCV to read video, to install !pip install opencv-python
from pytubefix import YouTube
import base64
import time
from openai import OpenAI
import os
import requests
import tempfile
import numpy as np

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY", "<your OpenAI API key if not set as env var>"))
video_url = 'https://www.youtube.com/watch?v=PIE5QtkxzvM'

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

def extract_keyframes(base64Frames, num_samples=38):
    total_frames = len(base64Frames)
    indices = np.round(np.linspace(0, total_frames - 1, num_samples)).astype(int)
    return [base64Frames[i] for i in indices]

with tempfile.TemporaryDirectory() as temp_dir:
    video_path = download_youtube_video(video_url, temp_dir)
    base64Frames = extract_frames(video_path)
    base64Keyframes = extract_keyframes(base64Frames)
    PROMPT_MESSAGES = [
    {
        "role": "user",
        "content": [
            "These are frames from a video that I want to upload. Generate a compelling description that I can upload along with the video.",
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
    print(result.choices[0].message.content)