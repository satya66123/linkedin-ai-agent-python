from flask import Flask
from routes.post_routes import post_bp
from routes.auth_routes import auth_bp

app = Flask(__name__)

app.register_blueprint(post_bp)
app.register_blueprint(auth_bp)

if __name__ == "__main__":
    app.run(debug=True)