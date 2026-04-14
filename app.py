from flask import Flask, request, jsonify
from services.ai_service import generate_linkedin_post

app = Flask(__name__)

@app.route("/")
def home():
    return "Ollama AI Agent Running 🚀"


@app.route("/generate", methods=["POST"])
def generate():
    data = request.json

    topic = data.get("topic")
    model = data.get("model", "llama3:instruct")

    print(f"[REQUEST] Topic: {topic}, Model: {model}")

    if not topic:
        return jsonify({
            "status": "error",
            "message": "Topic is required"
        }), 400

    content = generate_linkedin_post(topic, model)

    return jsonify({
        "status": "success",
        "data": {
            "topic": topic,
            "model": model,
            "content": content
        }
    })


if __name__ == "__main__":
    app.run(debug=True)