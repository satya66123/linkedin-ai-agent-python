from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
from repository.post_repository import get_all_posts

# Load model
model = SentenceTransformer("all-MiniLM-L6-v2")

# ----------------------------
# BUILD INDEX
# ----------------------------
def build_index():
    posts = get_all_posts()

    if not posts:
        return None, []

    texts = [p["content"] for p in posts]

    embeddings = model.encode(texts)

    dimension = embeddings.shape[1]
    index = faiss.IndexFlatL2(dimension)

    index.add(np.array(embeddings))

    return index, texts


# ----------------------------
# RETRIEVE CONTEXT
# ----------------------------
def retrieve_context(query, k=2):
    index, texts = build_index()

    if index is None:
        return []

    query_vector = model.encode([query])

    D, I = index.search(np.array(query_vector), k)

    results = []
    for i in I[0]:
        if i < len(texts):
            results.append(texts[i])

    return results