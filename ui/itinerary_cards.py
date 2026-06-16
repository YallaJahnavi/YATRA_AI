"""Day-wise itinerary cards.

Replaces the plain-text itinerary with rich, glassmorphism day cards. Each card
shows a time-slotted activity timeline, an estimated day cost, an estimated
in-city travel time, and native action buttons (open the day's route in Google
Maps, save the day to "My Trips").

The LLM itinerary only carries day-level cost + a flat activity list, so we
synthesise sensible time slots, split the cost across activities, and estimate
travel time between activities we can geo-match to the curated attraction set.
"""

from typing import Dict, Any, List, Optional, Tuple
from urllib.parse import quote_plus

import streamlit as st

from ui.destinations import (
    get_destination, match_attraction, haversine_km, travel_minutes,
)

# Time slots assigned to activities, in order (cycles if a day has more stops).
SLOTS: List[Tuple[str, str]] = [
    ("09:30", "Morning"),
    ("12:30", "Midday"),
    ("15:00", "Afternoon"),
    ("17:30", "Evening"),
    ("20:00", "Night"),
    ("22:00", "Late"),
]


def normalize_itinerary(itinerary: Any) -> List[Dict[str, Any]]:
    """Coerce the LLM itinerary (dict-of-days | list | strings) into a clean list."""
    days: List[Dict[str, Any]] = []

    def _clean_acts(acts) -> List[str]:
        if isinstance(acts, str):
            return [a.strip() for a in acts.split(",") if a.strip()]
        if isinstance(acts, list):
            out = []
            for a in acts:
                if isinstance(a, dict):
                    out.append(str(a.get("activity") or a.get("name") or a.get("title") or a))
                else:
                    out.append(str(a))
            return out
        return []

    if isinstance(itinerary, dict):
        items = itinerary.items()
    elif isinstance(itinerary, list):
        items = enumerate(itinerary, 1)
    else:
        return days

    for key, details in items:
        label = str(key).replace("_", " ").title() if not str(key).isdigit() else f"Day {key}"
        if isinstance(details, dict):
            title = details.get("title", "")
            acts = _clean_acts(details.get("activities", []))
            cost = details.get("estimated_cost", 0) or 0
        else:
            parts = _clean_acts(details)
            title = parts[0] if parts else ""
            acts = parts
            cost = 0
        days.append({"day": label, "title": title, "activities": acts, "estimated_cost": cost})
    return days


def _maps_route_url(activities: List[str], destination: str) -> str:
    """Google Maps multi-stop directions URL for a day's activities."""
    stops = [quote_plus(f"{a}, {destination}, India") for a in activities[:9]] or [quote_plus(destination)]
    return "https://www.google.com/maps/dir/" + "/".join(stops)


def _timeline_html(day: Dict[str, Any], destination: str) -> str:
    """Build the time-slotted activity timeline with travel-time connectors."""
    d = get_destination(destination)
    attractions = d.get("attractions", [])
    acts = day["activities"]
    n = max(len(acts), 1)
    per_act = (day["estimated_cost"] / n) if day["estimated_cost"] else 0

    rows = []
    prev_coords: Optional[Tuple[float, float]] = None
    for i, act in enumerate(acts):
        t, lbl = SLOTS[min(i, len(SLOTS) - 1)]

        # travel connector from the previous geo-matched stop
        travel = ""
        m = match_attraction(act, attractions)
        coords = (m[1], m[2]) if m else None
        if prev_coords and coords:
            km = haversine_km(prev_coords, coords)
            if km > 0.05:
                travel = (
                    f'<div class="tl-travel"><span class="chip">🚗 ~{travel_minutes(km)} min · '
                    f'{km:.1f} km</span></div>'
                )
        if coords:
            prev_coords = coords

        cost_html = f'<span class="tl-cost">~₹{per_act:,.0f}</span>' if per_act else ""
        is_last = i == len(acts) - 1
        line = "" if is_last else '<div class="tl-line"></div>'
        rows.append(
            f"""
            {travel}
            <div class="tl-item">
                <div class="tl-time"><div class="t">{t}</div><div class="l">{lbl}</div></div>
                <div class="tl-rail"><div class="tl-dot"></div>{line}</div>
                <div class="tl-body"><div class="tl-act">{act}</div>{cost_html}</div>
            </div>
            """
        )
    return '<div class="tl">' + "".join(rows) + "</div>"


def _day_travel_summary(day: Dict[str, Any], destination: str) -> Optional[str]:
    """Total intra-day travel estimate across geo-matched stops."""
    d = get_destination(destination)
    attractions = d.get("attractions", [])
    coords = []
    for act in day["activities"]:
        m = match_attraction(act, attractions)
        if m:
            coords.append((m[1], m[2]))
    if len(coords) < 2:
        return None
    total = sum(haversine_km(coords[i], coords[i + 1]) for i in range(len(coords) - 1))
    return f"🚗 ~{travel_minutes(total)} min · {total:.1f} km"


def render_itinerary(itinerary: Any, destination: str, daily_budget: float = 0) -> None:
    """Render the full day-by-day itinerary as cards."""
    days = normalize_itinerary(itinerary)
    if not days:
        st.warning("No itinerary available yet — generate a plan to see your day-by-day schedule.")
        return

    if "saved_days" not in st.session_state:
        st.session_state.saved_days = {}

    st.caption(f"{len(days)} days · {sum(len(d['activities']) for d in days)} curated experiences")

    for idx, day in enumerate(days):
        with st.container(border=True):
            travel = _day_travel_summary(day, destination)
            meta_bits = []
            if day["estimated_cost"]:
                meta_bits.append(f"💰 <b>₹{day['estimated_cost']:,.0f}</b> est.")
            meta_bits.append(f"📍 <b>{len(day['activities'])}</b> stops")
            if travel:
                meta_bits.append(travel)

            st.markdown(
                f"""
                <div class="day-head">
                    <span class="day-badge">{day['day']}</span>
                    <div class="day-meta">{' · '.join(meta_bits)}</div>
                </div>
                <div class="day-title" style="margin-top:8px;">{day['title']}</div>
                {_timeline_html(day, destination)}
                """,
                unsafe_allow_html=True,
            )

            c1, c2, _ = st.columns([1.1, 1, 2])
            c1.link_button("📍 Open route in Maps", _maps_route_url(day["activities"], destination),
                           use_container_width=True)
            saved = day["day"] in st.session_state.saved_days
            if c2.button("✓ Saved" if saved else "💾 Save day", key=f"save_day_{idx}",
                         use_container_width=True, type="primary" if not saved else "secondary"):
                if saved:
                    st.session_state.saved_days.pop(day["day"], None)
                else:
                    st.session_state.saved_days[day["day"]] = {"destination": destination, **day}
                    st.toast(f"Saved {day['day']} to My Trips", icon="💾")
                st.rerun()
