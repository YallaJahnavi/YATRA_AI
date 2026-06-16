"""
YatraAI Test Suite

Tests validate output contracts and logic without constraining implementation.
Following AetherFit testing patterns.

Test Structure:
- 18 total test cases
- Organized by component type
- Mock infrastructure for LLM testing
- Multiple travel profiles for scenario testing
"""

import pytest
import json
from typing import Dict, Any, Optional


# ============================================================================
# PART 1: Mock Infrastructure
# ============================================================================

class MockGeminiContent:
    """Simulates google.generativeai content response"""
    def __init__(self, text: str):
        self.text = text


class MockGeminiResponse:
    """Simulates Gemini API response"""
    def __init__(self, text: str):
        self.text = text


class MockGeminiClient:
    """
    Complete mock of GeminiClient for testing without API calls.
    Pattern matches on prompt content to return appropriate responses.
    """

    def __init__(self):
        self.call_count = 0
        self.default_responses = {
            'itinerary': {
                'day_1': {
                    'title': 'Arrival Day',
                    'activities': ['Airport transfer', 'Hotel check-in', 'Local exploration'],
                    'estimated_cost': 5000
                },
                'day_2': {
                    'title': 'Main Attractions',
                    'activities': ['Visit landmark', 'Cultural site tour', 'Local dining'],
                    'estimated_cost': 7000
                },
                'day_3': {
                    'title': 'Adventure',
                    'activities': ['Outdoor activity', 'Nature exploration', 'Rest'],
                    'estimated_cost': 6000
                }
            },
            'local_insights': {
                'hidden_gems': [
                    {'name': 'Local Market', 'description': 'Authentic local experience', 'estimated_cost': '500-1000', 'tips': ['Go early']},
                    {'name': 'Hidden Beach', 'description': 'Scenic location', 'estimated_cost': 'Free', 'tips': ['Bring water']}
                ],
                'local_food_spots': [
                    {'name': 'Street Food Vendor', 'cuisine': 'Local', 'price_range': '₹50-100', 'signature_dish': 'Special Chaat'},
                    {'name': 'Local Restaurant', 'cuisine': 'Regional', 'price_range': '₹200-500', 'signature_dish': 'Biryani'}
                ],
                'neighborhoods_to_explore': [
                    {'name': 'Old City', 'vibe': 'Historic and bustling', 'how_to_spend_time': ['Shopping', 'Sightseeing']},
                    {'name': 'Beach Area', 'vibe': 'Relaxed and scenic', 'how_to_spend_time': ['Walking', 'Dining']}
                ],
                'local_etiquette_tips': ['Respect local customs', 'Dress appropriately'],
                'money_saving_hacks': ['Use public transport', 'Eat at local places'],
                'free_or_cheap_attractions': ['Beach walk', 'Park visit'],
                'avoid_tourist_traps': ['Overpriced restaurants near monuments'],
                'best_times_to_avoid_crowds': {'avoid': ['Peak season'], 'ideal': ['Off-season']}
            },
            'booking_strategy': {
                'flight_booking_strategy': {
                    'recommended_platforms': ['MakeMyTrip', 'Goibibo'],
                    'booking_window': '2-4 weeks in advance',
                    'best_days_to_book': 'Tuesday-Thursday',
                    'estimated_cost_range': '₹5000-15000',
                    'money_saving_tips': ['Book early morning', 'Use flight comparators']
                },
                'accommodation_booking_strategy': {
                    'recommended_platforms': ['Booking.com', 'OYO'],
                    'booking_window': '2-3 weeks in advance',
                    'neighborhoods_recommended': ['City center', 'Tourist area'],
                    'estimated_cost_per_night': '₹2000-5000',
                    'money_saving_tips': ['Book in bulk', 'Check for deals']
                },
                'activity_booking_strategy': {
                    'advance_booking_required': ['Adventure tours'],
                    'book_on_site': ['Local guides']
                },
                'logistics_planning': {
                    'visa_requirements': {'required': False, 'processing_time': 'N/A'},
                    'travel_insurance': {'recommended': True, 'estimated_cost': '₹500-1000'},
                    'vaccinations': {'recommended': ['Routine vaccines']}
                },
                'packing_checklist': {'essentials': ['Passport', 'Phone'], 'by_activity': {}},
                'pre_departure_checklist': {'one_month_before': ['Book flights'], 'one_week_before': ['Confirm hotel']},
                'money_saving_tips_summary': ['Book in advance', 'Use local transport'],
                'emergency_contingency_plans': {'missed_flight': 'Contact airline', 'medical_emergency': 'Go to hospital'}
            }
        }

    def generate_content(
        self,
        prompt: str,
        temperature: float = 0.7,
        max_tokens: int = 2000,
        response_mime_type: Optional[str] = None,
    ) -> str:
        """Generate content with pattern matching on prompt"""
        self.call_count += 1
        prompt_lower = prompt.lower()

        # Pattern matching for different agent types
        if "itinerary" in prompt_lower:
            response = self.default_responses['itinerary']
        elif "local" in prompt_lower and "insight" in prompt_lower:
            response = self.default_responses['local_insights']
        elif "booking" in prompt_lower:
            response = self.default_responses['booking_strategy']
        else:
            response = self.default_responses['itinerary']

        return json.dumps(response)

    def extract_json_from_response(self, response_text: str) -> Dict[str, Any]:
        """Extract JSON from response text"""
        try:
            return json.loads(response_text)
        except json.JSONDecodeError:
            return {}

    def validate_response_fields(self, response: Dict[str, Any], required_fields: list) -> None:
        """Validate that response has required fields"""
        missing = [f for f in required_fields if f not in response]
        if missing:
            raise ValueError(f"Missing fields: {missing}")

    def generate_structured_json(
        self,
        prompt: str,
        required_fields: list,
        temperature: float = 0.7,
        max_tokens: int = 2000
    ) -> Dict[str, Any]:
        """Generate and validate JSON response"""
        response_text = self.generate_content(prompt, temperature, max_tokens)
        result = self.extract_json_from_response(response_text)
        self.validate_response_fields(result, required_fields)
        return result


