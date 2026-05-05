"""
rag/symptom_checker.py — Symptom Checker & Triage Engine
=========================================================
Adds real medical value by:
  1. Detecting when user describes symptoms
  2. Running structured triage via Groq
  3. Returning: severity level, recommended department,
     relevant doctor, urgency flag, and follow-up questions

TRIAGE LEVELS:
  RED    — Go to Emergency immediately (life-threatening signals)
  YELLOW — Visit OPD within 24-48 hours (concerning but stable)
  GREEN  — Schedule routine appointment (non-urgent)

The symptom checker does NOT diagnose. It triages — routes the
patient to the right care level and department.

SYMPTOM DETECTION:
  Trigger phrases are detected first (lightweight regex).
  If triggered → full Groq triage analysis runs.
  If not triggered → normal RAG flow continues unchanged.
"""

import re, os, requests
from typing import Dict, Optional, Tuple

GROQ_API_BASE  = "https://api.groq.com/openai/v1/chat/completions"
TRIAGE_MODEL   = "llama-3.3-70b-versatile"   # Best model for medical reasoning

# ── Symptom trigger detection patterns ─────────────────────
SYMPTOM_TRIGGERS = [
    r'\bi\s+(have|am\s+having|feel|am\s+feeling|am\s+experiencing|got|'
    r'notice|suffer)\b',
    r'\bmy\s+(chest|head|stomach|back|leg|arm|eye|ear|throat|heart|'
    r'breathing|pain|ache|fever|cough)\b',
    r'\b(hurts?|aching|burning|swollen|numb|dizzy|nausea|vomiting|'
    r'bleeding|rash|itching|fatigue|weakness|shortness)\b',
    r'\b(since\s+\d+\s+days?|for\s+\d+\s+days?|past\s+\d+\s+days?)\b',
    r'\b(high\s+fever|chest\s+pain|difficulty\s+breathing|can\'t\s+breathe|'
    r'unconscious|seizure|stroke|paralysis)\b',
    r'\bsymptoms?\b',
    r'\bi\s+am\s+(sick|unwell|ill|not\s+feeling\s+well)\b',
]

# ── Emergency red-flag patterns (instant RED triage) ────────
EMERGENCY_PATTERNS = [
    r'\b(chest\s+pain|heart\s+attack|stroke|can\'t\s+breathe|'
    r'difficulty\s+breathing|unconscious|seizure|paralysis|'
    r'severe\s+bleeding|coughing\s+blood|vomiting\s+blood|'
    r'sudden\s+severe\s+headache|loss\s+of\s+consciousness)\b',
]

# ── Hospital department mapping (for triage recommendations) ─
DEPT_MAP = {
    "cardiology"      : {"name": "Cardiology",       "phone": "Ext: 201"},
    "neurology"       : {"name": "Neurology",         "phone": "Ext: 202"},
    "orthopedics"     : {"name": "Orthopedics",       "phone": "Ext: 203"},
    "general medicine": {"name": "General Medicine",  "phone": "Ext: 204"},
    "gastroenterology": {"name": "Gastroenterology",  "phone": "Ext: 205"},
    "pulmonology"     : {"name": "Pulmonology",       "phone": "Ext: 206"},
    "endocrinology"   : {"name": "Endocrinology",     "phone": "Ext: 207"},
    "psychiatry"      : {"name": "Psychiatry",        "phone": "Ext: 208"},
    "dermatology"     : {"name": "Dermatology",       "phone": "Ext: 209"},
    "ent"             : {"name": "ENT",               "phone": "Ext: 210"},
    "ophthalmology"   : {"name": "Ophthalmology",     "phone": "Ext: 211"},
    "urology"         : {"name": "Urology",           "phone": "Ext: 212"},
    "emergency"       : {"name": "Emergency",         "phone": "108 / Gate 2"},
}


