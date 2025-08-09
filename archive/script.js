// File Name: script.js
// Owner: Andrew John Holland
// Purpose: JavaScript for the Cyberpunk Monk Chatbot frontend, handling user input and API calls to /monk endpoint
// Version Control: v1.1
// Change Log:
// 1. Adapted from provided HTML - 2025-08-07
// 2. Added fetch API for /monk endpoint - 2025-08-07
// 3. Implemented message display logic - 2025-08-07
// 4. Added error handling for API responses - 2025-08-07
// 5. Optimized for user input sanitization - 2025-08-08
// 6. Added URL parsing for clickable hyperlinks - 2025-08-08

function sendMessage() {
    const input = document.getElementById("user-input");
    const chatBox = document.getElementById("chat-box");
    const query = input.value.trim();
    if (query === "") return;
    chatBox.innerHTML += `<div class="message user-message">${query}</div>`;
    fetch("/monk", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: query })
    })
    .then(response => response.json())
    .then(data => {
        // Parse URLs in response to make them clickable
        const urlRegex = /(https?:\/\/[^\s]+)/g;
        const formattedResponse = data.response.replace(urlRegex, '<a href="$1" target="_blank" style="color: #F472B6">$1</a>');
        chatBox.innerHTML += `<div class="message bot-message">${formattedResponse}</div>`;
        chatBox.scrollTop = chatBox.scrollHeight;
    })
    .catch(error => {
        chatBox.innerHTML += `<div class="message bot-message" style="color: #DC2626;">Error: ${error.message}</div>`;
        chatBox.scrollTop = chatBox.scrollHeight;
    });
    input.value = "";
}
document.getElementById("user-input").addEventListener("keypress", function(event) {
    if (event.key === "Enter") sendMessage();
});