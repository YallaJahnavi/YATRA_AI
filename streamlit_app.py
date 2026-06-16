import streamlit as st
from datetime import datetime
from graph import plan_trip, get_trip_summary
from ml.evaluation.evaluate_models import evaluate_all_models
from utils.constants import (
    DESTINATIONS, INTERESTS, SECONDARY_INTERESTS, TRAVEL_SEASONS,
    BUDGET_MIN, BUDGET_MAX, BUDGET_STEP, BUDGET_DEFAULT,
    TRIP_DURATION_MIN, TRIP_DURATION_MAX, TRIP_DURATION_DEFAULT,
    GROUP_SIZE_MIN, GROUP_SIZE_MAX, GROUP_SIZE_DEFAULT,
)
from ui.theme import inject_theme, section_header
from ui.hero import render_hero
from ui.chat import render_chat
from ui.insights import render_destination_spotlight
from ui.destinations import get_destination
from ui.itinerary_cards import render_itinerary
from ui.maps import render_trip_map
from ui.analytics import render_budget_dashboard
from ui.hotels import render_hotels
from ui.weather import render_weather

# Travel-companion presets -> implied group size
COMPANION_GROUP = {"Solo": 1, "Couple": 2, "Family": 4, "Friends": 4}
# Travel-style presets -> a sensible default total budget (INR)
STYLE_BUDGET = {"Budget": 30000, "Mid-range": 60000, "Luxury": 150000}


def initialize_session_state():
    if "assessment_result" not in st.session_state:
        st.session_state.assessment_result = None

    if "eval_results" not in st.session_state:
        st.session_state.eval_results = None

    if "active_destination" not in st.session_state:
        st.session_state.active_destination = ""


def setup_page():
    st.set_page_config(
        page_title="YatraAI · AI Travel Planner",
        page_icon="🧭",
        layout="wide",
        initial_sidebar_state="expanded",
    )
    inject_theme()


def display_input_form():
    """Smart input panel — modern pill controls. Returns the 7 plan_trip params;
    extra preferences (companion / style / transport) are stashed in session_state."""
    sb = st.sidebar

    sb.markdown("### 🧳 Smart trip builder")
    sb.caption("Set your vibe here — or just chat with Yatra. Both build the same plan.")

    # --- Destination (type to search) ---
    destination = sb.selectbox("📍 Destination", DESTINATIONS, format_func=lambda x: f"{get_destination(x)['emoji']}  {x}")

    # --- Who's travelling -> group size ---
    companion = sb.pills("👥 Who's travelling", list(COMPANION_GROUP.keys()), default="Couple") or "Couple"
    implied = COMPANION_GROUP[companion]
    group_size = sb.number_input(
        "Travellers", min_value=GROUP_SIZE_MIN, max_value=GROUP_SIZE_MAX,
        value=implied, key=f"travellers_{companion}",
    )

    # --- Travel style -> default budget ---
    style = sb.pills("✨ Travel style", list(STYLE_BUDGET.keys()), default="Mid-range") or "Mid-range"
    total_budget = sb.slider(
        "💸 Total budget (₹)", BUDGET_MIN, BUDGET_MAX,
        value=STYLE_BUDGET[style], step=BUDGET_STEP, key=f"budget_{style}",
    )

    # --- Duration ---
    trip_duration = sb.slider(
        "🗓️ Trip duration (days)", TRIP_DURATION_MIN, TRIP_DURATION_MAX, TRIP_DURATION_DEFAULT,
    )

    # --- Interests (multi) -> primary + secondary ---
    selected = sb.pills("🎯 Interests", INTERESTS, selection_mode="multi", default=[INTERESTS[0]]) or [INTERESTS[0]]
    primary_interest = selected[0]
    secondary_interest = selected[1] if len(selected) > 1 else ""

    # --- Preferred transport (preference only; surfaced to the agents/UI) ---
    transport = sb.pills("🚆 Preferred transport", ["Flight", "Train", "Road trip", "Mixed"], default="Mixed") or "Mixed"

    # --- Season ---
    travel_season = sb.pills("🌤️ Season", TRAVEL_SEASONS, default="Moderate") or "Moderate"

    # stash soft preferences for the insights / agent-activity panels
    st.session_state.travel_prefs = {
        "companion": companion, "style": style, "transport": transport,
    }

    return {
        "destination": destination,
        "trip_duration_days": trip_duration,
        "total_budget_inr": total_budget,
        "group_size": group_size,
        "primary_interest": primary_interest,
        "secondary_interest": secondary_interest,
        "travel_season": travel_season,
    }