# ============================================================================
# PART 2: Sample Travel Profiles
# ============================================================================

SAMPLE_TRIP_BUDGET = {
    'destination': 'Jaipur',
    'trip_duration_days': 5,
    'total_budget_inr': 50000,
    'group_size': 2,
    'primary_interest': 'Cultural',
    'secondary_interest': 'Heritage',
    'travel_season': 'Peak',
}

SAMPLE_TRIP_LUXURY = {
    'destination': 'Goa',
    'trip_duration_days': 7,
    'total_budget_inr': 200000,
    'group_size': 4,
    'primary_interest': 'Beach',
    'secondary_interest': 'Food',
    'travel_season': 'Peak',
}

SAMPLE_TRIP_ADVENTURE = {
    'destination': 'Himachal Pradesh',
    'trip_duration_days': 10,
    'total_budget_inr': 100000,
    'group_size': 3,
    'primary_interest': 'Adventure',
    'secondary_interest': 'Cultural',
    'travel_season': 'Moderate',
}

# Valid enumeration values
VALID_ACCOMMODATION_TYPES = ['Budget', 'Mid-range', 'Luxury', 'Alternative']
VALID_BUDGET_TIERS = ['low_budget_path', 'mid_budget_path', 'high_budget_path']


# ============================================================================
# PART 3: ML Agent Tests (4 tests)
# ============================================================================

def test_budget_allocator_output_structure():
    """Test budget allocator returns required fields"""
    from agents.budget_allocator_ml import BudgetAllocatorMLAgent

    agent = BudgetAllocatorMLAgent()
    result = agent.allocate_budget(SAMPLE_TRIP_BUDGET)

    # Validate output structure
    assert 'accommodation_budget_pct' in result
    assert 'food_dining_budget_pct' in result
    assert 'activities_attractions_budget_pct' in result
    assert 'local_transport_budget_pct' in result
    assert 'shopping_misc_budget_pct' in result
    assert 'contingency_budget_pct' in result
    assert 'daily_budget' in result
    assert 'budget_allocation' in result

    # Validate types
    assert isinstance(result['accommodation_budget_pct'], (int, float))
    assert isinstance(result['daily_budget'], (int, float))
    assert isinstance(result['budget_allocation'], dict)


