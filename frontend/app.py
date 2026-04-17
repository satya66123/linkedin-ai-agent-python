import streamlit as st
import requests
import time
import tempfile

from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from docx import Document

API_URL = "http://127.0.0.1:5000"

st.set_page_config(page_title="LinkedIn AI Agent", layout="wide")

# ---------------- SESSION ----------------
if "token" not in st.session_state:
    st.session_state.token = None

if "page" not in st.session_state:
    st.session_state.page = "login"

if "messages" not in st.session_state:
    st.session_state.messages = []

# ---------------- FILE GENERATORS ----------------
def create_pdf(text):
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
    doc = SimpleDocTemplate(temp_file.name)
    styles = getSampleStyleSheet()
    content = [Paragraph(text, styles["Normal"])]
    doc.build(content)
    return temp_file.name

def create_docx(text):
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".docx")
    doc = Document()
    doc.add_paragraph(text)
    doc.save(temp_file.name)
    return temp_file.name

# ---------------- SAFE REQUEST ----------------
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

        if res.status_code == 401:
            st.session_state.token = None
            st.session_state.page = "login"
            st.warning("Session expired")
            st.rerun()

        if res.status_code == 422:
            st.session_state.token = None
            st.session_state.page = "login"
            st.error("Token invalid. Login again.")
            st.rerun()

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

    username = st.text_input("Username", key="login_user")
    password = st.text_input("Password", type="password", key="login_pass")

    if st.button("Login"):
        res = requests.post(
            f"{API_URL}/login",
            json={"username": username, "password": password}
        )

        if res.status_code == 200:
            st.session_state.token = res.json().get("access_token")
            st.session_state.page = "app"
            st.success("Login successful ✅")
            st.rerun()
        else:
            st.error("Invalid credentials")

    if st.button("Go to Register"):
        st.session_state.page = "register"
        st.rerun()

# =========================================================
# REGISTER
# =========================================================
elif st.session_state.page == "register":

    st.title("📝 Register")

    username = st.text_input("Username", key="reg_user")
    password = st.text_input("Password", type="password", key="reg_pass")

    if st.button("Register"):
        res = requests.post(
            f"{API_URL}/register",
            json={"username": username, "password": password}
        )

        if res.status_code == 200:
            st.success("User created! Please login.")
            st.session_state.page = "login"
            st.rerun()
        else:
            st.error(res.text)

    if st.button("Back to Login"):
        st.session_state.page = "login"
        st.rerun()

# =========================================================
# MAIN CHAT APP
# =========================================================
elif st.session_state.page == "app":

    if not st.session_state.token:
        st.session_state.page = "login"
        st.rerun()

    # ---------------- SIDEBAR ----------------
    st.sidebar.title("⚙️ Settings")

    model = st.sidebar.selectbox(
        "Model",
        [
            "phi3:latest",
            "mistral:latest",
            "llama3:latest",
            "llama3:instruct",
            "llama3:8b"
        ],
        key="model_select"
    )

    style = st.sidebar.selectbox(
        "Style",
        [
            "professional",
            "viral",
            "casual",
            "",
            "llama3:8b"
        ],
        key="style_select"
    )

    if st.sidebar.button("🧹 Clear Chat"):
        st.session_state.messages = []
        st.rerun()

    if st.sidebar.button("Logout"):
        st.session_state.token = None
        st.session_state.page = "login"
        st.rerun()

    # ---------------- HISTORY ----------------
    st.sidebar.subheader("📜 History")

    if st.sidebar.button("Load History"):
        res = safe_request("GET", f"{API_URL}/posts")

        if res and "data" in res:
            st.session_state.messages = []

            for p in res["data"]:
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": f"📌 {p['content']}"
                })

            st.rerun()

    # ---------------- FAVORITES ----------------
    st.sidebar.subheader("⭐ Favorites")

    if st.sidebar.button("Load Favorites"):
        res = safe_request("GET", f"{API_URL}/favorites")

        if res and "data" in res:
            st.session_state.messages = []

            for f in res["data"]:
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": f"⭐ {f['content']}"
                })

            st.rerun()

    # ---------------- CHAT ----------------
    st.title("💬 LinkedIn AI Chat")

    for i, msg in enumerate(st.session_state.messages):
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    prompt = st.chat_input("Type message or use /comment /hashtags")

    if prompt:
        st.session_state.messages.append({"role": "user", "content": prompt})

        with st.chat_message("user"):
            st.markdown(prompt)

        # ---------------- COMMANDS ----------------
        if prompt.startswith("/comment"):
            content = prompt.replace("/comment", "").strip()
            res = safe_request("POST", f"{API_URL}/comment", {"content": content})
            reply = res.get("comment") if res else "Error"

        elif prompt.startswith("/hashtags"):
            topic = prompt.replace("/hashtags", "").strip()
            res = safe_request("POST", f"{API_URL}/hashtags", {"topic": topic})
            reply = res.get("hashtags") if res else "Error"

        else:
            res = safe_request(
                "POST",
                f"{API_URL}/generate",
                {
                    "topic": prompt,
                    "style": style,
                    "model": model
                }
            )
            reply = res["data"]["content"] if res else "Error"

        # ---------------- STREAM RESPONSE ----------------
        with st.chat_message("assistant"):
            placeholder = st.empty()
            full = ""

            for word in reply.split():
                full += word + " "
                placeholder.markdown(full + "▌")
                time.sleep(0.02)

            placeholder.markdown(full)

            # ---------------- ACTION BUTTONS ----------------
            col1, col2, col3, col4 = st.columns(4)

            # COPY
            with col1:
                st.button("📋 Copy", key=f"copy_{len(st.session_state.messages)}")
                st.toast("Copied!")

            # FAVORITE
            with col2:
                if st.button("⭐ Add Favourite", key=f"fav_{len(st.session_state.messages)}"):
                    safe_request(
                        "POST",
                        f"{API_URL}/favorite",
                        {"topic": "chat", "content": full}
                    )
                    st.success("Saved!")

            # TXT
            with col3:
                st.download_button(
                    "⬇️ TXT",
                    full,
                    file_name="post.txt",
                    key=f"txt_{len(st.session_state.messages)}"
                )

            # PDF
            with col4:
                pdf_file = create_pdf(full)
                with open(pdf_file, "rb") as f:
                    st.download_button(
                        "⬇️ PDF",
                        f,
                        file_name="post.pdf",
                        key=f"pdf_{len(st.session_state.messages)}"
                    )

            # DOCX
            docx_file = create_docx(full)
            with open(docx_file, "rb") as f:
                st.download_button(
                    "⬇️ DOCX",
                    f,
                    file_name="post.docx",
                    key=f"docx_{len(st.session_state.messages)}"
                )

        st.session_state.messages.append({"role": "assistant", "content": full})