def display_overview_tab(assessment):
    st.subheader("Trip Overview")

    rupee = "₹"

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Destination", assessment.get("destination", "N/A"))

    duration = assessment.get("trip_duration_days", 0)
    col2.metric("Duration", f"{duration} days")

    budget = assessment.get("total_budget_inr", 0)
    col3.metric("Total Budget", f"{rupee}{budget:,.0f}")

    group = assessment.get("group_size", 1)
    col4.metric("Group Size", f"{group} people")

    st.divider()

    colA, colB = st.columns(2)

    with colA:
        st.subheader("Trip Preferences")
        st.write(f"Primary Interest: {assessment.get('primary_interest','N/A')}")
        st.write(f"Secondary Interest: {assessment.get('secondary_interest','None')}")
        st.write(f"Travel Season: {assessment.get('travel_season','N/A')}")

    with colB:
        st.subheader("Accommodation")

        st.write(f"Type: {assessment.get('accommodation_type','N/A')}")

        confidence = assessment.get("accommodation_confidence", 0)
        if confidence <= 1:
            confidence *= 100
        st.write(f"Confidence: {confidence:.1f}%")

        cost = assessment.get("estimated_cost_per_night", 0)
        st.write(f"Est. Cost/Night: {rupee}{cost:,.0f}")


def display_budget_tab(assessment):
    st.subheader("💰 Budget Analytics")
    render_budget_dashboard(assessment)


def display_accommodation_tab(assessment):
    st.subheader("🏨 Accommodation")
    render_hotels(assessment)


def display_weather_tab(assessment):
    st.subheader("🌤️ Weather Intelligence")
    render_weather(assessment)


def display_itinerary_tab(assessment):
    st.subheader("📍 Day-by-Day Itinerary")
    render_itinerary(
        assessment.get("itinerary"),
        assessment.get("destination", ""),
        assessment.get("daily_budget", 0),
    )


def display_map_tab(assessment):
    st.subheader("🗺️ Trip Map & Route")
    render_trip_map(
        assessment.get("destination", ""),
        assessment.get("itinerary"),
    )


def display_insights_tab(assessment):
    st.subheader("Local Insights")

    for section in [
        "hidden_gems", "local_food_spots", "neighborhoods_to_explore",
        "free_or_cheap_attractions", "money_saving_hacks", "avoid_tourist_traps"
    ]:
        st.markdown(f"### {section.replace('_',' ').title()}")
        for item in assessment.get(section, []):
            st.write(f"• {item}")

def display_booking_tab(assessment):
    import streamlit as st

    st.subheader("📌 Booking Strategy")

    flight = assessment.get("flight_booking_strategy", {})
    hotel = assessment.get("accommodation_booking_strategy", {})
    activity = assessment.get("activity_booking_strategy", {})
    logistics = assessment.get("visa_requirements", {})
    tips = assessment.get("budget_optimization_tips", [])
    checklist = assessment.get("booking_checklist", [])

    # ✈️ Flight Booking
    st.markdown("### ✈️ Flight Booking")
    if isinstance(flight, dict):
        for k, v in flight.items():
            st.markdown(f"**{k.replace('_',' ').title()}**")
            if isinstance(v, list):
                for item in v:
                    st.write(f"• {item}")
            else:
                st.write(v)

    # 🏨 Accommodation Booking
    st.markdown("### 🏨 Accommodation Booking")
    if isinstance(hotel, dict):
        for k, v in hotel.items():
            st.markdown(f"**{k.replace('_',' ').title()}**")
            if isinstance(v, list):
                for item in v:
                    st.write(f"• {item}")
            else:
                st.write(v)

    # 🎟️ Activity Booking
    st.markdown("### 🎟️ Activity Booking")
    if isinstance(activity, dict):
        for k, v in activity.items():
            st.markdown(f"**{k.replace('_',' ').title()}**")
            if isinstance(v, list):
                for item in v:
                    st.write(f"• {item}")
            else:
                st.write(v)

    # 🛂 Logistics
    st.markdown("### 🛂 Travel Logistics")
    if isinstance(logistics, dict):
        for k, v in logistics.items():
            st.write(f"**{k.replace('_',' ').title()}**: {v}")

    # 💰 Money Saving Tips
    st.markdown("### 💰 Money Saving Tips")
    if tips:
        for t in tips:
            st.write(f"• {t}")

    # ✅ Checklist
    st.markdown("### ✅ Booking Checklist")
    if checklist:
        for c in checklist:
            st.write(f"• {c}")