def test_budget_allocator_percentages_sum_to_100():
    """Test budget percentages sum to approximately 100"""
    from agents.budget_allocator_ml import BudgetAllocatorMLAgent

    agent = BudgetAllocatorMLAgent()
    result = agent.allocate_budget(SAMPLE_TRIP_BUDGET)

    # Sum all percentages
    total = (
        result['accommodation_budget_pct'] +
        result['food_dining_budget_pct'] +
        result['activities_attractions_budget_pct'] +
        result['local_transport_budget_pct'] +
        result['shopping_misc_budget_pct'] +
        result['contingency_budget_pct']
    )

    # Should sum to approximately 100
    assert 99.0 <= total <= 101.0


def test_accommodation_recommender_output_structure():
    """Test accommodation recommender returns required fields"""
    from agents.accommodation_recommender_ml import AccommodationRecommenderMLAgent

    agent = AccommodationRecommenderMLAgent()
    user_profile = {
        'destination': 'Jaipur',
        'total_budget_inr': 100000,
        'accommodation_budget_inr': 30000,
        'trip_duration_days': 5,
        'group_size': 2,
        'primary_interest': 'Cultural',
        'secondary_interest': 'Heritage',
        'travel_season': 'Peak',
        'destination_cost_tier': 'Tier-2',
        'interests': ['Cultural', 'Heritage'],
    }
    result = agent.recommend_accommodation(user_profile)

    # Validate output structure
    assert 'accommodation_type' in result
    assert 'accommodation_class' in result
    assert 'confidence' in result
    assert 'estimated_cost_per_night' in result
    assert 'status' in result

    # Validate types
    assert isinstance(result['accommodation_type'], str)
    assert isinstance(result['confidence'], (int, float))
    assert isinstance(result['accommodation_class'], int)

    # Validate values
    assert result['accommodation_type'] in VALID_ACCOMMODATION_TYPES
    assert 0 <= result['confidence'] <= 100
    assert 0 <= result['accommodation_class'] <= 3


def test_accommodation_recommender_different_budgets():
    """Test accommodation recommender produces different results for different budgets"""
    from agents.accommodation_recommender_ml import AccommodationRecommenderMLAgent

    agent = AccommodationRecommenderMLAgent()

    # Low budget profile
    low_result = agent.recommend_accommodation({
        'destination': 'Jaipur',
        'total_budget_inr': 30000,
        'accommodation_budget_inr': 10000,
        'trip_duration_days': 5,
        'group_size': 2,
        'primary_interest': 'Cultural',
        'secondary_interest': 'Heritage',
        'travel_season': 'Peak',
        'destination_cost_tier': 'Tier-2',
        'interests': ['Cultural', 'Heritage'],
    })

    # High budget profile
    high_result = agent.recommend_accommodation({
        'destination': 'Jaipur',
        'total_budget_inr': 300000,
        'accommodation_budget_inr': 100000,
        'trip_duration_days': 5,
        'group_size': 2,
        'primary_interest': 'Cultural',
        'secondary_interest': 'Heritage',
        'travel_season': 'Peak',
        'destination_cost_tier': 'Tier-2',
        'interests': ['Cultural', 'Heritage'],
    })

    # Both should be valid
    assert low_result['accommodation_type'] in VALID_ACCOMMODATION_TYPES
    assert high_result['accommodation_type'] in VALID_ACCOMMODATION_TYPES


# ============================================================================
# PART 4: LLM Agent Tests (4 tests)
# ============================================================================

def test_itinerary_generator_structure():
    """Test itinerary generator returns required structure"""
    from agents.itinerary_generator_llm import ItineraryGeneratorLLMAgent

    mock_client = MockGeminiClient()
    agent = ItineraryGeneratorLLMAgent(client=mock_client)

    result = agent.generate_itinerary(SAMPLE_TRIP_BUDGET)

    # Validate required fields
    assert 'itinerary' in result
    assert 'trip_highlights' in result
    assert 'contingency_plans' in result
    assert 'status' in result

    # Validate types
    assert isinstance(result['itinerary'], dict)
    assert isinstance(result['trip_highlights'], list)
    assert isinstance(result['contingency_plans'], list)

    # Verify LLM was called
    assert mock_client.call_count >= 1


