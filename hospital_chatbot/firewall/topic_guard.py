"""
firewall/topic_guard.py — Layer 2: Topic Relevance Guard
=========================================================
Ensures the question is related to the hospital / medical domain.
Uses keyword matching + intent scoring. No API calls.

Scoring system:
  - Each medical/hospital keyword found adds to the relevance score
  - If total score >= threshold → ALLOWED
  - If total score <  threshold → BLOCKED as off-topic

Also maintains a hard-block list for clearly irrelevant domains
(coding, politics, entertainment, etc.)
"""

import re
from typing import Tuple


# ── High-value medical / hospital keywords (2 points each) ────────
HIGH_VALUE_KEYWORDS = [
    # Hospital operations
    "opd", "appointment", "doctor", "hospital", "clinic", "ward",
    "admission", "discharge", "consultation", "emergency", "ambulance",
    "icu", "nicu", "operation", "surgery", "theatre",

    # Medical general
    "medicine", "medication", "prescription", "diagnosis", "treatment",
    "disease", "symptom", "pain", "fever", "infection", "injury",
    "patient", "nurse", "specialist", "physiotherapy", "therapy",

    # Body systems
    "heart", "lung", "liver", "kidney", "brain", "blood", "bone",
    "spine", "stomach", "cancer", "tumor", "diabetes", "thyroid",
    "pressure", "cholesterol", "glucose", "insulin",

    # Hospital services
    "xray", "x-ray", "mri", "ct scan", "ultrasound", "ecg", "echo",
    "lab", "test", "report", "pathology", "radiology", "pharmacy",
    "medicine", "drug", "vaccination", "vaccine",

    # Fees & admin
    "fee", "fees", "charge", "cost", "price", "rate", "bill",
    "insurance", "cashless", "tpa", "claim", "package",
    "timing", "timings", "time", "hours", "schedule", "open",

    # Departments
    "cardiology", "neurology", "orthopedic", "pediatric", "gynecology",
    "oncology", "urology", "dermatology", "psychiatry", "endocrinology",
    "pulmonology", "gastroenterology", "nephrology", "ophthalmology",
    "ent", "dental", "physiotherapy",

    # Conditions (common queries)
    "hypertension", "asthma", "arthritis", "fracture", "stroke",
    "pregnancy", "delivery", "maternity", "newborn", "child",
    "allergy", "cold", "cough", "headache", "migraine", "obesity",
    "anemia", "jaundice", "dengue", "malaria", "typhoid", "covid",
    "dialysis", "transplant", "bypass", "cataract", "hernia",
]

# ── Medium-value contextual words (1 point each) ──────────────────
MEDIUM_VALUE_KEYWORDS = [
    "help", "need", "want", "know", "find", "get", "book", "visit",
    "see", "meet", "call", "contact", "available", "near", "health",
    "body", "check", "scan", "result", "follow", "up", "problem",
    "issue", "concern", "advice", "suggest", "recommend", "tell",
    "what", "when", "where", "how", "which", "who", "why",
    "can", "should", "would", "could", "please", "thank",
]

# ── Hard-block domains — clearly not hospital related ─────────────
OFF_TOPIC_DOMAINS = [
    # Tech / coding
    r'\b(python|javascript|coding|programming|algorithm|github|sql|'
    r'machine learning|neural network|api|software|app|debug|code)\b',

    # Politics / news
    r'\b(election|parliament|government|minister|politics|president|'
    r'prime minister|modi|congress|bjp|vote|protest)\b',

    # Entertainment
    r'\b(movie|film|song|music|actor|actress|cricket|football|ipl|'
    r'netflix|youtube|instagram|tiktok|game|gaming|chess|sport)\b',

    # Finance (non-medical)
    r'\b(stock|share|market|crypto|bitcoin|investment|mutual fund|'
    r'loan|emi|tax|gst|income)\b',

    # Food / lifestyle (non-medical)
    r'\b(recipe|cooking|restaurant|hotel|travel|tour|flight|visa|'
    r'shopping|fashion|clothes|makeup)\b',

    # Harmful / clearly irrelevant
    r'\b(hack|exploit|crack|cheat|steal|illegal|weapon|gun|bomb|'
    r'drugs deal|smuggle|trafficking)\b',
]

# ── Minimum score to pass ──────────────────────────────────────────
RELEVANCE_THRESHOLD = 2


class TopicGuard:

    def check(self, text: str) -> Tuple[bool, str]:
        text_lower = text.lower()

        # ── Hard block off-topic domains first ────────────────────
        for pattern in OFF_TOPIC_DOMAINS:
            if re.search(pattern, text_lower):
                return (False,
                        "I'm a hospital assistant and can only help with "
                        "medical and hospital-related questions. "
                        "Please ask about appointments, doctors, fees, "
                        "timings, or health conditions.")

        # ── Score relevance ───────────────────────────────────────
        score = 0

        for keyword in HIGH_VALUE_KEYWORDS:
            if keyword in text_lower:
                score += 2

        for keyword in MEDIUM_VALUE_KEYWORDS:
            if keyword in text_lower:
                score += 1

        # Short questions like "OPD?" or "fees?" are valid
        # Give bonus for very short focused queries
        word_count = len(text_lower.split())
        if word_count <= 5 and score >= 2:
            score += 2   # short focused medical query bonus

        if score >= RELEVANCE_THRESHOLD:
            return True, ""

        return (False,
                "I can only assist with hospital and medical related questions. "
                "Please ask about our doctors, timings, fees, appointments, "
                "health packages, or medical conditions.")