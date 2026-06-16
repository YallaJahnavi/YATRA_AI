"""Booking Strategy Node - calls Booking Strategy LLM agent.

Imports: state.TravelPlanState, agents.booking_strategy_llm.BookingStrategyLLMAgent,
utils.gemini_client.build_gemini_client

Calls BookingStrategyLLMAgent.get_booking_strategy() with trip_profile.
Populates booking and logistics state fields from LLM output.
"""

from state import TravelPlanState
from agents.booking_strategy_llm import BookingStrategyLLMAgent
from utils.gemini_client import build_gemini_client


# TODO: Implement booking_strategy_node() function
# - Takes state: TravelPlanState parameter
# - Returns TravelPlanState
# - Build Gemini client using build_gemini_client()
# - Create BookingStrategyLLMAgent instance with client
# - Create trip_profile dict with fields: destination, trip_duration_days, total_budget_inr,
#   group_size, primary_interest, secondary_interest, travel_season, accommodation_type,
#   accommodation_budget_inr
# - Call agent.get_booking_strategy(trip_profile)
# - If status == "success": populate state with:
#   * flight_booking_strategy, accommodation_booking_strategy, activity_booking_strategy (dicts)
#   * logistics_planning (dict with visa_requirements, travel_insurance, vaccinations)
#   * packing_checklist, pre_departure_checklist (dicts)
#   * money_saving_tips_summary, budget_optimization_tips (lists)
#   * emergency_contingency_plans (dict)
#   * booking_checklist: extract from pre_departure_checklist
#   * visa_requirements: extract from logistics_planning
#   * booking_analysis_complete: True
# - If not success: append error, set error_occurred=True, booking_analysis_complete=False
# - Return state
# - On exception: append error, set error_occurred=True, booking_analysis_complete=False

def booking_strategy_node(state: TravelPlanState) -> TravelPlanState:
    try:
        client = build_gemini_client()
        agent = BookingStrategyLLMAgent(client)

        trip_profile = {
            "destination": state.get("destination"),
            "trip_duration_days": state.get("trip_duration_days"),
            "total_budget_inr": state.get("total_budget_inr"),
            "group_size": state.get("group_size"),
            "primary_interest": state.get("primary_interest"),
            "secondary_interest": state.get("secondary_interest"),
            "travel_season": state.get("travel_season"),
            "accommodation_type": state.get("accommodation_type"),
            "accommodation_budget_inr": state.get("budget_allocation", {}).get("accommodation", 0),
        }

        result = agent.get_booking_strategy(trip_profile)

        if not isinstance(result, dict):
            raise ValueError("Invalid booking response")

        if result.get("status") == "success":

            # ✅ FIXED KEYS
            state["flight_booking_strategy"] = result.get("flight_booking_strategy", {})
            state["accommodation_booking_strategy"] = result.get("accommodation_booking_strategy", {})
            state["activity_booking_strategy"] = result.get("activity_booking_strategy", {})

            logistics = result.get("logistics_planning", {})

            state["visa_requirements"] = logistics.get("visa_requirements", {})
            state["packing_checklist"] = result.get("packing_checklist", {})
            state["emergency_contingency_plans"] = result.get("emergency_contingency_plans", {})

            pre_departure = result.get("pre_departure_checklist", {})

            state["booking_checklist"] = (
                pre_departure.get("one_month_before", []) +
                pre_departure.get("one_week_before", [])
            )

            state["budget_optimization_tips"] = result.get("money_saving_tips_summary", [])

            # ✅ FIXED NAME
            state["booking_analysis_complete"] = True
            state["error_occurred"] = False

        else:
            state.setdefault("error_messages", []).append(
                result.get("error_message", "Booking strategy failed")
            )
            state["error_occurred"] = True
            state["booking_analysis_complete"] = False

        return state

    except Exception as e:
        state.setdefault("error_messages", []).append(str(e))
        state["error_occurred"] = True
        state["booking_analysis_complete"] = False
        return state
