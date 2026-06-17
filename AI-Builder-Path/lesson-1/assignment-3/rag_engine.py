"""
rag_engine.py
Ties together:
  - vector_store   → semantic retrieval
  - memory         → conversation history
  - gemini_client  → LLM generation

Exposes a single public function: ask()
"""

from vector_store import semantic_search, get_context_and_sources
from memory import format_history, add_message
from gemini_client import contextualize_query, generate_response


def ask(
    collection,
    query: str,
    session_id: str,
    n_chunks: int = 3,
    verbose: bool = False,
) -> tuple[str, list[str]]:
    """
    Full RAG pipeline for a single user turn.

    Steps
    -----
    1. Retrieve conversation history for this session.
    2. Rewrite the query as standalone (handles follow-ups like "Where is it?").
    3. Semantic search → top-n chunks from ChromaDB.
    4. Build prompt (context + history + query) and call Gemini.
    5. Persist both turns to memory.
    6. Return (answer, sources).

    Parameters
    ----------
    collection  : ChromaDB collection object
    query       : The user's raw message
    session_id  : Active session ID (from memory.create_session())
    n_chunks    : How many document chunks to retrieve (default 3)
    verbose     : Print intermediate steps (useful while building/debugging)

    Returns
    -------
    (answer: str, sources: list[str])
    """

    # ── Step 1: History ──────────────────────────────────────────────────────
    history_str = format_history(session_id)

    # ── Step 2: Contextualize ────────────────────────────────────────────────
    standalone_query = contextualize_query(query, history_str)
    if verbose:
        print(f"\n[rag] Contextualized query: {standalone_query}")

    # ── Step 3: Retrieve ─────────────────────────────────────────────────────
    results = semantic_search(collection, standalone_query, n_results=n_chunks)
    context, sources = get_context_and_sources(results)
    if verbose:
        print(f"[rag] Sources: {sources}")
        print(f"[rag] Context snippet: {context[:200]}...")

    # ── Step 4: Generate ─────────────────────────────────────────────────────
    answer = generate_response(standalone_query, context, history_str)

    # ── Step 5: Persist ──────────────────────────────────────────────────────
    add_message(session_id, "user", query)           # store original, not rewritten
    add_message(session_id, "assistant", answer)

    return answer, sources
