"""
Production WSGI Entry Point
===========================
This file exposes the WSGI application object that a production server
(such as Gunicorn or uWSGI) imports and runs.

Example - run with Gunicorn:

    gunicorn --bind 0.0.0.0:5000 wsgi:app

Gunicorn looks for the variable named `app` in this module.
"""

import os

from app import create_app
from app.config import config_by_name

# Force the production config when served via WSGI.
env = os.environ.get("FLASK_ENV", "production")
app = create_app(config_by_name.get(env, config_by_name["production"]))


if __name__ == "__main__":
    app.run()
