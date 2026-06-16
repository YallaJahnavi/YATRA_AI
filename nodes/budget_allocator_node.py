"""Budget Allocator Node - calls Budget Allocator ML agent.

Imports: state.TravelPlanState, agents.budget_allocator_ml.BudgetAllocatorMLAgent

Calls BudgetAllocatorMLAgent.allocate_budget() with trip_profile dict.
Populates all budget-related state fields from ML model predictions.
"""

from state import TravelPlanState
from agents.budget_allocator_ml import BudgetAllocatorMLAgent


# TODO: Implement budget_allocator_node() function
# - Takes state: TravelPlanState parameter
# - Returns TravelPlanState
# - Create trip_profile dict with fields: destination, trip_duration_days, total_budget_inr,
#   group_size, primary_interest, secondary_interest, travel_season, accommodation_preference,
#   destination_cost_tier
# - Create BudgetAllocatorMLAgent instance
# - Call agent.allocate_budget(trip_profile)
# - If status == "success": populate state with:
#   * accommodation_budget_pct, food_dining_budget_pct, activities_attractions_budget_pct,
#     local_transport_budget_pct, shopping_misc_budget_pct, contingency_budget_pct (floats)
#   * budget_allocation dict with all category amounts
#   * daily_budget, per_person_budget, per_person_daily (floats)
# - Return state
# - On exception: append error message, set error_occurred=True, use fallback percentages

def budget_allocator_node(state: TravelPlanState)-> TravelPlanState:
    try:
        trip_profile={
            "destination":state.get("destination"),
            "trip_duration_days":state.get("trip_duration_days"),
            "total_budget_inr":state.get("total_budget_inr"),
            "group_size":state.get("group_size"),
            "primary_interest":state.get("primary_interest"),
            "secondary_interest":state.get("secondary_interest"),
            "travel_season":state.get("travel_season"),
            "accommodation_preference": state.get("accommodation_preference"),
            "destination_cost_tier": state.get("destination_cost_tier"),
        }

        agent = BudgetAllocatorMLAgent()

        result = agent.allocate_budget(trip_profile)

        if result.get("status")=="success":
            state["accommodation_budget_pct"]=result.get("accommodation_budget_pct")
            state["food_dining_budget_pct"]=result.get("food_dining_budget_pct")
            state["activities_attractions_budget_pct"]=result.get("activities_attractions_budget_pct")
            state["local_transport_budget_pct"]=result.get("local_transport_budget_pct")
            state["shopping_misc_budget_pct"]=result.get("shopping_misc_budget_pct")
            state["contingency_budget_pct"]=result.get("contingency_budget_pct")

            state["budget_allocation"]=result.get("budget_allocation",{})

            state["daily_budget"]=result.get("daily_budget")
            state["per_person_budget"]=result.get("per_person_budget")
            state["per_person_daily"]=result.get("per_person_daily")
        
        else:
            state.setdefault("error_messages",[]).append(
                result.get("error_message","Budget allocation failed")
            )
            state["error_occurred"]=True
        return state
    except Exception as e:
        state.setdefault("error_messages",[]).append(str(e))
        state["error_occurred"]=True

        state["budget_allocation"]={}
        state["daily_budget"]=0

        return state
    

    
