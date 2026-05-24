"""
Chat API Routes
===============
The HTTP layer for the chat API. These route handlers are deliberately
"thin": they only parse the request and format the response. All medical
logic lives in the chat_engine service.

Defined as a Flask Blueprint so it can be cleanly registered by the
application factory.
"""

import datetime

from flask import Blueprint, request, jsonify, current_app

from app.services.chat_engine import analyze_message, list_topics

# All routes here are prefixed with /api (set during registration).
api_bp = Blueprint("api", __name__)


@api_bp.route("/chat", methods=["POST"])
def chat():
    """
    Main chat endpoint.

    Expects JSON: {"message": "..."}
    Returns JSON with the bot's structured reply.
    """
    data = request.get_json(silent=True) or {}
    message = data.get("message", "").strip()

    if not message:
        return jsonify({
            "ok": False,
            "error": "Empty message. Please type something.",
        }), 400

    result = analyze_message(message)
    result["ok"] = True
    result["timestamp"] = datetime.datetime.now().strftime("%H:%M")
    return jsonify(result)


@api_bp.route("/health", methods=["GET"])
def health_check():
    """Lightweight endpoint to confirm the backend is online."""
    return jsonify({
        "status": "online",
        "service": current_app.config["APP_NAME"] + " API",
        "version": current_app.config["APP_VERSION"],
    })


@api_bp.route("/topics", methods=["GET"])
def topics():
    """Return the list of conditions the bot knows - used by quick-chat."""
    return jsonify({
        "ok": True,
        "topics": list_topics(),
    })
