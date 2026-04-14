from flask import Blueprint, request, jsonify
from services.ai_service import generate_post, generate_comment, generate_hashtags
from repository.post_repository import save_post, get_all_posts
from dto.post_dto import PostRequestDTO

post_bp = Blueprint("post_bp", __name__)


# 🔹 Generate Post
@post_bp.route("/generate", methods=["POST"])
def generate():
    dto = PostRequestDTO(request.json)

    valid, error = dto.validate()
    if not valid:
        return jsonify({"error": error}), 400

    content = generate_post(dto.topic, dto.model, dto.style)

    save_post(dto.topic, content, dto.model)

    return jsonify({
        "message": "Post generated",
        "data": {
            "topic": dto.topic,
            "style": dto.style,
            "model": dto.model,
            "content": content
        }
    })


# 🔹 Get Posts
@post_bp.route("/posts", methods=["GET"])
def posts():
    data = get_all_posts()
    return jsonify({"count": len(data), "data": data})


# 🔹 Generate Comment
@post_bp.route("/comment", methods=["POST"])
def comment():
    content = request.json.get("content")
    if not content:
        return {"error": "Content required"}, 400

    return {"comment": generate_comment(content)}


# 🔹 Generate Hashtags
@post_bp.route("/hashtags", methods=["POST"])
def hashtags():
    topic = request.json.get("topic")
    if not topic:
        return {"error": "Topic required"}, 400

    return {"hashtags": generate_hashtags(topic)}