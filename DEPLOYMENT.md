# Deployment Guide — MediBot

This guide explains how to take MediBot from your laptop to the public
internet. It goes from simplest to most professional. For a college
submission, **Option B (Render)** is the recommended sweet spot.

---

## Background — Why You Can't Just Use `python run.py`

The `run.py` server is Flask's **development** server. It is single-
threaded, slow, and not secure enough for real users. For production you
need:

1. A **WSGI server** (Gunicorn) — actually runs the Python app, handles
   many requests at once.
2. Optionally a **reverse proxy** (Nginx) — sits in front, handles HTTPS
   and serves static files efficiently.

The deployment chain looks like this:

```
Users  →  HTTPS  →  [ Nginx ]  →  Gunicorn  →  Flask app (MediBot)
```

---

## Option A — Run with Gunicorn (local production test)

This proves the app works under a production server. Works on
Linux/macOS.

1. Install dependencies (already includes Gunicorn):
   ```
   pip install -r requirements.txt
   ```

2. Start the app with Gunicorn:
   ```
   gunicorn --bind 0.0.0.0:5000 --workers 4 wsgi:app
   ```
   - `wsgi:app` means "the `app` object inside `wsgi.py`".
   - `--workers 4` runs 4 processes to handle traffic concurrently.

3. Open `http://127.0.0.1:5000`.

> On Windows, Gunicorn is not supported — use `waitress` instead:
> `pip install waitress` then
> `waitress-serve --port=5000 wsgi:app`.

---

## Option B — Deploy to Render (recommended, free)

[Render](https://render.com) deploys straight from a GitHub repo and has
a free tier. This is the easiest way to get a real public URL.

**Step 1 — Push your code to GitHub**
```
git init
git add .
git commit -m "MediBot medical chatbot"
git branch -M main
git remote add origin https://github.com/<your-username>/medibot.git
git push -u origin main
```

**Step 2 — Create the service on Render**
1. Sign up at render.com and click **New → Web Service**.
2. Connect your GitHub account and pick the `medibot` repo.
3. Fill in the settings:
   - **Environment:** `Python 3`
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `gunicorn wsgi:app`
   - **Instance Type:** Free

**Step 3 — Add environment variables**
In the Render dashboard, under **Environment**, add:
   - `FLASK_ENV` = `production`
   - `SECRET_KEY` = (a long random string)

**Step 4 — Deploy**
Click **Create Web Service**. Render builds and deploys automatically.
After a few minutes you get a public URL like
`https://medibot.onrender.com`.

Every future `git push` redeploys automatically.

> Alternatives that work almost identically: **Railway**
> (railway.app) and **PythonAnywhere** (pythonanywhere.com).

---

## Option C — Deploy with Docker

Docker packages the app into a portable container that runs identically
anywhere. The `Dockerfile` is already included.

**Step 1 — Build the image**
```
docker build -t medibot .
```

**Step 2 — Run the container**
```
docker run -p 5000:5000 medibot
```

**Step 3 — Open** `http://127.0.0.1:5000`.

The image can be pushed to Docker Hub and run on any cloud that supports
containers (AWS, Google Cloud, Azure, DigitalOcean).

---

## Option D — Deploy on a Cloud VM (most control)

For a virtual machine (AWS EC2, DigitalOcean Droplet, etc.):

1. **Create a VM** with Ubuntu and SSH into it.

2. **Install requirements:**
   ```
   sudo apt update
   sudo apt install python3-pip python3-venv nginx -y
   ```

3. **Copy the project** to the server and install dependencies inside a
   virtual environment.

4. **Run Gunicorn** (ideally managed by `systemd` so it restarts on
   reboot):
   ```
   gunicorn --bind 127.0.0.1:5000 --workers 4 wsgi:app
   ```

5. **Configure Nginx** as a reverse proxy in front of Gunicorn, and add
   a free HTTPS certificate with Let's Encrypt (`certbot`).

This is how a real production team would host it, but it is the most
involved — Options B and C are better for a mini-project.

---

## Continuous Integration (CI)

The file `.github/workflows/ci.yml` makes GitHub **run all tests
automatically** on every push. If a change breaks a test, GitHub flags
it before the code is deployed. This is what keeps a deployed app
reliable.

---

## Deployment Checklist

Before going live, confirm:

- [ ] All tests pass (`pytest`).
- [ ] `FLASK_ENV` is set to `production`.
- [ ] `SECRET_KEY` is a real random value, not the default.
- [ ] `debug` mode is OFF (it is, in production config).
- [ ] The app is served by Gunicorn, not `run.py`.
- [ ] `.env` is **not** committed to git (it is git-ignored).

---

## Quick Summary

| Option | Difficulty | Best for                          |
|--------|-----------|-----------------------------------|
| A — Gunicorn | Easy | Testing production locally     |
| B — Render   | Easy | **Getting a real public URL**  |
| C — Docker   | Medium | Portable, cloud-agnostic     |
| D — Cloud VM | Hard | Full control, real-world setup |

For your submission: run **Option A** to demo locally, and mention
**Option B/C** to show you understand real deployment.
