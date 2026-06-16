"""Configuration constants for YatraAI application."""

# Destinations
DESTINATIONS = [
    "Jaipur",
    "Goa",
    "Delhi",
    "Mumbai",
    "Bangalore",
    "Udaipur",
    "Varanasi",
    "Kolkata",
    "Agra",
    "Kerala",
    "Pune",
    "Lucknow",
    "Rishikesh",
    "Rajasthan (non-GT)",
    "Himachal Pradesh",
    "Northeast India",
    "Hyderabad",
]

# Interests
INTERESTS = [
    "Adventure",
    "Cultural",
    "Beach",
    "Spiritual",
    "Food",
    "Heritage",
]

# Secondary interests (includes None option)
SECONDARY_INTERESTS = [
    "None",
    "Adventure",
    "Cultural",
    "Beach",
    "Spiritual",
    "Food",
    "Heritage",
]

# Travel seasons
TRAVEL_SEASONS = [
    "Peak",
    "Moderate",
    "Off-season",
]

# Budget ranges
BUDGET_MIN = 5000
BUDGET_MAX = 500000
BUDGET_STEP = 5000
BUDGET_DEFAULT = 50000

# Trip duration ranges
TRIP_DURATION_MIN = 2
TRIP_DURATION_MAX = 30
TRIP_DURATION_DEFAULT = 7

# Group size ranges
GROUP_SIZE_MIN = 1
GROUP_SIZE_MAX = 10
GROUP_SIZE_DEFAULT = 2

# Accommodation types
ACCOMMODATION_TYPES = [
    "Budget",
    "Mid-range",
    "Luxury",
    "Alternative",
]

# Destination cost tiers
DESTINATION_COST_TIERS = [
    "Tier-1",
    "Tier-2",
    "Tier-3",
]

# Budget threshold boundaries (in INR per day)
BUDGET_TIER_LOW = 7000      # < 7000
BUDGET_TIER_MID = 15000     # 7000 - 15000
# > 15000 is high

# Trip complexity threshold
COMPLEXITY_THRESHOLD = 0.7  # For determining max revisions

# Accommodation class names
ACCOMMODATION_CLASS_NAMES = {
    0: "Budget",
    1: "Mid-range",
    2: "Luxury",
    3: "Alternative",
}

# Cost ranges for each accommodation type (per night in INR)
ACCOMMODATION_COST_RANGES = {
    0: (500, 1500),      # Budget
    1: (2000, 5000),     # Mid-range
    2: (8000, 30000),    # Luxury
    3: (2500, 6000),     # Alternative
}

# Interest encoding for ML
INTEREST_ENCODING = {
    "Adventure": 1,
    "Cultural": 2,
    "Beach": 4,
    "Spiritual": 8,
    "Food": 16,
    "Heritage": 32,
}

# Destination encoding for ML
DESTINATION_ENCODING = {
    "Jaipur": 0,
    "Goa": 1,
    "Delhi": 2,
    "Mumbai": 3,
    "Bangalore": 4,
    "Udaipur": 5,
    "Varanasi": 6,
    "Kolkata": 7,
    "Agra": 8,
    "Kerala": 9,
    "Pune": 10,
    "Lucknow": 11,
    "Rishikesh": 12,
    "Rajasthan (non-GT)": 13,
    "Himachal Pradesh": 14,
    "Northeast India": 15,
    "Hyderabad": 16,
}

# Season encoding for ML
SEASON_ENCODING = {
    "Peak": 0,
    "Moderate": 1,
    "Off-season": 2,
}

# Accommodation preference encoding for ML
ACCOMMODATION_PREFERENCE_ENCODING = {
    "Budget": 0,
    "Mid-range": 1,
    "Luxury": 2,
    "Alternative": 3,
}

# Cost tier encoding for ML
COST_TIER_ENCODING = {
    "Tier-1": 0,
    "Tier-2": 1,
    "Tier-3": 2,
}
