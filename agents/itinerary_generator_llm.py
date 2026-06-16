import json
import re
from typing import Dict, Any


class ItineraryGeneratorLLMAgent:
    def __init__(self, client):
        self.client = client

    def clean_json(self, text: str) -> Dict:
        match = re.search(r'\{.*\}', text, re.DOTALL)

        if not match:
            raise ValueError("No JSON found in response")

        return json.loads(match.group(0))

    def generate_itinerary(self, trip_profile: Dict[str, Any]) -> Dict[str, Any]:
        try:
            destination = trip_profile.get("destination", "")
            trip_duration = trip_profile.get("trip_duration_days", 0)
            group_size = trip_profile.get("group_size", 1)
            total_budget = trip_profile.get("total_budget_inr", 0)

            prompt = f"""
Generate a STRICT JSON travel itinerary.

Destination: {destination}
Duration: {trip_duration} days
Group Size: {group_size}
Budget: {total_budget}

RULES:
- Return ONLY JSON
- EXACT {trip_duration} days
- Each day must be object with title, activities, estimated_cost

FORMAT:
{{
  "itinerary": {{
    "day_1": {{
      "title": "Title",
      "activities": ["A1", "A2"],
      "estimated_cost": 2000
    }}
  }},
  "trip_highlights": ["..."],
  "contingency_plans": ["..."],
  "tips_for_success": ["..."]
}}
"""

            response_text = self.client.generate_content(
                prompt,
                temperature=0.5,
                max_tokens=2000
            )

            response_json = self.clean_json(response_text)

            # Handle mock response format used in tests
            if "itinerary" not in response_json:
                day_keys = [
                    key for key in response_json.keys()
                    if key.startswith("day_")
                ]

                if day_keys:
                    response_json = {
                        "itinerary": response_json,
                        "trip_highlights": [],
                        "contingency_plans": [],
                        "tips_for_success": []
                    }
                else:
                    raise ValueError("Missing itinerary key")

            return {
                "itinerary": response_json.get("itinerary", {}),
                "trip_highlights": response_json.get("trip_highlights", []),
                "contingency_plans": response_json.get("contingency_plans", []),
                "tips_for_success": response_json.get("tips_for_success", []),
                "status": "success"
            }

        except Exception as e:
            return {
                "status": "error",
                "error_message": str(e)
            }
