from fastapi import FastAPI, Query, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from googleapiclient.discovery import build
from dotenv import load_dotenv
import os
import logging
from datetime import datetime
import math

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

# Simplified astrology calculation function
def calculate_astrology_chart(birth_date: str, birth_time: str, location: str):
    """
    Calculate simplified astrology chart based on birth date
    """
    try:
        # Parse birth date and time
        date_obj = datetime.strptime(f"{birth_date} {birth_time}", "%d/%m/%Y %H:%M")
        
        # Set location coordinates
        location_coords = {
            "SP Capital": (-23.5505, -46.6333),  # São Paulo
            "Santo André - SP": (-23.6639, -46.5384),  # Santo André
            "Itabuna, Bahia": (-14.7856, -39.2803)  # Itabuna
        }
        
        if location not in location_coords:
            logger.warning(f"Location {location} not found, using São Paulo coordinates")
            lat, lon = location_coords["SP Capital"]
        else:
            lat, lon = location_coords[location]
        
        # Simplified zodiac sign calculation based on birth date
        zodiac_signs = ['Capricorn', 'Aquarius', 'Pisces', 'Aries', 'Taurus', 'Gemini', 
                       'Cancer', 'Leo', 'Virgo', 'Libra', 'Scorpio', 'Sagittarius']
        
        # Calculate sun sign based on birth date
        month = date_obj.month
        day = date_obj.day
        
        def get_sun_sign(month, day):
            if (month == 3 and day >= 21) or (month == 4 and day <= 19):
                return "Aries"
            elif (month == 4 and day >= 20) or (month == 5 and day <= 20):
                return "Taurus"
            elif (month == 5 and day >= 21) or (month == 6 and day <= 20):
                return "Gemini"
            elif (month == 6 and day >= 21) or (month == 7 and day <= 22):
                return "Cancer"
            elif (month == 7 and day >= 23) or (month == 8 and day <= 22):
                return "Leo"
            elif (month == 8 and day >= 23) or (month == 9 and day <= 22):
                return "Virgo"
            elif (month == 9 and day >= 23) or (month == 10 and day <= 22):
                return "Libra"
            elif (month == 10 and day >= 23) or (month == 11 and day <= 21):
                return "Scorpio"
            elif (month == 11 and day >= 22) or (month == 12 and day <= 21):
                return "Sagittarius"
            elif (month == 12 and day >= 22) or (month == 1 and day <= 19):
                return "Capricorn"
            elif (month == 1 and day >= 20) or (month == 2 and day <= 18):
                return "Aquarius"
            else:
                return "Pisces"
        
        sun_sign = get_sun_sign(month, day)
        
        # Simplified house calculation based on time
        hour = date_obj.hour
        def estimate_ascendant(sun_sign, hour):
            # Very simplified ascendant estimation
            ascendants = {
                "Aries": ["Aries", "Taurus", "Gemini", "Cancer"],
                "Taurus": ["Taurus", "Gemini", "Cancer", "Leo"],
                "Gemini": ["Gemini", "Cancer", "Leo", "Virgo"],
                "Cancer": ["Cancer", "Leo", "Virgo", "Libra"],
                "Leo": ["Leo", "Virgo", "Libra", "Scorpio"],
                "Virgo": ["Virgo", "Libra", "Scorpio", "Sagittarius"],
                "Libra": ["Libra", "Scorpio", "Sagittarius", "Capricorn"],
                "Scorpio": ["Scorpio", "Sagittarius", "Capricorn", "Aquarius"],
                "Sagittarius": ["Sagittarius", "Capricorn", "Aquarius", "Pisces"],
                "Capricorn": ["Capricorn", "Aquarius", "Pisces", "Aries"],
                "Aquarius": ["Aquarius", "Pisces", "Aries", "Taurus"],
                "Pisces": ["Pisces", "Aries", "Taurus", "Gemini"]
            }
            hour_index = hour // 6  # Divide day into 4 periods
            return ascendants.get(sun_sign, ["Aries"])[hour_index % len(ascendants.get(sun_sign, ["Aries"]))]
        
        ascendant_sign = estimate_ascendant(sun_sign, hour)
        
        # Simplified Chiron position (based on year)
        year = date_obj.year
        chiron_signs = ["Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo", 
                       "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"]
        chiron_sign = chiron_signs[(year - 1977) % 12]  # Chiron cycle approximation
        
        # Build simplified chart data
        chart_data = {
            "birth_info": {
                "date": birth_date,
                "time": birth_time,
                "location": location,
                "coordinates": {"lat": lat, "lon": lon}
            },
            "ascendant": {
                "sign": ascendant_sign,
                "degree": round((hour * 15) % 30, 1)  # Simplified degree calculation
            },
            "planets": {
                "Sun": {
                    "sign": sun_sign,
                    "degree": round(day * 1.2 % 30, 1),
                    "house": 1
                },
                "Chiron": {
                    "sign": chiron_sign,
                    "degree": round((year - 1977) * 2.5 % 30, 1),
                    "house": 8 if chiron_sign in ["Scorpio", "Sagittarius"] else 12
                }
            }
        }
        
        return chart_data
        
    except Exception as e:
        logger.error(f"Error calculating astrology chart: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Astrology calculation error: {e}")

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

