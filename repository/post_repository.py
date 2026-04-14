from db import get_connection

def save_post(topic, content, model):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO posts (topic, content, model) VALUES (%s, %s, %s)",
        (topic, content, model)
    )
    conn.commit()


def get_all_posts():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM posts ORDER BY created_at DESC")
    return cursor.fetchall()