def display_model_evaluation_tab():
    import streamlit as st

    st.header("📊 Model Evaluation")

    if st.button("Load Evaluation"):
        try:
            st.session_state.eval_results = evaluate_all_models()
        except Exception as e:
            st.error(str(e))

    results = st.session_state.eval_results
    if not results:
        return

    if results.get("status") != "success":
        st.error(f"❌ Evaluation failed: {results.get('error_message')}")
        return

    budget_model = results.get("budget_allocator", {})
    acc_model = results.get("accommodation_recommender", {})

    # 🔥 Budget Model
    st.markdown("### 💰 Budget Allocator Model")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("MAPE", f"{budget_model.get('MAPE',0):.2f}")
    col2.metric("RMSE", f"{budget_model.get('RMSE',0):.2f}")
    col3.metric("MAE", f"{budget_model.get('MAE',0):.2f}")
    col4.metric("R² Score", f"{budget_model.get('R2',0):.2f}")

    st.write(f"📊 Samples Used: {budget_model.get('samples',0)}")

    st.divider()

    # 🔥 Accommodation Model
    st.markdown("### 🏨 Accommodation Recommender Model")

    col1, col2 = st.columns(2)

    col1.metric("Accuracy", f"{acc_model.get('accuracy',0)*100:.1f}%")

    # Optional extra metrics if exist
    precision = acc_model.get("precision")
    recall = acc_model.get("recall")

    if precision is not None:
        col2.metric("Precision", f"{precision*100:.1f}%")
    if recall is not None:
        st.metric("Recall", f"{recall*100:.1f}%")

    st.divider()

    # 🔥 Interpretation (INTERVIEW GOLD ⭐)
    st.markdown("### 📌 Model Insights")

    if budget_model.get("R2", 0) > 0.8:
        st.success("Budget model performs very well (high accuracy)")
    else:
        st.warning("Budget model may need improvement")

    if acc_model.get("accuracy", 0) > 0.8:
        st.success("Accommodation model is highly accurate")
    else:
        st.warning("Accommodation model accuracy is moderate")

def render_sidebar_actions(user_input):
    """Manual planning controls in the sidebar (secondary to the chat)."""
    st.sidebar.markdown("---")
    if st.sidebar.button("⚡ Generate Plan", type="primary", use_container_width=True):
        with st.spinner("Building your plan…"):
            result = plan_trip(**user_input)
        st.session_state.assessment_result = result
        st.session_state.active_destination = user_input.get("destination", "")
        st.rerun()

    if st.sidebar.button("🗑 Clear", use_container_width=True):
        st.session_state.assessment_result = None
        st.session_state.chat_history = []
        st.session_state.active_destination = ""
        st.rerun()


def render_results(assessment):
    """The full plan breakdown, shown once a plan exists."""
    section_header(
        "Your AI travel plan",
        "itinerary · budget · stays · insights · booking",
        icon="🧭",
    )
    tabs = st.tabs([
        "Overview", "Budget", "Accommodation",
        "Itinerary", "Map", "Weather", "Insights", "Booking", "Evaluation"
    ])

    with tabs[0]: display_overview_tab(assessment)
    with tabs[1]: display_budget_tab(assessment)
    with tabs[2]: display_accommodation_tab(assessment)
    with tabs[3]: display_itinerary_tab(assessment)
    with tabs[4]: display_map_tab(assessment)
    with tabs[5]: display_weather_tab(assessment)
    with tabs[6]: display_insights_tab(assessment)
    with tabs[7]: display_booking_tab(assessment)
    with tabs[8]: display_model_evaluation_tab()


def main():
    setup_page()
    initialize_session_state()

    # Sidebar = secondary manual planner
    user_input = display_input_form()
    render_sidebar_actions(user_input)

    # Hero (personalises to the active destination once one is chosen)
    render_hero(st.session_state.get("active_destination", ""))

    st.write("")

    # Destination insights react live to the sidebar selection
    render_destination_spotlight(user_input["destination"])

    st.write("")

    # Chat-first AI assistant is the primary interaction
    section_header(
        "Chat with Yatra",
        "your AI travel assistant — describe your trip in plain words",
        icon="💬",
    )
    render_chat(defaults=user_input)

    # Results appear below the conversation once a plan is generated
    assessment = st.session_state.assessment_result
    if assessment:
        st.write("")
        render_results(assessment)


if __name__ == "__main__":
    main()
