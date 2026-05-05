"""
firewall/rate_limiter.py — Layer 5: Per-Session Rate Limiting
=============================================================
Tracks message frequency per session and blocks abuse.

Three tiers of limits:
  TIER 1 — Per-minute burst limit    (stops rapid-fire abuse)
  TIER 2 — Per-hour sustained limit  (stops scripted crawling)
  TIER 3 — Per-day total limit       (stops daily quota drain)

Each session is identified by Flask session_id.
All data stored in-memory (resets on server restart).
For production → replace with Redis.
"""

import time
from collections import defaultdict, deque
from typing import Tuple


# ── Configurable limits ────────────────────────────────────────────
BURST_LIMIT        = 8    # max messages per 60 seconds
HOURLY_LIMIT       = 60   # max messages per hour
DAILY_LIMIT        = 200  # max messages per day
WARNING_THRESHOLD  = 0.80 # warn user when 80% of any limit is reached


class RateLimiter:

    def __init__(self):
        # Each stores deque of timestamps keyed by session_id
        self._minute_log  : dict[str, deque] = defaultdict(deque)
        self._hour_log    : dict[str, deque] = defaultdict(deque)
        self._day_log     : dict[str, deque] = defaultdict(deque)

    def check(self, session_id: str) -> Tuple[bool, str]:
        """
        Returns (is_allowed, message).
        Call this BEFORE processing the message.
        If allowed, also records the timestamp (one call does both).
        """
        now = time.time()

        # ── Clean up expired timestamps ───────────────────────────
        self._clean(self._minute_log[session_id], now, 60)
        self._clean(self._hour_log[session_id],   now, 3600)
        self._clean(self._day_log[session_id],    now, 86400)

        minute_count = len(self._minute_log[session_id])
        hour_count   = len(self._hour_log[session_id])
        day_count    = len(self._day_log[session_id])

        # ── Hard blocks ───────────────────────────────────────────
        if minute_count >= BURST_LIMIT:
            wait = int(60 - (now - self._minute_log[session_id][0]))
            return (False,
                    f"You're sending messages too quickly. "
                    f"Please wait {wait} seconds before trying again.")

        if hour_count >= HOURLY_LIMIT:
            wait_min = int((3600 - (now - self._hour_log[session_id][0])) / 60)
            return (False,
                    f"You've reached the hourly message limit ({HOURLY_LIMIT} messages). "
                    f"Please try again in about {wait_min} minutes.")

        if day_count >= DAILY_LIMIT:
            return (False,
                    f"You've reached the daily message limit ({DAILY_LIMIT} messages). "
                    "Please try again tomorrow or contact us directly at +1-800-HOSPITAL.")

        # ── Record this message ───────────────────────────────────
        self._minute_log[session_id].append(now)
        self._hour_log[session_id].append(now)
        self._day_log[session_id].append(now)

        # ── Soft warnings (approaching limits) ───────────────────
        # (these still allow the message through, just warn)
        if day_count >= int(DAILY_LIMIT * WARNING_THRESHOLD):
            remaining = DAILY_LIMIT - day_count - 1
            return (True,
                    f"⚠️ Note: You have {remaining} messages remaining today.")

        return True, ""

    def get_stats(self, session_id: str) -> dict:
        """Return current usage stats for a session (for debugging)."""
        now = time.time()
        self._clean(self._minute_log[session_id], now, 60)
        self._clean(self._hour_log[session_id],   now, 3600)
        self._clean(self._day_log[session_id],    now, 86400)
        return {
            "last_minute" : len(self._minute_log[session_id]),
            "last_hour"   : len(self._hour_log[session_id]),
            "today"       : len(self._day_log[session_id]),
            "limits"      : {
                "minute": BURST_LIMIT,
                "hour"  : HOURLY_LIMIT,
                "day"   : DAILY_LIMIT,
            }
        }

    @staticmethod
    def _clean(dq: deque, now: float, window: float):
        """Remove timestamps older than the window."""
        while dq and (now - dq[0]) > window:
            dq.popleft()