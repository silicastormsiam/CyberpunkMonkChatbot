# Chatbot Project Handover Report

## Metadata
- **File**: `Chatbot_Project_Handover_Report_Complete.md`
- **Owner**: Andrew Holland (@SilicaStormSiam)
- **Purpose**: Summarize project status, stakeholder details, technical configurations, and recovery plan for handover to new facilitator or technical team.
- **Version**: 1.4
- **Date**: July 28, 2025
- **Change Log**:
  - Version 1.4: Consolidated stakeholder inputs from July 27–28, 2025; added user `u605846297` creation, permissions, and WinSCP access; included interface performance issues (Chrome tab memory usage up to 2.4GB due to repeated text compounding, ~5-minute response delays from "Re-reading past attachments...", leading to inefficiency and frustration; recommended minimal output to prevent RAM buildup).

## Project Overview
- **Initiation**: July 23, 2025, by Andrew Holland (@SilicaStormSiam).
- **Purpose**: Flask-based chatbot to showcase projects (e.g., CPM, ATS, Homelab) for information retrieval, with Cyberpunk Monk persona blending spiritual enlightenment and dystopian resilience (serenity amid chaos, digital enlightenment, dignified resilience).
- **Stakeholders**: Andrew Holland (developer and Project Manager), incoming program manager, Hostinger (hosting provider).
- **Target Audience**: Potential recruitment offices, requiring professional responses.
- **Directive**: Cyberpunk Monk provides responses about Andrew John Holland’s online profile:
  - `andrewholland.com`
  - `https://www.andrewholland.com/timeline/`
  - `https://github.com/silicastormsiam`
  - `https://www.youtube.com/@SilicaStormSiam`
  - Resume/executive summary content.
- **Goals**: Restore chatbot to online status at `http://145.79.8.69:5000/` or final domain `http://chatbot.cyberpunkmonk.com:5000/`, test stability and response content.
- **Deadline**: 5 days after deployment on Hostinger.com for subdomain propagation and chatbot stability.
- **Domain Propagation Status**: Check starting July 29, 2025 (estimated completion July 29–30, 2025).

## Technical Configuration
- **VPS**: Ubuntu 24.04, Python 3.12.3, no Nginx/Gunicorn.
- **Hosting**: Hostinger VPS (IP: `145.79.8.69`, ports 5000, 65002), managed via `https://hpanel.hostinger.com/`.
- **File Inventory**: In `/home/u605846297/public_html/chatbot/`:
  - `monk_bot.py`
  - `chat.html`
  - `style.css`
  - `script.js`
  - `cyberpunk-bg.jpg`
  - `favicon.ico`
  - Directories: `venv` (confirmed via ls scan, 10:10 PM +07).
- **Color Palette**: #2A2D76 (chat window), #292D74 (input field), #A8C8D6 (border), #843880 (placeholder), #3D3F79 (button); defined in `chat.html`.
- **Font**: Orbitron (Google Fonts) for all UI text.
- **CSS**: Embedded in `chat.html`; background image at `/public_html/chatbot/cyberpunk-bg.jpg`.
- **UI Issue**: White background when stretching browser at `http://145.79.8.69:5000/`.
- **UI Fix**: Update `chat.html` with:
  ```css
  body {
    background-color: #2a2d76;
    background-image: url('/public_html/chatbot/cyberpunk-bg.jpg');
    background-size: cover;
    background-repeat: no-repeat;
    background-position: center;
    font-family: 'Orbitron', sans-serif;
  }
  ```

## Instability and Recovery Status
- **Instability Cause**: Went offline after background change to #2A2D76; due to previous facilitator’s insufficient skill level; exacerbated by Hostinger’s IP variability (e.g., `145.79.14.78` vs. `145.79.8.69`); facilitator removed.
- **Progress (July 27–28, 2025)**:
  - July 27: Confirmed project details, file inventory, UI issue, and initial recovery plan.
  - July 28: Created user `u605846297` (UID/GID 1001), set shell to `/bin/bash`, fixed permissions for `/home/u605846297/public_html/chatbot/` (ownership: `u605846297:u605846297`, 755); confirmed no “read only” errors; verified WinSCP access with files (`monk_bot.py`, `chat.html`, etc., 10:12 PM +07).
  - Interface Issues: Chrome tab memory usage up to 2.4GB due to repeated text compounding in responses; ~5-minute response delays from "Re-reading past attachments..."; reduced efficiency; recommended minimal output and new sessions to prevent RAM buildup; reported to developers for resolution.
- **Login Attempts**:
  - Successful: Windows Terminal (PowerShell, `ssh -p 65002 root@145.79.8.69`, 09:37 PM +07); PuTTY (`u605846297@145.79.14.78:65002`, incorrect IP, 07:05 PM +07).
  - Failed: Windows Terminal (`ssh root@145.79.8.69`, port 22, “Connection timed out,” 08:18 PM +07; `ssh -p 65002 root@145.79.8.69`, 09:25 PM +07).

## Recovery Plan
- **Current Status**: User `u605846297` created, permissions set, WinSCP access confirmed; pending file verification and `chat.html` update.
- **Next Steps** (Delegated to Technical Team):
  - Verify files in `/home/u605846297/public_html/chatbot/` via WinSCP.
  - Update `chat.html` with CSS to fix white background.
  - Run `monk_bot.py` (command: `python3 monk_bot.py`).
  - Test response library for Cyberpunk Monk persona.
  - Set up daily backup (cron job).
  - Verify domain propagation (`http://chatbot.cyberpunkmonk.com:5000/`, start July 29, 2025).
  - Check server logs (`/var/log/syslog`, Flask logs) for instability causes.
- **Support**: Contact Kobee via hPanel (`support@hostinger.com`) for issues; no ticket open.

## Submission Instructions
- **File**: Save this as `Chatbot_Project_Handover_Report_Complete.md`.
- **Archive**: Create `Chatbot_Project_Assets.zip`:
  - Place `Chatbot_Project_Handover_Report_Complete.md` in a folder (e.g., `C:\Users\Andrew\Documents\Chatbot_Project_Assets`).
  - Add related files (e.g., `Chatbot_Project_Handover_Supplement.md`).
  - Zip the folder (right-click > Send to > Compressed (zipped) folder).
- **Delivery**: Email `Chatbot_Project_Assets.zip` to the new facilitator or upload to a shared drive (e.g., Google Drive, Dropbox).
- **Verification**: Open `Chatbot_Project_Handover_Report_Complete.md` to confirm content; extract ZIP to verify files.