import os

from dotenv import load_dotenv
from flask import Flask, jsonify, render_template, request
from groq import Groq

load_dotenv()

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 1 * 1024 * 1024

MODEL_NAME = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")
SYSTEM_PROMPT = (
    "You are PyChat, a helpful and friendly AI assistant. "
    "Answer clearly and naturally. If you are unsure, say so rather than "
    "making things up. Use readable formatting when it helps."
)


def get_groq_client():
    """Create a client only when an API request needs it."""
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise RuntimeError(
            "GROQ_API_KEY is missing. Add your Groq API key to the .env file."
        )
    return Groq(api_key=api_key)


@app.get("/")
def index():
    return render_template("index.html")


@app.get("/api/health")
def health():
    return jsonify({"status": "ok", "assistant": "PyChat"})


@app.post("/api/chat")
def chat():
    data = request.get_json(silent=True) or {}
    messages = data.get("messages")

    if not isinstance(messages, list) or not messages:
        return jsonify({"error": "Send a message before asking PyChat."}), 400

    # Keep the latest messages only, and accept just user/assistant text.
    conversation = []
    for item in messages[-20:]:
        if not isinstance(item, dict):
            continue
        role = item.get("role")
        content = item.get("content")
        if role not in {"user", "assistant"} or not isinstance(content, str):
            continue
        content = content.strip()
        if content:
            conversation.append({"role": role, "content": content[:8000]})

    if not conversation or conversation[-1]["role"] != "user":
        return jsonify({"error": "Your latest message must be from you."}), 400

    try:
        client = get_groq_client()
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[{"role": "system", "content": SYSTEM_PROMPT}, *conversation],
            temperature=0.7,
            max_tokens=1200,
        )
        answer = response.choices[0].message.content
        return jsonify({"reply": answer or "I couldn't come up with a reply. Try again."})
    except RuntimeError as exc:
        return jsonify({"error": str(exc)}), 503
    except Exception:
        app.logger.exception("The Groq chat request failed")
        return jsonify({
            "error": "I couldn't reach the AI service just now. Check your API key "
                     "and connection, then try again."
        }), 502


if __name__ == "__main__":
    debug_mode = os.getenv("FLASK_DEBUG", "false").lower() == "true"
    app.run(host="127.0.0.1", port=int(os.getenv("PORT", "5000")), debug=debug_mode)
