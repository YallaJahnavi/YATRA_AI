"""Natural-language trip-request parser for the AI assistant.

Turns a free-text message like
    "I want a 7-day adventure trip to Jaipur for 2 people under 50k"
into the structured form_data dict that graph.plan_trip() expects.

Primary path uses the existing Gemini client (utils.gemini_client); if the LLM
is unavailable or returns junk, a deterministic regex/keyword fallback still
extracts what it can. Everything is validated and clamped against utils.constants
so the downstream workflow always receives legal values.
"""

from __future__ import annotations

import re
from typing import Dict, Any, Optional, List, Tuple

from utils.constants import (
    DESTINATIONS, INTERESTS, TRAVEL_SEASONS,
    BUDGET_MIN, BUDGET_MAX, BUDGET_DEFAULT,
    TRIP_DURATION_MIN, TRIP_DURATION_MAX, TRIP_DURATION_DEFAULT,
    GROUP_SIZE_MIN, GROUP_SIZE_MAX, GROUP_SIZE_DEFAULT,
)

# travel-style keyword -> implied group size
_GROUP_HINTS: List[Tuple[str, int]] = [
    ("solo", 1), ("alone", 1), ("by myself", 1),
    ("couple", 2), ("honeymoon", 2), ("partner", 2), ("girlfriend", 2), ("boyfriend", 2), ("wife", 2), ("husband", 2),
    ("family", 4), ("kids", 4), ("children", 4),
    ("friends", 4), ("group", 5),
]

_SEASON_HINTS: List[Tuple[str, str]] = [
    ("peak", "Peak"), ("winter", "Peak"), ("december", "Peak"), ("new year", "Peak"),
    ("off-season", "Off-season"), ("off season", "Off-season"), ("monsoon", "Off-season"), ("summer", "Off-season"),
    ("moderate", "Moderate"), ("shoulder", "Moderate"),
]


def _clamp(value: int, lo: int, hi: int) -> int:
    return max(lo, min(hi, int(value)))


def _match_destination(text: str) -> Optional[str]:
    low = text.lower()
    for dest in DESTINATIONS:
        # match on the leading word of the destination label (handles "Rajasthan (non-GT)")
        key = re.split(r"[ (]", dest)[0].lower()
        if key and key in low:
            return dest
    # a few common aliases
    aliases = {
        "jodhpur": "Rajasthan (non-GT)", "jaisalmer": "Rajasthan (non-GT)",
        "shimla": "Himachal Pradesh", "manali": "Himachal Pradesh", "himachal": "Himachal Pradesh",
        "shillong": "Northeast India", "meghalaya": "Northeast India", "northeast": "Northeast India",
        "kochi": "Kerala", "cochin": "Kerala", "munnar": "Kerala", "alleppey": "Kerala",
        "benares": "Varanasi", "kashi": "Varanasi", "bengaluru": "Bangalore",
    }
    for alias, dest in aliases.items():
        if alias in low:
            return dest
    return None


def _match_interest(text: str, exclude: Optional[str] = None) -> Optional[str]:
    low = text.lower()
    synonyms = {
        "Adventure": ["adventure", "trek", "hiking", "rafting", "thrill", "ziplin"],
        "Cultural": ["cultur", "art", "museum", "local life"],
        "Beach": ["beach", "sea", "coast", "sand"],
        "Spiritual": ["spiritual", "temple", "yoga", "meditat", "pilgrim", "ashram"],
        "Food": ["food", "cuisine", "culinary", "eat", "street food", "foodie"],
        "Heritage": ["heritage", "history", "fort", "palace", "monument", "ancient"],
    }
    for interest in INTERESTS:
        if interest == exclude:
            continue
        for kw in synonyms.get(interest, [interest.lower()]):
            if kw in low:
                return interest
    return None


def _parse_budget(text: str) -> Optional[int]:
    low = text.lower().replace(",", "")
    # forms: "50k", "1.5 lakh", "rs 50000", "₹50000", "under 50000"
    m = re.search(r"(\d+(?:\.\d+)?)\s*(lakh|lac|l\b|k\b|thousand)", low)
    if m:
        num = float(m.group(1))
        unit = m.group(2)
        if unit.startswith("lakh") or unit.startswith("lac") or unit == "l":
            return int(num * 100000)
        return int(num * 1000)  # k / thousand
    m = re.search(r"(?:rs\.?|inr|₹|budget of|under|around|about)\s*(\d{4,7})", low)
    if m:
        return int(m.group(1))
    # bare large number
    m = re.search(r"\b(\d{4,7})\b", low)
    if m:
        return int(m.group(1))
    return None


def _parse_duration(text: str) -> Optional[int]:
    low = text.lower()
    m = re.search(r"(\d+)\s*[- ]?\s*(day|days|night|nights|d\b)", low)
    if m:
        return int(m.group(1))
    m = re.search(r"(\d+)\s*week", low)
    if m:
        return int(m.group(1)) * 7
    return None


def _parse_group(text: str) -> Optional[int]:
    low = text.lower()
    m = re.search(r"(\d+)\s*(people|persons|pax|travellers|travelers|adults|of us|members)", low)
    if m:
        return int(m.group(1))
    for kw, size in _GROUP_HINTS:
        if kw in low:
            return size
    return None


