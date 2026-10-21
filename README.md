# PyChat AI

PyChat is a small AI chat app built to practise connecting a Python backend to a clean web interface. It uses Flask for the server and Groq for the AI replies.

The goal is to keep the project easy to run and easy to change, without adding a big framework just for the sake of it.

## What it can do

- Chat with an AI model through the Groq API.
- Keep recent messages in the current conversation so replies have context.
- Use the chat layout on desktop, tablet, or mobile.
- Start a fresh conversation or clear the current one.
- Show a typing indicator while the assistant is working.
- Keep API credentials in a local `.env` file instead of the source code.

Conversation history currently stays in the browser tab. It is not saved to a database.

## What you need

- Python 3.10 or newer
- A Groq API key
- An internet connection for AI responses

## Run it locally

Clone the repository, then open a terminal in the project folder.

```bash
python -m venv .venv
```

Activate the environment:

**Windows PowerShell**
```powershell
.venv\\Scripts\\Activate.ps1
```

**macOS or Linux**
```bash
source .venv/bin/activate
```

Install the packages:

```bash
pip install -r requirements.txt
```

Create your local environment file:

**Windows PowerShell**
```powershell
Copy-Item .env.example .env
```

**macOS or Linux**
```bash
cp .env.example .env
```

Open `.env` and replace `your_groq_api_key_here` with your own Groq API key. Keep that file private; it is intentionally excluded from Git.

Start the app:

```bash
python app.py
```

Then visit [http://127.0.0.1:5000](http://127.0.0.1:5000).

## Project layout

```text
Chat_bt/
├── app.py
├── requirements.txt
├── .env.example
├── .gitignore
├── README.md
├── templates/
│   └── index.html
└── static/
    ├── css/
    │   └── style.css
    └── js/
        └── chat.js
```

## A couple of notes

The default model name is set in `.env.example`. If it is unavailable for your Groq account, update `GROQ_MODEL` to a model your account supports.

The app sends the recent conversation to Groq when you send a message. Avoid entering passwords, private keys, or other sensitive information into the chat. The server limits each request to the latest 20 messages and caps message length.

This is a starter project, not a production service. Before deploying it for other people, add rate limiting, stronger input validation, and any privacy controls your use case needs.

## Built with

- Python and Flask
- Groq API
- HTML, CSS, and JavaScript

## License

This project is released under the MIT License. See [LICENSE](LICENSE).
