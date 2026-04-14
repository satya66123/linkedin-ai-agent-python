import streamlit as st
import requests
import time

API_URL = "http://127.0.0.1:5000"

st.set_page_config(page_title="LinkedIn AI Agent", layout="wide")

# ----------------------------
# SESSION STATE
# ----------------------------
if "token" not in st.session_state:
    st.session_state.token = None

if "page" not in st.session_state:
    st.session_state.page = "login"

if "post" not in st.session_state:
    st.session_state.post = ""

if "favourite_added" not in st.session_state:
    st.session_state.favourite_added = False

if "scored" not in st.session_state:
    st.session_state.scored = False

# ----------------------------
# SAFE REQUEST (NO FAKE ERRORS)
# ----------------------------
def safe_request(method, url, payload=None):
    headers = {}

    if st.session_state.token:
        headers["Authorization"] = f"Bearer {st.session_state.token}"

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

        if res.status_code != 200:
            return None

        return res.json()

    except:
        return None

# =========================================================
# LOGIN PAGE
# =========================================================
if st.session_state.page == "login":

    st.title("🔑 Login")

    username = st.text_input("Username", key="login_user")
    password = st.text_input("Password", type="password", key="login_pass")

    if st.button("Login"):
        try:
            res = requests.post(
                f"{API_URL}/login",
                json={"username": username, "password": password}
            )

            if res.status_code == 200:
                data = res.json()

                if "token" in data:
                    st.session_state.token = data["token"]
                    st.session_state.page = "app"

                    st.success("Login successful ✅")
                    st.rerun()
                else:
                    st.error("Token missing")

            else:
                st.error("Invalid credentials")

        except Exception as e:
            st.error(f"Error: {e}")

    if st.button("Go to Register"):
        st.session_state.page = "register"
        st.rerun()

# =========================================================
# REGISTER PAGE
# =========================================================
elif st.session_state.page == "register":

    st.title("📝 Register")

    username = st.text_input("Username", key="reg_user")
    password = st.text_input("Password", type="password", key="reg_pass")

    if st.button("Register"):
        try:
            res = requests.post(
                f"{API_URL}/register",
                json={"username": username, "password": password}
            )

            if res.status_code == 200:
                st.success("User created!")
                st.session_state.page = "login"
                st.rerun()
            else:
                st.error(res.text)

        except Exception as e:
            st.error(f"Error: {e}")

    if st.button("Back to Login"):
        st.session_state.page = "login"
        st.rerun()

# =========================================================
# MAIN APP
# =========================================================
elif st.session_state.page == "app":

    if not st.session_state.token:
        st.session_state.page = "login"
        st.rerun()

    # Sidebar
    st.sidebar.success("Logged in ✅")

    if st.sidebar.button("Logout"):
        st.session_state.token = None
        st.session_state.page = "login"
        st.rerun()

    st.title("🚀 LinkedIn AI Agent")

    tabs = st.tabs(["Generate", "Comment", "Hashtags", "History", "Favorites"])

    # =====================================================
    # GENERATE
    # =====================================================
    with tabs[0]:
        topic = st.text_input("Topic", key="gen_topic")
        style = st.selectbox("Style", ["professional", "viral", "story"], key="gen_style")
        use_rag = st.checkbox("Use RAG")

        if st.button("Generate Post"):

            progress = st.progress(0)
            status = st.empty()

            for i in range(0, 60, 10):
                progress.progress(i)
                status.text("Thinking...")
                time.sleep(0.2)

            endpoint = "/generate-rag" if use_rag else "/generate"

            res = safe_request(
                "POST",
                f"{API_URL}{endpoint}",
                {"topic": topic, "style": style}
            )

            progress.progress(100)

            if res:
                st.session_state.post = res["data"]["content"]
                st.session_state.favourite_added = False
                st.session_state.scored = False

        if st.session_state.post:
            edited = st.text_area("Edit Post", st.session_state.post, height=250)

            st.download_button("📥 Download", edited)

            col1, col2, col3 = st.columns(3)

            # ⭐ ADD FAVOURITE
            with col1:
                if st.session_state.favourite_added:
                    st.button("⭐ Added", disabled=True)
                else:
                    if st.button("⭐ Add Favourite"):
                        res = safe_request(
                            "POST",
                            f"{API_URL}/favorite",
                            {"topic": topic, "content": edited}
                        )
                        if res:
                            st.session_state.favourite_added = True
                            st.success("Added to favourites ✅")
                            st.rerun()

            # 🔄 REGENERATE
            with col2:
                if st.button("🔄 Regenerate"):
                    st.session_state.post = ""
                    st.session_state.favourite_added = False
                    st.session_state.scored = False
                    st.rerun()

            # 🧠 SCORE
            with col3:
                if st.session_state.scored:
                    st.button("🧠 Scored", disabled=True)
                else:
                    if st.button("🧠 Score"):
                        res = safe_request(
                            "POST",
                            f"{API_URL}/score",
                            {"content": edited}
                        )
                        if res:
                            st.session_state.scored = True
                            st.info(res["score"])

    # =====================================================
    # COMMENT
    # =====================================================
    with tabs[1]:
        content = st.text_area("Paste post")

        if st.button("Generate Comment"):
            res = safe_request(
                "POST",
                f"{API_URL}/comment",
                {"content": content}
            )
            if res:
                st.write(res["comment"])

    # =====================================================
    # HASHTAGS
    # =====================================================
    with tabs[2]:
        topic2 = st.text_input("Topic for hashtags")

        if st.button("Generate Tags"):
            res = safe_request(
                "POST",
                f"{API_URL}/hashtags",
                {"topic": topic2}
            )
            if res:
                st.write(res["hashtags"])
    # =====================================================
    # HISTORY
    # =====================================================

    with tabs[3]:
        if st.button("Load History"):
            res = safe_request("GET", f"{API_URL}/posts")
            if res:
                for p in res["data"]:
                    st.markdown(f"### 📌 {p['topic']}")
                    st.write(p["content"])

    # =====================================================
    # Favourites
    # =====================================================

    with tabs[4]:
        st.subheader("⭐ Saved Favourites")

        res = safe_request("GET", f"{API_URL}/favorites")

        if res and "data" in res:
            for f in res["data"]:
                st.markdown(f"### ⭐ {f['topic']}")
                st.write(f["content"])
                st.divider()
        else:
            st.info("No favourites yet")