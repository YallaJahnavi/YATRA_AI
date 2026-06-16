from state import TravelPlanState
from agents.itinerary_generator_llm import ItineraryGeneratorLLMAgent
from utils.gemini_client import build_gemini_client

def itinerary_generator_node(state: TravelPlanState) -> TravelPlanState:
    try:
        client = build_gemini_client()
        agent = ItineraryGeneratorLLMAgent(client)

        trip_profile = {
            "destination": state.get("destination"),
            "trip_duration_days": state.get("trip_duration_days"),
            "total_budget_inr": state.get("total_budget_inr"),
            "group_size": state.get("group_size"),
            "primary_interest": state.get("primary_interest"),
            "secondary_interest": state.get("secondary_interest"),
            "travel_season": state.get("travel_season"),
            "accommodation_type": state.get("accommodation_type"),
            "daily_budget": state.get("daily_budget")
        }

        result = agent.generate_itinerary(trip_profile)

        if result.get("status") == "success":
            itinerary = result.get("itinerary", {})

            if not isinstance(itinerary, dict):
                raise ValueError("Itinerary is not dict")

            state["itinerary"] = itinerary
            state["trip_highlights"] = result.get("trip_highlights", [])
            state["contingency_plans"] = result.get("contingency_plans", [])
            state["itinerary_tips"] = result.get("tips_for_success", [])

            state["itinerary_analysis_complete"] = True
            state["error_occurred"] = False
        else:
            raise ValueError(result.get("error_message"))

    except Exception as e:
        state.setdefault("error_messages", []).append(str(e))
        state["error_occurred"] = True
        state["itinerary_analysis_complete"] = False

    return state
