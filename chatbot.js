// Toggle chatbot visibility
function toggleChatbot() {
    let chatContainer = document.getElementById("chat-container");
    chatContainer.style.display = (chatContainer.style.display === "none" || chatContainer.style.display === "") ? "block" : "none";
}

// Send message function
async function sendMessage() {
    let userMessage = document.getElementById("userInput").value;
    if (!userMessage) return;

    let chatBox = document.getElementById("chatbox");

    let userDiv = document.createElement("div");
    userDiv.classList.add("message-container", "user-container");
    userDiv.innerHTML = `<div class='user-message'><strong>You :</strong> ${userMessage}</div>`;
    chatBox.appendChild(userDiv);
    chatBox.scrollTop = chatBox.scrollHeight;

    let response = await fetch("/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: userMessage })
    });

    let result = await response.json();
    let botMessage = result.message || "Error: No response from bot";

    let botDiv = document.createElement("div");
    botDiv.classList.add("message-container", "bot-container");
    botDiv.innerHTML = `<div class='bot-message'><strong>Optimiser:</strong> ${botMessage}</div>`;
    chatBox.appendChild(botDiv);
    chatBox.scrollTop = chatBox.scrollHeight;

    document.getElementById("userInput").value = "";
}
