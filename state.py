"""State management for travel planning workflow.

Imports: typing.TypedDict, typing.List, typing.Dict, typing.Any, typing.Optional, typing.Annotated
"""

from typing import TypedDict, List, Dict, Any, Optional, Annotated


# TODO: Implement merge_accommodations() function for handling parallel accommodation path merges
# - Takes left and right Dict[str, Any] parameters
# - Returns merged Dict[str, Any] with recommendations_by_budget key
# - Handle None/empty cases for both left and right
# - Update recommendations_by_budget from right into merged dict


# TODO: Define TravelPlanState TypedDict (total=False) with all required fields:
#
#   INPUT FIELDS (7):
#   - destination: str
#   - trip_duration_days: int
#   - total_budget_inr: int
#   - group_size: int
#   - primary_interest: str
#   - secondary_interest: str
#   - travel_season: str
#
#   DERIVED FIELDS (5):
#   - destination_cost_tier: str
#   - accommodation_preference: str
#   - parsed_profile: Dict[str, Any]
#   - validation_errors: List[str]
#   - parsing_complete: bool
#
#   BUDGET ALLOCATION ML OUTPUTS (8):
#   - accommodation_budget_pct: float
#   - food_dining_budget_pct: float
#   - activities_attractions_budget_pct: float
#   - local_transport_budget_pct: float
#   - shopping_misc_budget_pct: float
#   - contingency_budget_pct: float
#   - daily_budget: float
#   - budget_allocation: Dict[str, float]
#
#   DECISION NODE OUTPUTS (2):
#   - daily_budget_tier: str (LOW, MID, HIGH)
#   - complexity_score: float (0.0-1.0)
#
#   ACCOMMODATION RECOMMENDER ML OUTPUTS:
#   - accommodation_type: str
#   - accommodation_class: int
#   - accommodation_confidence: float
#   - accommodation_comfort_score: float
#   - estimated_cost_per_night: float
#   - accommodation_alternatives: List[Dict]
#   - accommodation_recommendations: Annotated[Dict[str, Any], merge_accommodations]
#
#   ITINERARY GENERATOR LLM OUTPUTS (11):
#   - itinerary: Dict[str, Any]
#   - trip_highlights: List[str]
#   - contingency_plans: List[str]
#   - itinerary_tips: List[str]
#   - daily_schedule: Dict[str, Any]
#   - itinerary_analysis_complete: bool
#   - itinerary_validation_score: float
#   - itinerary_validation_issues: List[str]
#   - itinerary_revision_count: int
#   - itinerary_revised: bool
#
#   LOCAL INSIGHTS LLM OUTPUTS (9):
#   - hidden_gems: List[Dict]
#   - local_food_spots: List[Dict]
#   - neighborhoods_to_explore: List[Dict]
#   - local_etiquette_tips: List[str]
#   - money_saving_hacks: List[str]
#   - free_or_cheap_attractions: List[str]
#   - avoid_tourist_traps: List[str]
#   - best_times_to_avoid_crowds: Dict[str, Any]
#   - insights_analysis_complete: bool
#
#   BOOKING STRATEGY LLM OUTPUTS (9):
#   - flight_booking_strategy: Dict[str, Any]
#   - accommodation_booking_strategy: Dict[str, Any]
#   - activity_booking_strategy: Dict[str, Any]
#   - visa_requirements: Dict[str, Any]
#   - budget_optimization_tips: List[str]
#   - booking_checklist: List[str]
#   - packing_checklist: Dict[str, Any]
#   - emergency_contingency_plans: Dict[str, Any]
#   - booking_analysis_complete: bool
#
#   SYSTEM METADATA (5):
#   - plan_id: str
#   - analysis_timestamp: str
#   - plan_generated: bool
#   - error_occurred: bool
#   - error_messages: List[str]


