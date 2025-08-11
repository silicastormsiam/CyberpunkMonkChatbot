# File Name: monk_bot.py
# Owner: Andrew John Holland
# Purpose: FastAPI backend to proxy Gemini AI requests securely using .env key with google-generativeai, prompts.py, and database.py. Serves frontend and static assets.
# Version: v2.9
# Last Updated: 2025-08-11
# Change Log:
# 1. v2.9 - Added StaticFiles mounts for /static and /frontend; added homepage route to serve ../frontend/index.html; retained existing CORS and DB init.
# 2. v2.8 - Load .env from project root explicitly; clarified CORS; minor log hardening
# 3. v2.7 - Fixed logger.getLogger(name), file references, and SQLite error logging
# 4. v2.6 - Fixed CORS import to CORSMiddleware
# 5. v2.5 - Fixed SyntaxError for unterminated string
# 6. v2.4 - Updated for PostgreSQL integration
# 7. v2.3 - Prepared for Hostinger VPS deployment

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from starlette.responses import FileResponse
from pydantic import BaseModel
from dotenv import load_dotenv
import os
import google.generativeai as genai
import logging
import psycopg2
from .prompts import get_prompt
from .database import init_db, DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASSWORD

# Ensure logs dir exists
LOG_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'logs'))
os.makedirs(LOG_DIR, exist_ok=True)

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(os.path.join(LOG_DIR, 'execution.log')),
        logging.FileHandler(os.path.join(LOG_DIR, 'error.log')),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Load .env from project root explicitly
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
load_dotenv(os.path.join(PROJECT_ROOT, '.env'))

api_key = os.getenv('GOOGLE_API_KEY')
if not api_key:
    logger.error("GOOGLE_API_KEY not found in .env")
    raise ValueError("GOOGLE_API_KEY not found in .env")
genai.configure(api_key=api_key)

# FastAPI app + CORS
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1",
        "http://127.0.0.1:8000",
        "http://192.168.1.225",
        "http://192.168.1.225:80",
        "http://192.168.1.225:8000",
        "*",  # dev only; tighten for production
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---- Serve static assets and frontend ----
STATIC_DIR = os.path.abspath(os.path.join(PROJECT_ROOT, 'static'))
FRONTEND_DIR = os.path.abspath(os.path.join(PROJECT_ROOT, 'frontend'))

app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")
app.mount("/frontend", StaticFiles(directory=FRONTEND_DIR), name="frontend")

@app.get("/")
async def serve_homepage():
    index_path = os.path.join(FRONTEND_DIR, 'index.html')
    if not os.path.exists(index_path):
        logger.error(f"index.html not found at {index_path}")
        raise HTTPException(status_code=404, detail="index.html not found")
    return FileResponse(index_path)

# Initialize database (PG → fallback SQLite handled inside)
init_db()
logger.info("Database initialized")

class ChatRequest(BaseModel):
    message: str

def get_cached_data(query: str) -> str:
    """Query data_cache for latest relevant content based on the query."""
    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            port=DB_PORT,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD
        )
        c = conn.cursor()
        c.execute(
            "SELECT content FROM data_cache WHERE content LIKE %s ORDER BY timestamp DESC LIMIT 1",
            (f'%{query}%',),
        )
        result = c.fetchone()
        conn.close()
        return result[0] if result else ""
    except Exception as e:
        logger.warning(f"PostgreSQL query failed: {str(e)}. Falling back to SQLite.")
        try:
            import sqlite3
            from .database import DB_PATH
            conn = sqlite3.connect(DB_PATH)
            c = conn.cursor()
            c.execute(
                "SELECT content FROM data_cache WHERE content LIKE ? ORDER BY timestamp DESC LIMIT 1",
                (f'%{query}%',),
            )
            result = c.fetchone()
            conn.close()
            return result[0] if result else ""
        except Exception as e2:
            logger.error(f"SQLite query failed: {str(e2)}")
            return ""

@app.post("/api/chat")
async def chat(request: ChatRequest):
    logger.info("Received request at /api/chat")
    message = (request.message or "").strip()
    if not message:
        logger.warning("No message provided in request")
        raise HTTPException(status_code=400, detail="No message provided")

    try:
        # Query cached data
        cached_data = get_cached_data(message)
        if cached_data:
            logger.info(f"Cached data found ({len(cached_data)} chars)")
        else:
            logger.info("No cached data found")

        # Generate CP Monk prompt
        prompt = get_prompt(message, cached_data)
        logger.info(f"Generated prompt ({len(prompt)} chars)")

        # Call Gemini AI
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content(prompt)
        bot_text = getattr(response, "text", "") or "No response from CP Monk"

        logger.info(f"Generated response ({min(len(bot_text), 80)} chars preview)")
        return {"response": bot_text}
    except Exception as e:
        logger.error(f"Error generating response: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == '__main__':
    import uvicorn
    logger.info("Starting FastAPI server on 0.0.0.0:5000")
    uvicorn.run(app, host="0.0.0.0", port=5000)
