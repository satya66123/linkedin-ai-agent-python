from flask import Blueprint, request
from services.post_service import generate_post, save_post
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


# ================= GENERATE =================
@post_bp.route("/generate", methods=["POST"])
def generate():
    user_id = get_user_id_from_token()

    data = request.json
    topic = data.get("topic")
    style = data.get("style", "professional")
    model = data.get("model", "phi3")
    doc_ids = data.get("doc_ids")

    # 🔥 RAG SEARCH
    context, score = search(topic, doc_filter=doc_ids)

    # 🔥 DECISION
    USE_LLM = True
    if context and len(context) > 40 and score > 0.5:
        USE_LLM = False

    # ================= RESPONSE =================
    if not USE_LLM:
        # RAG → summarize into bullets
        prompt = f"""
Convert the following into EXACTLY 3 bullet points.

STRICT RULES:
- Only bullet points starting with "-"
- Each bullet = 1 short sentence
- No extra explanation

Text:
{context}
"""
        content = generate_post(prompt, style, model)

    else:
        # LLM → strict format
        prompt = f"""
Answer the question in EXACTLY 3 bullet points.

STRICT RULES:
- Only bullet points starting with "-"
- Each bullet = 1 short sentence
- No paragraphs
- No extra text

Question:
{topic}
"""
        content = generate_post(prompt, style, model)

    # 🔥 FINAL CLEAN
    content = clean_output(content)

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