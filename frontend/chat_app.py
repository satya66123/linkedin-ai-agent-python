import streamlit as st
import streamlit.components.v1 as components
import requests
import tempfile
import time
import sys
import json


sys.stdout.reconfigure(encoding='utf-8')

API_URL = "http://127.0.0.1:5000"

st.set_page_config(page_title="AI Chat", layout="wide")

# ================= SESSION =================
if "token" not in st.session_state:
    st.session_state.token = None

if "page" not in st.session_state:
    st.session_state.page = "login"

if "current_chat" not in st.session_state:
    st.session_state.current_chat = None


# ================= HELPERS =================
def safe_request(method, url, payload=None, files=None):
    headers = {}
    if not files:
        headers["Content-Type"] = "application/json"

    if st.session_state.token:
        headers["Authorization"] = f"Bearer {st.session_state.token}"

    try:
        if method == "GET":
            res = requests.get(url, headers=headers)
        elif method == "DELETE":
            res = requests.delete(url, headers=headers)
        elif method == "PUT":
            res = requests.put(url, json=payload, headers=headers)
        else:
            res = requests.post(url, json=payload if not files else None, files=files, headers=headers)

        if res.status_code != 200:
            st.error(res.text)
            return None

        return res.json()

    except Exception as e:
        st.error(e)
        return None


def create_txt(text):
    file = tempfile.NamedTemporaryFile(delete=False, suffix=".txt", mode="w", encoding="utf-8")
    file.write(text)
    file.close()
    return file.name


# ================= LOGIN =================
if st.session_state.page == "login":

    st.title("🔑 Login")

    u = st.text_input("Username")
    p = st.text_input("Password", type="password")

    if st.button("Login"):
        res = requests.post(f"{API_URL}/login", json={"username": u, "password": p})
        if res.status_code == 200:
            st.session_state.token = res.json()["access_token"]
            st.session_state.page = "app"
            st.rerun()
        else:
            st.error("Invalid credentials")

    if st.button("Go to Register"):
        st.session_state.page = "register"
        st.rerun()


# ================= REGISTER =================
elif st.session_state.page == "register":

    st.title("📝 Register")

    u = st.text_input("Username")
    p = st.text_input("Password", type="password")

    if st.button("Register"):
        res = requests.post(f"{API_URL}/register", json={"username": u, "password": p})
        if res.status_code == 200:
            st.success("Registered! Login now")
            st.session_state.page = "login"
            st.rerun()
        else:
            st.error("Failed")

    if st.button("Back to Login"):
        st.session_state.page = "login"
        st.rerun()


# ================= APP =================
elif st.session_state.page == "app":

    # ================= SIDEBAR =================
    st.sidebar.title("💬 Conversations")

    # 🔍 Search
    search = st.sidebar.text_input("🔍 Search")

    # ➕ New Chat
    if st.sidebar.button("➕ New Chat"):
        res = safe_request("POST", f"{API_URL}/chat/create", {"title": "New Chat"})
        if res:
            st.session_state.current_chat = res["conversation_id"]
            st.rerun()

    # Load chats
    res = safe_request("GET", f"{API_URL}/chat/list")
    chats = res["data"] if res else []

    if search:
        chats = [c for c in chats if search.lower() in c["title"].lower()]

    for chat in chats:
        col1, col2 = st.sidebar.columns([4,1])

        with col1:
            if st.button(chat["title"], key=f"chat_{chat['id']}"):
                st.session_state.current_chat = chat["id"]
                st.rerun()

        with col2:
            if st.button("❌", key=f"del_{chat['id']}"):
                safe_request("DELETE", f"{API_URL}/chat/{chat['id']}")
                st.rerun()

    st.sidebar.divider()


    # ================= SAVED =================
    st.sidebar.markdown("### 📂 Saved")

    if st.sidebar.button("📜 History"):
        res = safe_request("GET", f"{API_URL}/posts")
        if res:
            st.session_state.temp_msgs = [{"role":"assistant","content":x["content"]} for x in res["data"]]

    if st.sidebar.button("⭐ Favorites"):
        res = safe_request("GET", f"{API_URL}/favorites")
        if res:
            st.session_state.temp_msgs = [{"role":"assistant","content":x["content"]} for x in res["data"]]

    st.sidebar.divider()

    # ================= RAG =================
    st.sidebar.markdown("### 📂 Knowledge Base")

    uploaded = st.sidebar.file_uploader("Upload", type=["pdf","txt"])

    if uploaded:
        safe_request("POST", f"{API_URL}/upload", files={"file": uploaded})

    res = safe_request("GET", f"{API_URL}/documents")

    selected_docs = []

    if res and "data" in res:
        for doc_id, name in res["data"].items():
            if st.sidebar.checkbox(name, key=doc_id):
                selected_docs.append(doc_id)

    st.sidebar.divider()

    # ================= SETTINGS (RESTORED) =================
    st.sidebar.markdown("### ⚙️ Settings")

    model = st.sidebar.selectbox("Model", ["phi3","mistral","llama3"])
    style = st.sidebar.selectbox("Style", ["professional","casual","storytelling"])

    # Logout
    if st.sidebar.button("Logout"):
        st.session_state.token = None
        st.session_state.page = "login"
        st.rerun()

    # ================= CHAT =================
    st.title("💬 Chat")

    if not st.session_state.current_chat:
        st.info("👉 Select or create chat")
        st.stop()

    res = safe_request("GET", f"{API_URL}/chat/{st.session_state.current_chat}")
    messages = res["data"] if res else []

    if "temp_msgs" in st.session_state:
        messages = st.session_state.temp_msgs

    for i, msg in enumerate(messages):

        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

            if msg["role"] == "assistant":

                col1, col2, col3, col4 = st.columns(4)

                with col1:
                    if st.button("⭐", key=f"fav_{i}"):
                        safe_request("POST", f"{API_URL}/favorite", {
                            "topic": "chat",
                            "content": msg["content"]
                        })
                        st.success("Saved")

                with col2:
                    if st.button("📋", key=f"copy_{i}"):
                        components.html(f"""
                        <script>
                        navigator.clipboard.writeText({json.dumps(msg["content"])});
                        </script>
                        """, height=0)
                        st.success("Copied")

                with col3:
                    txt = create_txt(msg["content"])
                    with open(txt, "rb") as f:
                        st.download_button("📄", f, file_name="chat.txt", key=f"txt_{i}")

                with col4:
                    if st.button("🗑", key=f"del_{i}"):
                        safe_request("DELETE", f"{API_URL}/chat/{st.session_state.current_chat}")
                        st.rerun()

    # ================= INPUT =================
    user_input = st.chat_input("Type your message...")

    if user_input:

        placeholder = st.empty()
        full = ""

        res = safe_request("POST", f"{API_URL}/generate2", {
            "topic": user_input,
            "model": model,
            "style": style,
            "doc_ids": selected_docs,
            "conversation_id": st.session_state.current_chat
        })

        reply = res["data"]["content"] if res else "Error"

        for char in reply:
            full += char
            placeholder.markdown(full + "▌")
            time.sleep(0.003)

        placeholder.markdown(full)

        st.rerun()