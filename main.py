from fastapi import FastAPI, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from openai import OpenAI
import os
import cv2
import base64
from pytubefix import YouTube
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
            raise ValueError("No suitable video stream found")
        video_path = stream.download(output_path=temp_dir)
        return video_path
    except Exception as e:
        raise ValueError(f"Error downloading video: {str(e)}")

def extract_frames(video_path, frame_rate=1):
    frames = []
    cap = cv2.VideoCapture(video_path)
    fps = cap.get(cv2.CAP_PROP_FPS)
    frame_interval = int(fps / frame_rate)
    
    count = 0
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        if count % frame_interval == 0:
            _, buffer = cv2.imencode('.jpg', frame)
            base64_frame = base64.b64encode(buffer).decode('utf-8')
            frames.append(base64_frame)
        count += 1
    
    cap.release()
    return frames

@app.post("/api/search/")
async def search(video_url: str = Form(...), query: str = Form(...)):
    try:
        with tempfile.TemporaryDirectory() as temp_dir:
            video_path = download_youtube_video(video_url, temp_dir)
            frames = extract_frames(video_path, frame_rate=0.5)  # Extract 1 frame every 2 seconds

        content = [{"type": "text", "text": f"{query}"}]

        for frame in frames:
            content.append({
                "type": "image_url",
                "image_url": {
                    "url": f"data:image/jpeg;base64,{frame}",
                    "detail": "low"
                }
            })

        messages = [{"role": "user", "content": content}]

        chat_completion = client.chat.completions.create(
            model="gpt-4-vision-preview",
            messages=messages,
            max_tokens=500,
        )

        llm_response = chat_completion.choices[0].message.content

        return {
            "answersInText": [
                {
                    "number": 1,
                    "relevantTextFromDocument": llm_response,
                    "sourceLink": video_url,
                    "documentTitle": "GPT-4V Response"
                }
            ],
            "fullJson": {
                "query": query,
                "llmResponse": llm_response
            }
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
