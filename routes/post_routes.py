from flask import Blueprint, request, jsonify
from services.ai_service import generate_post, generate_comment, generate_hashtags, score_post
from repository.post_repository import save_post, get_all_posts, save_favorite, get_favorites

post_bp = Blueprint("post_bp", __name__)


@post_bp.route("/generate", methods=["POST"])
def generate():
    data = request.json
    topic = data.get("topic")
    style = data.get("style", "professional")

    content = generate_post(topic, style=style)
    save_post(topic, content, "phi3")

    return jsonify({"data": {"content": content}})


@post_bp.route("/comment", methods=["POST"])
def comment():
    content = request.json.get("content")
    return jsonify({"comment": generate_comment(content)})


@post_bp.route("/hashtags", methods=["POST"])
def hashtags():
    topic = request.json.get("topic")
    return jsonify({"hashtags": generate_hashtags(topic)})


@post_bp.route("/posts", methods=["GET"])
def posts():
    return jsonify({"data": get_all_posts()})


# ⭐ Save favorite
@post_bp.route("/favorite", methods=["POST"])
def add_favorite():
    data = request.json
    save_favorite(data.get("topic"), data.get("content"))
    return jsonify({"message": "Saved"})


# ⭐ Get favorites
@post_bp.route("/favorites", methods=["GET"])
def fetch_favorites():
    return jsonify({"data": get_favorites()})


# 🧠 Score
@post_bp.route("/score", methods=["POST"])
def score():
    content = request.json.get("content")
    return jsonify({"score": score_post(content)})

from services.ai_service import generate_post_with_rag
@post_bp.route("/generate-rag", methods=["POST"])
def generate_rag():
    data = request.json
    topic = data.get("topic")

    content = generate_post_with_rag(topic)

    return {"data": {"content": content}}