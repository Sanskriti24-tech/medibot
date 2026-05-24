"""
Development Entry Point
=======================
Run this file to start MediBot locally for development:

    python run.py

This uses Flask's built-in server, which is convenient for development
but should NOT be used in production. For production, use wsgi.py with
a production server such as Gunicorn (see DEPLOYMENT.md).
"""

from app import create_app

app = create_app()


if __name__ == "__main__":
    print("=" * 55)
    print("  MediBot - Medical Chatbot (development server)")
    print("  Open: http://127.0.0.1:5000")
    print("  Press CTRL+C to stop")
    print("=" * 55)
    app.run(host="127.0.0.1", port=5000)
