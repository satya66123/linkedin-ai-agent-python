import streamlit as st
import streamlit.components.v1 as components
import requests
import uuid
import tempfile
import time
import sys
import json

from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from docx import Document

components.html("""
<script>
document.addEventListener("keydown", function(e) {

    // CTRL + C (copy last message)
    if (e.ctrlKey && e.key === "c") {
        const msgs = document.querySelectorAll('[data-testid="stMarkdownContainer"]');
        if (msgs.length > 0) {
            const last = msgs[msgs.length - 1].innerText;
            navigator.clipboard.writeText(last);
            alert("Copied last message");
        }
    }

    // CTRL + D (download text)
    if (e.ctrlKey && e.key === "d") {
        alert("Use menu to download (browser security)");
    }

});
</script>
""", height=0)

sys.stdout.reconfigure(encoding='utf-8')

API_URL = "http://127.0.0.1:5000"

st.set_page_config(page_title="LinkedIn AI Agent", layout="wide")

# ================= CSS (SAFE) =================

# ================= SESSION =================
if "token" not in st.session_state:
    st.session_state.token = None

if "page" not in st.session_state:
    st.session_state.page = "login"

if "conversations" not in st.session_state:
    st.session_state.conversations = {}

if "current_chat" not in st.session_state:
    cid = str(uuid.uuid4())
    st.session_state.current_chat = cid
    st.session_state.conversations[cid] = {
        "title": "New Chat",
        "messages": []
    }

# ================= HELPERS =================
def create_pdf(text):
    file = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
    doc = SimpleDocTemplate(file.name)
    styles = getSampleStyleSheet()
    doc.build([Paragraph(text, styles["Normal"])])
    return file.name

def create_docx(text):
    file = tempfile.NamedTemporaryFile(delete=False, suffix=".docx")
    doc = Document()
    doc.add_paragraph(text)
    doc.save(file.name)
    return file.name

def create_txt(text):
    file = tempfile.NamedTemporaryFile(delete=False, suffix=".txt", mode="w", encoding="utf-8")
    file.write(text)
    file.close()
    return file.name

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
        else:
            res = requests.post(url, json=payload if not files else None, files=files, headers=headers)

        if res.status_code != 200:
            st.error(res.text)
            return None

        return res.json()
    except Exception as e:
        st.error(e)
        return None

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

