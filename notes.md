# 🧠 Notes & Learnings

## 🔹 Ollama

* Runs LLM locally
* No API key required
* Models:

  * phi3 → fast
  * mistral → balanced
  * llama3 → high quality

---

## 🔹 Flask

* Lightweight backend framework
* Used for REST APIs

---

## 🔹 MySQL

* Stores generated posts
* Used for persistence

---

## 🔹 Architecture

* DTO → validation
* Service → business logic
* Repository → DB operations
* Routes → API layer

---

## 🔹 Performance Tips

* Use smaller models (phi3)
* Limit tokens (`num_predict`)
* Warm up models

---

## 🔹 Key Concept

Separation of concerns improves scalability and maintainability.
