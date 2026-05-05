"""
rag/memory.py — Summarized + Entity Memory
===========================================
Replaces simple history.py with intelligent memory that:

  1. ENTITY MEMORY — extracts and tracks named entities across turns
     "I have an appointment with Dr. Sharma on Monday"
     → stores: {doctor: "Dr. Sharma", day: "Monday"}
     → later "What floor is his OPD?" → knows "his" = Dr. Sharma

  2. SUMMARIZED MEMORY — after every 6 turns, summarize conversation
     Instead of sending all 6 turns raw (wastes tokens), send a
     compact summary + last 2 turns (saves ~60% of history tokens)

  3. TURN BUFFER — keeps raw last 2 turns always (for immediate context)

MEMORY STRUCTURE per session:
  {
    "turns"     : [...],          # raw turn buffer (last 2)
    "summary"   : "...",          # rolling summary of older turns
    "entities"  : {               # extracted entities
        "doctor"     : "Dr. Sharma",
        "department" : "Cardiology",
        "disease"    : "diabetes",
        "day"        : "Monday",
        "fee_asked"  : True,
    },
    "turn_count": 12,             # total turns so far
  }
"""

import os, re, requests
from collections import defaultdict
from typing import List, Dict, Optional

GROQ_API_BASE = "https://api.groq.com/openai/v1/chat/completions"
SUMMARY_MODEL = "llama-3.1-8b-instant"
SUMMARIZE_EVERY = 6   # summarize after every 6 turns


# ── Hospital-domain entity patterns ──────────────────────────
ENTITY_PATTERNS = {
    "doctor"      : r'\bdr\.?\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)?)',
    "department"  : r'\b(cardiology|neurology|orthopedic|pediatric|gynecology|'
                    r'oncology|urology|dermatology|psychiatry|endocrinology|'
                    r'pulmonology|gastroenterology|nephrology|ophthalmology|'
                    r'ent|dental|general medicine|general surgery)\b',
    "disease"     : r'\b(diabetes|hypertension|cancer|stroke|asthma|arthritis|'
                    r'fracture|pregnancy|anemia|jaundice|dengue|malaria|'
                    r'typhoid|covid|dialysis|thyroid|depression|anxiety)\b',
    "day"         : r'\b(monday|tuesday|wednesday|thursday|friday|saturday|sunday|'
                    r'today|tomorrow|this week)\b',
    "time"        : r'\b(\d{1,2}(?::\d{2})?\s*(?:am|pm))\b',
    "test"        : r'\b(mri|ct scan|x-?ray|ultrasound|ecg|echo|blood test|'
                    r'urine test|biopsy|endoscopy)\b',
}


