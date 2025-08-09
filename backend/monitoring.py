# File Name: monitoring.py
# Owner: Andrew John Holland
# Purpose: Monitors and caches content from specified URLs for the Cyberpunk Monk Chatbot, storing in data_cache.db.
# Version: v1.8
# Last Updated: 2025-08-08
# Change Log:
# 1. Initial creation of monitoring script - 2025-08-07
# 2. Added URL fetching and database storage - 2025-08-07
# 3. Integrated APScheduler for periodic execution - 2025-08-07
# 4. Standardized logging to execution.log - 2025-08-07
# 5. Added progress meter for URL caching - 2025-08-08
# 6. Fixed log path to '../logs/execution.log' for project root - 2025-08-08
# 7. Removed BlockingScheduler, run once, added timeout handling - 2025-08-08
# 8. Incremented version to v1.8 - 2025-08-08

import logging
import sqlite3
import requests
from tqdm import tqdm
from urllib.parse import urlparse
import time

logging.basicConfig(filename='../logs/execution.log', level=logging.DEBUG)

def monitor_urls():
    urls = [
        "http://www.andrewholland.com",
        "https://www.andrewholland.com/career/Career_Identity.html",
        "https://www.andrewholland.com/timeline/index.html",
        "https://github.com/silicastormsiam",
        "https://www.youtube.com/@SilicaStormSiam",
        "https://www.andrewholland.com/downloads/aholland_executive_summary.pdf"
    ]
    conn = sqlite3.connect('../data_cache.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS data_cache (url TEXT PRIMARY KEY, content TEXT)''')
    conn.commit()

    progress_bar = tqdm(urls, desc="Caching URLs", unit="url")
    for url in progress_bar:
        try:
            response = requests.get(url, timeout=5)
            response.raise_for_status()
            content = response.text
            cursor.execute("INSERT OR REPLACE INTO data_cache (url, content) VALUES (?, ?)", (url, content))
            conn.commit()
            logging.info(f"Successfully cached data from {url}")
            progress_bar.set_postfix(status=f"Cached {urlparse(url).netloc}")
        except requests.exceptions.RequestException as e:
            logging.error(f"Failed to cache {url}: {str(e)}")
            progress_bar.set_postfix(status=f"Failed {urlparse(url).netloc}")
    conn.close()
    logging.info("Monitoring completed")

if __name__ == "__main__":
    logging.info("Executing monitoring.py")
    try:
        monitor_urls()
    except Exception as e:
        logging.error(f"Monitoring failed: {str(e)}")
    finally:
        logging.info("Monitoring script finished")