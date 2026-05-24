"""
Chat Engine Service
===================
The "brain" of MediBot. This service layer contains the core business
logic: it analyses a user's message and decides what reply to produce.

Routes (the HTTP layer) call analyze_message() and never deal with
medical logic directly. This separation makes the engine easy to test
and to swap out later for a real ML model.
"""

import random

from app.data.knowledge_base import (
    KNOWLEDGE_BASE,
    EMERGENCY_KEYWORDS,
    GREETINGS,
    THANKS,
    GENERAL_TIPS,
)

# Rank used to pick the most serious urgency when several conditions match.
_URGENCY_RANK = {"none": 0, "low": 1, "moderate": 2, "emergency": 3}


def _check_emergency(text):
    """Return an emergency response if any critical keyword is present."""
    for keyword in EMERGENCY_KEYWORDS:
        if keyword in text:
            return {
                "type": "emergency",
                "reply": ("This may be a MEDICAL EMERGENCY. Please call your "
                          "local emergency number immediately or go to the "
                          "nearest hospital. In India, dial 112 or 102 for an "
                          "ambulance. Do not wait."),
                "urgency": "emergency",
            }
    return None


def _check_greeting(text):
    """Return a greeting response if the message is a greeting."""
    if any(text == g or text.startswith(g + " ") for g in GREETINGS):
        return {
            "type": "greeting",
            "reply": ("Hello! I'm MediBot, your health assistant. You can tell "
                      "me about a symptom (like 'I have a fever and headache') "
                      "and I'll share some guidance. How are you feeling "
                      "today?"),
            "urgency": "none",
        }
    return None


def _check_thanks(text):
    """Return a polite acknowledgement if the user says thanks."""
    if any(t in text for t in THANKS):
        return {
            "type": "thanks",
            "reply": ("You're welcome! Take care of yourself. Remember, I'm "
                      "just an educational assistant - always consult a real "
                      "doctor for proper medical advice."),
            "urgency": "none",
        }
    return None


def _check_tip(text):
    """Return a random health tip if the user asks for one."""
    if "tip" in text or ("advice" in text and len(text) < 25):
        return {
            "type": "tip",
            "reply": "Here's a health tip for you: " + random.choice(GENERAL_TIPS),
            "urgency": "none",
        }
    return None


def _match_conditions(text):
    """Match the message against the knowledge base; return matched data."""
    matched = []
    for data in KNOWLEDGE_BASE.values():
        for keyword in data["keywords"]:
            if keyword in text:
                matched.append(data)
                break
    return matched


def analyze_message(message):
    """
    Core engine entry point.

    Takes a raw user message and returns a structured dict describing the
    reply. The checks run in priority order, with safety (emergencies)
    always first.
    """
    text = message.lower().strip()

    # 1. Emergencies have the highest priority - safety first.
    result = _check_emergency(text)
    if result:
        return result

    # 2. Conversational intents: greeting, thanks, tip request.
    for checker in (_check_greeting, _check_thanks, _check_tip):
        result = checker(text)
        if result:
            return result

    # 3. Match symptoms against the medical knowledge base.
    matches = _match_conditions(text)
    if matches:
        conditions = []
        highest_urgency = "low"
        for data in matches:
            conditions.append({
                "condition": data["condition"],
                "info": data["info"],
                "advice": data["advice"],
                "see_doctor": data["see_doctor"],
            })
            if _URGENCY_RANK[data["urgency"]] > _URGENCY_RANK[highest_urgency]:
                highest_urgency = data["urgency"]
        return {
            "type": "diagnosis",
            "conditions": conditions,
            "urgency": highest_urgency,
        }

    # 4. Fallback when nothing matches.
    return {
        "type": "unknown",
        "reply": ("I'm not sure I understood that. I can help with common "
                  "issues like fever, cough, cold, headache, stomach ache, "
                  "sore throat, body pain, blood pressure, and diabetes. "
                  "Try describing your symptom, for example: 'I have a sore "
                  "throat and mild fever.'"),
        "urgency": "none",
    }


def list_topics():
    """Return the list of conditions the bot knows about."""
    return [data["condition"] for data in KNOWLEDGE_BASE.values()]
