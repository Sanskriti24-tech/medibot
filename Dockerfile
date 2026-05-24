# =====================================================================
# MediBot - Dockerfile
# Packages the app, Python, and all dependencies into one portable image.
# This is what makes the app run identically on any machine or cloud host.
# =====================================================================

# 1. Start from a small, official Python base image.
FROM python:3.12-slim

# 2. Environment settings for cleaner, faster Python in a container.
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    FLASK_ENV=production

# 3. Set the working directory inside the container.
WORKDIR /app

# 4. Install dependencies first (this layer is cached unless requirements change).
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copy the rest of the application code.
COPY . .

# 6. Document the port the app listens on.
EXPOSE 5000

# 7. Run the app with Gunicorn, a production-grade server.
#    4 workers handle requests concurrently.
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "4", "wsgi:app"]
