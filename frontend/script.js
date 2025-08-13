/*
File: frontend/script.js
Owner: Andrew John Holland
Purpose: Frontend logic for Cyberpunk Monk; calls FastAPI and renders replies
Version: 1.7
Change Log:
v1.7 - Mango "Send" button (black text + glow); accessibility focus ring
v1.6 - Email linkify (mailto:); quota message shows site + email only
v1.5 - Friendly error messages for quota/rate limits; preserve linkify/styling
v1.4 - White links for assistant messages; pink hover; visited color locked
v1.3 - Injected scoped link styles (brand colors, underline, hover/focus)
v1.2 - Safe linkify for assistant messages; optional session reset hook; minor UX polish
v1.1 - Env-aware API targeting (same-origin in prod, :5000 in dev), improved error handling
v1.0 - Basic submit, fetch POST, and message rendering
*/
(function () {
  const isHosted = !window.location.port || ["80", "443"].includes(window.location.port);
  const apiBase = isHosted ? "" : `http://${window.location.hostname}:5000`;
  const apiChat = `${apiBase}/api/chat`;
  const apiReset = `${apiBase}/api/reset`; // optional endpoint

  // ---------- Inject scoped link styles (assistant messages) ----------
  function ensureLinkStyles() {
    if (document.getElementById('chat-link-styles')) return;
    const css = `
      #chat-history .message.recipient a {
        color: #FFFFFF;
        text-decoration: underline;
        text-decoration-thickness: 1px;
        text-underline-offset: 2px;
        cursor: pointer;
        transition: color 0.15s ease, background-color 0.15s ease, text-decoration-thickness 0.15s ease;
      }
      #chat-history .message.recipient a:visited { color: #FFFFFF; }
      #chat-history .message.recipient a:hover {
        color: #F472B6; /* brand pink hover */
        background-color: rgba(244,114,182,0.12);
        text-decoration-thickness: from-font;
      }
      #chat-history .message.recipient a:focus {
        outline: 2px solid #F472B6;
        outline-offset: 2px;
        border-radius: 2px;
      }
    `;
    const style = document.createElement('style');
    style.id = 'chat-link-styles';
    style.type = 'text/css';
    style.appendChild(document.createTextNode(css));
    document.head.appendChild(style);
  }

  // ---------- Inject styles for the "Send" button (mango + glow) ----------
  function ensureButtonStyles() {
    if (document.getElementById('chat-send-styles')) return;
    const css = `
      /* Targets common submit button patterns without assuming exact IDs/classes */
      #chat-form button[type="submit"],
      #chat-form input[type="submit"],
      #send-btn,
      button.send,
      button#send {
        background-color: #FFB000; /* mango */
        color: #000000;            /* black text */
        border: none;
        border-radius: 9999px;     /* pill */
        padding: 10px 16px;
        font-weight: 700;
        letter-spacing: 0.2px;
        cursor: pointer;
        box-shadow: 0 6px 18px rgba(255, 176, 0, 0.35);
        transition: transform 0.06s ease, box-shadow 0.2s ease, background-color 0.2s ease;
      }
      #chat-form button[type="submit"]:hover,
      #chat-form input[type="submit"]:hover,
      #send-btn:hover,
      button.send:hover,
      button#send:hover {
        background-color: #FFC44D; /* lighter mango */
        box-shadow: 0 0 0 4px rgba(255,176,0,0.15), 0 8px 22px rgba(255,176,0,0.45);
      }
      #chat-form button[type="submit"]:active,
      #chat-form input[type="submit"]:active,
      #send-btn:active,
      button.send:active,
      button#send:active {
        background-color: #E69A00; /* deeper mango on press */
        transform: translateY(1px);
      }
      #chat-form button[type="submit"]:focus-visible,
      #chat-form input[type="submit"]:focus-visible,
      #send-btn:focus-visible,
      button.send:focus-visible,
      button#send:focus-visible {
        outline: 2px solid #000000; /* high-contrast focus ring */
        outline-offset: 2px;
      }
      /* Gentle pulsing glow (respects reduced-motion) */
      @media (prefers-reduced-motion: no-preference) {
        #chat-form button[type="submit"],
        #chat-form input[type="submit"],
        #send-btn,
        button.send,
        button#send {
          animation: mangoGlow 3s ease-in-out infinite;
        }
        @keyframes mangoGlow {
          0%, 100% { box-shadow: 0 6px 18px rgba(255,176,0,0.35); }
          50%      { box-shadow: 0 0 0 6px rgba(255,176,0,0.12), 0 10px 26px rgba(255,176,0,0.55); }
        }
      }
    `;
    const style = document.createElement('style');
    style.id = 'chat-send-styles';
    style.type = 'text/css';
    style.appendChild(document.createTextNode(css));
    document.head.appendChild(style);
  }

  // ---------- Escape + linkify (URLs first, then emails) ----------
  function escapeHTML(str) {
    return str
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;")
      .replace(/'/g, "&#39;");
  }
  function linkify(text) {
    const escaped = escapeHTML(text);

    // URLs -> anchors
    const urlRegex = /\bhttps?:\/\/[^\s<>()]+[^\s<>().,!?;:'")\]]/g;
    const withUrls = escaped.replace(urlRegex, (url) => {
      const safe = url;
      return `<a href="${safe}" target="_blank" rel="noopener noreferrer">${safe}</a>`;
    });

    // Avoid replacing inside existing anchors; then emails -> mailto:
    const parts = withUrls.split(/(<a [^>]+>.*?<\/a>)/gi);
    const emailRegex = /\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b/g;
    for (let i = 0; i < parts.length; i++) {
      if (/^<a [^>]+>/.test(parts[i])) continue;
      parts[i] = parts[i].replace(emailRegex, (email) => {
        const safe = email;
        return `<a href="mailto:${safe}" rel="noopener noreferrer">${safe}</a>`;
      });
    }
    return parts.join('');
  }

  function addMessage(text, type) {
    const history = document.getElementById('chat-history');
    const div = document.createElement('div');
    div.classList.add('message', type);
    if (type === 'recipient') {
      div.innerHTML = linkify(text);
    } else {
      div.textContent = text;
    }
    history.appendChild(div);
    history.scrollTop = history.scrollHeight;
  }

  async function sendChat(message) {
    const resp = await fetch(apiChat, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      credentials: 'include',
      body: JSON.stringify({ message })
    });

    if (!resp.ok) {
      let detail = "";
      try {
        const data = await resp.json();
        detail = (data && (data.detail || data.error || data.message)) || "";
      } catch {
        try { detail = await resp.text(); } catch { /* ignore */ }
      }

      const lower = (detail || "").toLowerCase();
      const isQuota = lower.includes("quota") || lower.includes("rate limit") || lower.includes("429");
      if (isQuota) {
        let retryHint = "";
        const m = detail.match(/retry[_\s]*delay[^0-9]*([0-9]+)/i);
        if (m && m[1]) retryHint = ` (~${m[1]}s)`;
        const friendly = [
          "We’ve reached today’s free-tier limit for the AI model.",
          "Please try again a bit later" + retryHint + " or tomorrow.",
          "In the meantime, you can find key info here:",
          "- https://www.andrewholland.com/",
          "- andrewjohnholland@gmail.com"
        ].join("\n");
        throw new Error(friendly);
      }

      throw new Error(`Request failed (HTTP ${resp.status})${detail ? ` – ${detail}` : ""}`);
    }

    return resp.json();
  }

  async function resetSession() {
    try {
      const resp = await fetch(apiReset, { method: 'POST', credentials: 'include' });
      if (!resp.ok) throw new Error(`HTTP ${resp.status}`);
      const history = document.getElementById('chat-history');
      history.innerHTML = '';
      addMessage('Session reset.', 'recipient');
    } catch (err) {
      console.warn('Reset endpoint not available or failed:', err.message);
      const history = document.getElementById('chat-history');
      history.innerHTML = '';
      addMessage('Session cleared locally. (Server reset not available.)', 'recipient');
    }
  }

  document.addEventListener('DOMContentLoaded', () => {
    ensureLinkStyles();
    ensureButtonStyles();

    const form = document.getElementById('chat-form');
    const input = document.getElementById('user-input');
    const resetBtn = document.getElementById('reset-session');

    form.addEventListener('submit', async (e) => {
      e.preventDefault();
      const message = (input.value || '').trim();
      if (!message) return;

      addMessage(message, 'sender');
      input.value = '';
      input.focus();

      try {
        const data = await sendChat(message);
        addMessage(data.response || 'No response from CP Monk', 'recipient');
      } catch (err) {
        addMessage(`${err.message}`, 'recipient');
        console.error('Chat error:', err);
      }
    });

    input.addEventListener('keydown', (e) => {
      if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        form.dispatchEvent(new Event('submit'));
      }
    });

    if (resetBtn) {
      resetBtn.addEventListener('click', (e) => {
        e.preventDefault();
        resetSession();
      });
    }
  });
})();
