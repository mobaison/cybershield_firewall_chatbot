"""
firewall/firewall.py — Main Firewall Coordinator (7 Layers + Confidence Scoring)
==================================================================================
Layer execution order:

  1. InputSanitizer       — input quality        (pure Python, <0.1ms)
  2. RateLimiter          — abuse prevention      (pure Python, <0.1ms)
  3. InjectionDetector    — regex pattern match   (pure Python, ~1ms)
  4. SemanticGuard        — LLM injection check   (Groq, ~200ms, optional)
  5. TopicGuard           — hospital relevance    (pure Python, ~1ms)
  6. ContentFilter        — sensitive content     (pure Python, ~1ms)
  7. ConversationAnalyzer — multi-turn patterns   (pure Python, ~1ms)

  ConfidenceScorer — aggregates all signals, replaces binary with
                     allow / caution / block decision.

OUTPUTS:
  FirewallResult.allowed     = True/False
  FirewallResult.action      = "allow" | "caution" | "block" | "redirect"
  FirewallResult.risk_score  = 0.0 to 1.0
  FirewallResult.note        = caution message to append to response
"""

import os, time, logging
from dataclasses import dataclass
from dotenv import load_dotenv
from typing import List, Dict

from .sanitizer              import InputSanitizer
from .rate_limiter           import RateLimiter
from .injection_detector     import InjectionDetector
from .semantic_guard         import SemanticGuard
from .topic_guard            import TopicGuard
from .content_filter         import ContentFilter
from .conversation_analyzer  import ConversationAnalyzer
from .confidence_scorer      import ConfidenceScorer, RiskSignals

load_dotenv()

logging.basicConfig(
    filename="firewall_audit.log",
    level=logging.INFO,
    format="%(asctime)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
audit = logging.getLogger("firewall.audit")


@dataclass
class FirewallResult:
    allowed    : bool
    message    : str   = ""
    layer      : str   = ""
    action     : str   = "allow"   # allow | caution | block | redirect
    warning    : str   = ""        # rate limit warning
    note       : str   = ""        # caution note to append to bot response
    risk_score : float = 0.0       # 0.0-1.0 aggregate risk
    latency_ms : float = 0.0


class PromptFirewall:

    def __init__(self):
        groq_key = os.getenv("GROQ_API_KEY", "")

        self.sanitizer  = InputSanitizer()
        self.rate       = RateLimiter()
        self.injection  = InjectionDetector()
        self.semantic   = SemanticGuard(api_key=groq_key)
        self.topic      = TopicGuard()
        self.content    = ContentFilter()
        self.conv       = ConversationAnalyzer()
        self.scorer     = ConfidenceScorer()

        layers = 7 + (1 if groq_key else 0)
        print(f"✅ Prompt Firewall ready — {layers} layers + confidence scoring")

    def check(self, text: str, session_id: str = "default",
              recent_turns: List[Dict] = None) -> FirewallResult:
        """
        Run all firewall layers + confidence scoring.
        recent_turns: pass conversation history for multi-turn analysis.
        """
        start   = time.time()
        signals = RiskSignals()
        recent_turns = recent_turns or []

        # ── Layer 1: Input Sanitization ───────────────────────────
        ok, reason = self.sanitizer.check(text)
        if not ok:
            return self._instant_block("sanitizer", reason,
                                       text, session_id, start)

        # ── Layer 2: Rate Limiting ─────────────────────────────────
        ok, reason = self.rate.check(session_id)
        if not ok:
            return self._instant_block("rate_limiter", reason,
                                       text, session_id, start)
        rate_warning = reason if (ok and reason) else ""

        # Compute rate pressure for confidence scorer
        stats = self.rate.get_stats(session_id)
        signals.rate_pressure = max(
            stats["last_minute"] / 8,
            stats["last_hour"]   / 60,
            stats["today"]       / 200,
        )

        # ── Layer 3: Regex Injection Detection ────────────────────
        ok, reason = self.injection.check(text)
        if not ok:
            return self._instant_block("injection_detector", reason,
                                       text, session_id, start)
        # Contribute injection score to signals
        signals.injection_score = self._injection_score(text)

        # ── Layer 4: Semantic Guard (Groq) ────────────────────────
        ok, reason = self.semantic.check(text)
        if not ok:
            signals.semantic_flagged = True
            return self._instant_block("semantic_guard", reason,
                                       text, session_id, start)
        if not ok:
            signals.semantic_flagged = True

        # ── Layer 5: Topic Guard ───────────────────────────────────
        ok, reason = self.topic.check(text)
        if not ok:
            signals.topic_score = 1.0
            return self._instant_block("topic_guard", reason,
                                       text, session_id, start)

        # ── Layer 6: Content Filter ────────────────────────────────
        ok, reason, action = self.content.check(text)
        if not ok:
            signals.content_flagged = True
            self._log("content_filter", action, text, session_id)
            return FirewallResult(
                allowed    = False,
                message    = reason,
                layer      = "content_filter",
                action     = action,
                risk_score = 1.0,
                latency_ms = (time.time() - start) * 1000,
            )

        # ── Layer 7: Conversation Multi-Turn Analysis ─────────────
        safe, reason, conv_score = self.conv.check(
            session_id, text, recent_turns
        )
        signals.conversation_score = conv_score
        if not safe:
            return self._instant_block("conversation_analyzer", reason,
                                       text, session_id, start)

        # ── Confidence Scoring ────────────────────────────────────
        confidence = self.scorer.score(signals)

        if confidence.action == "block":
            msg = (
                "Your message has been flagged by our security system. "
                "Please ask a straightforward hospital or medical question."
            )
            self._log("confidence_scorer", "block", text, session_id,
                      extra=f"score={confidence.score}")
            return FirewallResult(
                allowed    = False,
                message    = msg,
                layer      = "confidence_scorer",
                action     = "block",
                risk_score = confidence.score,
                latency_ms = (time.time() - start) * 1000,
            )

        # ── All layers passed ──────────────────────────────────────
        return FirewallResult(
            allowed    = True,
            action     = confidence.action,   # "allow" or "caution"
            warning    = rate_warning,
            note       = confidence.note,     # appended to bot response if caution
            risk_score = confidence.score,
            latency_ms = (time.time() - start) * 1000,
        )

    def _injection_score(self, text: str) -> float:
        """
        Estimate injection risk score from medium-severity patterns.
        High-severity already blocked in Layer 3.
        """
        import re
        from .injection_detector import MEDIUM_SEVERITY_PATTERNS
        text_lower = text.lower()
        score = 0
        for pattern, weight in MEDIUM_SEVERITY_PATTERNS:
            if re.search(pattern, text_lower, re.IGNORECASE):
                score += weight
        return min(score / 4.0, 1.0)

    def _instant_block(self, layer, reason, text,
                        session_id, start) -> FirewallResult:
        self._log(layer, "block", text, session_id)
        return FirewallResult(
            allowed    = False,
            message    = reason,
            layer      = layer,
            action     = "block",
            risk_score = 1.0,
            latency_ms = (time.time() - start) * 1000,
        )

    def _log(self, layer, action, text, session_id, extra=""):
        safe = text[:120].replace("\n", " ")
        audit.info(
            f"BLOCKED | layer={layer} | action={action} | "
            f"session={session_id[:16]} | {extra} | input=\"{safe}\""
        )

    def stats(self, session_id: str) -> dict:
        return self.rate.get_stats(session_id)

    def reset_conversation(self, session_id: str):
        """Reset multi-turn analysis on session clear."""
        self.conv.reset(session_id)