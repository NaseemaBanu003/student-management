from flask import Flask

from app.config import Config
from app.extensions import cors, db, jwt, limiter, ma, migrate
from app.routes import register_blueprints


def create_app(config_object=None):
    app = Flask(__name__, template_folder="templates", static_folder="static")
    app.config.from_object(config_object or Config)

    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    cors.init_app(app, resources={r"/api/*": {"origins": app.config.get("CORS_ORIGINS", "*").split(",")}})
    limiter.init_app(app)
    ma.init_app(app)

    register_blueprints(app)

    @app.errorhandler(404)
    def not_found(error):
        return {"success": False, "message": "Resource not found"}, 404

    @app.errorhandler(405)
    def method_not_allowed(error):
        return {"success": False, "message": "Method not allowed"}, 405

    @app.errorhandler(500)
    def internal_server_error(error):
        return {"success": False, "message": "Internal server error"}, 500

    return app
