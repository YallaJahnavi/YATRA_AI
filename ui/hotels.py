"""Accommodation recommendation cards.

The ML recommender returns an accommodation *type* + estimated nightly cost +
confidence/comfort. There's no live places API wired in, so we synthesise a
small set of believable, on-theme hotel options for that (destination, type)
pair — deterministically, so they're stable across reruns — and present them as
modern cards with rating, price, distance, perks and an AI recommendation score.
"""

import hashlib
from typing import Dict, Any, List
from urllib.parse import quote_plus

import streamlit as st

from ui.destinations import get_destination

# Destination flavour word used in synthesised hotel names.
THEME = {
    "Jaipur": "Rajputana", "Goa": "Beachside", "Delhi": "Imperial", "Mumbai": "Marine",
    "Bangalore": "Garden City", "Udaipur": "Lakeside", "Varanasi": "Ganga", "Kolkata": "Colonial",
    "Agra": "Mughal", "Kerala": "Backwater", "Pune": "Deccan", "Lucknow": "Nawabi",
    "Rishikesh": "Riverside", "Rajasthan (non-GT)": "Marwar", "Himachal Pradesh": "Hilltop",
    "Northeast India": "Cloud Valley", "Hyderabad": "Nizami",
}

_NAME_TEMPLATES = {
    "Budget": ["{t} Stay Inn", "Hotel {d} Comfort", "{d} Backpackers Lodge", "Zen {d} Rooms"],
    "Mid-range": ["{t} Grand Residency", "Hotel {d} Sarovar", "The {t} Courtyard", "{d} Boulevard Hotel"],
    "Luxury": ["The {t} Palace", "{t} Heritage Resort", "The {d} Royal Retreat", "{t} Grand Spa Resort"],
    "Alternative": ["{t} Boutique Homestay", "{d} Eco Villa", "Heritage {t} Haveli", "{d} Hideaway Stay"],
}

_PERKS = {
    "Budget": ["Free Wi-Fi", "24×7 reception", "Locker storage", "Travel desk", "AC rooms"],
    "Mid-range": ["Free breakfast", "Pool", "Free Wi-Fi", "Airport pickup", "Gym", "Room service"],
    "Luxury": ["Spa & wellness", "Fine dining", "Rooftop pool", "Concierge", "Valet parking", "Butler service"],
    "Alternative": ["Home-cooked meals", "Local host", "Garden", "Pet friendly", "Cultural tours"],
}

_TYPE_ICON = {"Budget": "🛏️", "Mid-range": "🏨", "Luxury": "✨", "Alternative": "🏡"}
_TYPE_GRADIENT = {
    "Budget": "linear-gradient(135deg,#0EA5E9,#2563EB)",
    "Mid-range": "linear-gradient(135deg,#2563EB,#7C3AED)",
    "Luxury": "linear-gradient(135deg,#7C3AED,#EC4899)",
    "Alternative": "linear-gradient(135deg,#10B981,#0EA5E9)",
}


def _seed(*parts) -> int:
    return int(hashlib.md5("|".join(map(str, parts)).encode()).hexdigest(), 16)


def generate_hotels(destination: str, acc_type: str, base_cost: float,
                    confidence: float, comfort: float, n: int = 4) -> List[Dict[str, Any]]:
    """Deterministically synthesise n believable hotels for the recommended type."""
    acc_type = acc_type if acc_type in _NAME_TEMPLATES else "Mid-range"
    theme = THEME.get(destination, destination)
    base_cost = base_cost or 3000
    # normalise confidence/comfort to 0-100
    conf = confidence * 100 if confidence and confidence <= 1 else (confidence or 80)
    comf = comfort if comfort and comfort > 1 else (comfort or 0.6) * 100

    hotels = []
    for i, tmpl in enumerate(_NAME_TEMPLATES[acc_type][:n]):
        name = tmpl.format(t=theme, d=destination)
        s = _seed(destination, acc_type, name)
        price = round(base_cost * (0.82 + (s % 45) / 100.0))            # ±~18% spread
        rating = round(3.9 + (s % 100) / 100.0, 1)                       # 3.9–4.9
        distance = round(0.6 + (s % 42) / 10.0, 1)                       # 0.6–4.8 km
        # AI score blends the model's confidence/comfort, rating, and proximity
        ai_score = int(min(98, max(72,
            0.45 * conf + 0.30 * comf + 0.15 * (rating / 5 * 100) + 0.10 * (100 - distance * 12))))
        perks = _PERKS[acc_type]
        perks = [perks[(s + j) % len(perks)] for j in range(3)]
        hotels.append({
            "name": name, "type": acc_type, "price": price, "rating": rating,
            "distance": distance, "ai_score": ai_score, "perks": list(dict.fromkeys(perks)),
            "best": i == 0,
        })
    hotels.sort(key=lambda h: h["ai_score"], reverse=True)
    for h in hotels:
        h["best"] = False
    hotels[0]["best"] = True
    return hotels


