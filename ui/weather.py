"""Weather intelligence widget (the Weather Agent's surface).

No live weather API is wired in, so this derives a grounded, deterministic
seasonal outlook from the destination's climate class + the chosen travel
season, then generates a short forecast strip, packing suggestions and
weather-aware activity recommendations. Fast, offline, and stable across reruns.
"""

import hashlib
from typing import Dict, Any, List

import streamlit as st

from ui.destinations import get_destination

# climate_type -> travel season -> typical outlook
_PROFILE: Dict[str, Dict[str, Dict[str, Any]]] = {
    "desert":    {"Peak": (28, 12, "Sunny & dry", "☀️"), "Moderate": (34, 18, "Hot, clear skies", "🌤️"), "Off-season": (42, 27, "Scorching heat", "🔥")},
    "coastal":   {"Peak": (31, 22, "Sunny sea breeze", "🌊"), "Moderate": (32, 25, "Warm & humid", "⛅"), "Off-season": (30, 25, "Monsoon showers", "🌧️")},
    "tropical":  {"Peak": (31, 23, "Pleasant & green", "🌴"), "Moderate": (33, 25, "Warm & humid", "⛅"), "Off-season": (29, 24, "Heavy monsoon", "🌧️")},
    "plains":    {"Peak": (24, 10, "Cool & clear", "☀️"), "Moderate": (33, 20, "Warm days", "🌤️"), "Off-season": (41, 28, "Very hot", "🔥")},
    "temperate": {"Peak": (27, 16, "Pleasant", "🌤️"), "Moderate": (29, 19, "Mild & breezy", "⛅"), "Off-season": (31, 21, "Warm, occasional rain", "🌦️")},
    "hill":      {"Peak": (24, 12, "Crisp & clear", "🌤️"), "Moderate": (18, 8, "Cool & misty", "🌥️"), "Off-season": (9, 1, "Cold, chance of snow", "❄️")},
}

_FORECAST_ICONS = ["☀️", "🌤️", "⛅", "🌦️", "🌧️", "❄️"]


def _seed(*parts) -> int:
    return int(hashlib.md5("|".join(map(str, parts)).encode()).hexdigest(), 16)


def _packing(climate_type: str, high: int, low: int, cond: str) -> List[str]:
    items = ["Comfortable walking shoes", "Power bank", "Reusable water bottle", "ID & travel docs"]
    c = cond.lower()
    if low < 8:
        items += ["Heavy jacket & thermals", "Woollen cap & gloves"]
    elif low < 15:
        items += ["Light jacket / hoodie"]
    if high >= 36:
        items += ["Light cotton clothing", "Sunscreen SPF 50", "Sunglasses & hat"]
    if "rain" in c or "monsoon" in c or "shower" in c:
        items += ["Compact umbrella / raincoat", "Quick-dry clothes", "Waterproof bag cover"]
    if "snow" in c:
        items += ["Snow boots", "Hand warmers"]
    if climate_type == "coastal" or climate_type == "tropical":
        items += ["Swimwear & flip-flops", "Mosquito repellent"]
    if climate_type == "hill":
        items += ["Trekking shoes", "Refillable flask"]
    return list(dict.fromkeys(items))


def _activities(cond: str, interests: List[str]) -> List[str]:
    c = cond.lower()
    wet = "rain" in c or "monsoon" in c or "shower" in c or "snow" in c
    hot = "hot" in c or "scorch" in c
    recs: List[str] = []
    if wet:
        recs += ["Museums & indoor heritage sites", "Café-hopping & local cuisine", "Spa / wellness afternoon"]
    elif hot:
        recs += ["Early-morning sightseeing", "Indoor attractions at midday", "Sunset viewpoints in the evening"]
    else:
        recs += ["Outdoor sightseeing all day", "Walking tours & markets", "Photography at golden hour"]
    # nudge by interest
    bias = {
        "Adventure": "Outdoor adventure activities" + (" (check conditions)" if wet else ""),
        "Beach": "Beach time" + (" — postpone if wet" if wet else " & water sports"),
        "Spiritual": "Temple & ghat visits at sunrise",
        "Heritage": "Fort & palace tours",
        "Food": "Guided street-food trail",
        "Cultural": "Local performances & galleries",
    }
    for it in interests:
        if it in bias:
            recs.append(bias[it])
    return list(dict.fromkeys(recs))[:5]


def render_weather(assessment: Dict[str, Any]) -> None:
    destination = assessment.get("destination", "")
    if not destination:
        st.info("Pick a destination to see the weather outlook.")
        return

    d = get_destination(destination)
    ctype = d["climate_type"]
    season = assessment.get("travel_season", "Moderate")
    high, low, cond, icon = _PROFILE.get(ctype, _PROFILE["plains"]).get(
        season, _PROFILE.get(ctype, _PROFILE["plains"])["Moderate"])

    interests = [assessment.get("primary_interest"), assessment.get("secondary_interest")]
    interests = [i for i in interests if i]

    # ---- current / typical conditions banner ----
    st.markdown(
        f"""
        <div class="yatra-hero" style="padding:28px 32px;">
            <span class="badge">🌤️ Weather Agent · {season} season</span>
            <div style="display:flex; align-items:center; gap:22px; margin-top:14px; flex-wrap:wrap;">
                <div style="font-size:3.4rem; line-height:1;">{icon}</div>
                <div>
                    <div style="font-family:'Plus Jakarta Sans'; font-weight:800; font-size:2.4rem; line-height:1;">{high}°C</div>
                    <div style="opacity:.9;">Feels like {high-1}° · Low {low}°C</div>
                </div>
                <div style="border-left:1px solid rgba(255,255,255,0.35); padding-left:22px;">
                    <div style="font-weight:700; font-size:1.1rem;">{cond}</div>
                    <div style="opacity:.9;">{d['name']} · {d['climate']}</div>
                    <div style="opacity:.9;">Best time to visit: {d['best_season']}</div>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.write("")

    # ---- forecast strip ----
    st.markdown("##### 5-day outlook")
    days = ["Today", "Day 2", "Day 3", "Day 4", "Day 5"]
    cols = st.columns(5)
    for i, (col, label) in enumerate(zip(cols, days)):
        s = _seed(destination, season, i)
        h = high + ((s % 5) - 2)
        l = low + ((s % 4) - 1)
        ic = icon if i % 3 != 2 else _FORECAST_ICONS[(s // 7) % len(_FORECAST_ICONS)]
        col.markdown(
            f"""
            <div class="glass-card" style="text-align:center; padding:14px 8px;">
                <div style="color:#475569; font-size:.8rem; font-weight:600;">{label}</div>
                <div style="font-size:1.8rem; margin:6px 0;">{ic}</div>
                <div style="font-family:'Plus Jakarta Sans'; font-weight:700;">{h}°<span style="color:#94A3B8;"> / {l}°</span></div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.write("")
    c1, c2 = st.columns(2)

    with c1:
        pack = _packing(ctype, high, low, cond)
        pills = "".join(f'<span class="pill mint">{p}</span>' for p in pack)
        st.markdown(
            f'<div class="glass-card"><b>🧳 Smart packing list</b><div style="margin-top:10px;">{pills}</div></div>',
            unsafe_allow_html=True,
        )

    with c2:
        acts = _activities(cond, interests)
        items = "".join(f'<div style="margin:6px 0;">✅ {a}</div>' for a in acts)
        st.markdown(
            f'<div class="glass-card"><b>🎯 Weather-smart activities</b><div style="margin-top:8px; color:#334155;">{items}</div></div>',
            unsafe_allow_html=True,
        )