class SymptomChecker:
    def __init__(self, groq_api_key: str = ""):
        self.api_key = groq_api_key
        self.enabled = bool(groq_api_key)
        if self.enabled:
            print(f"  ✅ Symptom Checker enabled (model: {TRIAGE_MODEL})")
        else:
            print("  ⚠️  Symptom Checker disabled (no GROQ_API_KEY)")

    def is_symptom_query(self, text: str) -> bool:
        """Quick check: does this message describe symptoms?"""
        text_lower = text.lower()
        return any(
            re.search(p, text_lower, re.IGNORECASE)
            for p in SYMPTOM_TRIGGERS
        )

    def is_emergency(self, text: str) -> bool:
        """Check for life-threatening red flags."""
        text_lower = text.lower()
        return any(
            re.search(p, text_lower, re.IGNORECASE)
            for p in EMERGENCY_PATTERNS
        )

    def triage(self, symptom_text: str,
               entities: Dict = None) -> Optional[Dict]:
        """
        Run full triage analysis via Groq.
        Returns triage result dict or None if disabled/failed.

        Result format:
        {
          "severity"    : "RED" | "YELLOW" | "GREEN",
          "department"  : "Cardiology",
          "urgency"     : "Immediate" | "Within 24h" | "Routine",
          "summary"     : "Brief clinical summary",
          "advice"      : "What patient should do now",
          "followup_q"  : "One clarifying question to ask",
          "disclaimer"  : standard disclaimer
        }
        """
        if not self.enabled:
            return None

        # Instant emergency check (no API needed)
        if self.is_emergency(symptom_text):
            return {
                "severity"  : "RED",
                "department": "Emergency",
                "urgency"   : "Immediate — call 108 NOW",
                "summary"   : "Potential life-threatening symptoms detected.",
                "advice"    : (
                    "Please call 108 or go to our Emergency Department "
                    "(Gate 2, open 24/7) immediately. Do not wait."
                ),
                "followup_q": None,
                "disclaimer": self._disclaimer(),
            }

        # Entity context (doctor/department already mentioned)
        context_hint = ""
        if entities:
            if "disease" in entities:
                context_hint = f"Known condition: {entities['disease']}. "
            if "department" in entities:
                context_hint += f"Previously mentioned dept: {entities['department']}."

        prompt = f"""You are a medical triage assistant for City General Hospital.
A patient describes symptoms. Analyze and provide structured triage guidance.

Patient message: "{symptom_text}"
{context_hint}

Respond in this EXACT format (fill in each field):
SEVERITY: [RED/YELLOW/GREEN]
DEPARTMENT: [most relevant department name]
URGENCY: [Immediate/Within 24 hours/Routine appointment]
SUMMARY: [1 sentence clinical summary of likely concern]
ADVICE: [1-2 sentences: what patient should do right now]
FOLLOWUP: [One important clarifying question to ask the patient]

Rules:
- RED only for potentially life-threatening conditions
- GREEN for minor/chronic/non-urgent concerns
- DEPARTMENT must be one of: Emergency, Cardiology, Neurology, Orthopedics,
  General Medicine, Gastroenterology, Pulmonology, Endocrinology, Psychiatry,
  Dermatology, ENT, Ophthalmology, Urology, Gynecology
- NEVER diagnose — only suggest appropriate care pathway
- Keep ADVICE under 40 words"""

        try:
            r = requests.post(
                GROQ_API_BASE,
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type" : "application/json",
                },
                json={
                    "model"      : TRIAGE_MODEL,
                    "messages"   : [{"role": "user", "content": prompt}],
                    "temperature": 0.2,
                    "max_tokens" : 250,
                    "stream"     : False,
                },
                timeout=15,
            )
            if r.status_code == 200:
                content = (
                    r.json()
                    .get("choices", [{}])[0]
                    .get("message", {})
                    .get("content", "")
                )
                parsed = self._parse_triage(content)
                if parsed:
                    parsed["disclaimer"] = self._disclaimer()
                    return parsed

        except Exception as e:
            print(f"  Triage error: {e}")

        return None

    def _parse_triage(self, text: str) -> Optional[Dict]:
        """Parse structured triage response."""
        result = {}
        fields = {
            "severity"  : r'SEVERITY\s*:\s*(.+)',
            "department": r'DEPARTMENT\s*:\s*(.+)',
            "urgency"   : r'URGENCY\s*:\s*(.+)',
            "summary"   : r'SUMMARY\s*:\s*(.+)',
            "advice"    : r'ADVICE\s*:\s*(.+)',
            "followup_q": r'FOLLOWUP\s*:\s*(.+)',
        }
        for key, pattern in fields.items():
            m = re.search(pattern, text, re.IGNORECASE)
            result[key] = m.group(1).strip() if m else ""

        return result if result.get("severity") else None

    def format_triage_response(self, triage: Dict,
                                hospital_info: str = "") -> str:
        """Format triage result into a user-friendly response."""
        severity = triage.get("severity", "GREEN").upper()
        dept     = triage.get("department", "General Medicine")
        urgency  = triage.get("urgency", "Routine appointment")
        summary  = triage.get("summary", "")
        advice   = triage.get("advice", "")
        followup = triage.get("followup_q", "")
        disclaim = triage.get("disclaimer", "")

        # Severity emoji and color indicator
        severity_display = {
            "RED"   : "🔴 HIGH PRIORITY",
            "YELLOW": "🟡 MODERATE",
            "GREEN" : "🟢 ROUTINE",
        }.get(severity, "🟢 ROUTINE")

        lines = [
            f"**Triage Assessment: {severity_display}**",
            f"",
            f"**{summary}**",
            f"",
            f"📍 **Recommended Department:** {dept}",
            f"⏱️ **Urgency:** {urgency}",
            f"",
            f"**What to do:** {advice}",
        ]

        if hospital_info:
            lines += ["", hospital_info]

        if followup:
            lines += ["", f"💬 *To help you better: {followup}*"]

        lines += ["", f"_{disclaim}_"]
        return "\n".join(lines)

    def _disclaimer(self) -> str:
        return (
            "This is a preliminary triage guide only, not a medical diagnosis. "
            "Please consult a qualified doctor for proper evaluation and treatment."
        )