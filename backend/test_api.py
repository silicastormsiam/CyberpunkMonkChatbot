# File Name: test_api.py
# Owner: Andrew John Holland
# Purpose: Tests the Google Gemini API connection and configuration for the Cyberpunk Monk Chatbot project.
# Version Control: v1.1
# Change Log:
# 1. Initial creation for API testing - 2025-08-07
# 2. Added dotenv for key loading - 2025-08-07
# 3. Configured genai with updated SDK syntax - 2025-08-07
# 4. Included generate_content test - 2025-08-07
# 5. Added execution and error logging with standardized metadata - 2025-08-08

import google.generativeai as genai
from dotenv import load_dotenv
import os
import logging

os.makedirs("../logs", exist_ok=True)
execution_handler = logging.FileHandler("../logs/execution.log")
execution_handler.setLevel(logging.DEBUG)
error_handler = logging.FileHandler("../logs/error.log", mode='a')
error_handler.setLevel(logging.ERROR)
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        execution_handler,
        error_handler,
        logging.StreamHandler()
    ]
)

def test_api():
    try:
        logging.info("Starting API test")
        load_dotenv()
        genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
        model = genai.GenerativeModel("gemini-1.5-flash")
        logging.debug("Generating content for 'Hello, world!'")
        response = model.generate_content("Hello, world!")
        logging.info(f"API response: {response.text}")
        print(response.text)
    except Exception as e:
        logging.error(f"Error in API test: {str(e)}")
        raise

if __name__ == "__main__":
    logging.info("Executing test_api.py")
    test_api()