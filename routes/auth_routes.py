from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from services.auth_service import register_user, login_user

auth_bp = Blueprint("auth_bp", __name__)

# ----------------------------
# REGISTER
# ----------------------------
@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.json

    try:
        username = data.get("username")
        password = data.get("password")

        if not username or not password:
            return jsonify({"error": "Username and password required"}), 400

        register_user(username, password)

        return jsonify({"message": "User created successfully"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 400


# ----------------------------
# LOGIN
# ----------------------------
@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.json

    try:
        username = data.get("username")
        password = data.get("password")

        user = login_user(username, password)

        if not user:
            return jsonify({"error": "Invalid credentials"}), 401

        token = create_access_token(identity=user["id"])

        return jsonify({"token": token}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 400