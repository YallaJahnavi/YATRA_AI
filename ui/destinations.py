"""Curated destination knowledge base for YatraAI.

A single source of structured, offline-safe data for the 17 supported
destinations: geo-coordinates, a tagline, best travel season, typical daily
cost band (INR/person), a safety score, local transport notes, an emoji motif,
and a list of headline attractions with coordinates (used for the map markers,
routes and distance estimates in later phases).

Coordinates are real lat/lon so the maps and distance math are meaningful.
This module is pure data + small helpers; it imports nothing from the app.
"""

import math
from typing import Dict, Any, List, Optional, Tuple

# Each attraction: (name, lat, lon, category)
DESTINATIONS: Dict[str, Dict[str, Any]] = {
    "Jaipur": {
        "emoji": "🏰",
        "tagline": "The Pink City — forts, palaces and Rajput grandeur",
        "lat": 26.9124, "lon": 75.7873,
        "best_season": "Oct – Mar",
        "daily_cost": (1800, 4500),
        "safety": 4.3,
        "transport": "Auto-rickshaw, app cabs (Ola/Uber), city buses",
        "attractions": [
            ("Amber Fort", 26.9855, 75.8513, "Heritage"),
            ("Hawa Mahal", 26.9239, 75.8267, "Heritage"),
            ("City Palace", 26.9258, 75.8237, "Heritage"),
            ("Jal Mahal", 26.9534, 75.8463, "Sightseeing"),
            ("Nahargarh Fort", 26.9374, 75.8155, "Adventure"),
        ],
    },
    "Goa": {
        "emoji": "🏖️",
        "tagline": "Sun, sand and Susegad — India's beach capital",
        "lat": 15.4909, "lon": 73.8278,
        "best_season": "Nov – Feb",
        "daily_cost": (2200, 6000),
        "safety": 4.1,
        "transport": "Rented scooters, taxis, GoaMiles app",
        "attractions": [
            ("Baga Beach", 15.5553, 73.7517, "Beach"),
            ("Calangute Beach", 15.5430, 73.7553, "Beach"),
            ("Basilica of Bom Jesus", 15.5009, 73.9116, "Heritage"),
            ("Fort Aguada", 15.4925, 73.7736, "Sightseeing"),
            ("Palolem Beach", 15.0100, 74.0233, "Beach"),
        ],
    },
    "Delhi": {
        "emoji": "🕌",
        "tagline": "The capital — Mughal monuments meets modern metropolis",
        "lat": 28.6139, "lon": 77.2090,
        "best_season": "Oct – Mar",
        "daily_cost": (1800, 5000),
        "safety": 3.8,
        "transport": "Delhi Metro (extensive), app cabs, autos",
        "attractions": [
            ("India Gate", 28.6129, 77.2295, "Sightseeing"),
            ("Red Fort", 28.6562, 77.2410, "Heritage"),
            ("Qutub Minar", 28.5245, 77.1855, "Heritage"),
            ("Humayun's Tomb", 28.5933, 77.2507, "Heritage"),
            ("Lotus Temple", 28.5535, 77.2588, "Spiritual"),
        ],
    },
    "Mumbai": {
        "emoji": "🌆",
        "tagline": "Maximum City — sea breeze, cinema and street food",
        "lat": 19.0760, "lon": 72.8777,
        "best_season": "Oct – Feb",
        "daily_cost": (2500, 6500),
        "safety": 4.2,
        "transport": "Local trains, metro, app cabs, kaali-peeli taxis",
        "attractions": [
            ("Gateway of India", 18.9220, 72.8347, "Sightseeing"),
            ("Marine Drive", 18.9437, 72.8234, "Sightseeing"),
            ("Elephanta Caves", 18.9633, 72.9315, "Heritage"),
            ("Juhu Beach", 19.0968, 72.8265, "Beach"),
            ("Siddhivinayak Temple", 19.0169, 72.8302, "Spiritual"),
        ],
    },
    "Bangalore": {
        "emoji": "🌳",
        "tagline": "The Garden City — gardens, breweries and tech buzz",
        "lat": 12.9716, "lon": 77.5946,
        "best_season": "Oct – Feb",
        "daily_cost": (2000, 5500),
        "safety": 4.3,
        "transport": "Namma Metro, app cabs, BMTC buses",
        "attractions": [
            ("Lalbagh Botanical Garden", 12.9507, 77.5848, "Nature"),
            ("Bangalore Palace", 12.9988, 77.5921, "Heritage"),
            ("Cubbon Park", 12.9763, 77.5929, "Nature"),
            ("ISKCON Temple", 13.0096, 77.5510, "Spiritual"),
            ("Nandi Hills", 13.3702, 77.6835, "Adventure"),
        ],
    },
    "Udaipur": {
        "emoji": "🛶",
        "tagline": "City of Lakes — palaces mirrored on still water",
        "lat": 24.5854, "lon": 73.7125,
        "best_season": "Sep – Mar",
        "daily_cost": (2000, 6000),
        "safety": 4.4,
        "transport": "Autos, app cabs, boat rides on Lake Pichola",
        "attractions": [
            ("City Palace", 24.5764, 73.6835, "Heritage"),
            ("Lake Pichola", 24.5715, 73.6790, "Sightseeing"),
            ("Jag Mandir", 24.5664, 73.6800, "Heritage"),
            ("Sajjangarh (Monsoon Palace)", 24.5984, 73.6469, "Sightseeing"),
            ("Fateh Sagar Lake", 24.6010, 73.6792, "Nature"),
        ],
    },
    "Varanasi": {
        "emoji": "🪔",
        "tagline": "The spiritual heart — ghats, aartis and the eternal Ganga",
        "lat": 25.3176, "lon": 82.9739,
        "best_season": "Oct – Mar",
        "daily_cost": (1200, 3500),
        "safety": 4.0,
        "transport": "Autos, e-rickshaws, boats on the Ganga",
        "attractions": [
            ("Dashashwamedh Ghat", 25.3052, 83.0107, "Spiritual"),
            ("Kashi Vishwanath Temple", 25.3109, 83.0107, "Spiritual"),
            ("Assi Ghat", 25.2877, 83.0067, "Spiritual"),
            ("Sarnath", 25.3811, 83.0247, "Heritage"),
            ("Manikarnika Ghat", 25.3109, 83.0150, "Spiritual"),
        ],
    },
    "Kolkata": {
        "emoji": "🎭",
        "tagline": "City of Joy — colonial grandeur, art and adda",
        "lat": 22.5726, "lon": 88.3639,
        "best_season": "Oct – Feb",
        "daily_cost": (1500, 4000),
        "safety": 4.2,
        "transport": "Metro, trams, yellow taxis, app cabs",
        "attractions": [
            ("Victoria Memorial", 22.5448, 88.3426, "Heritage"),
            ("Howrah Bridge", 22.5851, 88.3468, "Sightseeing"),
            ("Dakshineswar Temple", 22.6550, 88.3576, "Spiritual"),
            ("Indian Museum", 22.5580, 88.3510, "Heritage"),
            ("Park Street", 22.5530, 88.3520, "Food"),
        ],
    },
    "Agra": {
        "emoji": "🤍",
        "tagline": "Home of the Taj — Mughal marvels on the Yamuna",
        "lat": 27.1767, "lon": 78.0081,
        "best_season": "Oct – Mar",
        "daily_cost": (1500, 4500),
        "safety": 4.0,
        "transport": "Autos, e-rickshaws, app cabs",
        "attractions": [
            ("Taj Mahal", 27.1751, 78.0421, "Heritage"),
            ("Agra Fort", 27.1795, 78.0211, "Heritage"),
            ("Mehtab Bagh", 27.1820, 78.0420, "Nature"),
            ("Fatehpur Sikri", 27.0940, 77.6610, "Heritage"),
            ("Itimad-ud-Daulah", 27.1928, 78.0309, "Heritage"),
        ],
    },
    "Kerala": {
        "emoji": "🌴",
        "tagline": "God's Own Country — backwaters, beaches and spice hills",
        "lat": 9.9312, "lon": 76.2673,
        "best_season": "Sep – Mar",
        "daily_cost": (2000, 5500),
        "safety": 4.6,
        "transport": "Ferries, KSRTC buses, app cabs, houseboats",
        "attractions": [
            ("Fort Kochi", 9.9658, 76.2421, "Heritage"),
            ("Alleppey Backwaters", 9.4981, 76.3388, "Nature"),
            ("Munnar Tea Gardens", 10.0889, 77.0595, "Nature"),
            ("Chinese Fishing Nets", 9.9658, 76.2421, "Sightseeing"),
            ("Varkala Beach", 8.7333, 76.7167, "Beach"),
        ],
    },
    "Pune": {
        "emoji": "🏛️",
        "tagline": "The Oxford of the East — history meets youthful energy",
        "lat": 18.5204, "lon": 73.8567,
        "best_season": "Oct – Feb",
        "daily_cost": (1700, 4500),
        "safety": 4.3,
        "transport": "App cabs, autos, PMPML buses, metro",
        "attractions": [
            ("Shaniwar Wada", 18.5195, 73.8553, "Heritage"),
            ("Aga Khan Palace", 18.5523, 73.9013, "Heritage"),
            ("Sinhagad Fort", 18.3664, 73.7556, "Adventure"),
            ("Dagdusheth Temple", 18.5163, 73.8562, "Spiritual"),
            ("Pataleshwar Caves", 18.5246, 73.8447, "Heritage"),
        ],
    },
    "Lucknow": {
        "emoji": "🍢",
        "tagline": "City of Nawabs — adab, kebabs and Awadhi splendour",
        "lat": 26.8467, "lon": 80.9462,
        "best_season": "Oct – Mar",
        "daily_cost": (1300, 3800),
        "safety": 4.1,
        "transport": "Metro, autos, e-rickshaws, app cabs",
        "attractions": [
            ("Bara Imambara", 26.8693, 80.9120, "Heritage"),
            ("Rumi Darwaza", 26.8696, 80.9128, "Heritage"),
            ("Chota Imambara", 26.8721, 80.9090, "Heritage"),
            ("Hazratganj", 26.8500, 80.9430, "Food"),
            ("British Residency", 26.8649, 80.9270, "Heritage"),
        ],
    },
    "Rishikesh": {
        "emoji": "🧘",
        "tagline": "Yoga capital of the world — rapids, ashrams and the Ganga",
        "lat": 30.0869, "lon": 78.2676,
        "best_season": "Sep – Apr",
        "daily_cost": (1200, 3500),
        "safety": 4.4,
        "transport": "Autos, shared vikrams, rental bikes",
        "attractions": [
            ("Laxman Jhula", 30.1262, 78.3299, "Sightseeing"),
            ("Triveni Ghat", 30.1052, 78.2932, "Spiritual"),
            ("Ram Jhula", 30.1209, 78.3127, "Sightseeing"),
            ("Beatles Ashram", 30.1086, 78.3215, "Sightseeing"),
            ("White-water Rafting (Shivpuri)", 30.1500, 78.3833, "Adventure"),
        ],
    },
    "Rajasthan (non-GT)": {
        "emoji": "🐪",
        "tagline": "Jodhpur & the Thar — blue city, dunes and desert forts",
        "lat": 26.2389, "lon": 73.0243,
        "best_season": "Oct – Mar",
        "daily_cost": (1700, 5000),
        "safety": 4.3,
        "transport": "Autos, app cabs, intercity buses, desert jeeps",
        "attractions": [
            ("Mehrangarh Fort", 26.2978, 73.0184, "Heritage"),
            ("Jaswant Thada", 26.3055, 73.0227, "Heritage"),
            ("Umaid Bhawan Palace", 26.2829, 73.0479, "Heritage"),
            ("Clock Tower & Sardar Market", 26.2929, 73.0240, "Food"),
            ("Jaisalmer Dunes", 26.9157, 70.9083, "Adventure"),
        ],
    },
    "Himachal Pradesh": {
        "emoji": "🏔️",
        "tagline": "Land of the gods — pine valleys, snow peaks and hill towns",
        "lat": 31.1048, "lon": 77.1734,
        "best_season": "Mar – Jun, Dec (snow)",
        "daily_cost": (1500, 4500),
        "safety": 4.5,
        "transport": "Taxis, HRTC buses, toy train (Shimla)",
        "attractions": [
            ("The Ridge, Shimla", 31.1048, 77.1734, "Sightseeing"),
            ("Mall Road", 31.1033, 77.1722, "Food"),
            ("Kufri", 31.0976, 77.2650, "Adventure"),
            ("Jakhoo Temple", 31.1010, 77.1810, "Spiritual"),
            ("Solang Valley (Manali)", 32.3170, 77.1560, "Adventure"),
        ],
    },
    "Northeast India": {
        "emoji": "⛰️",
        "tagline": "Shillong & the hills — waterfalls, living roots and clouds",
        "lat": 25.5788, "lon": 91.8933,
        "best_season": "Oct – May",
        "daily_cost": (1600, 4500),
        "safety": 4.5,
        "transport": "Shared sumos, taxis, local buses",
        "attractions": [
            ("Umiam Lake", 25.6536, 91.8957, "Nature"),
            ("Elephant Falls", 25.5470, 91.8480, "Nature"),
            ("Living Root Bridges (Cherrapunji)", 25.2700, 91.7300, "Adventure"),
            ("Police Bazar", 25.5760, 91.8920, "Food"),
            ("Mawlynnong Village", 25.2030, 91.9170, "Nature"),
        ],
    },
    "Hyderabad": {
        "emoji": "🍛",
        "tagline": "City of Nizams — biryani, pearls and Charminar lanes",
        "lat": 17.3850, "lon": 78.4867,
        "best_season": "Oct – Feb",
        "daily_cost": (1700, 4500),
        "safety": 4.4,
        "transport": "Metro, MMTS, app cabs, autos",
        "attractions": [
            ("Charminar", 17.3616, 78.4747, "Heritage"),
            ("Golconda Fort", 17.3833, 78.4011, "Heritage"),
            ("Hussain Sagar Lake", 17.4239, 78.4738, "Sightseeing"),
            ("Ramoji Film City", 17.2543, 78.6808, "Sightseeing"),
            ("Chowmahalla Palace", 17.3578, 78.4717, "Heritage"),
        ],
    },
}

