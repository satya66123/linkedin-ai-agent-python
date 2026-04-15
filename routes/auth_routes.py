from flask import Blueprint, request
import jwt
import datetime
from db import get_connection

auth_bp = Blueprint("auth", __name__)

SECRET = "this_is_a_secure_secret_key_32_characters_long"

@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.json
    username = data.get("username")
    password = data.get("password")

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("INSERT INTO users(username,password) VALUES(%s,%s)", (username, password))
    conn.commit()
    conn.close()

    return {"message": "User created"}

@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.json
    username = data.get("username")
    password = data.get("password")

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM users WHERE username=%s AND password=%s", (username, password))
    user = cursor.fetchone()
    conn.close()

    if not user:
        return {"error": "Invalid"}, 401

    token = jwt.encode({
        "user_id": user["id"],
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=10)
    }, SECRET, algorithm="HS256")

    return {"access_token": token}