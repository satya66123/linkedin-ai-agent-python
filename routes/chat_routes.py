from flask import Blueprint, request
from repository.chat_repository import (
    create_conversation,
    save_message,
    get_conversations,
    get_messages,
    delete_conversation
)
from utils.jwt_util import get_user_id_from_token

chat_bp = Blueprint("chat", __name__)


# ================= CREATE CHAT =================
@chat_bp.route("/chat/create", methods=["POST"])
def create_chat():
    user_id = get_user_id_from_token()
    title = request.json.get("title", "New Chat")

    cid = create_conversation(user_id, title)

    return {"conversation_id": cid}


# ================= SAVE MESSAGE =================
@chat_bp.route("/chat/<cid>/message", methods=["POST"])
def add_message(cid):
    data = request.json

    save_message(cid, data["role"], data["content"])

    return {"message": "Saved"}


# ================= GET CHATS =================
@chat_bp.route("/chat/list", methods=["GET"])
def list_chats():
    user_id = get_user_id_from_token()
    return {"data": get_conversations(user_id)}


# ================= GET MESSAGES =================
@chat_bp.route("/chat/<cid>", methods=["GET"])
def get_chat(cid):
    return {"data": get_messages(cid)}


# ================= DELETE CHAT =================
@chat_bp.route("/chat/<cid>", methods=["DELETE"])
def delete_chat(cid):
    delete_conversation(cid)
    return {"message": "Deleted"}


# ================= UPDATE TITLE =================
@chat_bp.route("/chat/<cid>/title", methods=["PUT"])
def update_title(cid):
    data = request.json
    title = data.get("title")

    update_conversation_title(cid, title)

    return {"message": "Updated"}
