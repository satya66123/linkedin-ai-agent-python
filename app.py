from flask import Flask
from flask_jwt_extended import JWTManager
from routes.post_routes import post_bp
from routes.auth_routes import auth_bp

app = Flask(__name__)

app.config["JWT_SECRET_KEY"] = "super-secret-key"

jwt = JWTManager(app)

app.register_blueprint(post_bp)
app.register_blueprint(auth_bp)

@app.route("/")
def home():
    return {"message": "Running"}

if __name__ == "__main__":
    app.run(debug=True)