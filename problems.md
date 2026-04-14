# 📄 `problems.md`

````md id="problems-md-001"````
# 🧪 Problems Faced & Solutions

 This document highlights key challenges faced during the development of the **LinkedIn AI Agent** and how they were solved.

---

## 🔴 1. Streamlit Navigation Not Working After Login

### Problem
After successful login, the UI stayed on the login page instead of navigating to the main app.

### Root Cause
Streamlit re-runs the script and resets UI state unless managed explicitly.

### Solution
- Used `st.session_state` to manage navigation
- Introduced a `page` variable to control views

```python
st.session_state.page = "app"
st.rerun()
````

---

## 🔴 2. Streamlit Duplicate Element ID Error

### Problem

```
StreamlitDuplicateElementId: multiple text_input elements
```

### Root Cause

Multiple inputs used same labels without unique keys.

### Solution

Assigned unique keys to all inputs:

```python
st.text_input("Topic", key="gen_topic")
```

---

## 🔴 3. Backend Not Running (False Error)

### Problem

Frontend showed "Backend not running" even when backend was active.

### Root Cause

Generic exception handling in API calls.

### Solution

* Removed misleading error messages
* Handled only real exceptions

```python
except:
    return None
```

---

## 🔴 4. JWT Authentication Issues

### Problem

Protected APIs returned 401 Unauthorized.

### Root Cause

JWT token not passed correctly in headers.

### Solution

Added Authorization header:

```python
headers["Authorization"] = f"Bearer {token}"
```

---

## 🔴 5. Ollama Timeout / Slow Response

### Problem

AI responses took too long (>5 mins).

### Root Cause

Heavy models + large prompts.

### Solution

* Switched to lightweight models (phi3)
* Reduced prompt size
* Optimized generation parameters

---

## 🔴 6. RAG Import Error

### Problem

```
ImportError: cannot import name 'retrieve_context'
```

### Root Cause

Incorrect function definition or missing export.

### Solution

* Fixed function name
* Ensured proper module structure

---

## 🔴 7. Database Not Saving Data

### Problem

Favorites/posts not getting stored.

### Root Cause

* Missing commit
* Table not created

### Solution

```python
conn.commit()
```

---

## 🔴 8. API 404 Errors

### Problem

```
404 Not Found (/favorite, /register)
```

### Root Cause

Routes not registered in Flask app.

### Solution

```python
app.register_blueprint(post_bp)
```

---

## 🔴 9. UI Buttons Triggering Multiple Times

### Problem

Users could click buttons repeatedly.

### Root Cause

No state control in UI.

### Solution

Used session state flags:

```python
st.session_state.favourite_added = True
```

---

## 🔴 10. Streamlit State Reset on Refresh

### Problem

App reset on refresh.

### Root Cause

Stateless execution model.

### Solution

* Used `session_state`
* Controlled navigation manually

---

## 🧠 Key Learnings

* Always manage state explicitly in Streamlit
* Debug step-by-step instead of guessing
* Handle API errors carefully
* Optimize AI prompts for performance
* Use layered architecture for scalability

---

## 🙏 Acknowledgement

Many issues were debugged with the help of:

* ChatGPT 🤖 (debugging & guidance)
* Persistence and continuous learning ✝️

---

## 🚀 Conclusion

These challenges helped build a deeper understanding of:

* Full-stack development
* AI integration
* Debugging real-world systems
* Writing production-ready code
