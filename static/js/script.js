function sendQuery() {
    const userQuery = document.getElementById('user-query').value;
    const language = document.getElementById('language').value;
    const chatBox = document.getElementById('chat-box');

    if (!userQuery.trim()) {
        return; // Do not send empty queries
    }

    // Display user query
    chatBox.innerHTML += `
        <div class="message user">
            <div class="avatar"><i class="fas fa-user"></i></div>
            <div class="content">${userQuery}</div>
        </div>
    `;

    // Send query to the backend
    fetch('/chat', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: `user_query=${encodeURIComponent(userQuery)}&language=${language}`
    })
    .then(response => response.json())
    .then(data => {
        // Display bot response
        chatBox.innerHTML += `
            <div class="message bot">
                <div class="avatar"><i class="fas fa-robot"></i></div>
                <div class="content">${data.response}</div>
            </div>
        `;
        chatBox.scrollTop = chatBox.scrollHeight; // Auto-scroll
    });

    // Clear input
    document.getElementById('user-query').value = '';
}

function handleKeyPress(e) {
    if (e.key === 'Enter') {
        sendQuery();
    }
}