Set-Content -Path "M:\OneDrive\Documents\GitHub\CyberpunkMonkChatbot\backend\monk_bot.py" -Value @"
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
import os
import logging
import google.generativeai as genai
import psycopg2
from .prompts import get_prompt
from .database import init_db, DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASSWORD

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(os.path.join(os.path.dirname(__file__), '../logs/execution.log')),
        logging.FileHandler(os.path.join(os.path.dirname(__file__), '../logs/error.log')),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

load_dotenv(os.path.join(os.path.dirname(__file__), '..'))
api_key = os.getenv('GOOGLE_API_KEY')
if not api_key:
    logger.error('GOOGLE_API_KEY not found in .env')
    raise ValueError('GOOGLE_API_KEY not found in .env')
genai.configure(api_key=api_key)

init_db()
logger.info('Database initialized')

class ChatRequest(BaseModel):
    message: str

def get_cached_data(query: str) -> str:
    try:
        conn = psycopg2.connect(host=DB_HOST, port=DB_PORT, database=DB_NAME, user=DB_USER, password=DB_PASSWORD)
        c = conn.cursor()
        c.execute('SELECT content FROM data_cache WHERE content LIKE %s ORDER BY timestamp DESC LIMIT 1', (f'%{query}%',))
        result = c.fetchone()
        conn.close()
        return result[0] if result else ''
    except Exception as e:
        logger.warning(f'PostgreSQL query failed: {str(e)}. Falling back to SQLite.')
        try:
            import sqlite3
            conn = sqlite3.connect(DB_PATH)
            c = conn.cursor()
            c.execute('SELECT content FROM data_cache WHERE content LIKE ? ORDER BY timestamp DESC LIMIT 1', (f'%{query}%',))
            result = c.fetchone()
            conn.close()
            return result[0] if result else ''
        except Exception as e2:
            logger.error(f'SQLite query failed: {str(e2)}')
            return ''

@app.post('/api/chat')
async def chat(request: ChatRequest):
    message = request.message
    if not message:
        raise HTTPException(status_code=400, detail='No message provided')
    cached_data = get_cached_data(message)
    prompt = get_prompt(message, cached_data)
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content(prompt)
    return {'response': response.text}

if __name__ == '__main__':
    import uvicorn
    logger.info('Starting FastAPI server on 0.0.0.0:5000')
    uvicorn.run(app, host='0.0.0.0', port=5000)
"@

Set-Content -Path "M:\OneDrive\Documents\GitHub\CyberpunkMonkChatbot\backend\database.py" -Value @"
import os
import logging
import psycopg2
from dotenv import load_dotenv

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s', handlers=[logging.FileHandler(os.path.join(os.path.dirname(__file__), '../logs/execution.log')), logging.FileHandler(os.path.join(os.path.dirname(__file__), '../logs/error.log')), logging.StreamHandler()])
logger = logging.getLogger(__name__)

load_dotenv(os.path.join(os.path.dirname(__file__), '..'))
DB_HOST = os.getenv('DB_HOST', 'localhost')
DB_PORT = os.getenv('DB_PORT', '5432')
DB_NAME = os.getenv('DB_NAME', 'cyberpunk_monk')
DB_USER = os.getenv('DB_USER', 'postgres')
DB_PASSWORD = os.getenv('DB_PASSWORD', 'Predator67')

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
DB_PATH = os.path.join(PROJECT_ROOT, 'data_cache.db')

def init_db():
    try:
        conn = psycopg2.connect(host=DB_HOST, port=DB_PORT, database=DB_NAME, user=DB_USER, password=DB_PASSWORD)
        logger.debug(f'Connected to PostgreSQL database at {DB_HOST}:{DB_PORT}/{DB_NAME}')
        c = conn.cursor()
        c.execute('CREATE TABLE IF NOT EXISTS data_cache (id SERIAL PRIMARY KEY, url TEXT, content TEXT, timestamp TIMESTAMP)')
        conn.commit()
        logger.info('PostgreSQL database initialized with table data_cache')
        c.execute("SELECT EXISTS (SELECT FROM information_schema.tables WHERE table_name = 'data_cache')")
        if c.fetchone()[0]:
            logger.debug('Table data_cache confirmed to exist')
        else:
            logger.error('Table data_cache not created')
            raise Exception('Failed to create table data_cache')
        conn.close()
    except Exception as e:
        logger.warning(f'PostgreSQL failed: {str(e)}. Falling back to SQLite.')
        try:
            import sqlite3
            conn = sqlite3.connect(DB_PATH)
            logger.debug(f'Connected to SQLite database at: {DB_PATH}')
            c = conn.cursor()
            c.execute('CREATE TABLE IF NOT EXISTS data_cache (id INTEGER PRIMARY KEY, url TEXT, content TEXT, timestamp DATETIME)')
            conn.commit()
            logger.info('SQLite database initialized with table data_cache')
            c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='data_cache'")
            if c.fetchone():
                logger.debug('Table data_cache confirmed to exist')
            else:
                logger.error('Table data_cache not created')
                raise Exception('Failed to create table data_cache')
            conn.close()
        except Exception as e2:
            logger.error(f'SQLite initialization failed: {str(e2)}')
            raise
"@

cd M:\OneDrive\Documents\GitHub\CyberpunkMonkChatbot
python -m backend.monk_bot