"""
Test Suite for MediBot
======================
Automated tests using pytest. For a health-related product, the most
critical test is that EMERGENCY messages are always detected correctly -
a missed emergency could be dangerous.

Run all tests from the project root:

    pytest -v
"""

import pytest

from app import create_app
from app.config import TestingConfig
from app.services.chat_engine import analyze_message, list_topics


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------
@pytest.fixture
def client():
    """Provide a Flask test client backed by the testing config."""
    app = create_app(TestingConfig)
    with app.test_client() as test_client:
        yield test_client


# ---------------------------------------------------------------------------
# Engine tests - the medical logic
# ---------------------------------------------------------------------------
def test_emergency_detected():
    """Critical: a chest-pain message must trigger an emergency reply."""
    result = analyze_message("I am having severe chest pain")
    assert result["type"] == "emergency"
    assert result["urgency"] == "emergency"


def test_emergency_takes_priority():
    """An emergency keyword must win even alongside ordinary symptoms."""
    result = analyze_message("I have a mild fever but also chest pain")
    assert result["type"] == "emergency"


def test_single_symptom_match():
    """A fever message should return a fever diagnosis card."""
    result = analyze_message("I have a fever")
    assert result["type"] == "diagnosis"
    conditions = [c["condition"] for c in result["conditions"]]
    assert "Fever" in conditions


def test_multi_symptom_match():
    """A message with two symptoms should return both conditions."""
    result = analyze_message("I have a fever and a headache")
    conditions = [c["condition"] for c in result["conditions"]]
    assert "Fever" in conditions
    assert "Headache" in conditions


def test_greeting_detected():
    """A simple greeting should return a greeting response."""
    result = analyze_message("hello")
    assert result["type"] == "greeting"


def test_thanks_detected():
    """A thank-you message should return a polite acknowledgement."""
    result = analyze_message("thank you so much")
    assert result["type"] == "thanks"


def test_health_tip_request():
    """Asking for a tip should return a health tip."""
    result = analyze_message("give me a health tip")
    assert result["type"] == "tip"


def test_unknown_message_fallback():
    """An unrecognised message should return the fallback response."""
    result = analyze_message("xyz random gibberish text")
    assert result["type"] == "unknown"


def test_list_topics_not_empty():
    """The bot should expose a non-empty list of known conditions."""
    topics = list_topics()
    assert isinstance(topics, list)
    assert len(topics) > 0


# ---------------------------------------------------------------------------
# API tests - the HTTP layer
# ---------------------------------------------------------------------------
def test_home_page_loads(client):
    """The home page should load successfully."""
    response = client.get("/")
    assert response.status_code == 200


def test_health_endpoint(client):
    """The health endpoint should report the service as online."""
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.get_json()["status"] == "online"


def test_chat_endpoint_valid(client):
    """A valid chat request should return a successful reply."""
    response = client.post("/api/chat", json={"message": "I have a cough"})
    assert response.status_code == 200
    data = response.get_json()
    assert data["ok"] is True


def test_chat_endpoint_empty_message(client):
    """An empty message should return a 400 error."""
    response = client.post("/api/chat", json={"message": ""})
    assert response.status_code == 400
    assert response.get_json()["ok"] is False


def test_topics_endpoint(client):
    """The topics endpoint should return a list of conditions."""
    response = client.get("/api/topics")
    assert response.status_code == 200
    data = response.get_json()
    assert data["ok"] is True
    assert len(data["topics"]) > 0


def test_unknown_route_returns_json_404(client):
    """An unknown route should return a JSON 404, not an HTML page."""
    response = client.get("/api/does-not-exist")
    assert response.status_code == 404
    assert response.get_json()["ok"] is False
