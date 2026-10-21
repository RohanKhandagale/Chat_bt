import json
import logging

from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.http import require_GET, require_POST
from groq import Groq

logger = logging.getLogger(__name__)

SYSTEM_PROMPT = (
    "You are PyChat, a helpful and friendly AI assistant. "
    "Answer clearly and naturally. If you are unsure, say so rather than "
    "making things up. Use readable formatting when it helps."
)


@require_GET
def index(request):
    return render(request, "index.html")


@require_GET
def health(request):
    return JsonResponse({"status": "ok", "assistant": "PyChat"})


@require_POST
def chat(request):
    try:
        data = json.loads(request.body or b"{}")
    except (json.JSONDecodeError, UnicodeDecodeError):
        return JsonResponse({"error": "Request body must be valid JSON."}, status=400)

    if not isinstance(data, dict):
        return JsonResponse({"error": "Send a JSON object with your messages."}, status=400)

    messages = data.get("messages")
    if not isinstance(messages, list) or not messages:
        return JsonResponse({"error": "Send a message before asking PyChat."}, status=400)

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
        return JsonResponse({"error": "Your latest message must be from you."}, status=400)

    if not settings.GROQ_API_KEY:
        return JsonResponse({"error": "GROQ_API_KEY is missing. Add your Groq API key to the .env file."}, status=503)

    try:
        client = Groq(api_key=settings.GROQ_API_KEY)
        response = client.chat.completions.create(
            model=settings.GROQ_MODEL,
            messages=[{"role": "system", "content": SYSTEM_PROMPT}, *conversation],
            temperature=0.7,
            max_tokens=1200,
        )
        answer = response.choices[0].message.content
        return JsonResponse({"reply": answer or "I couldn't come up with a reply. Try again."})
    except Exception:
        logger.exception("The Groq chat request failed")
        return JsonResponse({
            "error": "I couldn't reach the AI service just now. Check your API key and connection, then try again."
        }, status=502)
