from dotenv import load_dotenv
from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
import os

from routes.auth_routes import auth_bp
from routes.project_routes import project_bp
from routes.analysis_routes import analysis_bp
from services.db_service import init_db
from services.project_service import ensure_indexes as ensure_project_indexes
from services.analysis_service import ensure_indexes as ensure_analysis_indexes
from services.recommendation_service import ensure_indexes as ensure_recommendation_indexes
from services.user_service import ensure_indexes as ensure_user_indexes


load_dotenv()


def create_app() -> Flask:
    app = Flask(__name__)
    app.config.from_object("config.Config")

    CORS(app, resources={r"/*": {"origins": app.config["CORS_ORIGINS"].split(",")}})
    JWTManager(app)

    init_db(app)
    ensure_project_indexes()
    ensure_analysis_indexes()
    ensure_recommendation_indexes()
    ensure_user_indexes()

    app.register_blueprint(auth_bp)
    app.register_blueprint(project_bp)
    app.register_blueprint(analysis_bp)

    @app.get("/")
    def health_check():
        return {"status": "ok", "service": "SPRS Backend"}, 200

    return app


app = create_app()


if __name__ == "__main__":
    is_windows = os.name == "nt"
    app.run(
        host=app.config["API_HOST"],
        port=app.config["API_PORT"],
        debug=app.config["API_DEBUG"],
        use_reloader=not is_windows,
    )
