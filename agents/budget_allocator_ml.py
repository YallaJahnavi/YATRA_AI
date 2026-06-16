"""Booking Strategy & Logistics LLM Agent - Pure Gemini API calls.

Imports: json, typing.Dict, typing.Any

Uses Gemini API client for LLM-based generation (100% LLM output, no heuristics).
"""

import json
from typing import Dict, Any
class BookingStrategyLLMAgent:
    def __init__(self, client):
        self.client = client

    def get_booking_strategy(self, trip_profile: Dict[str, Any]) -> Dict[str, Any]:
        try:
            destination = trip_profile.get("destination", "")
            total_budget = trip_profile.get("total_budget_inr", 0)
            trip_duration = trip_profile.get("trip_duration_days", 0)

            prompt = f"""
Return ONLY JSON.

Destination: {destination}
Budget: {total_budget}
Duration: {trip_duration}

FORMAT:
{{
  "flight_booking_strategy": {{"tips": ["Book early"]}},
  "accommodation_booking_strategy": {{"tips": ["Use Agoda"]}},
  "activity_booking_strategy": {{"tips": ["Book online"]}},
  "logistics_planning": {{"visa_requirements": "Check visa"}},
  "packing_checklist": {{"essentials": ["ID"]}},
  "pre_departure_checklist": {{
    "one_month_before": ["Book flights"],
    "one_week_before": ["Pack"]
  }},
  "money_saving_tips_summary": ["Save money"],
  "emergency_contingency_plans": {{"plan": "Backup hotel"}}
}}

NO TEXT OUTSIDE JSON.
"""

            response_text = self.client.generate_content(
                prompt,
                temperature=0.4,
                max_tokens=2000
            )

            response_json = self.client.extract_json_from_response(response_text)

            # 🔥 CRITICAL FIX
            if isinstance(response_json, str):
                response_json = json.loads(response_json)

            if not isinstance(response_json, dict):
                raise ValueError("Invalid JSON from LLM")

            return {
                "flight_booking_strategy": response_json.get("flight_booking_strategy", {}),
                "accommodation_booking_strategy": response_json.get("accommodation_booking_strategy", {}),
                "activity_booking_strategy": response_json.get("activity_booking_strategy", {}),
                "logistics_planning": response_json.get("logistics_planning", {}),
                "packing_checklist": response_json.get("packing_checklist", {}),
                "pre_departure_checklist": response_json.get("pre_departure_checklist", {}),
                "money_saving_tips_summary": response_json.get("money_saving_tips_summary", []),
                "emergency_contingency_plans": response_json.get("emergency_contingency_plans", {}),
                "status": "success",
            }

        except Exception as e:
            return {
                "status": "error",
                "error_message": str(e)
            }


# TODO: Implement BookingStrategyLLMAgent class
# - Purpose: Provides booking advice and travel logistics using Gemini API


# TODO: Implement __init__() method for BookingStrategyLLMAgent
# - Takes client parameter (Gemini API client)
# - Store as self.client


# TODO: Implement get_booking_strategy() method
# - Takes trip_profile: Dict[str, Any] parameter
# - Returns Dict[str, Any] with booking strategy results
# - Extract key trip details from trip_profile:
#   * accommodation_type, destination, total_budget, accommodation_budget,
#     trip_duration_days, group_size
# - Create detailed prompt for Gemini including trip details
# - Request JSON response with structure:
#   * flight_booking_strategy: recommended_platforms, booking_window, best_days_to_book,
#     estimated_cost_range, money_saving_tips
#   * accommodation_booking_strategy: recommended_platforms, booking_window,
#     neighborhoods_recommended, estimated_cost_per_night, money_saving_tips
#   * activity_booking_strategy: advance_booking_required, book_on_site,
#     estimated_daily_activity_cost
#   * logistics_planning: visa_requirements, travel_insurance, vaccinations
#   * packing_checklist: essentials, by_activity
#   * pre_departure_checklist: one_month_before, one_week_before
#   * money_saving_tips_summary: list of tips
#   * emergency_contingency_plans: scenarios and responses
# - Call self.client.generate_content() with:
#   * prompt (constructed above)
#   * temperature=0.6
#   * max_tokens=2500
# - Extract JSON from response using self.client.extract_json_from_response()
# - Return dict with keys:
#   * flight_booking_strategy, accommodation_booking_strategy, activity_booking_strategy,
#     logistics_planning, packing_checklist, pre_departure_checklist (dicts),
#     money_saving_tips_summary (list), emergency_contingency_plans (dict),
#     status: "success"
# - On exception: raise ValueError with descriptive message
