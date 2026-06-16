"""Chat-first AI travel assistant.

This is the primary way users interact with YatraAI. A user types a natural
request ("7-day adventure trip to Jaipur under 50k"); we parse it (ui.nlu),
run the existing LangGraph workflow (graph.plan_trip), store the result in
session state for the result tabs, and reply with a conversational summary.

The sidebar form remains as a secondary / manual path; both paths populate the
same st.session_state.assessment_result.
"""

from typing import Dict, Any, List

import streamlit as st

from graph import plan_trip
from ui.nlu import parse_trip_request
from ui.destinations import get_destination

# Which workflow nodes map to which user-facing "agent" — used for the
# live agent-activity strip so the agentic architecture is visible.
AGENT_TIMELINE: List[str] = [
    "🧭 Planner Agent — parsing your request",
    "💰 Budget Agent — optimising your spend",
    "🏨 Stay Agent — matching accommodation",
    "🗺️ Route Agent — sequencing the days",
    "🔎 Recommendation Agent — finding local gems",
    "📋 Booking Agent — building your checklist",
]

STARTERS = [
    "7-day adventure trip to Jaipur under ₹50,000 for 2 people",
    "Relaxing 5-day beach holiday in Goa for a couple",
    "Spiritual 4-day trip to Varanasi on a tight budget",
    "Family heritage tour of Agra & Delhi for 6 days",
]


def _ensure_state() -> None:
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    if "pending_prompt" not in st.session_state:
        st.session_state.pending_prompt = None


def _summarise_plan(result: Dict[str, Any], parsed: Dict[str, Any]) -> str:
    """Build the assistant's natural-language reply from a generated plan."""
    dest = result.get("destination", parsed.get("destination", "your destination"))
    d = get_destination(dest)
    days = result.get("trip_duration_days", parsed.get("trip_duration_days"))
    budget = result.get("total_budget_inr", parsed.get("total_budget_inr", 0))
    group = result.get("group_size", parsed.get("group_size"))
    acc = result.get("accommodation_type")
    daily = result.get("daily_budget", 0)

    if result.get("error_occurred") and not result.get("itinerary"):
        errs = result.get("error_messages", [])
        detail = errs[0] if errs else "something went wrong while planning"
        return (
            f"I hit a snag building your **{dest}** plan — {detail}. "
            "You can tweak the details in the planner panel on the left and try again."
        )

    lines = [
        f"{d['emoji']} Here's your **{days}-day {dest}** plan for **{group}** "
        f"traveller(s) on a **₹{budget:,.0f}** budget.",
        "",
        f"- **Best time to visit:** {d['best_season']}",
    ]
    if acc:
        lines.append(f"- **Recommended stay:** {acc}" + (f" · ~₹{daily:,.0f}/day total" if daily else ""))

    highlights = result.get("trip_highlights") or []
    if highlights:
        lines.append("- **Trip highlights:** " + ", ".join(str(h) for h in highlights[:3]))

    itinerary = result.get("itinerary") or {}
    if isinstance(itinerary, dict) and itinerary:
        first_key = next(iter(itinerary))
        first = itinerary[first_key]
        if isinstance(first, dict):
            title = first.get("title", "")
            lines.append(f"- **Day 1 kicks off with:** {title}")

    lines += [
        "",
        "I've laid out the full breakdown below — **itinerary, budget, stays, local insights "
        "and a booking checklist**. Ask me to adjust anything (budget, pace, interests) and I'll replan.",
    ]
    return "\n".join(lines)


def _run_plan(parsed: Dict[str, Any]) -> Dict[str, Any]:
    """Invoke the backend workflow with the parsed parameters."""
    form_data = {k: parsed[k] for k in (
        "destination", "trip_duration_days", "total_budget_inr", "group_size",
        "primary_interest", "secondary_interest", "travel_season",
    )}
    return plan_trip(**form_data)


def handle_user_message(text: str, defaults: Dict[str, Any]) -> None:
    """Parse, plan, and append the exchange to chat history."""
    st.session_state.chat_history.append({"role": "user", "content": text})

    parsed = parse_trip_request(text, defaults=defaults)

    # If we couldn't even identify a destination, ask instead of guessing.
    if "destination" in parsed.get("_missing", []) and not parsed.get("destination"):
        st.session_state.chat_history.append({
            "role": "assistant",
            "content": (
                "I'd love to plan that! **Which destination** did you have in mind? "
                "I currently cover 17 places across India — try Jaipur, Goa, Kerala, Varanasi, and more."
            ),
        })
        return

    with st.spinner("Your AI travel team is planning…"):
        result = _run_plan(parsed)

    st.session_state.assessment_result = result
    st.session_state.active_destination = parsed.get("destination")
    st.session_state.chat_history.append({
        "role": "assistant",
        "content": _summarise_plan(result, parsed),
    })


def render_chat(defaults: Dict[str, Any]) -> None:
    """Render the conversational assistant. `defaults` come from the sidebar form."""
    _ensure_state()

    # Greeting + starter chips when the conversation is empty
    if not st.session_state.chat_history:
        with st.chat_message("assistant", avatar="🧭"):
            st.markdown(
                "Hi, I'm **Yatra** — your AI travel planner. Tell me about the trip you're "
                "dreaming of and I'll build the whole thing. Try one of these:"
            )
        cols = st.columns(2)
        for i, starter in enumerate(STARTERS):
            if cols[i % 2].button(starter, key=f"starter_{i}", use_container_width=True):
                st.session_state.pending_prompt = starter
                st.rerun()

    # Replay history
    for msg in st.session_state.chat_history:
        avatar = "🧭" if msg["role"] == "assistant" else "🧑‍💻"
        with st.chat_message(msg["role"], avatar=avatar):
            st.markdown(msg["content"])

    # Input (a queued starter click takes priority)
    typed = st.chat_input("Describe your trip — destination, days, budget, vibe…")
    prompt = st.session_state.pending_prompt or typed
    st.session_state.pending_prompt = None

    if prompt:
        handle_user_message(prompt, defaults)
        st.rerun()
