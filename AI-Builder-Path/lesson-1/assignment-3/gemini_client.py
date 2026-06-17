"""
Supports:
  - generate_content()  — single-turn completion (used for response generation)
  - contextualize_query() — rewrite a follow-up question as a standalone query
"""

import os
import json
import requests
from datetime import datetime

LOG_FILE = "gemini_api.log"


def _log_api_call(payload: dict, response: dict):
    """Append request and response payloads to the log file."""
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write("=" * 80 + "\n")
        f.write(f"TIMESTAMP: {datetime.now().isoformat()}\n")
        f.write("-" * 40 + " REQUEST " + "-" * 40 + "\n")
        f.write(json.dumps(payload, indent=2))
        f.write("\n" + "-" * 40 + " RESPONSE " + "-" * 39 + "\n")
        f.write(json.dumps(response, indent=2))
        f.write("\n\n")

# ── Model to use ──────────────────────────────────────────────────────────────
# gemini-3.5-flash   → fast, free tier-friendly (recommended for development)
# gemini-2.5-flash   → another available option on your tier
DEFAULT_MODEL = "gemini-3.5-flash"

GEMINI_BASE = "https://generativelanguage.googleapis.com/v1beta/models"


def _get_api_key() -> str:
    key = os.getenv("GEMINI_API_KEY", "")
    if not key:
        raise EnvironmentError(
            "GEMINI_API_KEY not set. "
            "Please add it to your .env file: GEMINI_API_KEY='your-key-here'"
        )
    return key


def _call_gemini(system_instruction: str, user_text: str, model: str = DEFAULT_MODEL) -> str:
    """
    Gemini REST API shape:
        POST /v1beta/models/{model}:generateContent?key={api_key}
        {
          "system_instruction": { "parts": [{"text": "..."}] },
          "contents": [{ "role": "user", "parts": [{"text": "..."}] }]
        }

    Returns the first text candidate from the response.
    """
    api_key = _get_api_key()
    url = f"{GEMINI_BASE}/{model}:generateContent?key={api_key}"

    payload = {
        "system_instruction": {
            "parts": [{"text": system_instruction}]
        },
        "contents": [
            {
                "role": "user",
                "parts": [{"text": user_text}],
            }
        ],
        "generationConfig": {
            "temperature": 0.2, # 0 -> fully deterministic, 1 -> creative
            "maxOutputTokens": 1024,
        },
    }

    resp = requests.post(url, json=payload, timeout=60)

    if not resp.ok:
        raise RuntimeError(
            f"Gemini API error {resp.status_code}: {resp.text}"
        )

    data = resp.json()
    _log_api_call(payload, data)

    try:
        return data["candidates"][0]["content"]["parts"][0]["text"].strip()
    except (KeyError, IndexError) as e:
        raise RuntimeError(f"Unexpected Gemini response shape: {data}") from e


# ─────────────────────────────────────────────
# Public helpers
# ─────────────────────────────────────────────

def build_prompt(context: str, conversation_history: str, query: str) -> str:
    """
    Assemble the user-turn text that goes into the Gemini request.
    (The system instruction is passed separately.)
    """
    return (
        f"Context from documents:\n{context}\n\n"
        f"Previous conversation:\n{conversation_history}\n\n"
        f"Human: {query}\n\nAssistant:"
    )


def generate_response(
    query: str,
    context: str,
    conversation_history: str = "",
    model: str = DEFAULT_MODEL,
) -> str:
    """
    Generate a grounded answer from Gemini.
    The system instruction constrains it to the provided context.
    """
    system = (
        "You are a helpful assistant that answers questions based strictly on "
        "the provided document context and conversation history. "
        "If the answer cannot be found in the context, say: "
        "'I cannot answer this based on the provided information.' "
        "Be concise and factual."
    )
    user_text = build_prompt(context, conversation_history, query)
    return _call_gemini(system, user_text, model=model)


def contextualize_query(
    query: str,
    conversation_history: str,
    model: str = DEFAULT_MODEL,
) -> str:
    """
    Rewrite a follow-up question as a fully self-contained standalone question
    so the vector search does not depend on conversation context.

    Example:
        history:  "Q: When was GreenGrow founded?  A: 2010."
        query:    "Where is it headquartered?"
        output:   "Where is GreenGrow Innovations headquartered?"
    """
    if not conversation_history.strip():
        return query  # Nothing to contextualize

    system = (
        "Given a chat history and the latest user question which might reference "
        "context in the chat history, rewrite it as a standalone question that can "
        "be understood without the chat history. "
        "Do NOT answer the question. Return ONLY the rewritten question."
    )
    user_text = (
        f"Chat history:\n{conversation_history}\n\n"
        f"Question: {query}"
    )
    try:
        return _call_gemini(system, user_text, model=model)
    except Exception as e:
        print(f"[gemini_client] contextualize_query failed ({e}), using original.")
        return query
