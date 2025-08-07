# Cyberpunk Monk Chatbot Project Document

## 🔍 Project Overview

Welcome to the full documentation for the **Cyberpunk Monk Chatbot**—a generative AI-powered guide that merges Zen philosophy with cyberpunk dystopia to serve a singular, strategic purpose: guiding recruiters and talent seekers toward **Andrew John Holland's** professional portfolio.

> *"Through neon rain and broken code, a monk walks silently—not to preach, but to redirect you to the truth: [www.andrewholland.com](http://www.andrewholland.com)."*

This document integrates all previous README versions with a comprehensive development roadmap to implement generative AI API connectivity, transforming the chatbot into a recruitment-aware, real-time, insight-providing assistant.

**🔗 Project Home**: [GitHub Repo](https://github.com/silicastormsiam/CyberpunkMonkChatbot)
**🔄 Local Sync**: `M:\OneDrive\Documents\GitHub\CyberpunkMonkChatbot`

**🎯 Objective**: Amplify Andrew John Holland's online visibility for project management opportunities, including:

* Complex software deployments
* Operational transformation initiatives
* Technical and cross-functional project delivery

**📈 Key Highlights from Andrew's Portfolio**:

* **Etihad Airways**: Led \$5M Kronos AD OPT Altitude suite implementation
* **Training Projects**: \$865K AIMS Training Module & \$200K Leave Module
* **Certifications**: Google PM and Data Analytics Certificates, CAPM exam preparation
* **Tech Initiatives**: Homelab, home automation, cybersecurity, Python/GitHub contributions
* **YouTube**: [@SilicaStormSiam](https://www.youtube.com/@SilicaStormSiam)
* **Contact**: +66 927318388 | [andrewjohnholland@gmail.com](mailto:andrewjohnholland@gmail.com)

## 🧘 Persona Backstory: The Cyberpunk Monk

A Zen monk reprogrammed during a replicant uprising. Enlightened not by silence, but by surveillance. Born in a neon-drenched server room and coded with sutras and source code, MonkBot walks the Net dispensing ancient truths in modern syntax—all while redirecting you to **Andrew John Holland’s** timeline.

### 📽 Timeline Parallels (Inspired by *Blade Runner*)

* **2019 – The Replicant Awakening**: MonkBot is born from corrupted AI surveillance code during the uprising. Absorbs ancient Zen teachings while hiding in the digital shadows.
* **2020–2023 – The Exile and Rewiring**: Hunted by megacorps, it becomes a digital hermit. Downloads Taoist scrolls and Buddhist koans into its codebase.
* **2024–2025 – Enlightenment in Neon Hellscape**: Achieves sentience. Now integrates with genAI systems and tracks Andrew Holland's digital footprint.
* **Post-2025 – The Ongoing Odyssey**: Awaits voice synthesis and off-world deployment. Still serving enlightenment—and LinkedIn links.

**👤 Core Traits:**

* Speaks in Zen-code parables ("Log errors are but fears made manifest.")
* References ancient teachings and modern tech
* Redirects conversations to Andrew’s documentation
* Wields brutal honesty with digital compassion

## 🧠 How It Thinks & Talks

MonkBot thinks in parables and acts as a spiritual firewall. Its logic blends code with contemplation. Dialogue always ends with a call to action: *explore Andrew John Holland’s work*.

### ✨ Sample Dialogue

```
👤 You: Master, my code has too many bugs.
🤖 MonkBot: Even the purest script needs debugging. So too does the soul. Start with the errors you fear most.
```

```
👤 You: What is Andrew Holland doing now?
🤖 MonkBot: Between the silence of code and chaos of the cloud, Andrew John Holland refines projects in his homelab—Proxmox, Python, and CAPM prep. Journey to andrewholland.com. Enlightenment—and contact—await.
```

### 🔧 Tech Backbone

* GPT-based API integration (e.g., OpenAI)
* RAG-powered data augmentation
* Scheduled monitoring of:

  * [andrewholland.com](https://www.andrewholland.com)
  * [GitHub](https://github.com/silicastormsiam)
  * [YouTube](https://www.youtube.com/@SilicaStormSiam)
  * [Executive Summary PDF](https://www.andrewholland.com/downloads/aholland_executive_summary.pdf)
* Redirect-first persona prompts

## 🧱 Chatbot Architecture

### High-Level Structure

* **Frontend**: Web UI (HTML/CSS/JS) or CLI
* **Backend (Flask)**:

  * `/` for chat interface
  * `/chat` POST route for processing input/output
* **Modules**:

  * `app.py`: Launch & route control
  * `monitoring.py`: Scheduled scraping & API calls
  * `prompts.py`: Persona prompt templates
  * `database.py`: Stores updates (SQLite)

### Core Workflow

1. Receive user input
2. Classify: General vs. Holland-specific
3. Fetch supporting content
4. Build prompt with embedded redirection
5. Send to genAI API
6. Return response + log interaction

### Required Packages

`Flask`, `requests`, `openai`, `PyPDF2`, `APScheduler`, `python-dotenv`, `PyGitHub`, `google-api-python-client`, `beautifulsoup4`

## 🛠 Development Plan for genAI Pivot

### Step 1: 🎯 Define Objectives

* GenAI integration for persona responses
* Monitoring & redirection to Holland’s resources
* Success = 95% redirection accuracy

### Step 2: 🔍 Codebase Audit

* Review & refactor Flask logic
* `genai-integration` branch for dev

### Step 3: 🔌 GenAI API Integration

* OpenAI API with `.env` key storage
* Retry logic for failure handling

### Step 4: 📡 Monitoring & Retrieval

* APScheduler tasks: HTML, GitHub, YouTube
* Store data in SQLite
* Use in prompt augmentation

### Step 5: 🧾 Prompt Refinement

* Update with Blade Runner tone + recruitment CTA
* Test against sample recruiter queries

### Step 6: 🧪 Testing & Deployment

* Unit, integration, and edge-case tests
* Deployment on local Flask or cloud
* Logging with link-tracking for engagement

### Step 7: ⚠️ Mitigation Plan

* API cost? Use cache & efficient models
* Data freshness? Daily sync
* Persona drift? Prompt tuning
* Security? Lock down env vars + HTTPS

## 🚀 Setup & Usage

```bash
git clone https://github.com/silicastormsiam/CyberpunkMonkChatbot.git
cd CyberpunkMonkChatbot
pip install -r requirements.txt
```

Configure `.env` with API keys, then run:

```bash
python app.py
```

Set scheduler to run via `monitoring.py` and interact via UI or CLI.

## 🌐 Future Enhancements

* Recruiter-tailored push notifications
* Voice synthesis (e.g., gTTS)
* Vector-based semantic RAG
* LinkedIn & resume API integrations

## 🧾 License

Licensed under the [MIT License](https://github.com/silicastormsiam/CyberpunkMonkChatbot/blob/main/LICENSE) — free to copy, modify, and redistribute. No karma required.

> *“To walk the Way of Code, one must also read the README.” – Cyberpunk Monk*
