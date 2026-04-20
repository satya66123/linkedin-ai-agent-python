# 🚀 LinkedIn AI Agent + Chat app (Ollama + Python)

![Python](https://img.shields.io/badge/Python-3.10+-blue)
![Flask](https://img.shields.io/badge/Flask-Backend-black)
![Streamlit](https://img.shields.io/badge/Streamlit-Frontend-red)
![Ollama](https://img.shields.io/badge/Ollama-Local%20LLM-green)
![MySQL](https://img.shields.io/badge/MySQL-Database-orange)

![Status](https://img.shields.io/badge/Status-Completed-success)
![License](https://img.shields.io/badge/License-MIT-yellow)

![Repo Size](https://img.shields.io/github/repo-size/YOUR_USERNAME/linkedin-ai-agent-python)
![Last Commit](https://img.shields.io/github/last-commit/YOUR_USERNAME/linkedin-ai-agent-python)
![Stars](https://img.shields.io/github/stars/YOUR_USERNAME/linkedin-ai-agent-python?style=social)
![Forks](https://img.shields.io/github/forks/YOUR_USERNAME/linkedin-ai-agent-python?style=social)
![Issues](https://img.shields.io/github/issues/YOUR_USERNAME/linkedin-ai-agent-python)
---

## 🔥 Overview

An **AI-powered LinkedIn content generator** built using:

- 🧠 Ollama (Local LLMs: Llama3, Mistral, Phi3)
- ⚙️ Flask (Backend APIs)
- 🗄️ MySQL (Database)
- 🎨 Streamlit (Frontend UI)

👉 Generates:
- LinkedIn posts
- Comments
- Hashtags
- Chats

👉 Runs **fully locally without OpenAI or cloud APIs**

---

## ✨ Features

- 📝 Multi-style LinkedIn post generation  
  - Professional  
  - Viral  
  - Storytelling
- 📝Chat generation      

- 💬 Comment Generator  
- 🔖 Hashtag Generator
- 💬 Chat Generator
- 🧠 Multi-model support (phi3, mistral, llama3)  
- 📚 RAG (context-aware generation)  
- 🔐 JWT Authentication (Login/Register)  
- ⭐ Add Favourite + Post Scoring  
- 📜 Post History  
- ⚡ Streamlit UI with progress + state handling  
- 🧱 Clean Architecture (DTO + Service + Repository + Routes)

---

## 🛠 Tech Stack

| Layer     | Technology |
|----------|-----------|
| Backend  | Flask     |
| Frontend | Streamlit |
| AI Engine| Ollama    |
| Database | MySQL     |
| Language | Python    |
| RAG      | FAISS + Sentence Transformers |

---

## 🏗 Architecture

```

User → Streamlit UI → Flask API → Service Layer → Repository → MySQL
↓
RAG (FAISS)
↓
Ollama (LLM)

```

---

## 📂 Project Structure

```

linkedin-ai-agent-python/
├── backend/
├── frontend/
├── routes/
├── services/
├── repository/
├── dto/
├── db.py
├── app.py
├── requirements.txt
└── README.md

````

---

## ▶️ Setup Instructions

### 1️⃣ Clone Repository
```bash
git clone https://github.com/YOUR_USERNAME/linkedin-ai-agent-python.git
cd linkedin-ai-agent-python
````

---

### 2️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

---

### 3️⃣ Start Ollama

```bash
ollama serve
```

(Optional warm-up)

```bash
ollama run llama3
```

---

### 4️⃣ Run Backend

```bash
python app.py
```

---

### 5️⃣ Run Frontend

```bash
streamlit run frontend/app.py           #linkedin ai agent
streamlit run frontend/chat_app.py      # chat app
```

---

## 🔌 API Endpoints

### 📝 Generate Post

POST `/generate`

```json
{
  "topic": "Discipline vs motivation",
  "style": "viral"
}
```

---

### 💬 Generate Comment

POST `/comment`

```json
{
  "content": "AI is transforming careers..."
}
```

---

### 🔖 Generate Hashtags

POST `/hashtags`

```json
{
  "topic": "AI career growth"
}
```

---

### 📊 Get Posts

GET `/posts`

---

## ⚡ Performance Optimization

* Uses lightweight models (phi3, llama3)
* Optimized prompts for faster responses
* Controlled token generation (`num_predict`)
* Local inference (no API latency)

---

## 📌 Status

✅ Core Features Completed

✅ AI Integration Completed

✅ Database Integration Completed

✅ Authentication + UI Completed

---

## 🧠 Key Learnings

* Working with **Local LLMs (Ollama)**
* Building **RAG-based AI systems**
* Designing **scalable backend APIs**
* Handling **AI latency & optimization**
* Managing **stateful frontend (Streamlit)**

---

## 🏷️ Tags

`python` `flask` `streamlit` `ollama` `ai` `llm` `rag` `mysql` `backend` `machine-learning`

---

## 🧾 Resume Highlights

* Developed a **full-stack AI-powered LinkedIn content generator and chat app** using Python, Flask, MySQL, and Streamlit
* Implemented **RAG (FAISS + embeddings)** for contextual AI generation
* Integrated **local LLMs (Llama3, Mistral, Phi3)** via Ollama
* Designed secure APIs using **JWT authentication**
* Built scalable architecture using **DTO, service, repository layers**
* Optimized performance for real-time AI responses

---

## 👨‍💻 Author

**Nekkanti Satya Srinath**

🔗 GitHub:
https://github.com/satya66123/linkedin-ai-agent-python

---

## 🔐 Tokens (Example Only)

```env
JWT_SECRET_KEY=your_secret_key
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=your_password
DB_NAME=linkedin_ai
```

⚠️ Never expose real credentials

---

## 📜 License

MIT License

