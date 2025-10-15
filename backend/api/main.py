from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from googleapiclient.discovery import build
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

YOUTUBE_API_KEY = os.getenv("API_KEY")

if not YOUTUBE_API_KEY:
    raise SystemExit("API_KEY not found in .env or in Render environment variables.")

# Initialize the app
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "https://music-search-langchain.vercel.app",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Function to search for songs on YouTube
def search_music_youtube(query: str, max_results: int = 15):
    try:
        youtube = build("youtube", "v3", developerKey=YOUTUBE_API_KEY)
        search_response = youtube.search().list(
            q=query,
            part="snippet",
            maxResults=max_results,
            type="video"
        ).execute()

        music_results = [
            {
                "title": item["snippet"]["title"],
                "url": f"https://www.youtube.com/watch?v={item['id']['videoId']}",
                "channel": item["snippet"]["channelTitle"],
                "thumbnail": item["snippet"]["thumbnails"]["high"]["url"]  # ✅ adding image
            }
            for item in search_response.get("items", [])
        ]

        return music_results

    except Exception as e:
        return {"error": str(e)}

# Main search route
@app.get("/search")
def search_route(q: str = Query(..., description="Song query!")):
    results = search_music_youtube(q)
    return {"results": results}

# Health route (for curl testing)
@app.get("/health")
def health_check():
    return {"status": "ok"}
