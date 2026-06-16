"""Itinerary Revision Node - Validates and revises itinerary with max 2 attempts.

Imports: state.TravelPlanState, utils.gemini_client.build_gemini_client

Validates itinerary quality using LLM. For complex trips (complexity_score > 0.7),
allows up to 2 revision attempts. For simple trips, max 1 revision.
"""

from state import TravelPlanState
from utils.gemini_client import build_gemini_client


# TODO: Implement itinerary_validator_and_reviser_node() function
# - Takes state: TravelPlanState parameter
# - Returns TravelPlanState
# - Build Gemini client using build_gemini_client()
# - Extract itinerary, complexity_score, revision_count from state
# - Determine max_revisions: 2 if complexity_score > 0.7, else 1
# - Create trip_profile dict with essential trip details
# - Create validation prompt for Gemini requesting JSON with:
#   * is_valid: bool
#   * validation_score: float (0.0-1.0)
#   * issues: list of strings
#   * improvement_suggestions: list of strings
#   * revision_needed: bool
# - Call Gemini API to validate itinerary
# - Extract JSON from response
# - If revision_needed=true and revision_count < max_revisions:
#   * Create revision prompt with improvement suggestions
#   * Call Gemini API to revise itinerary
#   * Increment itinerary_revision_count
#   * Set itinerary_revised=true
#   * Update itinerary in state
# - Set state fields:
#   * itinerary_validation_score: float from response
#   * itinerary_validation_issues: list from response
#   * itinerary_revision_count: incremented if revised
#   * itinerary_revised: bool
# - Return state
# - On exception: append error, set error_occurred=True
def itinerary_validator_and_reviser_node(state:TravelPlanState) -> TravelPlanState:
    try:
        client =build_gemini_client()

        itinerary=state.get("itinerary",{})
        complexity_score=state.get("complexity_score",0.5)
        revision_count=state.get("itinerary_revision_count",0)

        max_revisions= 2 if complexity_score >0.7 else 1 
        trip_profile ={
            "destination":state.get("destination"),
            "trip_duration_days":state.get("trip_duration_days"),
            "group_size":state.get("group_size"),
            "daily_budget":state.get("daily_budget"),

        }
        validation_prompt = f""" 
        Validate the following itinerary .
        Itinerary:
        {itinerary}
        Return JSON with:
        is_valid 
        validation_score 
        issues 
        improvement_suggestions 
        revision_needed
        """
        response_text=client.generate_content(
            validation_prompt,
            temperature=0.5 ,
            max_tokens=1500
        )
        response_json = client.extract_json_from_response(response_text)
        validation_score=response_json.get("validation_score",0.8)
        issues=response_json.get("issues",[])
        revision_needed=response_json.get("revision_needed",False)

        state["itinerary_validation_score"]=validation_score 
        state["itinerary_validation_issues"]=issues 
        if revision_needed and revision_count < max_revisions: 
            revision_prompt= f"""
            Improve this itinerary based on the following suggestions:
            Suggestions:
            {response_json.get("improvement_suggestions",[])}

            Original itinerary:
            {itinerary}

            Return revised itinerary JSON.
            """
            revision_response=client.generate_content(
                revision_prompt,
                temperature=0.7,
                max_tokens=2000
            )
            revised_json=client.extract_json_from_response(revision_response)
            state["itinerary"]=revised_json.get("itinerary",itinerary)
            state["itinerary_revision_count"]=revision_count +1 
            state["itinerary_revised"]=True 
        else :
            state["itinerary_revised"]=False 
        return state 
    except Exception as e:
        state.setdefault("error_messages",[]).append(str(e))
        state["error_occurred"]=True 
        return state