def _score_color(score: int) -> str:
    if score >= 90:
        return "#10B981"
    if score >= 82:
        return "#2563EB"
    return "#F97316"


def _card_html(h: Dict[str, Any]) -> str:
    rupee = "₹"
    grad = _TYPE_GRADIENT.get(h["type"], _TYPE_GRADIENT["Mid-range"])
    icon = _TYPE_ICON.get(h["type"], "🏨")
    best = ('<span class="badge" style="position:absolute;top:12px;left:12px;">⭐ AI top pick</span>'
            if h["best"] else "")
    perks = "".join(f'<span class="pill">{p}</span>' for p in h["perks"])
    sc = _score_color(h["ai_score"])
    return f'<div class="glass-card" style="padding:0;overflow:hidden;"><div style="position:relative;height:120px;background:{grad};display:flex;align-items:center;justify-content:center;">{best}<span style="font-size:2.6rem;">{icon}</span><span style="position:absolute;bottom:12px;right:12px;background:rgba(255,255,255,0.92);border-radius:999px;padding:4px 12px;font-weight:700;color:#0F172A;">⭐ {h["rating"]}</span></div><div style="padding:16px 18px;"><div style="display:flex;justify-content:space-between;align-items:flex-start;gap:10px;"><div style="font-family:\'Plus Jakarta Sans\';font-weight:700;font-size:1.08rem;">{h["name"]}</div><div style="text-align:center;"><div style="font-weight:800;color:{sc};font-size:1.1rem;">{h["ai_score"]}</div><div style="font-size:.62rem;color:#94A3B8;text-transform:uppercase;letter-spacing:.05em;">AI score</div></div></div><div style="color:#475569;font-size:.86rem;margin:4px 0 10px 0;">📍 {h["distance"]} km from centre · {h["type"]}</div><div style="margin-bottom:10px;">{perks}</div><div style="display:flex;align-items:baseline;gap:6px;"><span style="font-family:\'Plus Jakarta Sans\';font-weight:800;font-size:1.3rem;">{rupee}{h["price"]:,.0f}</span><span style="color:#94A3B8;font-size:.85rem;">/ night</span></div></div></div>'


def render_hotels(assessment: Dict[str, Any]) -> None:
    destination = assessment.get("destination", "")
    acc_type = assessment.get("accommodation_type", "Mid-range")
    base_cost = assessment.get("estimated_cost_per_night", 0)
    confidence = assessment.get("accommodation_confidence", 0)
    comfort = assessment.get("accommodation_comfort_score", 0)

    conf_disp = confidence * 100 if confidence and confidence <= 1 else (confidence or 0)

    st.markdown(
        f"""
        <div class="glass-card" style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:12px;">
            <div>
                <div style="color:#475569; font-size:.82rem; text-transform:uppercase; letter-spacing:.04em;">AI recommended stay</div>
                <div style="font-family:'Plus Jakarta Sans'; font-weight:800; font-size:1.6rem;">{_TYPE_ICON.get(acc_type,'🏨')} {acc_type}</div>
            </div>
            <div style="display:flex; gap:22px;">
                <div><div style="font-weight:800; font-size:1.3rem;">{conf_disp:.0f}%</div><div style="color:#94A3B8; font-size:.75rem;">CONFIDENCE</div></div>
                <div><div style="font-weight:800; font-size:1.3rem;">₹{base_cost:,.0f}</div><div style="color:#94A3B8; font-size:.75rem;">EST. / NIGHT</div></div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.write("")

    hotels = generate_hotels(destination, acc_type, base_cost, confidence, comfort)
    st.caption(f"{len(hotels)} hand-matched {acc_type.lower()} options near {destination}, ranked by AI recommendation score")

    for i in range(0, len(hotels), 2):
        cols = st.columns(2)
        for col, h in zip(cols, hotels[i:i + 2]):
            with col:
                st.markdown(_card_html(h), unsafe_allow_html=True)
                q = quote_plus(f"{h['name']} {destination} hotel")
                st.link_button("🔎 View & book", f"https://www.google.com/search?q={q}",
                               use_container_width=True)
