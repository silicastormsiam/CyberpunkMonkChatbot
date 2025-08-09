# File Name: app.py
# Owner: Andrew John Holland
# Purpose: Flask application for the Cyberpunk Monk Chatbot, handling HTTP requests and Gemini API integration.
# Version: v2.3
# Last Updated: 2025-08-08
# Change Log:
# 1. Initial creation of Flask structure - 2025-08-07
# 2. Added Gemini API integration - 2025-08-07
# 3. Added CORS support - 2025-08-07
# 4. Implemented /monk route with query handling - 2025-08-07
# 5. Added execution and error logging - 2025-08-07
# 6. Updated to serve chat.html - 2025-08-08
# 7. Added retry logic for Gemini API 429 errors - 2025-08-08
# 8. Fixed log path to '../logs/execution.log' - 2025-08-08
# 9. Incremented version to v1.9, ensured environment compatibility - 2025-08-08
# 10. Fixed static file routing for chat.html, incremented to v2.0 - 2025-08-08
# 11. Fixed database query to use 'url' column, incremented to v2.1 - 2025-08-08
# 12. Enabled debug mode, enhanced static file checks, incremented to v2.2 - 2025-08-08
# 13. Simplified routing, added fallback response, incremented to v2.3 - 2025-08-08

import logging
import os
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from prompts import get_prompt
import google.generativeai as genai
import sqlite3
import time
from google.api_core.exceptions import ResourceExhausted

app = Flask(__name__, static_folder="../static")
CORS(app)
logging.basicConfig(
    filename="../logs/execution.log",
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

genai.configure(api_key=os.getenv('GEMINI_API_KEY'))
model = genai.GenerativeModel('gemini-1.5-flash')

@app.route('/')
def serve_chat():
    chat_path = os.path.join(app.static_folder, 'chat.html')
    logging.debug(f"Attempting to serve chat.html from {chat_path}")
    if not os.path.exists(chat_path):
        logging.error("chat.html not found in static folder")
        return "Error: chat.html not found in static folder", 404
    return send_from_directory(app.static_folder, 'chat.html')

@app.route('/static/<path:filename>')
def serve_static(filename):
    file_path = os.path.join(app.static_folder, filename)
    logging.debug(f"Attempting to serve static file: {filename}")
    if not os.path.exists(file_path):
        logging.error(f"Static file {filename} not found")
        return f"Error: {filename} not found", 404
    return send_from_directory(app.static_folder, filename)

@app.route('/monk', methods=['POST'])
def monk_endpoint():
    try:
        start_time = time.time()
        data = request.get_json()
        query = data.get('message', '').strip().lower()
        logging.debug(f"Received POST request to /monk: {data}")

        conn = sqlite3.connect('../data_cache.db')
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='data_cache'")
        if not cursor.fetchone():
            logging.error("Table 'data_cache' does not exist")
            raise Exception("Table 'data_cache' does not exist")
        cursor.execute("SELECT content FROM data_cache WHERE url LIKE ?", ('%' + query + '%',))
        result = cursor.fetchone()
        conn.close()

        data_content = result[0] if result else ""
        prompt = get_prompt(query, data_content)
        retries = 3
        for attempt in range(retries):
            try:
                response = model.generate_content(prompt)
                break
            except ResourceExhausted as e:
                if attempt < retries - 1:
                    logging.warning(f"429 error on attempt {attempt + 1}, retrying in {e.retry_delay} seconds")
                    time.sleep(e.retry_delay)
                else:
                    logging.error(f"Error in /monk endpoint: {str(e)}")
                    return jsonify({"error": str(e)}), 500

        response_text = response.text if response else "No response generated."
        latency = time.time() - start_time
        logging.info(f"Generated response for query: {query}, latency: {latency:.2f}s")
        return jsonify({"response": response_text})
    except Exception as e:
        logging.error(f"Error in /monk endpoint: {str(e)}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    logging.info("Starting Flask application")
    app.run(host='0.0.0.0', port=5000, debug=True)  # Debug mode enabled