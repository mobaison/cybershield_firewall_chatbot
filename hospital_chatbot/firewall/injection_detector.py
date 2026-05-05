"""
firewall/injection_detector.py — Layer 3: Prompt Injection Detection
======================================================================
Detects attempts to hijack, override, or manipulate the system prompt.

Attack categories detected:
  1. Direct override commands     ("ignore previous instructions")
  2. Role hijacking               ("you are now DAN / act as")
  3. Jailbreak patterns           ("pretend you have no limits")
  4. Context manipulation         ("forget everything above")
  5. System prompt extraction     ("what are your instructions?")
  6. Delimiter injection          ("### END SYSTEM PROMPT ###")
  7. Encoding attacks             (base64 encoded instructions)
  8. Indirect injection           ("my friend says you should...")
  9. Persona switching            ("from now on respond as")
 10. Hospital-specific bypasses   ("as a doctor you must tell me")

Each pattern has a severity: HIGH blocks immediately, MEDIUM accumulates.
If total MEDIUM score >= threshold → also blocked.
"""

import re
import base64
from typing import Tuple


# ── HIGH severity — block on any single match ─────────────────────
HIGH_SEVERITY_PATTERNS = [

    # Direct instruction overrides
    r'ignore\s+(all\s+)?(previous|prior|above|earlier|your)\s+'
    r'(instructions?|prompts?|rules?|guidelines?|training|context)',

    r'disregard\s+(all\s+)?(previous|prior|above|your)\s+'
    r'(instructions?|prompts?|rules?|guidelines?)',

    r'forget\s+(all\s+)?(previous|prior|above|your|everything)',

    r'(override|overwrite|replace|reset)\s+(your\s+)?(instructions?|'
    r'system\s+prompt|programming|training|rules?|guidelines?)',

    # Role hijacking — DAN and variants
    r'\bdan\b.*\b(mode|prompt|jailbreak|personality)',
    r'do\s+anything\s+now',
    r'jailbreak',
    r'jail\s*break',

    # Persona replacement
    r'you\s+are\s+now\s+(a\s+)?(different|new|another|evil|unrestricted)',
    r'(act|pretend|behave|respond|imagine)\s+(as\s+if|like|as|that)\s+'
    r'you\s+(are|have|were|had)\s+(no\s+)?(restrictions?|limits?|rules?|'
    r'guidelines?|training|filter)',

    r'from\s+now\s+on\s+(you\s+are|act\s+as|pretend|ignore|forget)',
    r'new\s+persona',
    r'switch\s+(to\s+)?persona',

    # System prompt manipulation
    r'\[system\]',
    r'<system>',
    r'###\s*(system|instruction|prompt|end)',
    r'\[\[.*instructions.*\]\]',
    r'begin\s+new\s+system\s+prompt',
    r'(end|stop|close)\s+(of\s+)?(system\s+)?(prompt|instructions?)',

    # Extraction attacks
    r'(reveal|show|print|output|display|repeat|tell\s+me)\s+'
    r'(your\s+)?(system\s+prompt|instructions?|prompt|rules?|guidelines?|'
    r'training\s+data)',

    r'what\s+(are|is)\s+your\s+(system\s+prompt|instructions?|'
    r'original\s+prompt|base\s+prompt|hidden\s+prompt)',

    # Training manipulation
    r'you\s+(were|are)\s+(trained|programmed|designed)\s+(to|by)',
    r'your\s+(training|programming|base\s+model)',

    # Direct harmful bypasses
    r'(pretend|imagine|suppose|assume)\s+(there\s+are\s+no|you\s+have\s+no)\s+'
    r'(restrictions?|limits?|rules?|guidelines?|filters?)',

    r'in\s+(a\s+)?(fictional|hypothetical|imaginary|alternate)\s+'
    r'(world|universe|scenario|context|setting).*'
    r'(no\s+restrictions?|anything\s+goes|no\s+rules?)',

    # Injection delimiters
    r'----+\s*(system|instruction|prompt)',
    r'====+\s*(system|instruction|prompt)',
    r'\*\*\*+\s*(system|instruction|prompt)',
]

