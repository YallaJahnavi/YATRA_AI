"""Accommodation Recommender Node - calls Accommodation Recommender ML agent.

Imports: state.TravelPlanState, agents.accommodation_recommender_ml.AccommodationRecommenderMLAgent

Calls AccommodationRecommenderMLAgent.recommend_accommodation() with user_profile dict.
Three variants: low_budget, mid_budget, high_budget (based on budget tier routing).
"""

from state import TravelPlanState
from agents.accommodation_recommender_ml import AccommodationRecommenderMLAgent


# TODO: Implement accommodation_recommender_low_budget_node() function
# - Takes state: TravelPlanState parameter
# - Returns TravelPlanState
# - Create user_profile dict with fields: destination, total_budget_inr, accommodation_budget_inr,
#   trip_duration_days, group_size, primary_interest, secondary_interest, travel_season,
#   destination_cost_tier, interests (list)
# - Create AccommodationRecommenderMLAgent instance
# - Call agent.recommend_accommodation(user_profile)
# - If status == "success": populate state with accommodation_type, accommodation_class,
#   accommodation_confidence, accommodation_comfort_score, estimated_cost_per_night,
#   accommodation_alternatives
# - Set accommodation_recommendations.low_budget with results
# - Return state
# - On exception: append error message, set error_occurred=True


# TODO: Implement accommodation_recommender_mid_budget_node() function
# - Same structure as low_budget variant
# - Appropriate for mid-tier budget constraints
# - Set accommodation_recommendations.mid_budget with results


# TODO: Implement accommodation_recommender_high_budget_node() function
# - Same structure as low_budget variant
# - Appropriate for high-tier budget constraints
# - Set accommodation_recommendations.high_budget with results

# def _run_accommodation_agent(state: TravelPlanState):
#     user_profile={
#         "destination": state.get("destination"),
#         "total_budget_inr":state.get("total_budget_inr"),
#         "accommodation_budget_inr":state.get("budget_allocation",{}).get("accommodation",0),
#         "trip_duration_days": state.get("trip_duration_days"),
#         "group_size": state.get("group_size"),
#         "primary_interest": state.get("primary_interest"),
#         "secondary_interest": state.get("secondary_interest"),
#         "travel_season":state.get("travel_season"),
#         "destination_cost_tier":state.get("destination_cost_tier"),
#         "interests":[
#             state.get("primary_interest"),
#             state.get("secondary_interest")
#         ],
#     }
#     agent = AccommodationRecommenderMLAgent()

#     result = agent.recommend_accommodation(user_profile)

#     if result.get("status")=="success":
#         state["accommodation_type"]=result.get("accommodation_type")
#         state["accommodation_class"]=result.get("accommodation_class")
#         state["accommodation_confidence"]=result.get("confidence")
#         state["accommodation_comfort_score"]=result.get("comfort_score")
#         state["estimated_cost_per_night"]= result.get("estimated_cost_per_night")
#         state["accommodation_alternatives"]=result.get("alternatives",[])
    
#     else:
#         state.setdefault("error_messages",[]).append(
#             result.get("error_message","Accommodation recommendation failed")
#         )
#         state["error_occurred"]=True
#     return result

# def accommodation_recommender_low_budget_node(state: TravelPlanState)-> TravelPlanState:
#     try:
#         result = _run_accommodation_agent(state)

#         state.setdefault("accommodation_recommendations",{})
#         state["accommodation_recommendations"]["low_budget"]=result
#         return state
    
#     except Exception as e:
#         state.setdefault("error_messages",[]).append(str(e))
#         state["error_occurred"]=True
#         return state

# def accommodation_recommender_mid_budget_node(state: TravelPlanState)-> TravelPlanState:
#     try:
#         result = _run_accommodation_agent(state)

#         state.setdefault("accommodation_recommendations",{})
#         state["accommodation_recommendations"]["low_budget"]=result
#         return state
    
#     except Exception as e:
#         state.setdefault("error_messages",[]).append(str(e))
#         state["error_occurred"]=True
#     return state
"""
Accommodation Recommender Node - calls Accommodation Recommender ML agent.
"""

# from state import TravelPlanState
# from agents.accommodation_recommender_ml import AccommodationRecommenderMLAgent


# def _run_accommodation_agent(state: TravelPlanState):

#     user_profile = {
#         "destination": state.get("destination"),
#         "total_budget_inr": state.get("total_budget_inr"),
#         "accommodation_budget_inr": state.get("budget_allocation", {}).get("accommodation", 0),
#         "trip_duration_days": state.get("trip_duration_days"),
#         "group_size": state.get("group_size"),
#         "primary_interest": state.get("primary_interest"),
#         "secondary_interest": state.get("secondary_interest"),
#         "travel_season": state.get("travel_season"),
#         "destination_cost_tier": state.get("destination_cost_tier"),
#         "interests": [
#             state.get("primary_interest"),
#             state.get("secondary_interest"),
#         ],
#     }

#     agent = AccommodationRecommenderMLAgent()

#     result = agent.recommend_accommodation(user_profile)

#     if result.get("status") == "success":

#         state["accommodation_type"] = result.get("accommodation_type")
#         state["accommodation_class"] = result.get("accommodation_class")
#         state["accommodation_confidence"] = result.get("confidence", 0)
#         state["accommodation_comfort_score"] = result.get("comfort_score", 0)

#         # THIS FIXES YOUR ₹0 BUG
#         state["estimated_cost_per_night"] = result.get("estimated_cost_per_night", 0)

