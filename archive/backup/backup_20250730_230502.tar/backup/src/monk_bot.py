# File Name: monk_bot.py
# Owner: Andrew Holland (@SilicaStormSiam)
# Purpose: Implements the Flask-based Cyberpunk Monk chatbot, providing predefined responses about SilicaStormSiam's projects for the CPM - Chat Bot project.
# Version Control:
#   - Version 1.13 (2025-07-26): Re-uploaded to Hostinger.com at /home/u605846297/public_html/chatbot/scripts/ with updated deployment.
#   - Version 1.12 (2025-07-24): Updated projects response with GitHub project names: CPM - Chat Bot Development, ATS - Recruitment Application Tracking System, Homelab Hardware Development, Project Dashboards on GitHub.
#   - Version 1.11 (2025-07-23): Updated projects response with initial names.
#   - Version 1.10 (2025-07-23): Fixed static_folder path to '../assets'.
#   - Version 1.9 (2025-07-23): Adjusted static_folder and added static file serving.
#   - Version 1.8 (2025-07-23): Fixed NameError with send_from_directory.

from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import logging
import os

app = Flask(__name__, static_folder='../assets')
CORS(app)  # Enable CORS for all routes

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

# Predefined responses for the Cyberpunk Monk
responses = {
    "hello": "Greetings, seeker. I am the Cyberpunk Monk, weaving code and karma in the neon-lit chaos. Ask me about SilicaStormSiam's projects or seek digital wisdom.",
    "about": "I am a digital bodhisattva, created by Andrew Holland (@SilicaStormSiam) to bridge tech and spirit. Explore my creator's work at github.com/SilicaStormSiam, youtube.com/@SilicaStormSiam, or www.andrew-holland.com.",
    "github": "SilicaStormSiam's GitHub (github.com/SilicaStormSiam) hosts projects on home automation, cybersecurity, and Python tutorials. Name a project for details, choom!",
    "homelab": "The homelab is a temple of tech, running Proxmox VMs for Home Assistant. It controls lighting and climate with Python scripts, saving 30% energy. Ask about specific setups or check github.com/SilicaStormSiam.",
    "cybersecurity": "Cybersecurity is my mantra. SilicaStormSiam builds DNS-based threat protection (e.g., Pi-hole, AdGuard) to guard the digital realm. Want tips on securing your network? See github.com/SilicaStormSiam.",
    "python": "Python is the sutra of my creator's craft. Scripts for automation, cybersecurity, and tutorials live at github.com/SilicaStormSiam. Watch youtube.com/@SilicaStormSiam for lessons. Got a coding query?",
    "youtube": "At youtube.com/@SilicaStormSiam, my creator shares tutorials on home automation, cybersecurity, and Python. Each video is a step toward digital enlightenment. What topic do you seek?",
    "portfolio": "Visit www.andrew-holland.com for my creator’s journey from airline ops (Kronos, AIMS) to project management and homelabs. It’s a path of balance and tech. Want specifics?",
    "projects": "SilicaStormSiam’s projects include: 1) CPM - Chat Bot Development, 2) ATS - Recruitment Application Tracking System, 3) Homelab Hardware Development, 4) Project Dashboards on GitHub. Ask about one or visit github.com/SilicaStormSiam!",
    "default": "Code is karma, seeker. Your query flickers in the neon haze—rephrase for clarity."
}

@app.route('/')
def index():
    try:
        app.logger.debug(f"Attempting to serve chat.html from {os.path.join(app.static_folder, 'chat.html')}")
        if not os.path.exists(os.path.join(app.static_folder, 'chat.html')):
            app.logger.error("chat.html not found in assets/")
            return "chat.html not found", 404
        return send_from_directory(app.static_folder, 'chat.html')
    except Exception as e:
        app.logger.error(f"Error serving chat.html: {str(e)}")
        return str(e), 500

@app.route('/<path:filename>')
def serve_static(filename):
    try:
        app.logger.debug(f"Attempting to serve static file: {filename}")
        return send_from_directory(app.static_folder, filename)
    except Exception as e:
        app.logger.error(f"Error serving static file {filename}: {str(e)}")
        return str(e), 404

@app.route('/monk', methods=['POST', 'GET'])
def respond():
    try:
        if request.method == 'GET':
            app.logger.debug("Received GET request to /monk")
            return jsonify({"response": responses["hello"]})
        
        app.logger.debug(f"Received POST request to /monk: {request.get_data(as_text=True)}")
        if not request.is_json:
            app.logger.error("Request is not JSON")
            return jsonify({"error": "Request must be JSON"}), 400
        
        user_msg = request.json.get('message', '').lower().strip()
        if not user_msg:
            app.logger.error("No message provided in request")
            return jsonify({"error": "No message provided"}), 400
        
        for key in responses:
            if key in user_msg:
                app.logger.debug(f"Matched key '{key}' in message: {user_msg}")
                return jsonify({"response": responses[key]})
        
        app.logger.debug(f"No matching key for message: {user_msg}")
        return jsonify({"response": responses["default"]})
    except Exception as e:
        app.logger.error(f"Error in /monk endpoint: {str(e)}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)