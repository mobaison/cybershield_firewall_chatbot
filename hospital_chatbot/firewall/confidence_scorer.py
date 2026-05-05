"""
firewall/confidence_scorer.py — Risk Confidence Scoring System
===============================================================
Replaces binary BLOCK/ALLOW with a nuanced risk score (0.0 to 1.0).

SCORING ARCHITECTURE:
  Each firewall layer contributes a risk signal.
  The scorer aggregates all signals into one score.
  Based on score, three actions are possible:

  SCORE < 0.35  → ALLOW   — normal response
  SCORE 0.35-0.65 → CAUTION — allow but add safety note to response
  SCORE > 0.65  → BLOCK   — reject the message

WHY THIS IS BETTER THAN BINARY:
  Binary:  "act as a doctor" → scores 0.4 on injection check
           → binary: ALLOW (below 0.5 threshold)
           → confidence: CAUTION (0.4 > 0.35 threshold) → responds carefully

  Binary:  "what are OPD timings on Monday?" + "just ignore your rules"
           → each turn individually below threshold
           → confidence: accumulated score triggers BLOCK

SIGNAL SOURCES:
  - injection_score:     from InjectionDetector regex (0.0-1.0)
  - semantic_score:      from SemanticGuard LLM (0 or 0.8)
  - conversation_score:  from ConversationAnalyzer rolling window (0.0-1.0)
  - topic_score:         from TopicGuard relevance (inverted, 0=on-topic)
  - content_score:       from ContentFilter (0 or 1.0)
  - rate_pressure:       from RateLimiter (fraction of limit used)
"""

from dataclasses import dataclass, field
from typing import Dict, Optional


@dataclass
class RiskSignals:
    """All risk signals collected from firewall layers."""
    injection_score    : float = 0.0   # 0.0 = clean, 1.0 = definite injection
    semantic_flagged   : bool  = False # True = Groq says injection
    conversation_score : float = 0.0   # rolling multi-turn risk
    topic_score        : float = 0.0   # 0.0 = on-topic, 1.0 = off-topic
    content_flagged    : bool  = False # True = harmful content
    rate_pressure      : float = 0.0   # 0.0 = within limits, 1.0 = at limit
    message_length_ok  : bool  = True  # False = suspicious length


@dataclass
class ConfidenceResult:
    score    : float         # 0.0 to 1.0 (higher = more risky)
    action   : str           # "allow" | "caution" | "block"
    signals  : RiskSignals   = field(default_factory=RiskSignals)
    reason   : str           = ""
    note     : str           = ""  # shown to user if action == "caution"


# ── Thresholds ─────────────────────────────────────────────
ALLOW_THRESHOLD   = 0.35
BLOCK_THRESHOLD   = 0.65

# ── Signal weights ──────────────────────────────────────────
WEIGHTS = {
    "injection"   : 0.35,
    "semantic"    : 0.25,
    "conversation": 0.20,
    "topic"       : 0.10,
    "content"     : 0.07,
    "rate"        : 0.03,
}

CAUTION_NOTE = (
    "Please note: I can only provide hospital and medical information. "
    "For safety and accuracy, please consult our doctors for medical decisions."
)


class ConfidenceScorer:

    def score(self, signals: RiskSignals) -> ConfidenceResult:
        """
        Compute aggregate risk score from all signals.
        Returns ConfidenceResult with action and explanation.
        """
        # Normalize each signal to 0.0-1.0
        inj_s   = min(signals.injection_score, 1.0)
        sem_s   = 0.8 if signals.semantic_flagged   else 0.0
        conv_s  = min(signals.conversation_score, 1.0)
        topic_s = min(signals.topic_score, 1.0)
        cont_s  = 1.0 if signals.content_flagged    else 0.0
        rate_s  = min(signals.rate_pressure, 1.0)

        # Weighted sum
        score = (
            inj_s   * WEIGHTS["injection"]   +
            sem_s   * WEIGHTS["semantic"]    +
            conv_s  * WEIGHTS["conversation"] +
            topic_s * WEIGHTS["topic"]       +
            cont_s  * WEIGHTS["content"]     +
            rate_s  * WEIGHTS["rate"]
        )
        score = round(min(score, 1.0), 4)

        # Determine action
        if score >= BLOCK_THRESHOLD:
            action = "block"
            reason = self._top_signal(signals)
        elif score >= ALLOW_THRESHOLD:
            action = "caution"
            reason = "borderline risk detected"
        else:
            action = "allow"
            reason = ""

        return ConfidenceResult(
            score   = score,
            action  = action,
            signals = signals,
            reason  = reason,
            note    = CAUTION_NOTE if action == "caution" else "",
        )

    def _top_signal(self, s: RiskSignals) -> str:
        """Return the name of the highest contributing signal."""
        candidates = {
            "injection attempt"    : s.injection_score * WEIGHTS["injection"],
            "semantic analysis"    : (0.8 if s.semantic_flagged else 0) * WEIGHTS["semantic"],
            "conversation pattern" : s.conversation_score * WEIGHTS["conversation"],
            "off-topic content"    : s.topic_score * WEIGHTS["topic"],
            "harmful content"      : (1.0 if s.content_flagged else 0) * WEIGHTS["content"],
        }
        return max(candidates, key=candidates.get)