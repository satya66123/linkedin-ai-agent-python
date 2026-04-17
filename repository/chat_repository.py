import uuid
from db import get_connection


# ================= CREATE CHAT =================
def create_conversation(user_id, title):
    cid = str(uuid.uuid4())
    db = get_connection()
    cur = db.cursor()

    cur.execute(
        "INSERT INTO conversations (id, user_id, title) VALUES (%s, %s, %s)",
        (cid, user_id, title)
    )

    db.commit()
    cur.close()
    db.close()
    return cid


# ================= SAVE MESSAGE =================
def save_message(cid, role, content):
    db = get_connection()
    cur = db.cursor()

    cur.execute(
        "INSERT INTO messages (id, conversation_id, role, content) VALUES (%s, %s, %s, %s)",
        (str(uuid.uuid4()), cid, role, content)
    )

    db.commit()
    cur.close()
    db.close()


# ================= GET ALL CHATS =================
def get_conversations(user_id):
    db = get_connection()
    cur = db.cursor()

    cur.execute(
        "SELECT id, title FROM conversations WHERE user_id=%s ORDER BY created_at DESC",
        (user_id,)
    )

    data = cur.fetchall()

    cur.close()
    db.close()

    return [{"id": d[0], "title": d[1]} for d in data]


# ================= GET MESSAGES =================
def get_messages(cid):
    db = get_connection()
    cur = db.cursor()

    cur.execute(
        "SELECT role, content FROM messages WHERE conversation_id=%s ORDER BY created_at",
        (cid,)
    )

    data = cur.fetchall()

    cur.close()
    db.close()

    return [{"role": d[0], "content": d[1]} for d in data]


# ================= DELETE CHAT =================
def delete_conversation(cid):
    db = get_connection()
    cur = db.cursor()

    cur.execute("DELETE FROM messages WHERE conversation_id=%s", (cid,))
    cur.execute("DELETE FROM conversations WHERE id=%s", (cid,))

    db.commit()
    cur.close()
    db.close()


def update_conversation_title(cid, title):
    db = get_db()
    cur = db.cursor()

    cur.execute(
        "UPDATE conversations SET title=%s WHERE id=%s",
        (title, cid)
    )

    db.commit()
    cur.close()
    db.close()