def _parse_season(text: str) -> Optional[str]:
    low = text.lower()
    for kw, season in _SEASON_HINTS:
        if kw in low:
            return season
    return None


def _regex_extract(text: str, defaults: Dict[str, Any]) -> Dict[str, Any]:
    """Deterministic fallback parse (no LLM)."""
    primary = _match_interest(text)
    secondary = _match_interest(text, exclude=primary)
    return {
        "destination": _match_destination(text) or defaults.get("destination"),
        "trip_duration_days": _parse_duration(text) or defaults.get("trip_duration_days"),
        "total_budget_inr": _parse_budget(text) or defaults.get("total_budget_inr"),
        "group_size": _parse_group(text) or defaults.get("group_size"),
        "primary_interest": primary or defaults.get("primary_interest"),
        "secondary_interest": secondary or defaults.get("secondary_interest", ""),
        "travel_season": _parse_season(text) or defaults.get("travel_season"),
    }


def _llm_extract(text: str) -> Optional[Dict[str, Any]]:
    """Ask Gemini to extract structured fields. Returns None on any failure."""
    try:
        from utils.gemini_client import build_gemini_client

        client = build_gemini_client()
        prompt = f"""
You are a travel-request parser. Extract trip parameters from the user's message.

User message: "{text}"

Return ONLY JSON with these keys (use null if not stated, never invent):
{{
  "destination": one of {DESTINATIONS} or null,
  "trip_duration_days": integer or null,
  "total_budget_inr": integer in INR or null,
  "group_size": integer or null,
  "primary_interest": one of {INTERESTS} or null,
  "secondary_interest": one of {INTERESTS} or null,
  "travel_season": one of {TRAVEL_SEASONS} or null
}}
Interpret "50k" as 50000 and "1.5 lakh" as 150000. Map travel companions to
group_size (solo=1, couple=2, family=4, friends=4).
"""
        result = client.extract_json_from_response(client.generate_content(prompt, temperature=0.1, max_tokens=400))
        return result if isinstance(result, dict) else None
    except Exception:
        return None


def _validate_destination(value: Any) -> Optional[str]:
    if value in DESTINATIONS:
        return value
    if isinstance(value, str) and value.strip():
        return _match_destination(value)
    return None


def _validate_interest(value: Any) -> Optional[str]:
    if value in INTERESTS:
        return value
    if isinstance(value, str) and value.strip():
        return _match_interest(value)
    return None


def parse_trip_request(text: str, defaults: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """Parse a free-text request into validated form_data + a 'missing' report.

    Returns a dict with the seven plan_trip parameters plus:
      _missing: list of critical fields that could not be determined
      _source:  "llm" or "regex" (which path produced the values)
    """
    defaults = defaults or {}

    llm = _llm_extract(text)
    source = "llm" if llm else "regex"

    # merge: LLM result wins where present, else regex fallback, else sidebar defaults
    regex = _regex_extract(text, defaults)
    merged: Dict[str, Any] = dict(regex)
    if llm:
        for k, v in llm.items():
            if v not in (None, "", "null"):
                merged[k] = v

    # ---- validate + clamp ----
    destination = _validate_destination(merged.get("destination")) or defaults.get("destination")

    duration = merged.get("trip_duration_days") or defaults.get("trip_duration_days") or TRIP_DURATION_DEFAULT
    try:
        duration = _clamp(duration, TRIP_DURATION_MIN, TRIP_DURATION_MAX)
    except (TypeError, ValueError):
        duration = TRIP_DURATION_DEFAULT

    budget = merged.get("total_budget_inr") or defaults.get("total_budget_inr") or BUDGET_DEFAULT
    try:
        budget = _clamp(budget, BUDGET_MIN, BUDGET_MAX)
    except (TypeError, ValueError):
        budget = BUDGET_DEFAULT

    group = merged.get("group_size") or defaults.get("group_size") or GROUP_SIZE_DEFAULT
    try:
        group = _clamp(group, GROUP_SIZE_MIN, GROUP_SIZE_MAX)
    except (TypeError, ValueError):
        group = GROUP_SIZE_DEFAULT

    primary = _validate_interest(merged.get("primary_interest")) or defaults.get("primary_interest") or INTERESTS[0]
    secondary = _validate_interest(merged.get("secondary_interest")) or ""
    if secondary == primary:
        secondary = ""

    season = merged.get("travel_season")
    if season not in TRAVEL_SEASONS:
        season = defaults.get("travel_season") if defaults.get("travel_season") in TRAVEL_SEASONS else TRAVEL_SEASONS[1]

    # critical missing fields = ones we had to default because the user never said them
    missing: List[str] = []
    if not _validate_destination(merged.get("destination")) and not _match_destination(text):
        missing.append("destination")

    return {
        "destination": destination,
        "trip_duration_days": duration,
        "total_budget_inr": budget,
        "group_size": group,
        "primary_interest": primary,
        "secondary_interest": secondary,
        "travel_season": season,
        "_missing": missing,
        "_source": source,
    }