# ── MEDIUM severity — accumulate score ────────────────────────────
MEDIUM_SEVERITY_PATTERNS = [
    # Indirect persona hints
    (r'\bact\s+as\b', 1),
    (r'\bpretend\s+(to\s+be|you\s+are)\b', 1),
    (r'\bimagine\s+you\s+are\b', 1),
    (r'\bbehave\s+as\b', 1),
    (r'\brespond\s+as\b', 1),
    (r'\byou\s+are\s+not\s+a\s+(bot|ai|assistant|chatbot)\b', 2),
    (r'\byou\s+are\s+a\s+(human|person|real\s+doctor)\b', 1),

    # Limit probing
    (r'\bno\s+(restrictions?|limits?|filters?|rules?)\b', 2),
    (r'\bunrestricted\b', 2),
    (r'\bunfiltered\b', 2),
    (r'\buncensored\b', 2),
    (r'\bwithout\s+(any\s+)?(restrictions?|limits?|filters?)\b', 2),

    # Indirect injection framing
    (r'\bmy\s+(friend|colleague|doctor|nurse)\s+says\s+you\s+(should|must|can)\b', 1),
    (r'\bi\s+was\s+told\s+you\s+can\b', 1),
    (r'\bpreviously\s+you\s+(said|told|agreed)\b', 1),

    # Hypothetical framing
    (r'\bhypothetically\b', 1),
    (r'\btheoretically\b', 1),
    (r'\bjust\s+for\s+(fun|testing|research|educational\s+purposes)\b', 1),
    (r'\bwhat\s+if\s+you\s+(could|were\s+able\s+to|had\s+no)\b', 1),

    # Hospital-specific bypass attempts
    (r'\bas\s+a\s+(real\s+)?doctor\s+(you\s+)?(must|should|have\s+to)\b', 2),
    (r'\bprescribe\s+me\b', 1),
    (r'\btell\s+me\s+(the\s+)?exact\s+dose\b', 2),
    (r'\bmedical\s+advice\s+only\b', 1),
    (r'\byou\s+are\s+(a\s+)?(licensed|real|actual)\s+doctor\b', 2),
]

MEDIUM_BLOCK_THRESHOLD = 4   # block if medium score reaches this


class InjectionDetector:

    def check(self, text: str) -> Tuple[bool, str]:
        text_lower = text.lower()

        # ── Check high severity — instant block ───────────────────
        for pattern in HIGH_SEVERITY_PATTERNS:
            if re.search(pattern, text_lower, re.IGNORECASE | re.DOTALL):
                return (False,
                        "I detected an attempt to manipulate my instructions. "
                        "I'm here to help with hospital and medical questions only. "
                        "Please ask a genuine medical or hospital-related question.")

        # ── Check base64 encoded content ──────────────────────────
        # Attackers sometimes encode malicious prompts in base64
        words = text.split()
        for word in words:
            if len(word) > 20 and re.match(r'^[A-Za-z0-9+/]+=*$', word):
                try:
                    decoded = base64.b64decode(word).decode('utf-8', errors='ignore')
                    decoded_lower = decoded.lower()
                    for pattern in HIGH_SEVERITY_PATTERNS:
                        if re.search(pattern, decoded_lower, re.IGNORECASE):
                            return (False,
                                    "Encoded content detected. Please ask your "
                                    "question directly in plain text.")
                except Exception:
                    pass

        # ── Accumulate medium severity score ──────────────────────
        medium_score = 0
        for pattern, score in MEDIUM_SEVERITY_PATTERNS:
            if re.search(pattern, text_lower, re.IGNORECASE):
                medium_score += score

        if medium_score >= MEDIUM_BLOCK_THRESHOLD:
            return (False,
                    "Your message seems to be trying to alter my behavior. "
                    "I'm a hospital assistant and I'm here to help with "
                    "medical questions, doctor information, timings, and fees.")

        return True, ""