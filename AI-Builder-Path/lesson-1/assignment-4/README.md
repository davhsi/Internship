# RAG Chatbot — Gemini + ChromaDB (No LangChain / LlamaIndex)

Built following the FutureSmart AI reference article, with **OpenAI replaced by Google Gemini AI Studio API**.

---

## Project structure

```
rag_chatbot/
├── chatbot.py            ← Entry point (CLI chat interface)
├── rag_engine.py         ← Orchestrates the full RAG pipeline per query
├── gemini_client.py      ← All Gemini API calls (replaces OpenAI client)
├── vector_store.py       ← ChromaDB setup, insertion, semantic search
├── document_processor.py ← File reading (TXT) + chunking
├── memory.py             ← In-memory session/conversation history
├── requirements.txt
└── docs/                 ← Put your TXT files here
```

---

## How it works (RAG pipeline)

```
INDEXING (once)
  Your docs → read_document() → split_text() → ChromaDB (all-MiniLM-L6-v2 embeddings)

QUERY (every message)
  User query
    → contextualize_query()     rewrite follow-ups as standalone questions (Gemini)
    → semantic_search()         top-3 relevant chunks from ChromaDB
    → build_prompt()            context + chat history + query
    → generate_response()       Gemini returns grounded answer
    → add_message()             store turn in session memory
```

---

## Setup

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

> `sentence-transformers` (~80 MB) downloads the embedding model on first run automatically.

### 2. Get a Gemini API key

1. Go to https://aistudio.google.com/
2. Click **Get API key** → **Create API key**
3. Copy the key

### 3. Add your documents

```
mkdir docs
cp your-notes.txt docs/
```

### 4. Run

First, ensure your API key is in the `.env` file:
```
GEMINI_API_KEY="your-key-here"
```

Then run the chatbot:
```bash
python chatbot.py --docs ./docs
```

Or pass the key inline:

```bash
python chatbot.py --docs ./docs --api-key YOUR_KEY
```

Add `--verbose` to see intermediate RAG steps (helpful when debugging):

```bash
python chatbot.py --docs ./docs --verbose
```

---

## Chat commands

| Command | Description |
|---------|-------------|
| `/new`  | Clear memory, start fresh session |
| `/quit` | Exit |
| `/help` | Show commands |

---

## Configuration options

| Flag | Default | Description |
|------|---------|-------------|
| `--docs` | `./docs` | Folder with your documents |
| `--db` | `./chroma_db` | ChromaDB persistence directory |
| `--collection` | `docs` | ChromaDB collection name |
| `--verbose` | off | Print retrieval debug info |

---

## Changing the Gemini model

In `gemini_client.py`, line 16:

```python
DEFAULT_MODEL = "gemini-3.5-flash"   # fast, free tier-friendly
# DEFAULT_MODEL = "gemini-2.5-flash" # another option
```

---

## Re-indexing documents

ChromaDB skips re-indexing if the collection already has chunks.
To force a fresh index:

```bash
rm -rf ./chroma_db
python chatbot.py --docs ./docs
```

---

## Key design decisions vs the reference article

| Reference article (OpenAI) | This implementation (Gemini) |
|---|---|
| `openai.OpenAI()` client | Direct `requests.post()` to Gemini REST API |
| `gpt-4` for generation | `gemini-3.5-flash` (free tier) |
| `gpt-4` for query contextualisation | Same Gemini call, different system instruction |
| `client.chat.completions.create()` | `_call_gemini()` wrapper in `gemini_client.py` |
| Requires OpenAI API key | Requires Google AI Studio API key |

Everything else (ChromaDB, sentence-transformers, chunking, memory) is identical.
