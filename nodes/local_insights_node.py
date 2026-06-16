"""Local Insights Node - calls Local Insights LLM agent.

Imports: state.TravelPlanState, agents.local_insights_llm.LocalInsightsLLMAgent,
utils.gemini_client.build_gemini_client

Calls LocalInsightsLLMAgent.get_local_insights() with trip_profile and itinerary.
Populates local insights state fields from LLM output.
"""

from state import TravelPlanState
from agents.local_insights_llm import LocalInsightsLLMAgent
from utils.gemini_client import build_gemini_client


# TODO: Implement local_insights_node() function
# - Takes state: TravelPlanState parameter
# - Returns TravelPlanState
# - Build Gemini client using build_gemini_client()
# - Create LocalInsightsLLMAgent instance with client
# - Create trip_profile dict with fields: destination, trip_duration_days, total_budget_inr,
#   group_size, primary_interest, secondary_interest, travel_season, accommodation_type
# - Get itinerary from state
# - Call agent.get_local_insights(trip_profile, itinerary)
# - If status == "success": populate state with:
#   * hidden_gems, local_food_spots, neighborhoods_to_explore (lists)
#   * local_etiquette_tips, money_saving_hacks, free_or_cheap_attractions,
#     avoid_tourist_traps (lists)
#   * best_times_to_avoid_crowds (dict)
#   * insights_analysis_complete: True
# - If not success: append error, set error_occurred=True, insights_analysis_complete=False
# - Return state
# - On exception: append error, set error_occurred=True, insights_analysis_complete=False
def local_insights_node(state:TravelPlanState)-> TravelPlanState:
    try:
            client =build_gemini_client()
            agent=LocalInsightsLLMAgent(client)
            trip_profile = {
            "destination":state.get("destination"),
            "trip_duration_days":state.get("trip_duration_days"),
            "total_budget_inr":state.get("total_budget_inr"),
            "group_size":state.get("group_size"),
            "primary_interest":state.get("primary_interest"),
            "secondary_interest":state.get("secondary_interest"),
            "travel_season":state.get("travel_season"),
            "accommodation_type":state.get("accommodation_type")}

            itinerary=state.get("itinerary",{})
            result=agent.get_local_insights(trip_profile,itinerary)
            if result.get("status")=="success":
                state["hidden_gems"]=result.get("hidden_gems",[])
                state["local_food_spots"]=result.get("local_food_spots",[])
                state["neighborhoods_to_explore"]=result.get("neighborhoods_to_explore",[])

                state["local_etiquette_tips"]=result.get("local_etiquette_tips",[])
                state["money_saving_hacks"]=result.get("money_saving_hacks",[])
                state["free_or_cheap_attractions"]=result.get("free_or_cheap_attractions",[])
                state["avoid_tourist_traps"]=result.get("avoid_tourist_traps",[])

                state["best_times_to_avoid_crowds"]=result.get("best_times_to_avoid_crowds",{})
                state["insights_analysis_complete"]=True
            else :
                state.setdefault("error_messages",[]).append(
                    result.get("error_message","Local insights generation failed")
                )
                state["error_occurred"]=True 
                state["insights_analysis_complete"]=False 
            return state 
     
    except Exception as e:
         state.setdefault("error_messages",[]).append(str(e))
         state["error_occurred"]=True 
         state["insights_analysis_complete"]=False 
         return state 
