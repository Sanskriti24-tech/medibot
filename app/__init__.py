"""
Application Factory
===================
This module defines create_app(), the application factory.

Instead of creating the Flask app at import time, a factory function
builds and configures it on demand. This is a Flask best practice
because it:
  - allows different configs for dev / testing / production,
  - makes automated testing clean (each test gets a fresh app),
  - avoids circular-import problems as the project grows.
"""

from flask import Flask, jsonify
from flask_cors import CORS

from app.config import get_config


def create_app(config_class=None):
    """
    Build, configure, and return a Flask application instance.

    Args:
        config_class: optional config class. If not given, it is chosen
                      from the FLASK_ENV environment variable.
    """
    app = Flask(__name__)

    # --- Configuration ---------------------------------------------------
    if config_class is None:
        config_class = get_config()
    app.config.from_object(config_class)

    # --- Extensions ------------------------------------------------------
    CORS(app)  # allow the frontend to call the API

    # --- Blueprints (registered here to avoid circular imports) ----------
    from app.routes.views import views_bp
    from app.routes.chat import api_bp

    app.register_blueprint(views_bp)
    app.register_blueprint(api_bp, url_prefix="/api")

    # --- Error handlers --------------------------------------------------
    register_error_handlers(app)

    return app


def register_error_handlers(app):
    """Attach JSON error handlers so the API fails gracefully."""

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "ok": False,
            "error": "Resource not found.",
        }), 404

    @app.errorhandler(405)
    def method_not_allowed(error):
        return jsonify({
            "ok": False,
            "error": "Method not allowed for this endpoint.",
        }), 405

    @app.errorhandler(500)
    def server_error(error):
        return jsonify({
            "ok": False,
            "error": "An internal server error occurred.",
        }), 500
