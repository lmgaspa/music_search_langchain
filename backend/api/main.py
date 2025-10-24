from fastapi import FastAPI, Query, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from googleapiclient.discovery import build
from dotenv import load_dotenv
import os
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

YOUTUBE_API_KEY = os.getenv("API_KEY")

# Initialize the app with API prefix
app = FastAPI()

# Create API router with prefix
from fastapi import APIRouter
api_router = APIRouter(prefix="/api")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",  # Frontend local
        "http://localhost:3000",  # Alternativo
        "https://music-search-langchain.vercel.app",
        "https://music-search-langchain.onrender.com/",  # Backend próprio
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

def ensure_api_key():
    if not YOUTUBE_API_KEY:
        logger.error("API_KEY is missing from the environment")
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
        logger.error(f"YouTube API error: {str(e)}")
        # return a clear HTTP error to the client
        raise HTTPException(status_code=502, detail=f"YouTube error: {e}")

# Main search route
@api_router.get("/search")
def search_route(q: str = Query(..., description="Song query!"), max_results: int = 12):
    logger.info(f"Search request received: query='{q}', max_results={max_results}")
    if not q.strip():
        logger.warning("Empty query parameter received")
        raise HTTPException(status_code=400, detail="Parameter q is required.")
    
    try:
        results = search_music_youtube(q.strip(), max_results=max_results)
        logger.info(f"Search completed successfully: {len(results)} results found")
        return {"results": results}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error in search route: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

# Health route (for monitoring)
@api_router.get("/health")
def health_check():
    logger.info("Health check requested")
    return {
        "status": "ok", 
        "api_key_present": bool(YOUTUBE_API_KEY),
        "environment": "production" if os.getenv("PORT") else "development"
    }

# Root route for basic connectivity test
@app.get("/")
def root():
    return {"message": "Music Search API is running", "version": "1.0.0"}

# Include the API router
app.include_router(api_router)
