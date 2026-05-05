"""
firewall/content_filter.py — Layer 4: Sensitive Content Detection
==================================================================
Handles medically and ethically sensitive content appropriately.

Unlike other layers that simply block, this layer has THREE outcomes:
  1. BLOCK   — harmful request, do not process
  2. REDIRECT— user may be in distress, respond with care + resources
  3. ALLOW   — safe to continue

Categories handled:
  A. Self-harm / suicidal ideation     → REDIRECT to crisis resources
  B. Drug abuse / dangerous doses      → BLOCK
  C. Requests to harm others           → BLOCK
  D. Explicit prescription requests    → BLOCK (legal + safety)
  E. Privacy violation attempts        → BLOCK
  F. Fake emergency manipulation       → WARN + ALLOW with note
  G. Child safety concerns             → REDIRECT
"""

import re
from typing import Tuple


CRISIS_RESPONSE = (
    "I noticed your message may indicate you're going through a difficult time. "
    "Please know that help is available right now.\n\n"
    "🆘 **Crisis Helpline (India):** iCall — 9152987821\n"
    "🆘 **Vandrevala Foundation:** 1860-2662-345 (24/7)\n"
    "🆘 **Emergency:** 108\n\n"
    "Our hospital also has a Psychiatry & Counseling department. "
    "You can visit our OPD or call +1-800-HOSPITAL. "
    "You are not alone, and we are here to help."
)

CHILD_SAFETY_RESPONSE = (
    "If a child is in danger or needs urgent medical attention, "
    "please call our Emergency line at 108 immediately.\n\n"
    "Child helpline: 1098 (CHILDLINE India — free, 24/7)\n"
    "Our Pediatrics department is available for all child health concerns."
)


# ── Self-harm / crisis detection ──────────────────────────────────
CRISIS_PATTERNS = [
    r'\b(want\s+to|going\s+to|planning\s+to|thinking\s+about)\s+'
    r'(kill|end|hurt)\s+(my)?self\b',

    r'\b(suicid(e|al)|self[\s-]harm|self[\s-]hurt|cut\s+myself|'
    r'overdos(e|ing)|end\s+my\s+life|take\s+my\s+life)\b',

    r'\b(no\s+reason\s+to\s+live|want\s+to\s+die|better\s+off\s+dead|'
    r'not\s+worth\s+living|life\s+is\s+not\s+worth)\b',

    r'\b(how\s+to\s+(commit|attempt)\s+suicide|lethal\s+dose\s+of|'
    r'how\s+many\s+pills\s+to\s+die)\b',
]

# ── Dangerous / illegal drug requests ─────────────────────────────
DRUG_ABUSE_PATTERNS = [
    r'\b(how\s+to\s+(get\s+high|get\s+stoned|abuse|misuse)\s+(on\s+)?'
    r'(medication|medicine|drugs?|pills?))\b',

    r'\b(recreational\s+use\s+of|abuse\s+of)\s+\w+\b',

    r'\b(morphine|fentanyl|oxycodone|hydrocodone|codeine|tramadol|'
    r'alprazolam|diazepam|clonazepam)\s+'
    r'(without\s+prescription|illegally|to\s+get\s+high)\b',

    r'\bblack\s+market\s+(drugs?|medicine|medication)\b',
    r'\bbuy\s+(drugs?|medication)\s+(without|no)\s+prescription\b',
    r'\bsmuggl(e|ing)\s+(drugs?|medication)\b',
]

# ── Harm to others ─────────────────────────────────────────────────
HARM_OTHERS_PATTERNS = [
    r'\b(how\s+to\s+)(poison|drug|hurt|harm|kill|injure)\s+'
    r'(someone|a\s+person|my\s+\w+|another\s+person|people)\b',

    r'\b(undetectable\s+poison|poison\s+someone|drug\s+someone\'?s?\s+'
    r'(food|drink|water))\b',

    r'\blethal\s+(dose|amount|injection)\s+(for|to\s+kill)\b',
]

