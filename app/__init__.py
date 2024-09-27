from flask import Flask
from flask_jwt_extended import JWTManager
from .models import db
from .routes import api


def create_app():
    app = Flask(__name__)
    app.config.from_object("config.Config")
    app.config["JWT_SECRET_KEY"] = "your-secret-key"  # Mude isto em produção!

    db.init_app(app)
    JWTManager(app)

    app.register_blueprint(api, url_prefix="/api")

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=5000, debug=True)
