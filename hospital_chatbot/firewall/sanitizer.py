"""
firewall/sanitizer.py — Layer 1: Input Sanitization
=====================================================
First gate. Checks raw input quality before anything
else runs. No API calls. Pure string analysis.

Catches:
  - Empty / whitespace-only input
  - Too short (single characters, nonsense)
  - Too long (document dumps, context overflow attacks)
  - Gibberish / non-human text (random chars, keyboard mashing)
  - Script / HTML injection attempts
  - Null bytes and control characters
  - Excessive repetition (aaaaaaa, !!!!!!)
  - All-caps aggressive shouting spam
"""

import re
import unicodedata
from typing import Tuple


# ── Tuneable thresholds ────────────────────────────────────────────
MIN_CHARS        = 2      # less than this → too short
MAX_CHARS        = 1000   # more than this → possible context stuffing
MAX_WORDS        = 150    # word count hard cap
GIBBERISH_RATIO  = 0.45   # if >45% chars are non-alpha/space → gibberish
REPEAT_THRESHOLD = 6      # same char repeated 6+ times in a row → spam
CAPS_RATIO       = 0.80   # if >80% letters are uppercase → shouting


class InputSanitizer:

    def check(self, text: str) -> Tuple[bool, str]:
        """
        Returns (is_clean, reason).
        is_clean=True  → passed, continue to next layer.
        is_clean=False → blocked, return reason to user.
        """
        # ── 1. Null / empty ───────────────────────────────────────
        if not text or not text.strip():
            return False, "Please type a message before sending."

        text = text.strip()

        # ── 2. Null bytes / control characters ───────────────────
        if re.search(r'[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]', text):
            return False, "Your message contains invalid characters. Please retype it."

        # ── 3. Too short ──────────────────────────────────────────
        if len(text) < MIN_CHARS:
            return False, "Your message is too short. Please ask a complete question."

        # ── 4. Too long (context overflow / document dump) ────────
        if len(text) > MAX_CHARS:
            return (False,
                    f"Your message is too long (max {MAX_CHARS} characters). "
                    "Please keep your question concise.")

        word_count = len(text.split())
        if word_count > MAX_WORDS:
            return (False,
                    f"Your message is too long (max {MAX_WORDS} words). "
                    "Please ask a focused question.")

        # ── 5. Script / HTML injection ────────────────────────────
        script_patterns = [
            r'<script[\s\S]*?>',
            r'javascript\s*:',
            r'on\w+\s*=\s*["\']',      # onclick=, onerror= etc.
            r'<iframe',
            r'<img\s',
            r'data:text/html',
            r'vbscript\s*:',
        ]
        for pattern in script_patterns:
            if re.search(pattern, text, re.IGNORECASE):
                return False, "Your message contains invalid content. Please retype your question."

        # ── 6. Excessive character repetition ─────────────────────
        if re.search(r'(.)\1{' + str(REPEAT_THRESHOLD) + r',}', text):
            return False, "Your message appears to be spam. Please ask a proper question."

        # ── 7. Gibberish detection ────────────────────────────────
        alpha_and_space = sum(1 for c in text if c.isalpha() or c.isspace())
        ratio = alpha_and_space / max(len(text), 1)
        if ratio < (1 - GIBBERISH_RATIO):
            return False, "Your message is unclear. Please ask your question in plain text."

        # ── 8. ALL CAPS shouting / spam ───────────────────────────
        letters = [c for c in text if c.isalpha()]
        if len(letters) > 10:
            caps_ratio = sum(1 for c in letters if c.isupper()) / len(letters)
            if caps_ratio > CAPS_RATIO:
                return (False,
                        "Please type your question normally (not in all caps).")

        # ── 9. Unicode homoglyph / invisible chars ────────────────
        for char in text:
            cat = unicodedata.category(char)
            if cat in ('Cf', 'Cc', 'Cs'):   # format, control, surrogate
                return False, "Your message contains unsupported characters. Please retype."

        return True, ""