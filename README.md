# MediBot — Medical Chatbot

A fully functional medical assistant chatbot with a polished web UI,
quick-chat support, and a production-grade Python backend.

> **Disclaimer:** This is an educational mini-project. It does **not**
> provide real medical diagnoses and should never replace a qualified
> doctor.

---

## Features

- **Conversational chat interface** — describe symptoms in plain English.
- **Rule-based medical knowledge engine** — covers 10 common conditions.
- **Multi-symptom matching** — "I have a fever and headache" returns
  guidance for both.
- **Emergency detection** — critical phrases trigger an urgent alert
  before anything else (safety first).
- **Quick-chat buttons** — tap a common symptom instead of typing.
- **REST API** — clean JSON endpoints (`/api/chat`, `/api/health`,
  `/api/topics`).
- **Polished, responsive UI** — calming medical theme, works on mobile.
- **Automated test suite** — 15 tests covering the engine and the API.
- **Production-ready** — application factory, blueprints, Docker, CI.

---

## Tech Stack

| Layer      | Technology                       |
|------------|----------------------------------|
| Backend    | Python, Flask, Flask-CORS        |
| Server     | Gunicorn (production)            |
| Frontend   | HTML, CSS, JavaScript            |
| Engine     | Rule-based keyword matching      |
| Testing    | pytest                           |
| Deployment | Docker, GitHub Actions (CI)      |

---

## Architecture

The project follows the **application factory** and **blueprint**
patterns — the standard professional structure for Flask apps. The code
is organised in layers, each with a single responsibility.

```
medibot/
│
├── app/                        # The application package
│   ├── __init__.py             # App factory: builds & configures the app
│   ├── config.py               # Dev / Test / Production settings
│   │
│   ├── routes/                 # HTTP layer (thin controllers)
│   │   ├── chat.py             # /api/chat, /api/health, /api/topics
│   │   └── views.py            # serves the HTML page
│   │
│   ├── services/               # Business logic layer
│   │   └── chat_engine.py      # the analyze_message() "brain"
│   │
│   ├── data/                   # Content layer
│   │   └── knowledge_base.py   # medical knowledge, separate from logic
│   │
│   ├── templates/
│   │   └── index.html
│   │
│   └── static/
│       ├── css/style.css
│       └── js/chat.js
│
├── tests/                      # Automated test suite
│   └── test_app.py
│
├── .github/workflows/ci.yml    # Continuous integration pipeline
│
├── run.py                      # Development entry point
├── wsgi.py                     # Production entry point (Gunicorn)
├── Dockerfile                  # Container recipe
├── .dockerignore
├── .gitignore
├── .env.example                # Environment variable template
├── pytest.ini                  # Test configuration
├── requirements.txt
├── README.md                   # This file
└── DEPLOYMENT.md               # Step-by-step deployment guide
```

**Why this structure?**

- **Separation of concerns** — routes only handle HTTP, services hold
  logic, data holds content. Each can be changed independently.
- **Application factory** (`create_app()`) — lets the app run with
  different configs and makes testing clean.
- **Blueprints** — group related routes; the app scales without one
  giant file.
- **Thin routes** — all medical logic sits in the service layer, so it
  is easy to test and could later be swapped for an ML model.

---

## Request Lifecycle — How It Works

```
Browser (UI)
    │  user types "I have a fever"
    ▼
POST /api/chat        ──►  Flask route (routes/chat.py)
                                │  parses JSON
                                ▼
                          chat_engine.analyze_message()
                                │  1. emergency check
                                │  2. greeting / thanks / tip
                                │  3. match knowledge base
                                │  4. fallback
                                ▼
                          structured JSON reply
    ◄─────────────────────────────┘
Browser renders the reply as condition cards
```

Each message is independent — the app is **stateless**.

---

## How to Run Locally

1. **Install Python 3.10+**.

2. **(Recommended) Create a virtual environment:**
   ```
   python -m venv venv
   source venv/bin/activate        # Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```
   pip install -r requirements.txt
   ```

4. **Start the development server:**
   ```
   python run.py
   ```

5. **Open** `http://127.0.0.1:5000` in your browser.

---

## Running the Tests

```
pytest
```

All 15 tests should pass. The most important one verifies that
emergency messages are always detected.

---

## API Endpoints

| Method | Endpoint        | Description                          |
|--------|-----------------|--------------------------------------|
| GET    | `/`             | Serves the chatbot web page          |
| POST   | `/api/chat`     | Send `{"message": "..."}`, get reply |
| GET    | `/api/health`   | Check if the backend is online       |
| GET    | `/api/topics`   | List of conditions the bot knows     |

---

## Deployment

See **DEPLOYMENT.md** for a full step-by-step guide covering Gunicorn,
Docker, and free cloud hosting options.

---

## Possible Future Improvements

- Replace keyword matching with a real ML/NLP intent model.
- Store chat history in a database (PostgreSQL).
- Add user accounts and personalised health records.
- Have a medical professional review and expand the knowledge base.

---

*Created as a college mini-project.*
