"""
chatbot.py
Terminal chatbot interface for the RAG system.

Usage
-----
    python chatbot.py --docs ./docs --api-key YOUR_GEMINI_KEY

Or set the key in a .env file:
    GEMINI_API_KEY="your-key-here"
    python chatbot.py --docs ./docs

Commands during chat
--------------------
    /new    → start a fresh session (clears memory)
    /quit   → exit
    /help   → show commands
"""

import argparse
import os
import sys
from dotenv import load_dotenv

from vector_store import create_collection, add_folder, add_file
from memory import create_session, clear_session, list_sessions, get_history, find_session
from rag_engine import ask


BANNER = """
Type your question and press Enter.
Commands: /new  /sessions  /switch <id>  /quit  /help
"""

HELP_TEXT = """
Commands:
  /new              Start a new session (keeps current one intact)
  /sessions         List all active sessions
  /switch <id>      Switch to a session by its ID prefix (e.g. /switch a3f2c1)
  /quit             Exit the chatbot
  /help             Show this message
"""


def parse_args():
    parser = argparse.ArgumentParser(description="RAG chatbot with Gemini + ChromaDB")
    parser.add_argument(
        "--docs",
        default="./docs",
        help="Path to folder containing your documents (TXT)",
    )
    parser.add_argument(
        "--api-key",
        default="",
        help="Gemini AI Studio API key (or set GEMINI_API_KEY env var)",
    )
    parser.add_argument(
        "--db",
        default="./chroma_db",
        help="Directory to persist ChromaDB (default: ./chroma_db)",
    )
    parser.add_argument(
        "--collection",
        default="docs",
        help="ChromaDB collection name (default: docs)",
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Print intermediate RAG steps (good for debugging)",
    )
    return parser.parse_args()


def setup_collection(db_path: str, collection_name: str, docs_path: str):
    """Initialise the vector store and index documents if needed."""
    print(f"[setup] Opening ChromaDB at '{db_path}' …")
    collection = create_collection(persist_dir=db_path, collection_name=collection_name)

    # Check if the collection already has documents
    count = collection.count()
    if count > 0:
        print(f"[setup] Collection '{collection_name}' already contains {count} chunks — skipping re-index.")
        print("[setup] Delete the chroma_db folder to force a fresh index.")
    else:
        if not os.path.isdir(docs_path):
            print(f"[setup] Docs folder '{docs_path}' not found — creating it.")
            os.makedirs(docs_path, exist_ok=True)
            print("[setup] Add your .txt files to ./docs and restart.")
            sys.exit(0)

        print(f"[setup] Indexing documents from '{docs_path}' …")
        add_folder(collection, docs_path)
        new_count = collection.count()
        if new_count == 0:
            print("[setup] No supported documents found in the docs folder.")
            print("[setup] Add .txt files and restart.")
            sys.exit(0)
        print(f"[setup] Done — {new_count} chunks indexed.\n")

    return collection


def chat_loop(collection, verbose: bool):
    session_id = create_session()
    print(BANNER)

    while True:
        try:
            user_input = input("You: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\n[chatbot] Goodbye!")
            break

        if not user_input:
            continue

        # ── Commands ──────────────────────────────────────────────────────────
        if user_input.lower() == "/quit":
            print("[chatbot] Goodbye!")
            break
        elif user_input.lower() == "/new":
            # Keep current session intact, just spin up a fresh one
            session_id = create_session()
            print(f"[chatbot] New session started — ID: {session_id[:8]}…\n")
            continue
        elif user_input.lower() == "/sessions":
            all_sessions = list_sessions()
            print(f"\n[chatbot] Active sessions ({len(all_sessions)}):")
            for sid in all_sessions:
                msg_count = len(get_history(sid))
                marker = " ← current" if sid == session_id else ""
                print(f"  {sid[:8]}…  ({msg_count} messages){marker}")
            print()
            continue
        elif user_input.lower().startswith("/switch"):
            parts = user_input.split(maxsplit=1)
            if len(parts) < 2 or not parts[1].strip():
                print("[chatbot] Usage: /switch <session-id-prefix>\n")
                continue
            prefix = parts[1].strip()
            matched = find_session(prefix)
            if matched is None:
                # Check if multiple matched (ambiguous prefix)
                all_sessions = list_sessions()
                candidates = [s for s in all_sessions if s.lower().startswith(prefix.lower())]
                if len(candidates) > 1:
                    print(f"[chatbot] Ambiguous prefix '{prefix}' matches {len(candidates)} sessions — be more specific.\n")
                else:
                    print(f"[chatbot] No session found with prefix '{prefix}'. Use /sessions to see IDs.\n")
            elif matched == session_id:
                print(f"[chatbot] Already on session {matched[:8]}…\n")
            else:
                session_id = matched
                msg_count = len(get_history(session_id))
                print(f"[chatbot] Switched to session {session_id[:8]}… ({msg_count} messages in history)\n")
            continue
        elif user_input.lower() == "/help":
            print(HELP_TEXT)
            continue

        # ── RAG query ─────────────────────────────────────────────────────────
        try:
            answer, sources = ask(
                collection,
                query=user_input,
                session_id=session_id,
                verbose=verbose,
            )
            print(f"\nBot: {answer}")
            if sources:
                print(f"     Sources: {', '.join(sources)}")
            print()
        except Exception as e:
            print(f"[error] {e}\n")


def main():
    load_dotenv()
    args = parse_args()

    if args.api_key:
        os.environ["GEMINI_API_KEY"] = args.api_key
    if not os.getenv("GEMINI_API_KEY"):
        print("[error] No Gemini API key found.")
        print("  Set it in a .env file: GEMINI_API_KEY='your-key'")
        print("  Or pass: python chatbot.py --api-key YOUR_KEY")
        sys.exit(1)

    collection = setup_collection(args.db, args.collection, args.docs)
    chat_loop(collection, verbose=args.verbose)


if __name__ == "__main__":
    main()
