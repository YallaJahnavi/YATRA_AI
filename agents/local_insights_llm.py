"""Local Insights & Hidden Gems LLM Agent - Pure Gemini API calls.

Imports: json, typing.Dict, typing.Any

Uses Gemini API client for LLM-based generation (100% LLM output, no heuristics).
"""

import json
from typing import Dict, Any

class LocalInsightsLLMAgent:
    """
    Generates local insights, hidden gems, and tips using Gemini LLM.
    """
    def __init__(self,client):
        self.client=client
    def get_local_insights(self,trip_profile: Dict[str, Any],itinerary:Dict)->Dict[str,Any]:
        try:
            destination=trip_profile.get("destination","")
            group_size=trip_profile.get("group_size",1)
            primary_interest=trip_profile.get("primary_interest","")
            secondary_interest=trip_profile.get("secondary_interest","")
            travel_season=trip_profile.get("travel_season","")
            accommodation_type=trip_profile.get("accommodation_type","Mid-range")
            total_budget=trip_profile.get("total_budget_inr",0)
            prompt=f"""
Provide local travel insights.

Destination: {destination}
Group Size: {group_size}
Primary Interest: {primary_interest}
Secondary Interest: {secondary_interest}
Travel Season: {travel_season}
Accommodation Type: {accommodation_type}
Total Budget: {total_budget}

Return JSON with:
hidden_gems
local_food_spots
neighborhoods_to_explore
local_etiquette_tips
money_saving_hacks
free_or_cheap_attractions
avoid_tourist_traps
best_times_to_avoid_crowds
"""
            response_text=self.client.generate_content(
                prompt,
                temperature=0.8,
                max_tokens=2000
            )
            response_json=self.client.extract_json_from_response(response_text)
            return{
                "hidden_gems":response_json.get("hidden_gems",[]),
                "local_food_spots":response_json.get("local_food_spots",[]),
                "neighborhoods_to_explore":response_json.get("neighborhoods_to_explore",[]),
                "local_etiquette_tips":response_json.get("local_etiquette_tips",[]),
                "money_saving_hacks":response_json.get("money_saving_hacks",[]),
                "free_or_cheap_attractions":response_json.get("free_or_cheap_attractions",[]),
                "avoid_tourist_traps":response_json.get("avoid_tourist_traps",[]),
                "best_times_to_avoid_crowds":response_json.get("best_times_to_avoid_crowds",{}),
                "status":"success",
            }
        except Exception as e:
            raise ValueError(f"Local insights generation failed: {str(e)}")
            
# TODO: Implement LocalInsightsLLMAgent class
# - Purpose: Provides insider tips, hidden gems, and local recommendations using Gemini API


# TODO: Implement __init__() method for LocalInsightsLLMAgent
# - Takes client parameter (Gemini API client)
# - Store as self.client


# TODO: Implement get_local_insights() method
# - Takes trip_profile: Dict[str, Any] and itinerary: Dict parameters
# - Returns Dict[str, Any] with local insights results
# - Extract accommodation_type and destination from trip_profile
# - Create budget_guidance string based on accommodation_type:
#   * "luxury" -> focus on exclusive experiences and premium options
#   * "budget" -> emphasize money-saving and free/cheap options
#   * else -> balance both approaches
# - Create detailed prompt for Gemini including:
#   * trip_profile details: destination, group_size, primary/secondary interest,
#     accommodation_type, travel_season, total_budget_inr
#   * budget_guidance string
#   * Request JSON response with structure: hidden_gems, local_food_spots,
#     neighborhoods_to_explore, local_etiquette_tips, money_saving_hacks,
#     free_or_cheap_attractions, avoid_tourist_traps, best_times_to_avoid_crowds
# - Call self.client.generate_content() with:
#   * prompt (constructed above)
#   * temperature=0.8
#   * max_tokens=2000
# - Extract JSON from response using self.client.extract_json_from_response()
# - Return dict with keys:
#   * hidden_gems, local_food_spots, neighborhoods_to_explore (lists),
#     local_etiquette_tips, money_saving_hacks, free_or_cheap_attractions,
#     avoid_tourist_traps (lists), best_times_to_avoid_crowds (dict),
#     status: "success"
# - On exception: raise ValueError with descriptive message
