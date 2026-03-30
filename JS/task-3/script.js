const button = document.getElementById("send-btn");
const inputField = document.getElementById("user-input");

function sendMessage() {
  const textMessage = inputField.value.trim();
  if (textMessage === "") return;
  addMessage(textMessage, "user1");

  inputField.value = "";

  setTimeout(() => {
    const replies = [
      "Hello there!",
      "Good Morning!!",
      "Nice to meet you",
      "LOL :D",
      "Have a nice day",
      "It was nice talking to you",
      "I got work to do, bye.",
    ];

    const reply = replies[Math.floor(Math.random() * replies.length)];
    addMessage(reply, "user2");
  }, 1500);
}

button.addEventListener("click", sendMessage());

document.addEventListener("keydown", (e) => {
  if (e.key === "Enter") {
    sendMessage();
  }
});

function addMessage(message, sender) {
  const messageList = document.getElementById("message-list");
  const messageElement = document.createElement("div");
  messageElement.classList.add("message", sender);
  messageElement.innerHTML =
    message +
    `<div class="timestamp">${new Date().toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" })}</div>`;
  messageList.appendChild(messageElement);
  messageList.scrollTop = messageList.scrollHeight;
}
