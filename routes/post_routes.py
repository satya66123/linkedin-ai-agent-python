from flask import Blueprint, request
from services.post_service import generate_post, save_post
from repository.post_repository import get_user_posts, get_user_favorites, save_favorite
from utils.jwt_util import get_user_id_from_token

post_bp = Blueprint("post", __name__)

@post_bp.route("/generate", methods=["POST"])
def generate():
    user_id = get_user_id_from_token()

    data = request.json
    topic = data.get("topic")
    style = data.get("style", "professional")
    model = data.get("model", "phi3")  # NEW

    content = generate_post(topic, style, model)

    save_post(user_id, topic, content, model)

    return {
        "data": {
            "topic": topic,
            "content": content,
            "model": model
        }
    }


@post_bp.route("/posts", methods=["GET"])
def posts():
    user_id = get_user_id_from_token()
    data = get_user_posts(user_id)
    return {"data": data}

@post_bp.route("/favorite", methods=["POST"])
def favorite():
    user_id = get_user_id_from_token()

    data = request.json
    topic = data.get("topic")
    content = data.get("content")

    save_favorite(user_id, topic, content)

    return {"message": "Saved"}

@post_bp.route("/favorites", methods=["GET"])
def favorites():
    user_id = get_user_id_from_token()
    data = get_user_favorites(user_id)
    return {"data": data}