const input = document.getElementById("userInput");
const button = document.getElementById("sendButton");
const chatBox = document.querySelector(".chat-box");

button.addEventListener("click", async function () {

    const message = input.value.trim();

    if (message === "") {
        return;
    }

    const userMessage = document.createElement("div");
    userMessage.className = "user-message";
    userMessage.textContent = message;
    chatBox.appendChild(userMessage);

    input.value = "";

    const botMessage = document.createElement("div");
    botMessage.className = "bot-message";
    botMessage.textContent = "Thinking... 🤖";
    chatBox.appendChild(botMessage);

    try {

        const response = await fetch("/chat", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                message: message
            })
        });

        const data = await response.json();

        botMessage.textContent = data.reply;

    } catch (error) {

        console.error(error);
        botMessage.textContent = "Sorry, something went wrong.";

    }

    chatBox.scrollTop = chatBox.scrollHeight;
});