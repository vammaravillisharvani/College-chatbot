/* =====================================================================
   College Enquiry Chatbot - script.js
   =====================================================================
   Controls everything on the Chat Page:
     - Sending user messages to the Flask "/chat" API
     - Displaying user + bot chat bubbles with timestamps
     - Showing a "Bot is typing..." animation
     - Auto-scrolling to the latest message
     - Enter key support
     - Suggested question chips
     - Clear chat button
   ===================================================================== */

// ---------------------------------------------------------------
// STEP 1: Grab references to the HTML elements we need
// ---------------------------------------------------------------
const chatWindow    = document.getElementById("chat-window");
const userInput      = document.getElementById("user-input");
const sendBtn        = document.getElementById("send-btn");
const clearBtn        = document.getElementById("clear-btn");
const suggestedRow     = document.getElementById("suggested-row");

// ---------------------------------------------------------------
// STEP 2: Helper - get a nicely formatted current time, e.g. "10:45 AM"
// ---------------------------------------------------------------
function getCurrentTime() {
  return new Date().toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" });
}

// ---------------------------------------------------------------
// STEP 3: Add a message bubble to the chat window
// ---------------------------------------------------------------
function addMessage(sender, text, timestamp) {
  // sender is either "user" or "bot" -- this controls bubble side/color via CSS
  const row = document.createElement("div");
  row.className = `message-row ${sender}`;

  const bubble = document.createElement("div");
  bubble.className = "bubble";
  bubble.textContent = text;

  const timeLabel = document.createElement("span");
  timeLabel.className = "msg-time";
  timeLabel.textContent = timestamp;

  row.appendChild(bubble);
  row.appendChild(timeLabel);
  chatWindow.appendChild(row);

  scrollToBottom();
}

// Auto-scroll so the newest message is always visible
function scrollToBottom() {
  chatWindow.scrollTo({ top: chatWindow.scrollHeight, behavior: "smooth" });
}

// ---------------------------------------------------------------
// STEP 4: "Bot is typing..." animation
// ---------------------------------------------------------------
function showTypingIndicator() {
  const row = document.createElement("div");
  row.className = "message-row bot typing-row";
  row.id = "typing-indicator";

  row.innerHTML = `
    <div class="typing-bubble">
      <span class="typing-dot"></span>
      <span class="typing-dot"></span>
      <span class="typing-dot"></span>
    </div>
  `;

  chatWindow.appendChild(row);
  scrollToBottom();
}

function removeTypingIndicator() {
  const typingRow = document.getElementById("typing-indicator");
  if (typingRow) typingRow.remove();
}

// ---------------------------------------------------------------
// STEP 5: Send the user's message to the Flask backend ("/chat")
// ---------------------------------------------------------------
async function sendMessage(messageText) {
  const trimmedMessage = messageText.trim();
  if (trimmedMessage === "") return; // Ignore empty messages

  // 1) Show the user's own message right away
  addMessage("user", trimmedMessage, getCurrentTime());
  userInput.value = "";

  // 2) Show the typing animation while we wait for the bot's reply
  showTypingIndicator();

  try {
    // 3) POST the message to our Flask API endpoint
    const response = await fetch("/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message: trimmedMessage })
    });

    const data = await response.json();

    // Small delay makes the "typing" animation feel natural
    setTimeout(() => {
      removeTypingIndicator();
      addMessage("bot", data.reply, data.timestamp || getCurrentTime());
    }, 500);

  } catch (error) {
    removeTypingIndicator();
    addMessage("bot", "Sorry, I'm having trouble connecting right now. Please try again.", getCurrentTime());
    console.error("Chat request failed:", error);
  }
}

// ---------------------------------------------------------------
// STEP 6: Event Listeners - Send button, Enter key, Suggested chips
// ---------------------------------------------------------------
sendBtn.addEventListener("click", () => sendMessage(userInput.value));

// Pressing Enter sends the message, just like clicking the Send button
userInput.addEventListener("keydown", (event) => {
  if (event.key === "Enter") {
    event.preventDefault();
    sendMessage(userInput.value);
  }
});

if (suggestedRow) {
  suggestedRow.addEventListener("click", (event) => {
    const chip = event.target.closest(".suggested-chip");
    if (chip) sendMessage(chip.dataset.question);
  });
}

// ---------------------------------------------------------------
// STEP 7: Clear Chat button
// ---------------------------------------------------------------
clearBtn.addEventListener("click", () => {
  const confirmed = confirm("Clear the entire chat history?");
  if (!confirmed) return;

  chatWindow.innerHTML = "";
  showWelcomeMessage();
});

// ---------------------------------------------------------------
// STEP 8: Welcome message shown automatically when the chat opens
// ---------------------------------------------------------------
function showWelcomeMessage() {
  addMessage(
    "bot",
    "Hello! I'm your College Enquiry Chatbot. Ask me about admissions, courses, " +
    "fees, placements, hostel life, exams, or anything else about the college!",
    getCurrentTime()
  );
}

// Run once when the chat page first loads
document.addEventListener("DOMContentLoaded", () => {
  showWelcomeMessage();
  userInput.focus();
});
