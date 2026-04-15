from flask import request
import jwt

SECRET = "this_is_a_secure_secret_key_32_characters_long"

def get_user_id_from_token():
    auth = request.headers.get("Authorization")

    if not auth:
        raise Exception("Token missing")

    token = auth.split(" ")[1]

    decoded = jwt.decode(token, SECRET, algorithms=["HS256"])

    return decoded["user_id"]