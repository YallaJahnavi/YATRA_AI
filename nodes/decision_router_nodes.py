"""Decision Router Nodes - Pure logic nodes for routing workflow paths.

Imports: state.TravelPlanState

Constants:
  - Budget thresholds (in INR daily): 7000 (low/mid), 15000 (mid/high)
  - Complexity weights: trip_duration 40%, group_size 30%, interests 30%
  - Complexity threshold: 0.7
"""

from state import TravelPlanState


# TODO: Implement budget_feasibility_router() function
# - Takes state: TravelPlanState parameter
# - Returns TravelPlanState
# - Extract daily_budget from state
# - Set daily_budget_tier based on thresholds:
#   * If daily_budget < 7000 -> "low_budget_path"
#   * If 7000 <= daily_budget < 15000 -> "mid_budget_path"
#   * If daily_budget >= 15000 -> "high_budget_path"
# - Return modified state
# - On exception: set error_occurred=True, error message, default tier to "mid_budget_path"


# TODO: Implement trip_complexity_analyzer() function
# - Takes state: TravelPlanState parameter
# - Returns TravelPlanState
# - Extract trip_duration_days and group_size from state
# - Count interests: 1 for primary_interest + 1 for secondary (if non-empty/"None")
# - Normalize values:
#   * duration_normalized = min(trip_duration_days / 30.0, 1.0)
#   * group_normalized = min(group_size / 10.0, 1.0)
#   * interests_normalized = interests_count / 2.0
# - Calculate complexity_score = (duration_normalized * 0.4) + (group_normalized * 0.3) + (interests_normalized * 0.3)
# - Set state["complexity_score"] = complexity_score
# - Return modified state
# - On exception: set error_occurred=True, error message, default score to 0.5
def budget_feasibility_router(state: TravelPlanState)-> TravelPlanState:

  try:
    daily_budget = state.get("daily_budget",0)

    if daily_budget < 7000:
      state["daily_budget_tier"]="low_budget_path"
    
    elif 7000 <= daily_budget < 15000:
      state["daily_budget_tier"]="mid_budget_path"
    
    else:
      state["daily_budget_tier"]="high_budget_path"
    
    return state


  
  except Exception as e:
    state["error_occurred"]=True
    state.setdefault("error_messages",[]).append(str(e))
    state["daily_budget_tier"]="mid_budget_path"

    return state

def trip_complexity_analyzer(state: TravelPlanState)-> TravelPlanState:
  try:
    trip_duration = state.get("trip_duration_days",0)
    group_size=state.get("group_size",1)

    primary_interest = state.get("primary_interest")
    secondary_interest=state.get("secondary_interest")

    interests_count =1

    if secondary_interest and secondary_interest != "None":
      interests_count+=1
    
    duration_normalized = min(trip_duration/30.0,1.0)
    group_normalized=min(group_size/10.0,1.0)
    interests_normalized = interests_count/2.0

    complexity_score=(
      duration_normalized * 0.4
      + group_normalized * 0.3
      + interests_normalized * 0.3
    )

    state["complexity_score"]=complexity_score
    return state
  
  except Exception as e:
    state["error_occurred"]= True
    state.setdefault("error_messages",[]).append(str(e))
    state["complexity_score"]=0.5

    return state
