# 🚀 LinkedIn AI Agent (Ollama + Python)

![Python](https://img.shields.io/badge/Python-3.10+-blue)
![Flask](https://img.shields.io/badge/Flask-Backend-black)
![Ollama](https://img.shields.io/badge/Ollama-Local%20LLM-green)
![MySQL](https://img.shields.io/badge/MySQL-Database-orange)
![Status](https://img.shields.io/badge/Status-Active-success)
![License](https://img.shields.io/badge/License-MIT-yellow)

---

## 🔥 Overview

An **AI-powered LinkedIn content generator** built using:

* 🧠 Ollama (Local LLM)
* ⚙️ Flask (Backend API)
* 🗄️ MySQL (Data Storage)

This project generates:

* LinkedIn posts
* Comments
* Hashtags

👉 All running **locally without cloud APIs**

---

## ✨ Features

* 📝 Multi-style LinkedIn post generation

  * Professional
  * Viral
  * Storytelling

* 💬 Comment Generator

* 🔖 Hashtag Generator

* 🤖 Multi-model support (phi3, mistral, llama3)

* 🧱 Clean Architecture (DTO + Repository + Routes)

* 💾 MySQL integration

---

## 🛠 Tech Stack

| Layer     | Technology |
| --------- | ---------- |
| Backend   | Flask      |
| AI Engine | Ollama     |
| Database  | MySQL      |
| Language  | Python     |

---

## 📂 Project Structure

```
linkedin-ai-agent-python/
 ├── app.py
 ├── db.py
 ├── routes/
 ├── services/
 ├── repository/
 ├── dto/
 ├── index.html
 ├── .env
 ├── requirements.txt
 └── README.md
```

---

## ▶️ Setup Instructions

### 1️⃣ Clone Repository

```
git clone https://github.com/YOUR_USERNAME/linkedin-ai-agent-python.git
cd linkedin-ai-agent-python
```

---

### 2️⃣ Install Dependencies

```
pip install -r requirements.txt
```

---

### 3️⃣ Start Ollama

```
ollama serve
```

(Optional warm-up)

```
ollama run phi3
```

---

### 4️⃣ Run Application

```
python app.py
```

---

## 🔌 API Endpoints

### 📝 Generate Post

POST `/generate`

```
{
  "topic": "Discipline vs motivation",
  "style": "viral"
}
```

---

### 💬 Generate Comment

POST `/comment`

```
{
  "content": "AI is transforming careers..."
}
```

---

### 🔖 Generate Hashtags

POST `/hashtags`

```
{
  "topic": "AI career growth"
}
```

---

### 📊 Get All Posts

GET `/posts`

---

## ⚡ Performance Optimization

* Uses **phi3 model** for fast response
* Token limit applied (`num_predict`)
* Optimized prompt design

---

## 📌 Status

✅ Core Features Completed
✅ AI Integration Done
✅ Database Integration Done
🔄 UI Improvements (Planned)
🔄 Authentication (Future)

---

## 🛣️ Roadmap (Future Updates)

* 🔐 User Authentication (Login/Register)
* 🌐 React Frontend UI
* 📊 Analytics Dashboard
* 📅 Scheduled Post Generator
* 📈 Engagement Prediction
* 🤖 Auto Comment Reply System

---

## 🧠 Key Learnings

* Working with **Local LLMs (Ollama)**
* Designing **REST APIs with Flask**
* Implementing **Clean Architecture**
* Handling **AI latency & optimization**

---

## 🏷️ Tags

`python` `flask` `ollama` `ai` `machine-learning`
`backend` `mysql` `llm` `rest-api`

---
## 🧾 Resume Highlights

* Developed an **AI-powered LinkedIn content generator** using **Python, Flask, Ollama, and MySQL**
* Implemented **multi-model LLM integration** (phi3, mistral, llama3)
* Designed **REST APIs** for post, comment, and hashtag generation
* Built **clean architecture** using DTO, service, repository, and route layers
* Optimized performance using **token limits and lightweight models**

---
## 👨‍💻 Author

Nekkanti Satya Srinath

---

## 📜 License

MIT License
