import streamlit as st
import requests
import uuid
import tempfile
import time
import sys

from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from docx import Document

# UTF-8 FIX
sys.stdout.reconfigure(encoding='utf-8')

API_URL = "http://127.0.0.1:5000"

st.set_page_config(page_title="LinkedIn AI Agent", layout="wide")

# ---------------- SESSION ----------------
if "token" not in st.session_state:
    st.session_state.token = None

if "page" not in st.session_state:
    st.session_state.page = "login"

if "conversations" not in st.session_state:
    st.session_state.conversations = {}

if "current_chat" not in st.session_state:
    chat_id = str(uuid.uuid4())
    st.session_state.current_chat = chat_id
    st.session_state.conversations[chat_id] = []

# ---------------- FILE HELPERS ----------------
def create_pdf(text):
    file = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
    doc = SimpleDocTemplate(file.name)
    styles = getSampleStyleSheet()

    safe_text = text.encode("utf-8", "ignore").decode("utf-8")
    doc.build([Paragraph(safe_text, styles["Normal"])])

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

# ---------------- API ----------------
def safe_request(method, url, payload=None):
    headers = {"Content-Type": "application/json"}

    token = st.session_state.get("token")
    if token:
        headers["Authorization"] = f"Bearer {token}"

    try:
        if method == "GET":
            res = requests.get(url, headers=headers)
        else:
            res = requests.post(url, json=payload, headers=headers)

        if res.status_code != 200:
            st.error(res.text)
            return None

        return res.json()

    except Exception as e:
        st.error(f"Error: {e}")
        return None

# =========================================================
# LOGIN
# =========================================================
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

# =========================================================
# APP
# =========================================================
elif st.session_state.page == "app":

    # ---------------- SIDEBAR ----------------
    st.sidebar.title("💬 Conversations")

    # New Chat
    if st.sidebar.button("➕ New Chat"):
        new_id = str(uuid.uuid4())
        st.session_state.conversations[new_id] = []
        st.session_state.current_chat = new_id
        st.rerun()

    # Chat list
    for cid in list(st.session_state.conversations.keys()):
        if st.sidebar.button(f"Chat {cid[:5]}", key=cid):
            st.session_state.current_chat = cid
            st.rerun()

    st.sidebar.divider()

    # ---------------- HISTORY ----------------
    st.sidebar.subheader("📜 History")

    if st.sidebar.button("Load History"):
        res = safe_request("GET", f"{API_URL}/posts")
        if res and "data" in res:
            new_id = str(uuid.uuid4())
            st.session_state.conversations[new_id] = [
                {
                    "role": "assistant",
                    "content": p["content"],
                    "readonly": True   # 👈 NO BUTTONS
                }
                for p in res["data"]
            ]
            st.session_state.current_chat = new_id
            st.rerun()

    # ---------------- FAVORITES ----------------
    st.sidebar.subheader("⭐ Favorites")

    if st.sidebar.button("Load Favorites"):
        res = safe_request("GET", f"{API_URL}/favorites")
        if res and "data" in res:
            new_id = str(uuid.uuid4())
            st.session_state.conversations[new_id] = [
                {
                    "role": "assistant",
                    "content": f["content"],
                    "readonly": True   # 👈 NO BUTTONS
                }
                for f in res["data"]
            ]
            st.session_state.current_chat = new_id
            st.rerun()

    st.sidebar.divider()

    # ---------------- SETTINGS ----------------
    model = st.sidebar.selectbox("Model", ["phi3", "mistral", "llama3"])
    style = st.sidebar.selectbox("Style", ["professional", "casual", "storytelling"])

    if st.sidebar.button("🧹 Clear Chat"):
        st.session_state.conversations[st.session_state.current_chat] = []
        st.rerun()

    if st.sidebar.button("Logout"):
        st.session_state.token = None
        st.session_state.page = "login"
        st.rerun()

    # ---------------- CHAT ----------------
    st.title("💬 LinkedIn AI Generator")

    messages = st.session_state.conversations[st.session_state.current_chat]

    for i, msg in enumerate(messages):

        readonly = msg.get("readonly", False)

        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

            # SHOW BUTTONS ONLY FOR NORMAL CHAT
            if not readonly:

                if msg["role"] == "assistant":

                    col1, col2, col3, col4, col5 = st.columns(5)

                    # Favorite
                    with col1:
                        if st.button("⭐", key=f"fav_{i}"):
                            safe_request("POST", f"{API_URL}/favorite", {
                                "topic": "chat",
                                "content": msg["content"]
                            })
                            st.toast("Saved")

                    # PDF
                    with col2:
                        pdf = create_pdf(msg["content"])
                        st.download_button(
                            "PDF",
                            open(pdf, "rb"),
                            file_name="chat.pdf",
                            key=f"pdf_{i}"  # ✅ UNIQUE
                        )

                    # DOCX
                    with col3:
                        docx = create_docx(msg["content"])
                        st.download_button(
                            "DOCX",
                            open(docx, "rb"),
                            file_name="chat.docx",
                            key=f"docx_{i}"  # ✅ UNIQUE
                        )

                    # TXT
                    with col4:
                        txt = create_txt(msg["content"])
                        st.download_button(
                            "TXT",
                            open(txt, "rb"),
                            file_name="chat.txt",
                            key=f"txt_{i}"  # ✅ UNIQUE
                        )

                    # DELETE
                    with col5:
                        if st.button("🗑", key=f"del_{i}"):
                            messages.pop(i)
                            st.rerun()

                # EDIT (only user)
                if msg["role"] == "user":
                    if st.button("✏️ Edit", key=f"edit_{i}"):
                        st.session_state.edit_index = i

    # ---------------- EDIT ----------------
    if "edit_index" in st.session_state:
        idx = st.session_state.edit_index
        new_text = st.text_input("Edit message", value=messages[idx]["content"])

        if st.button("Update"):
            messages[idx]["content"] = new_text
            messages[idx]["readonly"] = False
            del st.session_state.edit_index
            st.rerun()

    # ---------------- INPUT ----------------
    user_input = st.chat_input("Enter topic...")

    if user_input:

        messages.append({
            "role": "user",
            "content": user_input,
            "readonly": False
        })

        placeholder = st.empty()
        full_text = ""

        res = safe_request(
            "POST",
            f"{API_URL}/generate",
            {
                "topic": user_input,
                "style": style,
                "model": model
            }
        )

        if res and "data" in res:
            reply = res["data"]["content"]
        else:
            reply = "❌ Error generating response"

        for word in reply.split():
            full_text += word + " "
            placeholder.markdown(full_text)
            time.sleep(0.02)

        messages.append({
            "role": "assistant",
            "content": reply,
            "readonly": False
        })

        st.rerun()