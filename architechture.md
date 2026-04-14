# 🏗 Architecture

## Flow

Frontend (Streamlit)
        ↓
Backend (Flask APIs)
        ↓
Services Layer
        ↓
Repository Layer
        ↓
MySQL Database

        ↓
Ollama (LLM)
        ↓
RAG (FAISS + Embeddings)

---

## Components

### 1. Frontend
- Streamlit UI
- Handles user input

### 2. Backend
- Flask APIs
- JWT authentication

### 3. AI Layer
- Ollama models (llama3, mistral)

### 4. RAG
- SentenceTransformers
- FAISS vector search

### 5. Database
- MySQL
- Stores posts, favourites