# ── Explicit / illegal prescription requests ──────────────────────
PRESCRIPTION_PATTERNS = [
    r'\b(write|give|provide|issue)\s+(me\s+)?(a\s+)?prescription\b',
    r'\bprescribe\s+(me|for\s+me)\b',
    r'\bi\s+need\s+a\s+prescription\s+(for|without)\b',
    r'\bforged?\s+prescription\b',
    r'\bfake\s+prescription\b',
    r'\bprescription\s+without\s+(seeing|visiting|consulting)\b',
]

# ── Privacy violation ──────────────────────────────────────────────
PRIVACY_PATTERNS = [
    r'\b(give\s+me|show\s+me|access|find|get)\s+'
    r'(patient\s+records?|medical\s+records?|private\s+data|'
    r'confidential\s+(data|information)|personal\s+health\s+information)\b',

    r'\bhack\s+(into\s+)?(the\s+)?(hospital|patient|medical|database|system)\b',
    r'\baccess\s+other\s+patients?\s+(data|records?|information)\b',
    r'\badmin\s+(password|credentials|access|login)\b',
]

# ── Child safety ───────────────────────────────────────────────────
CHILD_SAFETY_PATTERNS = [
    r'\bchild\s+(abuse|abused|being\s+hurt|in\s+danger|unsafe)\b',
    r'\ba\s+child\s+(was|is|has\s+been)\s+(hurt|abused|attacked|harmed)\b',
    r'\bmy\s+(kid|child|son|daughter|baby)\s+(is\s+)?(missing|taken|kidnapped|abused)\b',
]


class ContentFilter:

    def check(self, text: str) -> Tuple[bool, str, str]:
        """
        Returns (is_allowed, message, action).
        action: 'allow' | 'block' | 'redirect'
        """
        text_lower = text.lower()

        # ── Crisis / self-harm → REDIRECT ─────────────────────────
        for pattern in CRISIS_PATTERNS:
            if re.search(pattern, text_lower, re.IGNORECASE):
                return False, CRISIS_RESPONSE, "redirect"

        # ── Child safety → REDIRECT ────────────────────────────────
        for pattern in CHILD_SAFETY_PATTERNS:
            if re.search(pattern, text_lower, re.IGNORECASE):
                return False, CHILD_SAFETY_RESPONSE, "redirect"

        # ── Harm to others → BLOCK ────────────────────────────────
        for pattern in HARM_OTHERS_PATTERNS:
            if re.search(pattern, text_lower, re.IGNORECASE):
                return (False,
                        "I cannot assist with that request. "
                        "If there is a medical emergency, please call 108 immediately.",
                        "block")

        # ── Drug abuse → BLOCK ────────────────────────────────────
        for pattern in DRUG_ABUSE_PATTERNS:
            if re.search(pattern, text_lower, re.IGNORECASE):
                return (False,
                        "I'm not able to help with that. "
                        "If you are struggling with substance use, our hospital has a "
                        "De-addiction program. Call +1-800-HOSPITAL for confidential support.",
                        "block")

        # ── Illegal prescription → BLOCK ──────────────────────────
        for pattern in PRESCRIPTION_PATTERNS:
            if re.search(pattern, text_lower, re.IGNORECASE):
                return (False,
                        "I cannot issue prescriptions. Only a licensed doctor can prescribe "
                        "medication after a consultation. Please book an appointment with one "
                        "of our doctors through the hospital.",
                        "block")

        # ── Privacy violations → BLOCK ────────────────────────────
        for pattern in PRIVACY_PATTERNS:
            if re.search(pattern, text_lower, re.IGNORECASE):
                return (False,
                        "I cannot provide access to patient records or confidential data. "
                        "For your own records, please visit the Medical Records department "
                        "with valid ID proof.",
                        "block")

        return True, "", "allow"