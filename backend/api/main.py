from fastapi import FastAPI, Query, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from googleapiclient.discovery import build
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

YOUTUBE_API_KEY = os.getenv("API_KEY")

# Initialize the app (without SystemExit)
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

def ensure_api_key():
    if not YOUTUBE_API_KEY:
        raise HTTPException(status_code=500, detail="API_KEY is missing from the environment.")

# Function to search for songs on YouTube
def search_music_youtube(query: str, max_results: int = 15):
    ensure_api_key()
    try:
        youtube = build("youtube", "v3", developerKey=YOUTUBE_API_KEY)
        search_response = youtube.search().list(
            q=query,
            part="snippet",
            maxResults=max_results,
            type="video",
            safeSearch="none",
        ).execute()

        music_results = [
            {
                "title": item["snippet"]["title"],
                "url": f"https://www.youtube.com/watch?v={item['id']['videoId']}",
                "channel": item["snippet"]["channelTitle"],
                "thumbnail": (
                    item["snippet"]["thumbnails"].get("high")
                    or item["snippet"]["thumbnails"].get("medium")
                    or item["snippet"]["thumbnails"].get("default")
                )["url"],
                "publishedAt": item["snippet"]["publishedAt"],
            }
            for item in search_response.get("items", [])
            if item.get("id", {}).get("videoId")
        ]

        return music_results

    except Exception as e:
        # return a clear HTTP error to the client
        raise HTTPException(status_code=502, detail=f"YouTube error: {e}")

# Main search route
@app.get("/search")
def search_route(q: str = Query(..., description="Song query!"), max_results: int = 15):
    if not q.strip():
        raise HTTPException(status_code=400, detail="Parameter q is required.")
    return {"results": search_music_youtube(q.strip(), max_results=max_results)}

# Health route (for curl testing)
@app.get("/health")
def health_check():
    return {"status": "ok", "api_key_present": bool(YOUTUBE_API_KEY)}