# ================= APP =================
elif st.session_state.page == "app":

    # ================= SIDEBAR =================
    st.sidebar.title("💬 Conversations")

    # New Chat
    if st.sidebar.button("➕ New Chat"):
        cid = str(uuid.uuid4())
        st.session_state.conversations[cid] = {
            "title": "New Chat",
            "messages": []
        }
        st.session_state.current_chat = cid
        st.rerun()

    chat_data = st.session_state.conversations[st.session_state.current_chat]

    # Rename Chat
    st.sidebar.markdown("### ✏️ Rename Chat")
    new_name = st.sidebar.text_input("Name", value=chat_data["title"])
    if st.sidebar.button("Update"):
        chat_data["title"] = new_name
        st.rerun()

    st.sidebar.divider()

    # ================= CONVERSATIONS =================
    st.sidebar.markdown("### 💬 Your Chats")

    for cid, chat in st.session_state.conversations.items():
        col1, col2 = st.sidebar.columns([4, 1])

        with col1:
            if st.button(chat["title"], key=f"chat_{cid}"):
                st.session_state.current_chat = cid
                st.rerun()

        with col2:
            if st.button("❌", key=f"del_{cid}"):
                del st.session_state.conversations[cid]
                st.rerun()

    st.sidebar.divider()

    # ================= HISTORY & FAVORITES =================
    st.sidebar.markdown("### 📂 Saved")

    # 📜 History
    if st.sidebar.button("📜 Load History"):
        res = safe_request("GET", f"{API_URL}/posts")
        if res:
            cid = str(uuid.uuid4())
            st.session_state.conversations[cid] = {
                "title": "📜 History",
                "messages": [
                    {"role": "assistant", "content": p["content"], "readonly": True}
                    for p in res["data"]
                ]
            }
            st.session_state.current_chat = cid
            st.rerun()

    # ⭐ Favorites
    if st.sidebar.button("⭐ Load Favorites"):
        res = safe_request("GET", f"{API_URL}/favorites")
        if res:
            cid = str(uuid.uuid4())
            st.session_state.conversations[cid] = {
                "title": "⭐ Favorites",
                "messages": [
                    {"role": "assistant", "content": f["content"], "readonly": True}
                    for f in res["data"]
                ]
            }
            st.session_state.current_chat = cid
            st.rerun()

    st.sidebar.divider()

    # ================= RAG =================
    st.sidebar.markdown("### 📂 Knowledge Base")

    uploaded = st.sidebar.file_uploader("Upload file", type=["pdf", "txt"])

    if uploaded:
        res = safe_request("POST", f"{API_URL}/upload", files={"file": uploaded})
        if res:
            st.sidebar.success("Uploaded")

    res = safe_request("GET", f"{API_URL}/documents")

    selected_docs = []

    if res and "data" in res:
        for doc_id, name in res["data"].items():
            if st.sidebar.checkbox(name, key=doc_id):
                selected_docs.append(doc_id)

    st.sidebar.divider()

    # ================= SETTINGS =================
    st.sidebar.markdown("### ⚙️ Settings")

    model = st.sidebar.selectbox("Model", ["phi3", "mistral", "llama3"])
    style = st.sidebar.selectbox("Style", ["professional", "casual", "storytelling"])

    # Logout
    if st.sidebar.button("Logout"):
        st.session_state.token = None
        st.session_state.page = "login"
        st.rerun()

    # ================= CHAT =================
    st.title("💬 Chat")

    messages = chat_data["messages"]

    for i, msg in enumerate(messages):

        with st.chat_message(msg["role"]):

            col_main, col_actions = st.columns([9, 1])

            with col_main:
                st.markdown(msg["content"])

            with col_actions:

                if msg["role"] == "assistant":

                    with st.popover("⋮"):

                        # ⭐
                        if st.button("⭐", key=f"fav_{i}"):
                            safe_request("POST", f"{API_URL}/favorite", {
                                "topic": "chat",
                                "content": msg["content"]
                            })
                            st.toast("Saved")

                        # 📋
                        if st.button("📋", key=f"copy_{i}"):
                            safe_text = json.dumps(msg["content"])
                            components.html(f"""
                            <script>
                            navigator.clipboard.writeText({safe_text});
                            </script>
                            """, height=0)
                            st.toast("Copied")

                        # 📄
                        if st.button("📄", key=f"pdf_{i}"):
                            pdf = create_pdf(msg["content"])
                            with open(pdf, "rb") as f:
                                st.download_button("Download", f, file_name="chat.pdf", key=f"pdf_dl_{i}")

                        # 📝
                        if st.button("📝", key=f"docx_{i}"):
                            docx = create_docx(msg["content"])
                            with open(docx, "rb") as f:
                                st.download_button("Download", f, file_name="chat.docx", key=f"docx_dl_{i}")

                        # 📃
                        if st.button("📃", key=f"txt_{i}"):
                            txt = create_txt(msg["content"])
                            with open(txt, "rb") as f:
                                st.download_button("Download", f, file_name="chat.txt", key=f"txt_dl_{i}")

                        # 🗑
                        if st.button("🗑", key=f"del_{i}"):
                            messages.pop(i)
                            st.rerun()


    # ================= INPUT =================
    user_input = st.chat_input("Enter topic...")

    if user_input:

        messages.append({"role": "user", "content": user_input})

        placeholder = st.empty()
        full = ""

        res = safe_request("POST", f"{API_URL}/generate", {
            "topic": user_input,
            "model": model,
            "doc_ids": selected_docs
        })

        reply = res["data"]["content"] if res else "Error"

        progress = st.progress(0)

        for i, char in enumerate(reply):
            full += char
            placeholder.markdown(full + "▌")
            progress.progress((i + 1)/len(reply))
            time.sleep(0.005)

        progress.empty()
        placeholder.markdown(full)

        messages.append({"role": "assistant", "content": reply})

        st.rerun()