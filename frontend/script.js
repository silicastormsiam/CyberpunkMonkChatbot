/*
File: frontend/script.js
Owner: Andrew John Holland
Purpose: Frontend logic for Cyberpunk Monk; calls FastAPI and renders replies
Version: 1.1
Change Log:
v1.1 - Env-aware API targeting (same-origin in prod, :5000 in dev), improved error handling
v1.0 - Basic submit, fetch POST, and message rendering
*/
(function () {
  // API base URL detection
  const isHosted = !window.location.port || ["80", "443"].includes(window.location.port);
  const apiUrl = isHosted ? "/api/chat" : `http://${window.location.hostname}:5000/api/chat`;

  document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('chat-form');
    const input = document.getElementById('user-input');
    const history = document.getElementById('chat-history');

    form.addEventListener('submit', async (e) => {
      e.preventDefault();
      const message = input.value.trim();
      if (!message) return;

      addMessage(message, 'sender');
      input.value = '';
      input.focus();

      try {
        const resp = await fetch(apiUrl, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ message })
        });

        if (!resp.ok) {
          const text = await resp.text().catch(() => '');
          throw new Error(`HTTP ${resp.status}${text ? ` – ${text}` : ''}`);
        }

        const data = await resp.json();
        addMessage(data.response || 'No response from CP Monk', 'recipient');
      } catch (err) {
        addMessage(`Error: ${err.message}`, 'recipient');
        console.error('Chat error:', err);
      }
    });

    function addMessage(text, type) {
      const div = document.createElement('div');
      div.classList.add('message', type);
      div.textContent = text;
      history.appendChild(div);
      history.scrollTop = history.scrollHeight;
    }
  });
})();
