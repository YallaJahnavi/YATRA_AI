"""Interactive trip map (streamlit-folium + OpenStreetMap).

Plots the trip's attractions as numbered markers, optimises the visiting order
with a nearest-neighbour route from the city centre, draws the route line, and
reports total route distance + estimated travel time. Points are pulled from the
generated itinerary (geo-matched to curated attractions) and topped up from the
destination's curated attraction set so the map is always meaningful.
"""

from typing import Any, List, Tuple, Dict

import streamlit as st
import folium
from streamlit_folium import st_folium

from ui.destinations import get_destination, match_attraction, haversine_km, travel_minutes
from ui.itinerary_cards import normalize_itinerary

# category -> marker colour (folium named colours)
_CAT_COLOR = {
    "Heritage": "purple", "Beach": "blue", "Spiritual": "darkpurple",
    "Adventure": "orange", "Nature": "green", "Food": "red",
    "Sightseeing": "cadetblue",
}


def _collect_points(destination: str, itinerary: Any) -> List[Tuple[str, float, float, str]]:
    """Attractions to plot: itinerary matches first, then curated picks, de-duped."""
    d = get_destination(destination)
    attractions = d.get("attractions", [])
    seen, points = set(), []

    for day in normalize_itinerary(itinerary):
        for act in day["activities"]:
            m = match_attraction(act, attractions)
            if m and m[0] not in seen:
                seen.add(m[0])
                points.append(m)

    for attr in attractions:  # top up so the map is never empty
        if attr[0] not in seen:
            seen.add(attr[0])
            points.append(attr)

    return points


def _optimize_route(start: Tuple[float, float],
                    points: List[Tuple[str, float, float, str]]) -> List[Tuple[str, float, float, str]]:
    """Nearest-neighbour ordering from the city centre (lightweight TSP heuristic)."""
    remaining = list(points)
    ordered, cur = [], start
    while remaining:
        nxt = min(remaining, key=lambda p: haversine_km(cur, (p[1], p[2])))
        ordered.append(nxt)
        cur = (nxt[1], nxt[2])
        remaining.remove(nxt)
    return ordered


def _route_distance(points: List[Tuple[str, float, float, str]]) -> float:
    return sum(
        haversine_km((points[i][1], points[i][2]), (points[i + 1][1], points[i + 1][2]))
        for i in range(len(points) - 1)
    )


def render_trip_map(destination: str, itinerary: Any) -> None:
    """Render the interactive map section for the given trip."""
    d = get_destination(destination)
    center = (d["lat"], d["lon"])

    points = _collect_points(destination, itinerary)
    if not points:
        st.info("Map markers will appear here once your itinerary is generated.")
        return

    ordered = _optimize_route(center, points)
    dist = _route_distance(ordered)

    # ---- headline metrics ----
    c1, c2, c3 = st.columns(3)
    c1.metric("📍 Attractions mapped", len(ordered))
    c2.metric("🛣️ Optimised route", f"{dist:.1f} km")
    c3.metric("⏱️ Est. travel time", f"~{travel_minutes(dist)} min")
    st.caption("Route ordered by a nearest-neighbour optimiser from the city centre · powered by OpenStreetMap")

    # ---- folium map ----
    fmap = folium.Map(location=center, zoom_start=12, tiles="CartoDB positron", control_scale=True)

    folium.Marker(
        center, tooltip=f"{destination} — city centre",
        icon=folium.Icon(color="lightgray", icon="home", prefix="fa"),
    ).add_to(fmap)

    route_coords = [center]
    for i, (name, lat, lon, cat) in enumerate(ordered, 1):
        route_coords.append((lat, lon))
        folium.Marker(
            (lat, lon),
            tooltip=f"{i}. {name}",
            popup=folium.Popup(f"<b>{i}. {name}</b><br><span style='color:#64748b'>{cat}</span>", max_width=220),
            icon=folium.Icon(color=_CAT_COLOR.get(cat, "blue"), icon="star", prefix="fa"),
        ).add_to(fmap)

    folium.PolyLine(
        route_coords, color="#7C3AED", weight=4, opacity=0.75, dash_array="8,6",
    ).add_to(fmap)

    fmap.fit_bounds([[min(p[0] for p in route_coords), min(p[1] for p in route_coords)],
                     [max(p[0] for p in route_coords), max(p[1] for p in route_coords)]])

    st_folium(fmap, use_container_width=True, height=480, returned_objects=[])

    # ---- ordered legend ----
    chips = "".join(
        f'<span class="pill">{i}. {name}</span>' for i, (name, *_rest) in enumerate(ordered, 1)
    )
    st.markdown(f'<div class="glass-card"><b>🧭 Suggested visiting order</b><div style="margin-top:10px;">{chips}</div></div>',
                unsafe_allow_html=True)
