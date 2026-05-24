"""
Knowledge Base
==============
The medical knowledge content, kept separate from application logic.
A future improvement could load this from a database or JSON file so a
medical content reviewer can update it without touching code.

DISCLAIMER: Educational content only. Not a substitute for a doctor.
"""

# Each entry maps an internal key to structured medical guidance.
KNOWLEDGE_BASE = {
    "fever": {
        "keywords": ["fever", "temperature", "high temp", "hot body", "chills"],
        "condition": "Fever",
        "info": "Fever is a temporary rise in body temperature, often due to an "
                "infection. A normal temperature is around 37 C (98.6 F).",
        "advice": [
            "Rest well and drink plenty of fluids to stay hydrated.",
            "Use a damp cloth on the forehead to help cool down.",
            "Paracetamol can reduce fever (follow the label dosage).",
            "Wear light clothing and keep the room cool.",
        ],
        "see_doctor": "Seek medical care if the fever stays above 39.4 C (103 F), "
                      "lasts more than 3 days, or comes with a rash, stiff neck, "
                      "confusion, or difficulty breathing.",
        "urgency": "moderate",
    },
    "headache": {
        "keywords": ["headache", "head pain", "migraine", "head hurts"],
        "condition": "Headache",
        "info": "Headaches are very common and usually not serious. They can be "
                "caused by stress, dehydration, lack of sleep, or eye strain.",
        "advice": [
            "Rest in a quiet, dark room.",
            "Drink water - dehydration is a common cause.",
            "Apply a cold or warm compress to your head or neck.",
            "Limit screen time and take regular breaks.",
        ],
        "see_doctor": "Get urgent help if the headache is sudden and severe, "
                      "follows a head injury, or comes with vision loss, "
                      "weakness, or trouble speaking.",
        "urgency": "low",
    },
    "cough": {
        "keywords": ["cough", "coughing", "dry cough", "wet cough", "phlegm"],
        "condition": "Cough",
        "info": "A cough is the body's way of clearing the airways. Most coughs "
                "are caused by viral infections and clear up on their own.",
        "advice": [
            "Drink warm fluids like honey-lemon water or herbal tea.",
            "Use a humidifier or inhale steam to soothe airways.",
            "Avoid smoke and other irritants.",
            "Honey can ease a cough (do not give to children under 1 year).",
        ],
        "see_doctor": "Consult a doctor if the cough lasts over 3 weeks, brings "
                      "up blood, or comes with chest pain or breathlessness.",
        "urgency": "low",
    },
    "cold": {
        "keywords": ["cold", "runny nose", "sneezing", "blocked nose",
                     "congestion"],
        "condition": "Common Cold",
        "info": "The common cold is a mild viral infection of the nose and "
                "throat. It usually clears up within 7-10 days.",
        "advice": [
            "Get plenty of rest and sleep.",
            "Stay hydrated with water, soup, and warm drinks.",
            "Saline nasal drops can relieve congestion.",
            "Gargle with warm salt water for a sore throat.",
        ],
        "see_doctor": "See a doctor if symptoms last beyond 10 days, get worse, "
                      "or you develop a high fever or sinus pain.",
        "urgency": "low",
    },
    "stomach": {
        "keywords": ["stomach pain", "stomach ache", "abdominal", "tummy",
                     "indigestion", "gas", "bloating"],
        "condition": "Stomach Ache / Indigestion",
        "info": "Stomach pain has many causes - indigestion, gas, mild "
                "infections, or stress. Most cases are not serious.",
        "advice": [
            "Eat light, bland foods (rice, toast, bananas).",
            "Avoid spicy, oily, or very heavy meals for a while.",
            "Sip water slowly and stay hydrated.",
            "A warm compress on the abdomen can ease cramps.",
        ],
        "see_doctor": "Seek urgent care for severe pain, persistent vomiting, "
                      "blood in stool/vomit, or pain in the lower-right abdomen.",
        "urgency": "moderate",
    },
    "diarrhea": {
        "keywords": ["diarrhea", "diarrhoea", "loose motion", "loose stool"],
        "condition": "Diarrhea",
        "info": "Diarrhea is frequent loose, watery stools. It is often caused "
                "by infections or food and usually resolves within a few days.",
        "advice": [
            "Drink ORS (oral rehydration solution) to replace lost fluids.",
            "Eat simple foods - bananas, rice, applesauce, toast.",
            "Avoid dairy, caffeine, and fatty foods for now.",
            "Wash hands frequently to prevent spreading infection.",
        ],
        "see_doctor": "See a doctor if there is blood in the stool, signs of "
                      "dehydration, high fever, or it lasts more than 2 days.",
        "urgency": "moderate",
    },
    "sore_throat": {
        "keywords": ["sore throat", "throat pain", "throat hurts", "swallowing"],
        "condition": "Sore Throat",
        "info": "A sore throat is usually caused by a viral infection and gets "
                "better on its own within a week.",
        "advice": [
            "Gargle with warm salt water several times a day.",
            "Drink warm fluids and stay hydrated.",
            "Suck on lozenges or hard candy to soothe the throat.",
            "Rest your voice and avoid irritants like smoke.",
        ],
        "see_doctor": "Consult a doctor for severe pain, difficulty breathing "
                      "or swallowing, or white patches on the tonsils.",
        "urgency": "low",
    },
    "body_pain": {
        "keywords": ["body pain", "body ache", "muscle pain", "joint pain",
                     "weakness", "fatigue", "tired"],
        "condition": "Body Ache / Fatigue",
        "info": "Generalised body aches and tiredness often accompany viral "
                "infections, overexertion, stress, or poor sleep.",
        "advice": [
            "Get adequate rest and good quality sleep.",
            "Stay hydrated and eat balanced, nutritious meals.",
            "Gentle stretching or a warm bath can relieve muscle aches.",
            "Manage stress with breaks and relaxation.",
        ],
        "see_doctor": "See a doctor if the pain is severe, localised to one "
                      "area, or comes with swelling, fever, or weight loss.",
        "urgency": "low",
    },
    "blood_pressure": {
        "keywords": ["blood pressure", "bp", "hypertension", "high bp"],
        "condition": "Blood Pressure",
        "info": "Normal blood pressure is around 120/80 mmHg. Consistently high "
                "readings (hypertension) increase the risk of heart disease.",
        "advice": [
            "Reduce salt intake and eat more fruits and vegetables.",
            "Exercise regularly - even 30 minutes of walking helps.",
            "Limit alcohol and avoid smoking.",
            "Manage stress and get your BP checked regularly.",
        ],
        "see_doctor": "If readings are consistently above 140/90, or you feel "
                      "chest pain, severe headache, or dizziness, see a doctor.",
        "urgency": "moderate",
    },
    "diabetes": {
        "keywords": ["diabetes", "sugar", "blood sugar", "glucose"],
        "condition": "Diabetes / Blood Sugar",
        "info": "Diabetes is a condition where blood sugar levels are too high. "
                "It is managed with diet, exercise, and sometimes medication.",
        "advice": [
            "Eat balanced meals; limit sugary foods and refined carbs.",
            "Exercise regularly to help control blood sugar.",
            "Monitor your blood sugar as advised by your doctor.",
            "Maintain a healthy weight and stay hydrated.",
        ],
        "see_doctor": "See a doctor for proper testing and a management plan. "
                      "Seek urgent care for confusion, fruity breath, or "
                      "very high/low sugar readings.",
        "urgency": "moderate",
    },
}

# Symptoms that need IMMEDIATE attention - safety always comes first.
EMERGENCY_KEYWORDS = [
    "chest pain", "heart attack", "can't breathe", "cant breathe",
    "difficulty breathing", "unconscious", "severe bleeding", "stroke",
    "suicide", "seizure", "choking", "overdose", "not breathing",
]

GREETINGS = ["hi", "hello", "hey", "hii", "good morning", "good evening",
             "good afternoon", "namaste", "hola"]

THANKS = ["thank", "thanks", "thx", "thank you", "appreciate"]

GENERAL_TIPS = [
    "Drink at least 8 glasses of water a day to stay hydrated.",
    "Aim for 7-8 hours of quality sleep every night.",
    "A 30-minute daily walk greatly improves overall health.",
    "Wash your hands regularly to prevent infections.",
    "Include fruits and vegetables in every meal.",
    "Take short breaks from screens to protect your eyes.",
]
