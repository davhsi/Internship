"""
vector_store.py
Sets up ChromaDB with sentence-transformer embeddings, handles insertion
and semantic search.  No LangChain / LlamaIndex.
"""

import chromadb
from chromadb.utils import embedding_functions

from document_processor import process_document, process_folder


# ─────────────────────────────────────────────
# 1. Initialise ChromaDB + collection
# ─────────────────────────────────────────────

def create_collection(persist_dir: str = "chroma_db", collection_name: str = "docs"):
    """
    Create (or reopen) a persistent ChromaDB collection.
    Embeddings are generated locally via sentence-transformers — no extra API key.
    Model: all-MiniLM-L6-v2  (~80 MB, downloads once automatically)
    """
    client = chromadb.PersistentClient(path=persist_dir)
    ef = embedding_functions.SentenceTransformerEmbeddingFunction(
        model_name="all-MiniLM-L6-v2"
    )
    collection = client.get_or_create_collection(
        name=collection_name,
        embedding_function=ef,
    )
    return collection


# ─────────────────────────────────────────────
# 2. Insertion helpers
# ─────────────────────────────────────────────

def _add_batch(collection, ids, texts, metadatas, batch_size: int = 100):
    """Insert documents in batches (ChromaDB has a per-call limit)."""
    for i in range(0, len(texts), batch_size):
        end = min(i + batch_size, len(texts))
        collection.add(
            documents=texts[i:end],
            metadatas=metadatas[i:end],
            ids=ids[i:end],
        )


def add_file(collection, file_path: str):
    """Process a single file and add its chunks to the collection."""
    ids, texts, metadatas = process_document(file_path)
    if texts:
        _add_batch(collection, ids, texts, metadatas)
        print(f"[vector_store] Added {len(texts)} chunks from {file_path}")
    else:
        print(f"[vector_store] Skipped {file_path} (no content extracted)")


def add_folder(collection, folder_path: str):
    """Process every supported document in a folder and index all chunks."""
    for ids, texts, metadatas in process_folder(folder_path):
        if texts:
            src = metadatas[0]["source"]
            _add_batch(collection, ids, texts, metadatas)
            print(f"[vector_store] Indexed {len(texts)} chunks from {src}")


# ─────────────────────────────────────────────
# 3. Semantic search
# ─────────────────────────────────────────────

def semantic_search(collection, query: str, n_results: int = 3) -> dict:
    """
    Find the top-n most relevant chunks for a query.
    Returns the raw ChromaDB result dict (documents, metadatas, distances).
    """
    return collection.query(query_texts=[query], n_results=n_results)


def get_context_and_sources(results: dict) -> tuple[str, list[str]]:
    """
    Extract a single context string and a list of source labels
    from a ChromaDB query result.
    """
    docs = results["documents"][0]
    metas = results["metadatas"][0]
    context = "\n\n".join(docs)
    sources = [f"{m['source']} (chunk {m['chunk']})" for m in metas]
    return context, sources
