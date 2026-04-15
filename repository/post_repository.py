from db import get_connection

def insert_post(user_id, topic, content, model):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO posts(user_id, topic, content, model) VALUES(%s,%s,%s,%s)",
        (user_id, topic, content, model)
    )

    conn.commit()
    conn.close()

def get_user_posts(user_id):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM posts WHERE user_id=%s", (user_id,))
    data = cursor.fetchall()

    conn.close()
    return data

def save_favorite(user_id, topic, content):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO favorites(user_id, topic, content) VALUES(%s,%s,%s)",
        (user_id, topic, content)
    )

    conn.commit()
    conn.close()

def get_user_favorites(user_id):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM favorites WHERE user_id=%s", (user_id,))
    data = cursor.fetchall()

    conn.close()
    return data