# Headline photo per destination (Wikimedia Commons file names, served via the
# stable Special:FilePath redirect). These are layered *over* the brand gradient
# in CSS, so a missing/blocked image silently falls back to the gradient banner —
# no broken-image boxes, ever.
IMAGES: Dict[str, str] = {
    "Jaipur": "Hawa_Mahal_2011.jpg",
    "Goa": "Baga_Beach_Goa.jpg",
    "Delhi": "India_Gate_in_New_Delhi_03-2016.jpg",
    "Mumbai": "Mumbai_03-2016_10_skyline_of_Nariman_Point.jpg",
    "Bangalore": "Vidhana_Soudha_evening.jpg",
    "Udaipur": "Lake_Palace_Udaipur.jpg",
    "Varanasi": "Varanasi_Dashashwamedh_Ghat.jpg",
    "Kolkata": "Victoria_Memorial_situated_in_Kolkata.jpg",
    "Agra": "Taj_Mahal,_Agra,_India_edit3.jpg",
    "Kerala": "Kerala_Backwaters_(2).jpg",
    "Pune": "Shaniwarwada_Pune.jpg",
    "Lucknow": "Bara_Imambara_Lucknow.jpg",
    "Rishikesh": "Lakshman_Jhula_Rishikesh.jpg",
    "Rajasthan (non-GT)": "Mehrangarh_Fort_Jodhpur.jpg",
    "Himachal Pradesh": "The_Ridge,_Shimla.jpg",
    "Northeast India": "Umiam_Lake_Meghalaya.jpg",
    "Hyderabad": "Charminar-Pride_of_Hyderabad.jpg",
}

