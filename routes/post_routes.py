from flask import Blueprint, request
from services.post_service import generate_post, save_post, generate_post2
from repository.post_repository import (
    get_user_posts,
    get_user_favorites,
    save_favorite
)
from utils.jwt_util import get_user_id_from_token

from services.rag_service import (
    search,
    add_document,
    list_documents,
    delete_document
)

post_bp = Blueprint("post", __name__)


# ================= HELPER =================
def clean_output(text):
    lines = text.split("\n")
    bullets = [l.strip() for l in lines if l.strip().startswith("-")]

    # fallback if model fails
    if not bullets:
        sentences = text.split(".")
        bullets = [f"- {s.strip()}" for s in sentences if s.strip()]

    return "\n".join(bullets[:3])

from repository.chat_repository import save_message

@post_bp.route("/generate", methods=["POST"])
def generate():
    user_id = get_user_id_from_token()

    data = request.json
    topic = data.get("topic")
    style = data.get("style", "professional")
    model = data.get("model", "phi3")
    doc_ids = data.get("doc_ids")
    conversation_id = data.get("conversation_id")  # 🔥 IMPORTANT

    # 🔥 SAVE USER MESSAGE FIRST
    if conversation_id:
        save_message(conversation_id, "user", topic)

    # 🔥 RAG SEARCH
    context, score = search(topic, doc_filter=doc_ids)

    USE_LLM = True
    if context and score > 0.5:
        USE_LLM = False

    # 🔥 GENERATE RESPONSE
    if not USE_LLM:
        content = context
    else:
        prompt = f"""
Use this context if relevant:
{context}

Question:
{topic}
"""
        content = generate_post(prompt, style, model)

    # 🔥 SAVE AI MESSAGE
    if conversation_id:
        save_message(conversation_id, "assistant", content)

    # (optional) keep your post history
    save_post(user_id, topic, content, model)

    return {"data": {"content": content}}

# ================= HISTORY =================
@post_bp.route("/posts", methods=["GET"])
def posts():
    user_id = get_user_id_from_token()
    return {"data": get_user_posts(user_id)}


# ================= FAVORITE =================
@post_bp.route("/favorite", methods=["POST"])
def favorite():
    user_id = get_user_id_from_token()
    data = request.json

    save_favorite(user_id, data.get("topic"), data.get("content"))

    return {"message": "Saved"}


@post_bp.route("/favorites", methods=["GET"])
def favorites():
    user_id = get_user_id_from_token()
    return {"data": get_user_favorites(user_id)}


# ================= RAG =================
@post_bp.route("/upload", methods=["POST"])
def upload():
    file = request.files.get("file")

    if not file:
        return {"error": "No file"}, 400

    return {"doc_id": add_document(file)}


@post_bp.route("/documents", methods=["GET"])
def documents():
    return {"data": list_documents()}


@post_bp.route("/documents/<doc_id>", methods=["DELETE"])
def delete_doc(doc_id):
    delete_document(doc_id)
    return {"message": "Deleted"}



# ================= CHAT GENERATE =================
@post_bp.route("/generate2", methods=["POST"])
def generate2():
    user_id = get_user_id_from_token()
    data = request.json
    message = data.get("topic")  # rename logically
    style = data.get("style", "professional")
    model = data.get("model", "phi3")
    doc_ids = data.get("doc_ids")
    conversation_id = data.get("conversation_id")

    # 🔥 SAVE USER MESSAGE
    if conversation_id:
        save_message(conversation_id, "user", message)

    # 🔥 RAG SEARCH
    context, score = search(message, doc_filter=doc_ids)

    USE_LLM = True
    if context and score > 0.5:
        USE_LLM = False

    # 🔥 RESPONSE
    if not USE_LLM:
        response = context
    else:
        prompt = f"""
        Answer naturally like ChatGPT.

        User: {message}
        """
        response = generate_post2(prompt, style, model)

    # 🔥 SAVE AI MESSAGE
    if conversation_id:
        save_message(conversation_id, "assistant", response)

    return {"data": {"content": response}}