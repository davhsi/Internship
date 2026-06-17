"""
document_processor.py
Handles reading PDF / DOCX / TXT files and splitting them into sentence-aware chunks.
No LangChain or LlamaIndex — pure Python.
"""

import os


# ─────────────────────────────────────────────
# 1. File readers
# ─────────────────────────────────────────────

def read_text_file(file_path: str) -> str:
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()


def read_document(file_path: str) -> str:
    """Unified entry point — dispatches by extension."""
    ext = os.path.splitext(file_path)[1].lower()
    if ext == ".txt":
        return read_text_file(file_path)
    else:
        raise ValueError(f"Unsupported file format: {ext}")


# ─────────────────────────────────────────────
# 2. Text chunking (sentence-aware)
# ─────────────────────────────────────────────

def split_text(text: str, chunk_size: int = 500) -> list[str]:
    """
    Split text into chunks of ~chunk_size characters while preserving
    sentence boundaries to avoid cutting context mid-thought.
    """
    sentences = text.replace("\n", " ").split(". ")
    chunks = []
    current_chunk: list[str] = []
    current_size = 0

    for sentence in sentences:
        sentence = sentence.strip()
        if not sentence:
            continue
        if not sentence.endswith("."):
            sentence += "."

        size = len(sentence)
        if current_size + size > chunk_size and current_chunk:
            chunks.append(" ".join(current_chunk))
            current_chunk = [sentence]
            current_size = size
        else:
            current_chunk.append(sentence)
            current_size += size

    if current_chunk:
        chunks.append(" ".join(current_chunk))

    return chunks


# ─────────────────────────────────────────────
# 3. Pipeline: read → chunk → return (ids, texts, metadatas)
# ─────────────────────────────────────────────

def process_document(file_path: str):
    """
    Read a single document, split into chunks, and produce
    (ids, texts, metadatas) ready for ChromaDB insertion.
    """
    try:
        content = read_document(file_path)
        chunks = split_text(content)
        file_name = os.path.basename(file_path)
        metadatas = [{"source": file_name, "chunk": i} for i in range(len(chunks))]
        ids = [f"{file_name}_chunk_{i}" for i in range(len(chunks))]
        return ids, chunks, metadatas
    except Exception as e:
        print(f"[processor] Error processing {file_path}: {e}")
        return [], [], []


def process_folder(folder_path: str):
    """
    Process every supported file in a folder and yield
    (ids, texts, metadatas) per document.
    """
    supported = {".txt"}
    for fname in os.listdir(folder_path):
        full_path = os.path.join(folder_path, fname)
        if os.path.isfile(full_path) and os.path.splitext(fname)[1].lower() in supported:
            yield process_document(full_path)