# One-line climate descriptor for the destination-insights card.
CLIMATE: Dict[str, str] = {
    "Jaipur": "Hot, dry summers · crisp pleasant winters",
    "Goa": "Warm & humid coastal · dry Nov–Feb, monsoon Jun–Sep",
    "Delhi": "Extreme — hot summers, foggy cold winters",
    "Mumbai": "Warm & humid year-round · heavy monsoon",
    "Bangalore": "Mild & temperate all year · pleasant evenings",
    "Udaipur": "Warm days, cool nights · best in winter",
    "Varanasi": "Hot summers · cool, misty winter mornings",
    "Kolkata": "Hot, humid summers · comfortable winters",
    "Agra": "Hot dry summers · cool winters, river fog",
    "Kerala": "Tropical & humid · two monsoons, lush greenery",
    "Pune": "Pleasant & moderate · cool monsoon breeze",
    "Lucknow": "Hot summers · cool, foggy winters",
    "Rishikesh": "Cool foothills · refreshing river climate",
    "Rajasthan (non-GT)": "Desert — scorching summers, cool winters",
    "Himachal Pradesh": "Cool hills · snow in winter, pleasant summers",
    "Northeast India": "Cool, misty & rainy · among India's wettest",
    "Hyderabad": "Warm semi-arid · mild, dry winters",
}