class SmartMemory:
    def __init__(self, groq_api_key: str = ""):
        self.api_key = groq_api_key
        self._store: Dict[str, Dict] = defaultdict(lambda: {
            "turns"     : [],
            "summary"   : "",
            "entities"  : {},
            "turn_count": 0,
        })

    # ── Public API ───────────────────────────────────────────

    def add(self, session_id: str, user_msg: str, bot_msg: str):
        """Record a completed conversation turn."""
        mem = self._store[session_id]

        # Extract entities from user message
        self._extract_entities(user_msg, mem["entities"])

        # Add to turn buffer
        mem["turns"].append({"user": user_msg, "bot": bot_msg})
        mem["turn_count"] += 1

        # Summarize when buffer fills up
        if len(mem["turns"]) >= SUMMARIZE_EVERY:
            self._summarize(session_id)

    def get_context(self, session_id: str) -> str:
        """
        Build the memory context string to inject into the prompt.
        Format:
          [Entity Memory]
          Doctor: Dr. Sharma | Department: Cardiology | ...

          [Conversation Summary]
          Patient asked about ... Bot explained ...

          [Recent Turns]
          Patient: ...
          Assistant: ...
        """
        mem      = self._store[session_id]
        parts    = []

        # Entity memory
        if mem["entities"]:
            entity_str = " | ".join(
                f"{k.title()}: {v}"
                for k, v in mem["entities"].items()
                if v
            )
            parts.append(f"[Patient Context]\n{entity_str}")

        # Rolling summary
        if mem["summary"]:
            parts.append(f"[Conversation Summary]\n{mem['summary']}")

        # Last 2 raw turns
        recent = mem["turns"][-2:] if mem["turns"] else []
        if recent:
            recent_text = "\n".join([
                f"Patient: {t['user']}\nAssistant: {t['bot']}"
                for t in recent
            ])
            parts.append(f"[Recent Exchange]\n{recent_text}")

        return "\n\n".join(parts) if parts else ""

    def get_recent_turns(self, session_id: str,
                         last_n: int = 6) -> List[Dict]:
        """Backward-compat method for pipeline history access."""
        return self._store[session_id]["turns"][-last_n:]

    def get_entities(self, session_id: str) -> Dict:
        return dict(self._store[session_id]["entities"])

    def clear(self, session_id: str):
        self._store[session_id] = {
            "turns": [], "summary": "",
            "entities": {}, "turn_count": 0
        }

    # ── Internal helpers ─────────────────────────────────────

    def _extract_entities(self, text: str, entities: Dict):
        """Extract hospital-domain entities from user message."""
        text_lower = text.lower()
        for entity_type, pattern in ENTITY_PATTERNS.items():
            match = re.search(pattern, text_lower, re.IGNORECASE)
            if match:
                # Doctor name needs title case
                value = match.group(1) if entity_type == "doctor" \
                        else match.group(0)
                entities[entity_type] = value.strip().title()

    def _summarize(self, session_id: str):
        """
        Summarize the current turn buffer into rolling summary.
        Uses Groq if available, otherwise creates a simple text summary.
        """
        mem       = self._store[session_id]
        turns     = mem["turns"]
        old_summ  = mem["summary"]

        # Build text of turns to summarize
        turns_text = "\n".join([
            f"Patient: {t['user']}\nAssistant: {t['bot']}"
            for t in turns
        ])

        if self.api_key:
            summary = self._groq_summarize(turns_text, old_summ)
        else:
            summary = self._simple_summarize(turns, old_summ)

        mem["summary"] = summary
        # Keep only last 2 turns in buffer after summarizing
        mem["turns"]   = turns[-2:]

    def _groq_summarize(self, turns_text: str, prev_summary: str) -> str:
        """Use Groq to produce a concise rolling summary."""
        prev_part = (f"Previous summary: {prev_summary}\n\n"
                     if prev_summary else "")
        prompt = (
            f"{prev_part}"
            f"New conversation turns:\n{turns_text}\n\n"
            "Write a 2-3 sentence summary of what the patient asked and "
            "what information was provided. Focus on medical topics, "
            "doctor names, departments, fees, and any decisions made. "
            "Be concise."
        )
        try:
            r = requests.post(
                GROQ_API_BASE,
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type" : "application/json",
                },
                json={
                    "model"      : SUMMARY_MODEL,
                    "messages"   : [{"role": "user", "content": prompt}],
                    "temperature": 0.3,
                    "max_tokens" : 150,
                    "stream"     : False,
                },
                timeout=10,
            )
            if r.status_code == 200:
                return (r.json()
                          .get("choices", [{}])[0]
                          .get("message", {})
                          .get("content", "")
                          .strip())
        except Exception:
            pass
        return self._simple_summarize([], prev_summary)

    def _simple_summarize(self, turns: List[Dict],
                           prev: str) -> str:
        """Fallback: extract first sentence of each user turn."""
        sentences = []
        for t in turns[-4:]:
            first = t["user"].split(".")[0][:80]
            sentences.append(f"Asked about: {first}")
        new_part = ". ".join(sentences)
        if prev and new_part:
            return f"{prev}. {new_part}"
        return prev or new_part