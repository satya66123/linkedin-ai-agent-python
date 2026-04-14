from flask import Flask
from routes.post_routes import post_bp

app = Flask(__name__)

@app.route("/")
def home():
    return "Production Ready AI Agent 🚀"

# Register routes
app.register_blueprint(post_bp)

import os

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))