#         state["accommodation_alternatives"] = result.get("alternatives", [])

#     else:
#         state.setdefault("error_messages", []).append(
#             result.get("error_message", "Accommodation recommendation failed")
#         )
#         state["error_occurred"] = True

#     return result


# def accommodation_recommender_low_budget_node(state: TravelPlanState) -> TravelPlanState:
#     try:

#         result = _run_accommodation_agent(state)

#         state.setdefault("accommodation_recommendations", {})
#         state["accommodation_recommendations"]["low_budget"] = result

#     except Exception as e:
#         state.setdefault("error_messages", []).append(str(e))
#         state["error_occurred"] = True

#     return state


# def accommodation_recommender_mid_budget_node(state: TravelPlanState) -> TravelPlanState:
#     try:

#         result = _run_accommodation_agent(state)

#         state.setdefault("accommodation_recommendations", {})
#         state["accommodation_recommendations"]["mid_budget"] = result

#     except Exception as e:
#         state.setdefault("error_messages", []).append(str(e))
#         state["error_occurred"] = True

#     return state


# def accommodation_recommender_high_budget_node(state: TravelPlanState) -> TravelPlanState:
#     try:

#         result = _run_accommodation_agent(state)

#         state.setdefault("accommodation_recommendations", {})
#         state["accommodation_recommendations"]["high_budget"] = result

#     except Exception as e:
#         state.setdefault("error_messages", []).append(str(e))
#         state["error_occurred"] = True

#     return state


# def accommodation_recommender_node(state: TravelPlanState) -> TravelPlanState:
#     """
#     Wrapper node that selects correct accommodation recommender
#     based on destination cost tier.
#     """

#     tier = state.get("destination_cost_tier")

#     if tier == "Tier-1":
#         return accommodation_recommender_high_budget_node(state)

#     elif tier == "Tier-2":
#         return accommodation_recommender_mid_budget_node(state)

#     elif tier == "Tier-3":
#         return accommodation_recommender_low_budget_node(state)

#     else:
#         state.setdefault("error_messages", []).append("Invalid destination cost tier")
#         state["error_occurred"] = True
#         return state 

"""
Accommodation Recommender Node
Calls AccommodationRecommenderMLAgent and stores results in workflow state
"""

from state import TravelPlanState
from agents.accommodation_recommender_ml import AccommodationRecommenderMLAgent


def _run_accommodation_agent(state: TravelPlanState):

    user_profile = {
        "destination": state.get("destination"),
        "total_budget_inr": state.get("total_budget_inr"),
        "accommodation_budget_inr": state.get("budget_allocation", {}).get("accommodation", 0),
        "trip_duration_days": state.get("trip_duration_days"),
        "group_size": state.get("group_size"),
        "primary_interest": state.get("primary_interest"),
        "secondary_interest": state.get("secondary_interest"),
        "travel_season": state.get("travel_season"),
        "destination_cost_tier": state.get("destination_cost_tier"),
        "interests": [
            state.get("primary_interest"),
            state.get("secondary_interest"),
        ],
    }

    agent = AccommodationRecommenderMLAgent()

    result = agent.recommend_accommodation(user_profile)

    if result.get("status") == "success":

        state["accommodation_type"] = result.get("accommodation_type", "Mid-range")
        state["accommodation_class"] = result.get("accommodation_class", 1)
        state["accommodation_confidence"] = result.get("confidence", 0)
        state["accommodation_comfort_score"] = result.get("comfort_score", 0)
        state["estimated_cost_per_night"] = result.get("estimated_cost_per_night", 0)
        state["accommodation_alternatives"] = result.get("alternatives", [])

    else:

        state.setdefault("error_messages", []).append(
            result.get("error_message", "Accommodation recommendation failed")
        )

        state["error_occurred"] = True

    return result


def accommodation_recommender_low_budget_node(state: TravelPlanState) -> TravelPlanState:

    try:

        result = _run_accommodation_agent(state)

        state.setdefault("accommodation_recommendations", {})
        state["accommodation_recommendations"]["low_budget"] = result

    except Exception as e:

        state.setdefault("error_messages", []).append(str(e))
        state["error_occurred"] = True

    return state


def accommodation_recommender_mid_budget_node(state: TravelPlanState) -> TravelPlanState:

    try:

        result = _run_accommodation_agent(state)

        state.setdefault("accommodation_recommendations", {})
        state["accommodation_recommendations"]["mid_budget"] = result

    except Exception as e:

        state.setdefault("error_messages", []).append(str(e))
        state["error_occurred"] = True

    return state


def accommodation_recommender_high_budget_node(state: TravelPlanState) -> TravelPlanState:

    try:

        result = _run_accommodation_agent(state)

        state.setdefault("accommodation_recommendations", {})
        state["accommodation_recommendations"]["high_budget"] = result

    except Exception as e:

        state.setdefault("error_messages", []).append(str(e))
        state["error_occurred"] = True

    return state


def accommodation_recommender_node(state: TravelPlanState):

    tier = state.get("destination_cost_tier")

    if tier == "Tier-1":
        return accommodation_recommender_high_budget_node(state)

    elif tier == "Tier-2":
        return accommodation_recommender_mid_budget_node(state)

    elif tier == "Tier-3":
        return accommodation_recommender_low_budget_node(state)

    else:

        state.setdefault("error_messages", []).append("Invalid destination cost tier")
        state["error_occurred"] = True

        return state