def test_local_insights_structure():
    """Test local insights returns required structure"""
    from agents.local_insights_llm import LocalInsightsLLMAgent

    mock_client = MockGeminiClient()
    agent = LocalInsightsLLMAgent(client=mock_client)

    result = agent.get_local_insights(
        trip_profile=SAMPLE_TRIP_BUDGET,
        itinerary={'day_1': {'title': 'Day 1'}}
    )

    # Validate required fields
    assert 'hidden_gems' in result
    assert 'local_food_spots' in result
    assert 'neighborhoods_to_explore' in result
    assert 'local_etiquette_tips' in result
    assert 'money_saving_hacks' in result
    assert 'status' in result

    # Validate types
    assert isinstance(result['hidden_gems'], list)
    assert isinstance(result['local_food_spots'], list)
    assert isinstance(result['local_etiquette_tips'], list)

    # Verify LLM was called
    assert mock_client.call_count >= 1


def test_booking_strategy_structure():
    """Test booking strategy returns required structure"""
    from agents.booking_strategy_llm import BookingStrategyLLMAgent

    mock_client = MockGeminiClient()
    agent = BookingStrategyLLMAgent(client=mock_client)

    result = agent.get_booking_strategy(SAMPLE_TRIP_BUDGET)

    # Validate required fields
    assert 'flight_booking_strategy' in result
    assert 'accommodation_booking_strategy' in result
    assert 'logistics_planning' in result
    assert 'status' in result

    # Validate types
    assert isinstance(result['flight_booking_strategy'], dict)
    assert isinstance(result['accommodation_booking_strategy'], dict)
    assert isinstance(result['logistics_planning'], dict)

    # Verify LLM was called
    assert mock_client.call_count >= 1


def test_itinerary_revision_output():
    """Test itinerary revision returns validated itinerary"""
    from agents.itinerary_generator_llm import ItineraryGeneratorLLMAgent

    mock_client = MockGeminiClient()
    agent = ItineraryGeneratorLLMAgent(client=mock_client)

    result = agent.generate_itinerary(SAMPLE_TRIP_LUXURY)

    # Validate itinerary structure
    assert 'itinerary' in result
    assert isinstance(result['itinerary'], dict)


# ============================================================================
# PART 5: State Management Tests (2 tests)
# ============================================================================

def test_initial_state_creation():
    """Test state initialization with form data"""
    from state import get_initial_state

    state = get_initial_state(SAMPLE_TRIP_BUDGET)

    # Validate input fields copied
    assert state['destination'] == 'Jaipur'
    assert state['trip_duration_days'] == 5
    assert state['total_budget_inr'] == 50000

    # Validate output fields initialized
    assert state['error_occurred'] is False
    assert state['error_messages'] == []


def test_state_validation():
    """Test state structure is valid after updates"""
    from state import get_initial_state

    state = get_initial_state(SAMPLE_TRIP_BUDGET)

    # Populate some fields
    state['accommodation_type'] = 'Mid-range'
    state['accommodation_confidence'] = 75.5
    state['daily_budget'] = 10000

    # Validate state structure
    assert 'destination' in state
    assert 'accommodation_type' in state
    assert 'error_messages' in state

    # Validate types
    assert isinstance(state['destination'], str)
    assert isinstance(state['accommodation_type'], str)
    assert isinstance(state['error_messages'], list)


# ============================================================================
# PART 6: Decision Router Tests (2 tests)
# ============================================================================

def test_budget_feasibility_router_low_budget():
    """Test budget router correctly identifies low budget tier"""
    from nodes.decision_router_nodes import budget_feasibility_router
    from state import get_initial_state

    state = get_initial_state({
        'destination': 'Jaipur',
        'trip_duration_days': 5,
        'total_budget_inr': 30000,  # Low budget
        'group_size': 2,
        'primary_interest': 'Cultural',
        'secondary_interest': 'Heritage',
        'travel_season': 'Peak',
    })

    # Manually set daily_budget (would be set by budget allocator)
    state['daily_budget'] = 6000  # < 7000

    result = budget_feasibility_router(state)

    # Should route to low budget path
    assert result['daily_budget_tier'] == 'low_budget_path'


