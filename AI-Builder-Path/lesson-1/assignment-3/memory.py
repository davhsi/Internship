"""
memory.py
In-memory session store for multi-turn conversation history.
No external dependency — plain Python dicts + lists.
"""

import uuid
from datetime import datetime
from typing import Optional

# Global store: { session_id: [ {role, content, timestamp}, ... ] }
_sessions: dict[str, list[dict]] = {}


def create_session() -> str:
    """Create a new conversation session and return its ID."""
    sid = str(uuid.uuid4())
    _sessions[sid] = []
    return sid


def add_message(session_id: str, role: str, content: str):
    """
    Append a message to an existing session.
    role must be "user" or "assistant".
    """
    if session_id not in _sessions:
        _sessions[session_id] = []
    _sessions[session_id].append(
        {"role": role, "content": content, "timestamp": datetime.now().isoformat()}
    )


def get_history(session_id: str, max_messages: Optional[int] = None) -> list[dict]:
    """Return message list, optionally limited to the last N messages."""
    history = _sessions.get(session_id, [])
    if max_messages:
        history = history[-max_messages:]
    return history


def format_history(session_id: str, max_messages: int = 6) -> str:
    """
    Return a human-readable string of the recent conversation,
    suitable for inclusion in an LLM prompt.

    Example output:
        Human: When was GreenGrow founded?
        Assistant: GreenGrow was founded in 2010.
    """
    history = get_history(session_id, max_messages)
    lines = []
    for msg in history:
        label = "Human" if msg["role"] == "user" else "Assistant"
        lines.append(f"{label}: {msg['content']}")
    return "\n\n".join(lines)


def clear_session(session_id: str):
    """Delete a session entirely (removes the key, not just its messages)."""
    _sessions.pop(session_id, None)


def list_sessions() -> list[str]:
    """Return all known session IDs."""
    return list(_sessions.keys())


def find_session(prefix: str) -> Optional[str]:
    """
    Find a session ID by prefix (case-insensitive).
    Returns the full session ID if exactly one match is found, else None.
    """
    prefix = prefix.lower()
    matches = [sid for sid in _sessions if sid.lower().startswith(prefix)]
    if len(matches) == 1:
        return matches[0]
    return None