# TODO: Implement get_initial_state() function
# - Takes form_data: Dict[str, Any] parameter
# - Returns initialized TravelPlanState with:
#   * All input fields from form_data with defaults
#   * parsing_complete = False
#   * error_occurred = False
#   * error_messages = []
#   * validation_errors = []
#   * complexity_score = 0.5
#   * itinerary_revision_count = 0
#   * itinerary_validation_issues = []


def merge_accommodations(left: Dict[str, Any], right: Dict[str, Any]) -> Dict[str, Any]:

    if not left:
        return right or {} 
    if not right:
        return left 
    
    merged = dict(left) 

    merged.setdefault("recommendations_by_budget", {}) 
    merged["recommendations_by_budget"].update(right.get("recommendations_by_budget", {})) 

    return merged

class TravelPlanState(TypedDict, total=False):

    #input 

    destination: str
    trip_duration_days: int
    total_budget_inr: int
    group_size: int
    primary_interest: str
    secondary_interest: str
    travel_season: str

    # derived 

    destination_cost_tier: str
    accommodation_preference: str
    parsed_profile: Dict[str, Any]
    validation_errors: List[str]
    parsing_complete: bool

    #budget ml output 

    accommodation_budget_pct: float
    food_dining_budget_pct: float
    activities_attractions_budget_pct: float
    local_transport_budget_pct: float
    shopping_misc_budget_pct: float
    contingency_budget_pct: float
    daily_budget: float
    budget_allocation: Dict[str, float] 

    #decision 

    daily_budget_tier: str #(LOW, MID, HIGH)
    complexity_score: float #(0.0-1.0)

    #accommodation 
    accommodation_type: str
    accommodation_class: int
    accommodation_confidence: float
    accommodation_comfort_score: float
    estimated_cost_per_night: float
    accommodation_alternatives: List[Dict]
    accommodation_recommendations: Annotated[Dict[str, Any], merge_accommodations]

    #itinerary 

    itinerary: Dict[str, Any]
    trip_highlights: List[str]
    contingency_plans: List[str]
    itinerary_tips: List[str]
    daily_schedule: Dict[str, Any]
    itinerary_analysis_complete: bool
    itinerary_validation_score: float
    itinerary_validation_issues: List[str]
    itinerary_revision_count: int
    itinerary_revised: bool 

    #local insights 

    hidden_gems: List[Dict]
    local_food_spots: List[Dict]
    neighborhoods_to_explore: List[Dict]
    local_etiquette_tips: List[str]
    money_saving_hacks: List[str]
    free_or_cheap_attractions: List[str]
    avoid_tourist_traps: List[str]
    best_times_to_avoid_crowds: Dict[str, Any]
    insights_analysis_complete: bool 

    #booking 

    flight_booking_strategy: Dict[str, Any]
    accommodation_booking_strategy: Dict[str, Any]
    activity_booking_strategy: Dict[str, Any]
    visa_requirements: Dict[str, Any]
    budget_optimization_tips: List[str]
    booking_checklist: List[str]
    packing_checklist: Dict[str, Any]
    emergency_contingency_plans: Dict[str, Any]
    booking_analysis_complete: bool 

    #system 

    plan_id: str
    analysis_timestamp: str
    plan_generated: bool
    error_occurred: bool
    error_messages: List[str] 


def get_initial_state(form_data: Dict[str, Any]) -> TravelPlanState: 
    return TravelPlanState(
         destination = form_data.get("destination",""),
         trip_duration_days = form_data.get("trip_duration_days",0),
         total_budget_inr = form_data.get("total_budget_inr",0),
         group_size = form_data.get("group_size",1),
         primary_interest = form_data.get("primary_interest",""),
         secondary_interest = form_data.get("secondary_interest",""),
         travel_season = form_data.get("travel_season",""),

         parsing_complete = False,
         validation_errors = [],

         complexity_score = 0.5,
         itinerary_revision_count = 0,
         itinerary_validation_issues = [],

         error_occurred = False,
         error_messages = [],

    )






    

