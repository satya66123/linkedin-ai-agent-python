from flask import Flask, request, jsonify
from services.ai_service import generate_linkedin_post
from db import get_connection

app = Flask(__name__)

@app.route("/")
def home():
    return "AI Agent Running with DB 🚀"


# ✅ Generate + Save
@app.route("/generate", methods=["POST"])
def generate():
    data = request.json

    topic = data.get("topic")
    model = data.get("model", "llama3:instruct")

    if not topic:
        return jsonify({"error": "Topic is required"}), 400

    print(f"[REQUEST] Topic: {topic}, Model: {model}")

    # 🔹 Generate AI content
    content = generate_linkedin_post(topic, model)

    # 🔹 Save to MySQL
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO posts (topic, content, model) VALUES (%s, %s, %s)",
        (topic, content, model)
    )
    conn.commit()

    return jsonify({
        "message": "Post generated and saved successfully",
        "data": {
            "topic": topic,
            "model": model,
            "content": content
        }
    })


# ✅ Fetch all posts
@app.route("/posts", methods=["GET"])
def get_posts():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM posts ORDER BY created_at DESC")
    posts = cursor.fetchall()

    return jsonify({
        "count": len(posts),
        "data": posts
    })


if __name__ == "__main__":
    app.run(debug=True)