# Broad climate class per destination -> drives the Weather Agent's profiles.
# One of: desert | coastal | tropical | plains | temperate | hill
CLIMATE_TYPE: Dict[str, str] = {
    "Jaipur": "desert", "Goa": "coastal", "Delhi": "plains", "Mumbai": "coastal",
    "Bangalore": "temperate", "Udaipur": "desert", "Varanasi": "plains",
    "Kolkata": "plains", "Agra": "plains", "Kerala": "tropical", "Pune": "temperate",
    "Lucknow": "plains", "Rishikesh": "hill", "Rajasthan (non-GT)": "desert",
    "Himachal Pradesh": "hill", "Northeast India": "hill", "Hyderabad": "temperate",
}

_DEFAULT = {
    "emoji": "📍",
    "tagline": "Discover this destination with a smart AI-built plan",
    "lat": 22.5, "lon": 78.9,
    "best_season": "Oct – Mar",
    "daily_cost": (1800, 4500),
    "safety": 4.0,
    "transport": "App cabs, autos and local buses",
    "attractions": [],
    "image": "",
    "climate": "Pleasant for most of the year",
    "climate_type": "plains",
}


def image_url(name: str) -> str:
    """Stable Wikimedia redirect URL for a destination photo (or '' if none)."""
    fname = IMAGES.get(name)
    if not fname:
        return ""
    return f"https://commons.wikimedia.org/wiki/Special:FilePath/{fname}?width=1200"


