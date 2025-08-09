/*
File: frontend/script.js
Owner: Andrew John Holland
Purpose: JavaScript logic for futuristic chatbot with secure Gemini AI integration via backend proxy
Version: 2.1
*/
document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('chat-form');
    const input = document.getElementById('user-input');
    const history = document.getElementById('chat-history');

    // Use 127.0.0.1 for local testing; switch to 192.168.1.225:5000 for network testing
    const apiUrl = 'http://127.0.0.1:5000/api/chat';

    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        const message = input.value.trim();
        if (!message) return;

        addMessage(message, 'sender');
        input.value = '';

        try {
            const response = await fetch(apiUrl, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ message })
            });

            if (!response.ok) throw new Error(`HTTP error: ${response.status}`);

            const data = await response.json();
            const botText = data.response || 'No response from CP Monk';
            setTimeout(() => addMessage(botText, 'recipient'), 1200);
        } catch (error) {
            setTimeout(() => addMessage(`Error: ${error.message}`, 'recipient'), 1200);
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