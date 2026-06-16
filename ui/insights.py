"""Dynamic destination insights.

When a destination is in context, render a spotlight: a photo/gradient banner
plus glass cards for best season, average daily cost, safety rating, climate and
local transport, and a row of headline attractions. All data comes from the
curated ui.destinations knowledge base, so it renders instantly and offline.
"""

import streamlit as st

from ui.destinations import get_destination
from ui.theme import section_header


def _stars(rating: float) -> str:
    """Render a 0–5 rating as filled/half/empty stars."""
    full = int(rating)
    half = 1 if (rating - full) >= 0.25 and (rating - full) < 0.75 else 0
    if (rating - full) >= 0.75:
        full += 1
    empty = 5 - full - half
    return "★" * full + ("⯪" if half else "") + "☆" * empty


def _banner(d: dict) -> None:
    """Photo banner layered over the brand gradient (gradient shows if image fails)."""
    img_layer = f", url('{d['image']}')" if d.get("image") else ""
    st.markdown(
        f"""
        <div style="
            position:relative; border-radius:22px; overflow:hidden;
            min-height:210px; display:flex; align-items:flex-end;
            padding:22px 26px; color:#fff;
            background:
                linear-gradient(0deg, rgba(15,23,42,0.78) 0%, rgba(15,23,42,0.15) 55%, rgba(124,58,237,0.35) 100%)
                {img_layer};
            background-size: cover; background-position: center;
            box-shadow: 0 22px 50px rgba(15,23,42,0.22);">
            <div>
                <span class="badge" style="margin-bottom:10px;">{d['emoji']} Destination spotlight</span>
                <div style="font-family:'Plus Jakarta Sans'; font-weight:800; font-size:2rem; line-height:1.1;">
                    {d['name']}
                </div>
                <div style="opacity:.92; max-width:560px; margin-top:4px;">{d['tagline']}</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def _fact_card(icon: str, label: str, value: str, accent: str = "violet") -> str:
    colors = {"violet": "#7C3AED", "coral": "#F97316", "mint": "#10B981", "blue": "#2563EB"}
    c = colors.get(accent, colors["violet"])
    return f"""
        <div class="glass-card" style="padding:16px 18px; height:100%;">
            <div style="display:flex; align-items:center; gap:8px; color:{c}; font-weight:600; font-size:.82rem;
                        text-transform:uppercase; letter-spacing:.04em;">
                <span style="font-size:1.05rem;">{icon}</span> {label}
            </div>
            <div style="font-family:'Plus Jakarta Sans'; font-weight:700; font-size:1.12rem; margin-top:6px; color:#0F172A;">
                {value}
            </div>
        </div>
    """


def render_destination_spotlight(destination: str) -> None:
    """Render the full insights block for a destination."""
    if not destination:
        return
    d = get_destination(destination)

    section_header(
        "Destination insights",
        "auto-generated the moment you pick a place",
        icon="📍",
    )

    _banner(d)
    st.write("")

    lo, hi = d["daily_cost"]
    facts = [
        _fact_card("🗓️", "Best season", d["best_season"], "violet"),
        _fact_card("💸", "Avg daily cost", f"₹{lo:,}–₹{hi:,} / person", "coral"),
        _fact_card("🛡️", "Safety", f"{_stars(d['safety'])}  {d['safety']:.1f}", "mint"),
        _fact_card("🌤️", "Climate", d["climate"], "blue"),
    ]
    cols = st.columns(4)
    for col, html in zip(cols, facts):
        col.markdown(html, unsafe_allow_html=True)

    st.write("")
    c1, c2 = st.columns([2, 1])

    with c1:
        attractions = d.get("attractions", [])
        pills = "".join(
            f'<span class="pill">{name}</span>'
            for (name, _lat, _lon, _cat) in attractions
        ) or '<span class="pill">Curated picks coming up in your itinerary</span>'
        st.markdown(
            f"""
            <div class="glass-card" style="height:100%;">
                <div style="font-family:'Plus Jakarta Sans'; font-weight:700; margin-bottom:10px;">
                    🌟 Popular attractions
                </div>
                <div>{pills}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with c2:
        st.markdown(
            f"""
            <div class="glass-card" style="height:100%;">
                <div style="font-family:'Plus Jakarta Sans'; font-weight:700; margin-bottom:10px;">
                    🚖 Getting around
                </div>
                <div style="color:#475569; line-height:1.5;">{d['transport']}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
