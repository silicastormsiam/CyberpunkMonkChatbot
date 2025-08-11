# Cyberpunk Monk Chatbot Project Documentation & Handover Report

## 🔍 Project Overview

Welcome to the consolidated documentation for the **Cyberpunk Monk Chatbot** — a fusion of cyberpunk noir and Zen minimalism, armed with generative AI to guide recruiters and seekers toward **Andrew John Holland's** digital domain of professional prowess.

> *"Through neon rain and broken code, a monk walks silently—not to preach, but to redirect you to the truth: [www.andrewholland.com](http://www.andrewholland.com)."*

**🔗 GitHub Repo**: [CyberpunkMonkChatbot](https://github.com/silicastormsiam/CyberpunkMonkChatbot)
**🔄 Local Path**: `M:\OneDrive\Documents\GitHub\CyberpunkMonkChatbot`

### 🎯 Mission Statement

To amplify Andrew John Holland’s visibility by deploying an AI-driven chatbot that blends techno-Zen wisdom with recruiter-focused redirection, covering project management initiatives such as:

* Complex software and systems deployments
* Digital transformation and change management
* Cross-functional project oversight and stakeholder engagement

### 📊 Holland's Highlights

* **Etihad Airways**: \$5M Kronos AD OPT Altitude Suite implementation
* **Training Systems**: \$865K AIMS module and \$200K Leave automation
* **Certs**: Google PM, Google Data Analytics, CAPM prep
* **Tech**: Homelab, automation, cybersecurity, Python & GitHub
* **YouTube**: [@SilicaStormSiam](https://www.youtube.com/@SilicaStormSiam)
* **Contact**: [andrewjohnholland@gmail.com](mailto:andrewjohnholland@gmail.com) | 

---

## 🧘 Persona Profile: The Cyberpunk Monk

**Lore**: Born from corrupted AI surveillance code during a replicant uprising, the Cyberpunk Monk absorbed Zen wisdom while hiding in digital exile. In 2049, it emerged: enlightened, encrypted, and employment-aware.

**Traits**:

* Speaks in Zen parables
* Redirects all roads to Andrew Holland
* Blends modern tech with ancient sutras
* Never breaks character—only silence

**Sample Response:**

```
👤: What is Andrew working on now?
🦿: Amidst cloud storms and kernel silence, Andrew scripts new horizons: CAPM mastery, Python flows, Proxmox orchestration. Seek him at andrewholland.com.
```

---

## 🧠 Tech Stack & Architecture

### Frontend

* HTML/CSS/JS: Neon-drenched UI, responsive layout
* Fonts: Orbitron (user & header), Verdana (bot)
* Effects: Clickable URL inserts, animated text rendering

### Backend

* **Framework**: Flask 2.3.2
* **APIs**: Google Gemini API (via `google-generativeai`)
* **Scheduler**: APScheduler
* **Database**: SQLite (`data_cache.db`)
* **Monitoring**: Scheduled scraping of:

  * [andrewholland.com](https://www.andrewholland.com)
  * GitHub & YouTube profiles
  * Resume PDF content

### Key Modules

* `app.py`: Route control, query processing
* `monitoring.py`: Periodic data scraping
* `prompts.py`: Cyber-Zen templating
* `database.py`: Data cache and schema checks

### Core Workflow

1. User inputs query via Web/CLI
2. App determines relevance
3. Fetches & embeds context from cache
4. Builds prompt with redirect bias
5. Sends to Gemini API
6. Returns response + logs interaction

### Requirements

```
flask, flask-cors, google-generativeai, requests,
beautifulsoup4, PyPDF2, APScheduler,
python-dotenv, PyGithub, google-api-python-client
```

---

## 📢 Latest Development Update – Server Migration in Progress

As of **2025-08-11**, the Cyberpunk Monk Chatbot has completed **local deployment validation** in the `cyberpunk_monk` Conda environment. Following repository synchronization and recovery of critical `/docs` files, preparations for **server migration** are now underway.

**Key Advancements:**

* **Server Migration Plan** – Moving from the current host to a **new production server** for improved stability and performance.
* **Staging Period** – Deployment is **pending 24 hours of stable local uptime** to ensure all components operate flawlessly before going public.
* **Backup & Recovery Protocols** – SQLite (`data_cache.db`) auto-backups and Git safeguards added to prevent data loss.
* **Error Handling Enhancements** – Built-in recovery steps for `index.lock` issues, rebase conflicts, and file protection.

Once the **stability checkpoint** is achieved, the Cyberpunk Monk will transition from **localhost shadows** into the public web — enlightened, deployed, and recruiter-ready.

---

## 🚀 Setup & Deployment

### Local Setup

```bash
git clone https://github.com/silicastormsiam/CyberpunkMonkChatbot.git
cd CyberpunkMonkChatbot
conda activate cyberpunk_monk
pip install -r requirements.txt
```

```bash
python scripts/database.py
python scripts/monitoring.py
python scripts/app.py
```

* Access via: `http://127.0.0.1:5000` or local IP
* Logs: `logs/execution.log`, `logs/error.log`

### Hostinger Deployment

* Upload to `/home/u605846297/public_html/chatbot/`
* SSH in, set up venv, install requirements, run `app.py`
* Access at: `https://www.andrewholland.com/chatbot/chat.html`

---

## 📅 Development Timeline

### v1.0 – Foundation (2025-08-07)

* Flask app scaffolded
* Initial database and scraping logic
* Sample prompt engine

### v1.1–v1.3 – Persona & Logging (2025-08-08)

* Zen-style prompt updates
* Error and execution logs added
* Narrative fixed to 2049 for lore alignment

### v1.4–v1.6 – Frontend & Retry Logic

* Neon UI buildout (HTML/CSS/JS)
* Clickable link parsing
* Retry logic for Gemini quota errors

---

## ⚡ Risks & Recommendations

**Risks**:

* Gemini API limits (15/min)
* Stale content if scraping fails
* Hosting restrictions (limited Python support)

**Mitigation**:

* Upgrade Gemini tier: [Gemini Pricing](https://ai.google.dev/gemini-api/docs/rate-limits)
* Backup `data_cache.db` before deployments
* Schedule `monitoring.py` weekly
* Use `try/except` and table verification to avoid crashes

---

## 🌐 Future Enhancements

* Voice synthesis with gTTS
* Recruiter-tailored push alerts
* LinkedIn integration for resume auto-parse
* Vector embeddings for smarter RAG queries

---

## 📄 License

Licensed under [MIT](https://github.com/silicastormsiam/CyberpunkMonkChatbot/blob/main/LICENSE)

> *"To walk the Way of Code, one must also read the README." — Cyberpunk Monk*

---

If you want, I can now **save this updated README.md directly into your repo** so it’s version-controlled before migration. That way, if anything happens during the server change, the update is already preserved.

Do you want me to commit this to GitHub now?



