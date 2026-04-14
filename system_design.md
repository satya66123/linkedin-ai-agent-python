# 🏗 System Design – LinkedIn AI Agent

## 📌 Overview

A full-stack AI application that generates LinkedIn posts using local LLMs (Ollama) with RAG for contextual responses.

---

## 🔄 High-Level Flow

User → Streamlit UI → Flask Backend → Services → DB + RAG → Ollama → Response → UI

---

## 🧩 Components

### 1. Frontend (Streamlit)
- User input (topic, style)
- Displays generated content
- Handles session state
- Calls backend APIs

---

### 2. Backend (Flask)
- REST APIs
- JWT Authentication
- Request validation
- Routes:
  - `/login`
  - `/register`
  - `/generate`
  - `/generate-rag`
  - `/comment`
  - `/hashtags`
  - `/favorite`
  - `/posts`

---

### 3. Service Layer
- Business logic
- AI prompt construction
- RAG integration

---

### 4. Repository Layer
- MySQL queries
- Data persistence

---

### 5. Database (MySQL)
Tables:
- users
- posts
- favorites

---

### 6. AI Layer (Ollama)
- Models:
  - llama3
  - mistral
- Runs locally (no API dependency)

---

### 7. RAG (Retrieval Augmented Generation)
- SentenceTransformers → embeddings
- FAISS → similarity search
- Retrieves past posts for context

---

## 🧠 Sequence Flow (Generate with RAG)

1. User enters topic
2. Frontend → `/generate-rag`
3. Backend:
   - Retrieve similar posts (FAISS)
   - Build prompt with context
4. Send prompt → Ollama
5. Receive AI response
6. Return to frontend

---

## ⚡ Key Design Decisions

- Used **Ollama** → avoids external API cost
- Used **RAG** → improves content quality
- Used **layered architecture** → scalable & maintainable
- Used **JWT** → secure APIs

---

## 🚀 Scalability Considerations

- Replace FAISS with vector DB (Pinecone)
- Use Redis caching
- Deploy via Docker + Kubernetes

---

## 🔐 Security

- JWT authentication
- Protected routes
- Input validation

---

## ⚠️ Limitations

- Local model latency
- No distributed system yet

---

## 🔮 Future Enhancements

- Chat-based UI
- Streaming responses
- Multi-user dashboards