def get_destination(name: str) -> Dict[str, Any]:
    """Return curated data for a destination, falling back to safe defaults."""
    data = DESTINATIONS.get(name, _DEFAULT)
    merged = {**_DEFAULT, **data, "name": name}
    merged["image"] = image_url(name)
    merged["climate"] = CLIMATE.get(name, _DEFAULT["climate"])
    merged["climate_type"] = CLIMATE_TYPE.get(name, _DEFAULT["climate_type"])
    return merged


def list_destinations() -> List[str]:
    return list(DESTINATIONS.keys())


# ---------------------------------------------------------------------------
# Geo helpers (used by the map + itinerary travel-time estimates)
# ---------------------------------------------------------------------------
URBAN_SPEED_KMH = 22.0  # realistic average city travel speed incl. traffic/stops


def haversine_km(a: Tuple[float, float], b: Tuple[float, float]) -> float:
    """Great-circle distance in km between two (lat, lon) points."""
    lat1, lon1, lat2, lon2 = map(math.radians, (a[0], a[1], b[0], b[1]))
    dlat, dlon = lat2 - lat1, lon2 - lon1
    h = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
    return 2 * 6371.0 * math.asin(math.sqrt(h))


def travel_minutes(km: float) -> int:
    """Rough urban travel time in minutes for a given distance."""
    return max(1, round(km / URBAN_SPEED_KMH * 60))


def match_attraction(activity: str, attractions: List[tuple]) -> Optional[tuple]:
    """Best-effort match of a free-text activity to a known attraction tuple."""
    if not activity:
        return None
    text = activity.lower()
    for attr in attractions:
        name = attr[0].lower()
        core = name.split("(")[0].strip()
        if core and (core in text or text in name):
            return attr
        # token overlap (e.g. "Visit Amber Fort" -> "Amber Fort")
        tokens = [t for t in core.split() if len(t) > 3]
        if tokens and all(t in text for t in tokens):
            return attr
    return None
