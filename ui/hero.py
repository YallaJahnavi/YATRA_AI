"""Hero / banner section for YatraAI.

A gradient hero with product branding, an AI badge, a value proposition and a
strip of trust stats. When a destination is in context it personalises the
headline ("Plan your trip to Goa") and surfaces the destination motif.
"""

import streamlit as st

from ui.destinations import get_destination


def render_hero(active_destination: str = "") -> None:
    """Render the top hero. Pass the currently selected destination to personalise."""
    if active_destination:
        d = get_destination(active_destination)
        eyebrow = f"{d['emoji']}  Now planning · {active_destination}"
        headline = f"Plan your trip to<br>{active_destination}, beautifully."
        sub = d["tagline"]
    else:
        eyebrow = "✨  AI-powered travel assistant"
        headline = "Your personal AI<br>travel planner."
        sub = (
            "Tell me where you want to go and your budget — a team of AI agents will "
            "build a day-by-day itinerary, optimise your spend and uncover local gems."
        )

    st.markdown(
        f"""
        <div class="yatra-hero">
            <span class="badge">{eyebrow}</span>
            <h1>{headline}</h1>
            <p class="sub">{sub}</p>
            <div class="hero-stats">
                <div class="hero-stat"><div class="n">17</div><div class="l">Destinations</div></div>
                <div class="hero-stat"><div class="n">6</div><div class="l">AI Agents</div></div>
                <div class="hero-stat"><div class="n">2</div><div class="l">ML Models</div></div>
                <div class="hero-stat"><div class="n">&lt;60s</div><div class="l">To a full plan</div></div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
