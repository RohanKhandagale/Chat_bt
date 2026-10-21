# PyChat AI

PyChat is a lightweight AI chat app built with Django and the Groq API. It has a responsive dark chat interface, a small Python backend, and straightforward setup so it is easy to understand and extend.

## Features

- AI responses powered by Groq.
- Recent conversation context sent with each request.
- Responsive desktop and mobile interface.
- Typing indicator, starter prompts, and new/clear chat controls.
- API credentials loaded from a local `.env` file, not hard-coded.
- Django CSRF protection for chat requests.

Conversation history currently stays in the browser tab and is not saved to a database.

## Requirements

- Python 3.10 or newer
- A Groq API key
- Internet access for AI responses

## Run locally

Clone this repository and open a terminal in the project folder.

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

Install dependencies:

```bash
pip install -r requirements.txt
```

Create a local environment file:

**Windows PowerShell**
```powershell
Copy-Item .env.example .env
```

**macOS or Linux**
```bash
cp .env.example .env
```

Edit `.env` and replace `paste_your_groq_api_key_here` with your Groq API key. The `.env` file is ignored by Git, so do not commit it or paste your real key into source files.

Start Django's development server:

```bash
python manage.py migrate
python manage.py runserver
```

Open [http://127.0.0.1:8000](http://127.0.0.1:8000).

## Project structure

```text
Chat_bt/
├── manage.py
├── config/
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── chat/
│   ├── apps.py
│   ├── urls.py
│   └── views.py
├── templates/index.html
├── static/css/style.css
├── static/js/chat.js
├── requirements.txt
├── .env.example
└── README.md
```

## Configuration

- `GROQ_API_KEY`: your private Groq API key.
- `GROQ_MODEL`: model name available to your Groq account.
- `DJANGO_SECRET_KEY`: Django's secret key. Use a unique, private value for deployment.
- `DJANGO_DEBUG`: set to `false` in production.
- `DJANGO_ALLOWED_HOSTS`: comma-separated hostnames for deployment.
- `PORT`: optional port override; defaults to `8000`.

The default values in `.env.example` are intended for local development only. Generate a secure `DJANGO_SECRET_KEY` and configure allowed hosts before deployment.

## Safety notes

The backend only accepts user/assistant text messages, limits the conversation to the latest 20 messages, and caps each message length. Do not enter passwords or other sensitive information into the chatbot. This starter project does not include production rate limiting or persistent chat storage.

## Built with

- Python and Django
- Groq API
- HTML, CSS, and JavaScript

## License

MIT. See [LICENSE](LICENSE).
