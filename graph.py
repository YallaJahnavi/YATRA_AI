"""Main graph execution for YatraAI.

Imports: datetime.datetime, typing.Dict, typing.Any, uuid.uuid4,
workflow.workflow (build_trip_planning_graph, get_workflow_structure),
state (TravelPlanState, get_initial_state)
"""

from datetime import datetime
from typing import Dict, Any
from uuid import uuid4
from workflow.workflow import build_trip_planning_graph, get_workflow_structure
from state import TravelPlanState, get_initial_state


# TODO: Implement plan_trip() function
# - Takes parameters: destination, trip_duration_days, total_budget_inr, group_size,
#   primary_interest, secondary_interest, travel_season (all as specified)
# - Returns Dict[str, Any]
# - Create form_data dict from all input parameters
# - Initialize state using get_initial_state(form_data)
# - Add plan_id (str from uuid4()) and analysis_timestamp (current ISO format)
# - Build graph using build_trip_planning_graph()
# - Try-except block:
#   * Execute workflow: final_state = graph.invoke(state)
#   * Set plan_generated = True
#   * Return final_state
#   * On exception: set error_occurred = True, append error message, plan_generated = False, return state


# TODO: Implement get_trip_summary() function
# - Takes assessment_result: Dict[str, Any] parameter
# - Returns Dict[str, Any] with summary structure:
#   * user_profile: destination, trip_duration, total_budget, group_size, interests, travel_season
#   * budget_summary: all budget percentages and daily_budget
#   * accommodation: type, confidence, estimated_cost_per_night
#   * itinerary_status: itinerary_analysis_complete bool
#   * local_insights_status: insights_analysis_complete bool
#   * booking_strategy_status: booking_analysis_complete bool
#   * system: plan_id, timestamp, plan_generated, errors list


# TODO: Implement get_workflow_info() function
# - Returns Dict[str, Any]
# - Call get_workflow_structure() from workflow module
# - Return the result
def plan_trip(
    destination:str,
    trip_duration_days:int,
    total_budget_inr:int,
    group_size:int,
    primary_interest:str,
    secondary_interest:str,
    travel_season:str,
    ) -> Dict[str,Any]:

    form_data={
    "destination":destination,
    "trip_duration_days":trip_duration_days,
    "total_budget_inr":total_budget_inr,
    "group_size":group_size,
    "primary_interest":primary_interest,
    "secondary_interest":secondary_interest,
    "travel_season":travel_season,
    }
    state =get_initial_state(form_data)
    state["plan_id"]=str(uuid4())
    state["analysis_timestamp"]=datetime.utcnow().isoformat()
    graph=build_trip_planning_graph()
    try:
        final_state=graph.invoke(state)
        final_state["plan_generated"]=True 
        return final_state 
    except Exception as e:
        state["error_occurred"]=True 
        state.setdefault("error_messages",[]).append(str(e))
        state["plan_generated"]=False

        return state 
def get_trip_summary(assessment_result:Dict[str,Any])-> Dict[str,Any]:
    return{
        "user_profile":{
            "destination":assessment_result.get("destination"),
            "trip_duration":assessment_result.get("trip_duration_days"),
            "total_budget":assessment_result.get("total_budget_inr"),
            "group_size":assessment_result.get("group_size"),
            "interests":[
                assessment_result.get("primary_interest"),
                assessment_result.get("secondary_interest"),

            ],
            "travel_season":assessment_result.get("travel_season"),

        },
        "budget_summary":{
            "accommodation_pct":assessment_result.get("accommodation_budget_pct"),
            "food_pct":assessment_result.get("food_dining_budget_pct"),
            "activities_pct":assessment_result.get("activities_attractions_budget_pct"),
            "transport_pct":assessment_result.get("local_transport_budget_pct"),
            "shopping_pct":assessment_result.get("shopping_misc_budget_pct"),
            "contingency_pct":assessment_result.get("contingency_budget_pct"),
            "daily_budget":assessment_result.get("daily_budget"),
        },
        "accommodation":{
            "type":assessment_result.get("accommodation_type"),
            "confidence":assessment_result.get("accommodation_confidence"),
            "estimated_cost_per_night":assessment_result.get("estimated_cost_per_night"),

        },
        "itinerary_status":assessment_result.get("itinerary_analysis_complete"),
        "local_insights_status":assessment_result.get("insights_analysis_complete"),
        "booking_strategy_status":assessment_result.get("booking_analysis_complete"),
        "system":{
            "plan_id":assessment_result.get("plan_id"),
            "timestamp":assessment_result.get("analysis_timestamp"),
            "plan_generated":assessment_result.get("plan_generated"),
            "errors":assessment_result.get("error_messages",[]),

        },

    }
def get_workflow_info() -> Dict[str,Any]:
    return get_workflow_structure()
