Set-Content -Path "M:\OneDrive\Documents\GitHub\CyberpunkMonkChatbot\backend\database.py" -Value @"
"""
File: backend/database.py
Owner: Andrew John Holland
Purpose: Manages PostgreSQL database for caching data retrieved from Holland's URLs for the Cyberpunk Monk Chatbot
Version: 2.5
Change Log:
v2.5 - Fixed SyntaxError at line 1
v2.4 - Fixed invalid content at line 1
v2.3 - Re-verified syntax for line 38 issue
"""
import os
import logging
import psycopg2
from dotenv import load_dotenv

# Setup logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(os.path.join(os.path.dirname(__file__), '../logs/execution.log')),
        logging.FileHandler(os.path.join(os.path.dirname(__file__), '../logs/error.log')),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Load .env from root
load_dotenv(os.path.join(os.path.dirname(__file__), '..'))
DB_HOST = os.getenv('DB_HOST', 'localhost')
DB_PORT = os.getenv('DB_PORT', '5432')
DB_NAME = os.getenv('DB_NAME', 'cyberpunk_monk')
DB_USER = os.getenv('DB_USER', 'postgres')
DB_PASSWORD = os.getenv('DB_PASSWORD', 'Predator67')

# Fallback SQLite path
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
DB_PATH = os.path.join(PROJECT_ROOT, 'data_cache.db')

def init_db():
    """Initialize PostgreSQL or SQLite database."""
    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            port=DB_PORT,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD
        )
        logger.debug(f'Connected to PostgreSQL database at {DB_HOST}:{DB_PORT}/{DB_NAME}')
        c = conn.cursor()
        c.execute('''
            CREATE TABLE IF NOT EXISTS data_cache (
                id SERIAL PRIMARY KEY,
                url TEXT,
                content TEXT,
                timestamp TIMESTAMP
            )
        ''')
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
            c.execute('''
                CREATE TABLE IF NOT EXISTS data_cache (
                    id INTEGER PRIMARY KEY,
                    url TEXT,
                    content TEXT,
                    timestamp DATETIME
                )
            ''')
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