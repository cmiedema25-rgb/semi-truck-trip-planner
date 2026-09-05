"""Rule-based natural-language helpers for destination / trip text.

No LLM key required. Optional OpenAI/Anthropic summarization is gated behind env vars.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Optional


@dataclass
class ParsedTripRequest:
    """Structured fields extracted from free-text trip input."""

    destination: Optional[str] = None
    origin: Optional[str] = None
    hazmat: bool = False
    notes: str = ""
    raw: str = ""


_TO_PATTERNS = [
    re.compile(r"\b(?:to|destination|deliver(?:ing)?\s+to|drop(?:\s*off)?\s+at)\s+[:\-]?\s*(.+)$", re.I),
    re.compile(r"\bgoing\s+to\s+(.+)$", re.I),
]
_FROM_PATTERNS = [
    re.compile(r"\b(?:from|origin|pickup(?:\s+at)?|leaving)\s+[:\-]?\s*(.+?)(?:\s+(?:to|destination|deliver)\b|$)", re.I),
]
_HAZMAT = re.compile(r"\b(hazmat|hazardous|placard(?:ed)?|dangerous\s+goods)\b", re.I)


def parse_trip_text(text: str) -> ParsedTripRequest:
    """Parse destination-first free text into structured trip fields.

    Examples:
      - "Houston warehouse"
      - "to 5600 Warehouse Blvd, Houston, TX from Dallas yard"
      - "Deliver to Houston, hazmat"
    """
    raw = (text or "").strip()
    result = ParsedTripRequest(raw=raw, hazmat=bool(_HAZMAT.search(raw)))
    if not raw:
        return result

    cleaned = _HAZMAT.sub("", raw).strip(" ,;")

    origin: Optional[str] = None
    destination: Optional[str] = None

    for pat in _FROM_PATTERNS:
        m = pat.search(cleaned)
        if m:
            origin = m.group(1).strip(" ,;")
            break

    for pat in _TO_PATTERNS:
        m = pat.search(cleaned)
        if m:
            destination = m.group(1).strip(" ,;")
            # Strip trailing "from X" if still attached
            destination = re.split(r"\bfrom\b", destination, maxsplit=1, flags=re.I)[0].strip(" ,;")
            break

    if destination is None and origin is None:
        # Destination-only UX: treat whole string as destination
        destination = cleaned
    elif destination is None and origin is not None:
        # "from Dallas to Houston" already handled; leftover after from
        remainder = cleaned
        for pat in _FROM_PATTERNS:
            remainder = pat.sub("", remainder).strip(" ,;")
        destination = remainder or None

    result.origin = origin or None
    result.destination = destination or None
    result.notes = "Parsed with rule-based NL (no LLM)."
    return result


def template_summary(
    origin_label: str,
    dest_label: str,
    distance_mi: float,
    eta: str,
    vehicle_name: str,
    provider: str,
    hazmat: bool,
) -> str:
    """Plain-English trip card without an LLM."""
    haz = " HAZMAT flagged — confirm permits and restricted routes." if hazmat else ""
    return (
        f"Trip plan ({provider}): {origin_label} → {dest_label}. "
        f"About {distance_mi:.1f} miles, ETA {eta}, using {vehicle_name} HGV profile.{haz} "
        f"This is decision support — verify height/weight/local restrictions before dispatch."
    )


def maybe_llm_polish(summary: str, openai_key: Optional[str] = None, anthropic_key: Optional[str] = None) -> str:
    """Optional LLM polish — only if a key is present; otherwise return template as-is."""
    # Intentionally no network call in MVP unless keys exist; keep deterministic for CI.
    if not openai_key and not anthropic_key:
        return summary
    # Live LLM calls are out of scope for offline verify; callers may extend later.
    return summary + " (LLM polish skipped in MVP — template summary used.)"