# Astrology search route
@api_router.get("/astrology")
def astrology_search(
    chiron: str = Query(None, description="Quíron position"),
    house: str = Query(None, description="Planetary house"),
    position: str = Query(None, description="Planetary position"),
    sign: str = Query(None, description="Zodiac sign"),
    max_results: int = 15
):
    logger.info(f"Astrology search request: chiron='{chiron}', house='{house}', position='{position}', sign='{sign}'")
    
    # Build search query based on astrology parameters
    search_terms = []
    if chiron:
        search_terms.append(f"Quíron {chiron}")
    if house:
        search_terms.append(f"casa {house}")
    if position:
        search_terms.append(f"posição {position}")
    if sign:
        search_terms.append(f"signo {sign}")
    
    if not search_terms:
        logger.warning("No astrology parameters provided")
        raise HTTPException(status_code=400, detail="At least one astrology parameter is required (chiron, house, position, sign)")
    
    query = " ".join(search_terms)
    logger.info(f"Generated astrology query: '{query}'")
    
    try:
        results = search_music_youtube(query, max_results=max_results)
        logger.info(f"Astrology search completed: {len(results)} results found")
        return {
            "query": query,
            "parameters": {
                "chiron": chiron,
                "house": house,
                "position": position,
                "sign": sign
            },
            "results": results
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error in astrology search: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

# Real astrology chart calculation endpoint
@api_router.get("/astrology-chart")
def calculate_chart(
    birth_date: str = Query(..., description="Birth date in DD/MM/YYYY format"),
    birth_time: str = Query(..., description="Birth time in HH:MM format"),
    location: str = Query(..., description="Birth location")
):
    logger.info(f"Astrology chart calculation request: {birth_date} {birth_time} - {location}")
    
    try:
        chart = calculate_astrology_chart(birth_date, birth_time, location)
        logger.info(f"Chart calculated successfully for {location}")
        return chart
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error in chart calculation: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

# User-specific astrology test route
@api_router.get("/test-users")
def test_users_astrology():
    logger.info("Testing astrology endpoints with specific user data")
    
    users = [
        {
            "name": "Astro",
            "birth_date": "28/03/1999",
            "birth_time": "02:02",
            "location": "SP Capital"
        },
        {
            "name": "Roberta", 
            "birth_date": "22/05/1998",
            "birth_time": "16:40",
            "location": "Santo André - SP"
        },
        {
            "name": "Luiz",
            "birth_date": "12/10/1988", 
            "birth_time": "21:45",
            "location": "Itabuna, Bahia"
        }
    ]
    
    results = []
    
    for user in users:
        try:
            # Calculate real astrology chart
            chart = calculate_astrology_chart(user["birth_date"], user["birth_time"], user["location"])
            
            # Build search query based on real chart data
            search_terms = []
            if "Chiron" in chart["planets"]:
                chiron_sign = chart["planets"]["Chiron"]["sign"].lower()
                chiron_house = chart["planets"]["Chiron"]["house"]
                search_terms.append(f"Quíron {chiron_sign} casa {chiron_house}")
            
            if "Sun" in chart["planets"]:
                sun_sign = chart["planets"]["Sun"]["sign"].lower()
                search_terms.append(f"signo {sun_sign}")
            
            if chart["ascendant"]["sign"]:
                asc_sign = chart["ascendant"]["sign"].lower()
                search_terms.append(f"ascendente {asc_sign}")
            
            query = " ".join(search_terms) if search_terms else "astrologia"
            
            # Search for this user
            search_results = search_music_youtube(query, max_results=5)
            
            results.append({
                "user": user["name"],
                "birth_info": f"{user['birth_date']} {user['birth_time']} - {user['location']}",
                "real_chart": {
                    "sun": chart["planets"].get("Sun", {}),
                    "moon": chart["planets"].get("Moon", {}),
                    "chiron": chart["planets"].get("Chiron", {}),
                    "ascendant": chart["ascendant"]
                },
                "astrology_query": query,
                "results_count": len(search_results),
                "sample_results": search_results[:2] if search_results else []
            })
            
        except Exception as e:
            logger.error(f"Error testing user {user['name']}: {str(e)}")
            results.append({
                "user": user["name"],
                "error": str(e)
            })
    
    return {
        "message": "Astrology tests completed for all users",
        "users_tested": len(users),
        "results": results
    }

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
