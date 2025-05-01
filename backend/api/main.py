from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from googleapiclient.discovery import build
from dotenv import load_dotenv
import os

# Carregar variáveis de ambiente
load_dotenv()

YOUTUBE_API_KEY = os.getenv("API_KEY")

if not YOUTUBE_API_KEY:
    raise SystemExit("API_KEY não encontrada no .env ou nas variáveis do Heroku.")

# Inicializar o app
app = FastAPI()

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "https://music-search-liart.vercel.app",
        "https://music-search-git-main-lmgaspas-projects.vercel.app",
        "https://music-search-langchain.vercel.app",
        "*"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Função para buscar músicas no YouTube
def search_music_youtube(query: str, max_results: int = 5):
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
                "thumbnail": item["snippet"]["thumbnails"]["high"]["url"]  # ✅ adicionando imagem
            }
            for item in search_response.get("items", [])
        ]

        return music_results

    except Exception as e:
        return {"error": str(e)}

# Rota principal de busca
@app.get("/search")
def search_route(q: str = Query(..., description="Consulta da música!")):
    results = search_music_youtube(q)
    return {"results": results}

# Rota de saúde (para teste com curl)
@app.get("/health")
def health_check():
    return {"status": "ok"}
