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



# Save Favorite
def save_favorite(topic, content):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO favorites (topic, content) VALUES (%s, %s)",
        (topic, content)
    )
    conn.commit()


# Get Favorites
def get_favorites():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM favorites ORDER BY created_at DESC")
    return cursor.fetchall()