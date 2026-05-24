"""
View Routes
===========
Serves the frontend HTML page. Kept separate from the API blueprint so
that page rendering and the JSON API are cleanly distinct concerns.
"""

from flask import Blueprint, render_template

views_bp = Blueprint("views", __name__)


@views_bp.route("/")
def home():
    """Serve the main chatbot web page."""
    return render_template("index.html")
