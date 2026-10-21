const form = document.querySelector("#chatForm");
const input = document.querySelector("#messageInput");
const messagesEl = document.querySelector("#messages");
const welcomeEl = document.querySelector("#welcome");
const sendButton = document.querySelector("#sendButton");
const newChatButton = document.querySelector("#newChat");
const clearChatButton = document.querySelector("#clearChat");
const sidebar = document.querySelector("#sidebar");
const overlay = document.querySelector("#mobileOverlay");

let conversation = [];
let isSending = false;

function getCookie(name) {
  const cookie = document.cookie.split("; ").find((item) => item.startsWith(`${name}=`));
  return cookie ? decodeURIComponent(cookie.split("=").slice(1).join("=")) : "";
}

function scrollToBottom() {
  const area = document.querySelector("#conversation");
  area.scrollTop = area.scrollHeight;
}

function addMessage(role, content) {
  welcomeEl.hidden = true;
  const article = document.createElement("article");
  article.className = `message ${role}`;
  const avatar = document.createElement("div");
  avatar.className = "avatar";
  avatar.textContent = role === "user" ? "Y" : "P";
  const body = document.createElement("div");
  body.className = "message-body";
  const meta = document.createElement("div");
  meta.className = "message-meta";
  meta.textContent = role === "user" ? "You" : "PyChat";
  const text = document.createElement("div");
  text.className = "message-text";
  // textContent prevents model replies from being interpreted as HTML.
  text.textContent = content;
  body.append(meta, text);
  article.append(avatar, body);
  messagesEl.append(article);
  scrollToBottom();
  return article;
}

function showTyping() {
  const article = document.createElement("article");
  article.className = "message assistant";
  article.id = "typingIndicator";
  const avatar = document.createElement("div");
  avatar.className = "avatar";
  avatar.textContent = "P";
  const body = document.createElement("div");
  body.className = "message-body";
  const meta = document.createElement("div");
  meta.className = "message-meta";
  meta.textContent = "PyChat is thinking";
  const dots = document.createElement("div");
  dots.className = "typing";
  dots.setAttribute("aria-label", "PyChat is typing");
  for (let i = 0; i < 3; i += 1) dots.append(document.createElement("span"));
  body.append(meta, dots);
  article.append(avatar, body);
  messagesEl.append(article);
  scrollToBottom();
}

function setBusy(busy) {
  isSending = busy;
  sendButton.disabled = busy;
  input.disabled = busy;
  sendButton.querySelector("span:first-child").textContent = busy ? "Thinking" : "Send";
}

async function sendMessage(rawText) {
  const content = rawText.trim();
  if (!content || isSending) return;
  conversation.push({ role: "user", content });
  addMessage("user", content);
  input.value = "";
  resizeInput();
  setBusy(true);
  showTyping();

  try {
    const response = await fetch("/api/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json", "X-CSRFToken": getCookie("csrftoken") },
      body: JSON.stringify({ messages: conversation })
    });
    const data = await response.json();
    document.querySelector("#typingIndicator")?.remove();
    if (!response.ok) throw new Error(data.error || "Something went wrong.");
    const reply = data.reply || "I couldn't create a reply. Please try again.";
    conversation.push({ role: "assistant", content: reply });
    addMessage("assistant", reply);
  } catch (error) {
    document.querySelector("#typingIndicator")?.remove();
    addMessage("assistant", `Sorry, I hit a problem: ${error.message}`);
    // Keep the failed turn out of history so the user can retry naturally.
    conversation.pop();
  } finally {
    setBusy(false);
    input.focus();
  }
}

function resizeInput() {
  input.style.height = "auto";
  input.style.height = `${Math.min(input.scrollHeight, 180)}px`;
}

function resetChat() {
  conversation = [];
  messagesEl.replaceChildren();
  welcomeEl.hidden = false;
  input.value = "";
  resizeInput();
  closeSidebar();
  input.focus();
}

function openSidebar() {
  sidebar.classList.add("open");
  overlay.classList.add("visible");
}

function closeSidebar() {
  sidebar.classList.remove("open");
  overlay.classList.remove("visible");
}

form.addEventListener("submit", (event) => {
  event.preventDefault();
  sendMessage(input.value);
});
input.addEventListener("input", resizeInput);
input.addEventListener("keydown", (event) => {
  if (event.key === "Enter" && !event.shiftKey) {
    event.preventDefault();
    form.requestSubmit();
  }
});
newChatButton.addEventListener("click", resetChat);
clearChatButton.addEventListener("click", resetChat);
document.querySelector("#openSidebar").addEventListener("click", openSidebar);
document.querySelector("#closeSidebar").addEventListener("click", closeSidebar);
overlay.addEventListener("click", closeSidebar);
document.querySelectorAll("[data-prompt]").forEach((button) => {
  button.addEventListener("click", () => {
    input.value = button.dataset.prompt;
    resizeInput();
    sendMessage(input.value);
  });
});