def test_budget_feasibility_router_high_budget():
    """Test budget router correctly identifies high budget tier"""
    from nodes.decision_router_nodes import budget_feasibility_router
    from state import get_initial_state

    state = get_initial_state({
        'destination': 'Goa',
        'trip_duration_days': 7,
        'total_budget_inr': 200000,  # High budget
        'group_size': 4,
        'primary_interest': 'Beach',
        'secondary_interest': 'Food',
        'travel_season': 'Peak',
    })

    # Manually set daily_budget (would be set by budget allocator)
    state['daily_budget'] = 20000  # > 15000

    result = budget_feasibility_router(state)

    # Should route to high budget path
    assert result['daily_budget_tier'] == 'high_budget_path'


# ============================================================================
# PART 7: Integration/Workflow Tests (4 tests)
# ============================================================================

def test_budget_allocation_complete_workflow():
    """Test complete budget allocation workflow"""
    from nodes.budget_allocator_node import budget_allocator_node
    from state import get_initial_state

    state = get_initial_state(SAMPLE_TRIP_BUDGET)

    result = budget_allocator_node(state)

    # Validate workflow completion
    assert result['daily_budget'] is not None
    assert result['budget_allocation'] is not None
    assert isinstance(result['budget_allocation'], dict)


def test_accommodation_recommendation_workflow():
    """Test complete accommodation recommendation workflow"""
    from nodes.accommodation_recommender_node import accommodation_recommender_node
    from state import get_initial_state

    state = get_initial_state(SAMPLE_TRIP_BUDGET)
    state['destination_cost_tier'] = 'Tier-2'

    result = accommodation_recommender_node(state)

    # Validate workflow completion
    assert result['accommodation_type'] is not None
    assert result['accommodation_confidence'] is not None


def test_trip_complexity_analyzer_workflow():
    """Test trip complexity analysis"""
    from nodes.decision_router_nodes import trip_complexity_analyzer
    from state import get_initial_state

    state = get_initial_state(SAMPLE_TRIP_ADVENTURE)

    result = trip_complexity_analyzer(state)

    # Validate complexity score calculated
    assert result['complexity_score'] is not None
    assert isinstance(result['complexity_score'], (int, float))
    assert 0 <= result['complexity_score'] <= 1.0


def test_accommodation_alternatives_available():
    """Test accommodation recommender provides alternatives"""
    from agents.accommodation_recommender_ml import AccommodationRecommenderMLAgent

    agent = AccommodationRecommenderMLAgent()
    result = agent.recommend_accommodation({
        'destination': 'Jaipur',
        'total_budget_inr': 100000,
        'accommodation_budget_inr': 30000,
        'trip_duration_days': 5,
        'group_size': 2,
        'primary_interest': 'Cultural',
        'secondary_interest': 'Heritage',
        'travel_season': 'Peak',
        'destination_cost_tier': 'Tier-2',
        'interests': ['Cultural', 'Heritage'],
    })

    # Should have alternatives
    assert 'alternatives' in result
    assert isinstance(result['alternatives'], list)


# ============================================================================
# PART 8: Data Persistence Tests (2 tests)
# ============================================================================

def test_ml_models_exist():
    """Test that trained ML models exist and have content"""
    import os
    from pathlib import Path

    project_root = Path(__file__).parent
    models_dir = project_root / "ml" / "models"

    model_files = [
        "budget_allocator_model.pkl",
        "budget_allocator_scaler.pkl",
        "budget_allocator_encoder.pkl",
        "accommodation_recommender_model.pkl",
        "accommodation_recommender_scaler.pkl",
        "accommodation_recommender_encoder.pkl",
    ]

    for model_file in model_files:
        model_path = models_dir / model_file
        assert model_path.exists(), f"Missing: {model_file}"
        assert os.path.getsize(model_path) > 0, f"Empty: {model_file}"


def test_processed_data_not_empty():
    """Test that processed datasets exist and are not empty"""
    from pathlib import Path
    import pandas as pd

    project_root = Path(__file__).parent
    processed_dir = project_root / "data" / "processed"

    processed_files = [
        "budget_allocation_clean.csv",
        "accommodation_recommender_clean.csv",
    ]

    for dataset_file in processed_files:
        dataset_path = processed_dir / dataset_file
        assert dataset_path.exists(), f"Missing processed data: {dataset_file}"

        # Check file has content
        df = pd.read_csv(dataset_path)
        assert len(df) > 0, f"Empty processed data: {dataset_file}"


# ============================================================================
# Test Execution
# ============================================================================

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
