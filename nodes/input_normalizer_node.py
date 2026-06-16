"""Input Normalizer Node - normalizes user preferences.

Imports: state.TravelPlanState

Constants:
  - tier_map: Dict mapping destinations to cost tiers (Tier-1, Tier-2, Tier-3)
  - Accommodation preference rules based on tier
"""

from state import TravelPlanState


# TODO: Implement input_normalizer_node() function
# - Takes state: TravelPlanState parameter
# - Returns TravelPlanState
# - Define tier_map dict with all 17 destinations:
#   * Tier-1 (expensive): Mumbai, Delhi, Goa, Bangalore
#   * Tier-2 (moderate): Udaipur, Varanasi, Kolkata, Lucknow, Agra, Pune, Hyderabad, Jaipur
#   * Tier-3 (affordable): Kerala, Rishikesh, Himachal Pradesh, Rajasthan (non-GT), Northeast India
# - Determine destination_cost_tier from tier_map (default "Tier-2")
# - Set accommodation_preference based on tier:
#   * Tier-1 -> "Mid-range"
#   * Tier-3 -> "Budget"
#   * Tier-2 -> "Mid-range"
# - Normalize interests (primary and secondary):
#   * Collect primary_interest if non-empty
#   * Collect secondary_interest if non-empty and != "None"
#   * Create interests list
# - Build parsed_profile dict with:
#   * destination, trip_duration_days, total_budget_inr, group_size
#   * primary_interest, secondary_interest, travel_season
#   * destination_cost_tier, accommodation_preference, interests list
# - Set state["parsed_profile"] = parsed_profile
# - Return modified state
# - On exception: append error, set error_occurred=True

def input_normalizer_node(state: TravelPlanState)-> TravelPlanState:
  try:
    tier_map={
      "Mumbai": "Tier-1",
      "Delhi":"Tier-1",
      "Goa": "Tier-1",
      "Bangalore": "Tier-1",

      "Udaipur": "Tier-2",
      "Varanasi": "Tier-2",
      "Kolkata": "Tier-2",
      "Lucknow": "Tier-2",
      "Agra":"Tier-2",
      "Pune":"Tier-2",
      "Hyderabad": "Tier-2",
      "Jaipur": "Tier-2",

      "Kerala": "Tier-3",
      "Rishikesh": "Tier-3",
      "Himachal Pradesh": "Tier-3",
      "Rajasthan (non-GT)": "Tier-3",
      "Northeast India": "Tier-3",
    }

    destination= state.get("destination")
    destination_cost_tier = tier_map.get(destination,"Tier-2")

    state["destination_cost_tier"]=destination_cost_tier

    if destination_cost_tier == "Tier-1":
      accommodation_preference = "Mid-range"
    elif destination_cost_tier == "Tier-3":
      accommodation_preference = "Budget"
    else:
      accommodation_preference="Mid-range"

    state["accommodation_preference"]=accommodation_preference

    interests=[]

    primary_interest= state.get("primary_interest")
    secondary_interest = state.get("secondary_interest")

    if primary_interest:
      interests.append(primary_interest)

    if secondary_interest and secondary_interest != "None":
      interests.append(secondary_interest)

    parsed_profile={
      "destination": state.get("destination"),
      "trip_duration_days": state.get("trip_duration_days"),
      "total_budget_inr": state.get("total_budget_inr"),
      "group_size":state.get("group_size"),
      "primary_interest": primary_interest,
      "secondary_interest": secondary_interest,
      "travel_season": state.get("travel_season"),
      "destination_cost_tier": destination_cost_tier,
      "accommodation_preference":accommodation_preference,
      "interests":interests,
    }

    state["parsed_profile"]=parsed_profile

    return state

  except Exception as e:
    state.setdefault("error_messages",[]).append(str(e))
    state["error_occurred"]=True

    return state
