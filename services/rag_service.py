import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
from pypdf import PdfReader
import uuid
import re

# ================= CONFIG =================
embed_model = SentenceTransformer("all-MiniLM-L6-v2")

documents = []
metadata = []
doc_store = {}
index = None


# ================= CLEAN TEXT =================
def clean_text(text):
    text = re.sub(r'\S+@\S+', '', text)
    text = re.sub(r'Proprietary content.*?action\.', '', text, flags=re.DOTALL)
    text = re.sub(r'\s+', ' ', text)
    return text.strip()


# ================= READ =================
def read_file(file):
    if file.filename.endswith(".pdf"):
        reader = PdfReader(file)
        text = ""
        for page in reader.pages:
            text += page.extract_text() or ""
        return text
    else:
        return file.read().decode("utf-8", errors="ignore")


# ================= CHUNK =================
def chunk_text(text, size=600, overlap=50):
    chunks = []
    start = 0

    while start < len(text):
        chunk = text[start:start + size]
        chunks.append(chunk.strip())
        start += size - overlap

    return chunks


# ================= ADD DOCUMENT =================
def add_document(file):
    global index, doc_store

    text = clean_text(read_file(file))

    if not text.strip():
        return None

    # prevent duplicate
    for existing_id, name in doc_store.items():
        if name == file.filename:
            return existing_id

    doc_id = str(uuid.uuid4())
    chunks = chunk_text(text)

    embeddings = embed_model.encode(chunks, normalize_embeddings=True)
    embeddings = np.array(embeddings).astype("float32")

    if index is None:
        index = faiss.IndexFlatIP(embeddings.shape[1])

    index.add(embeddings)

    doc_store[doc_id] = file.filename

    for chunk in chunks:
        documents.append(chunk)
        metadata.append({
            "doc_id": doc_id,
            "filename": file.filename
        })

    return doc_id


# ================= SEARCH =================
def search(query, doc_filter=None):
    global index

    if index is None:
        return "", 0.0

    q = embed_model.encode([query], normalize_embeddings=True)
    q = np.array(q).astype("float32")

    scores, indices = index.search(q, 3)

    results = []
    max_score = 0.0

    for i, score in zip(indices[0], scores[0]):
        if i < len(documents):
            meta = metadata[i]

            if doc_filter and meta["doc_id"] not in doc_filter:
                continue

            results.append(documents[i])
            max_score = max(max_score, float(score))

    return "\n".join(results), max_score


# ================= LIST =================
def list_documents():
    return doc_store


# ================= DELETE =================
def delete_document(doc_id):
    global documents, metadata, index, doc_store

    documents = [d for d, m in zip(documents, metadata) if m["doc_id"] != doc_id]
    metadata = [m for m in metadata if m["doc_id"] != doc_id]

    if doc_id in doc_store:
        del doc_store[doc_id]

    if documents:
        emb = embed_model.encode(documents, normalize_embeddings=True)
        emb = np.array(emb).astype("float32")

        index = faiss.IndexFlatIP(emb.shape[1])
        index.add(emb)
    else:
        index = None