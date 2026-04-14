from flask import Flask
from db import get_connection

app = Flask(__name__)

@app.route("/")
def home():
    try:
        get_connection()
        return "DB Connected Successfully ✅"
    except Exception as e:
        return f"DB Connection Failed ❌ {str(e)}"

@app.route("/test-insert")
def test_insert():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO posts (topic, content, model) VALUES (%s, %s, %s)",
        ("Test Topic", "This is a test post", "llama3")
    )

    conn.commit()

    return "Data Inserted ✅"

if __name__ == "__main__":
    app.run(debug=True)