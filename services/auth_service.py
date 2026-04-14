import bcrypt
from db import get_connection

# ----------------------------
# REGISTER USER
# ----------------------------
def register_user(username, password):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    # Check if user exists
    cursor.execute("SELECT * FROM users WHERE username=%s", (username,))
    existing = cursor.fetchone()

    if existing:
        raise Exception("Username already exists")

    # 🔥 FIX: decode hash to string
    hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

    cursor.execute(
        "INSERT INTO users (username, password) VALUES (%s, %s)",
        (username, hashed)
    )
    conn.commit()


# ----------------------------
# LOGIN USER
# ----------------------------
def login_user(username, password):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM users WHERE username=%s", (username,))
    user = cursor.fetchone()

    if user and bcrypt.checkpw(password.encode(), user["password"].encode()):
        return user

    return None