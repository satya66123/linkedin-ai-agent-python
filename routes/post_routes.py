from flask import Blueprint, request, jsonify
from services.ai_service import generate_linkedin_post
from repository.post_repository import save_post, get_all_posts
from dto.post_dto import PostRequestDTO

post_bp = Blueprint("post_bp", __name__)


@post_bp.route("/generate", methods=["POST"])
def generate():
    dto = PostRequestDTO(request.json)

    is_valid, error = dto.validate()
    if not is_valid:
        return jsonify({"error": error}), 400

    content = generate_linkedin_post(dto.topic, dto.model)

    save_post(dto.topic, content, dto.model)

    return jsonify({
        "message": "Post generated and saved",
        "data": {
            "topic": dto.topic,
            "model": dto.model,
            "content": content
        }
    })


@post_bp.route("/posts", methods=["GET"])
def get_posts():
    posts = get_all_posts()

    return jsonify({
        "count": len(posts),
        "data": posts
    })