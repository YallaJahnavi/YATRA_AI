"""LangGraph workflow definition for YatraAI.

Imports: langgraph.graph.StateGraph, state.TravelPlanState, nodes.input_parser_node.input_parser_node,
nodes.input_normalizer_node.input_normalizer_node, nodes.budget_allocator_node.budget_allocator_node,
nodes.decision_router_nodes (budget_feasibility_router, trip_complexity_analyzer),
nodes.accommodation_recommender_node (accommodation_recommender_low_budget_node,
accommodation_recommender_mid_budget_node, accommodation_recommender_high_budget_node),
nodes.itinerary_generator_node.itinerary_generator_node, nodes.itinerary_revision_node.itinerary_validator_and_reviser_node,
nodes.local_insights_node.local_insights_node, nodes.booking_strategy_node.booking_strategy_node
"""

from langgraph.graph import StateGraph
from state import TravelPlanState
from nodes.input_parser_node import input_parser_node
from nodes.input_normalizer_node import input_normalizer_node
from nodes.budget_allocator_node import budget_allocator_node
from nodes.decision_router_nodes import budget_feasibility_router, trip_complexity_analyzer
from nodes.accommodation_recommender_node import (
    accommodation_recommender_low_budget_node,
    accommodation_recommender_mid_budget_node,
    accommodation_recommender_high_budget_node,
)
from nodes.itinerary_generator_node import itinerary_generator_node
from nodes.itinerary_revision_node import itinerary_validator_and_reviser_node
from nodes.local_insights_node import local_insights_node
from nodes.booking_strategy_node import booking_strategy_node


# TODO: Implement build_trip_planning_graph() function
# - Returns compiled LangGraph StateGraph
# - Create StateGraph with TravelPlanState
# - Add nodes (12 total):
#   Stage 1 (Input Processing): input_parser, input_normalizer
#   Stage 2 (Budget): budget_allocator
#   Stage 3 (Decision): budget_feasibility_router
#   Stage 4 (Accommodation): accommodation_recommender_low_budget, mid_budget, high_budget
#   Stage 5 (Decision): trip_complexity_analyzer
#   Stage 6 (Itinerary): itinerary_generator, itinerary_validator_and_reviser
#   Stage 7 (LLM): local_insights, booking_strategy
# - Set entry point to "input_parser"
# - Add sequential edges: input_parser -> input_normalizer -> budget_allocator -> budget_feasibility_router
# - Add conditional edges from budget_feasibility_router using route_by_budget():
#   * Route based on daily_budget_tier state value
#   * If "low_budget_path" -> accommodation_recommender_low_budget
#   * If "high_budget_path" -> accommodation_recommender_high_budget
#   * Else -> accommodation_recommender_mid_budget
# - Add convergence edges: all 3 accommodation nodes -> trip_complexity_analyzer
# - Add sequential edges: trip_complexity_analyzer -> itinerary_generator -> itinerary_validator_and_reviser
# - Add sequential edges: itinerary_validator_and_reviser -> local_insights -> booking_strategy
# - Set finish point to "booking_strategy"
# - Return graph.compile()


# TODO: Implement route_by_budget() function (nested inside build_trip_planning_graph)
# - Takes state: TravelPlanState parameter
# - Returns str (node name)
# - Extract daily_budget_tier from state with "mid_budget_path" default
# - Return appropriate node name based on budget tier value


# TODO: Implement get_workflow_structure() function
# - Returns Dict[str, Any] with workflow metadata
# - Include "nodes" list with all 12 node names
# - Include "workflow" string describing stage sequence
# - Include "description" string about the workflow purpose


def build_trip_planning_graph():
    graph=StateGraph(TravelPlanState)
    #stage1
    graph.add_node("input_parser",input_parser_node)
    graph.add_node("input_normalizer",input_normalizer_node)

    #stage2
    graph.add_node("budget_allocator",budget_allocator_node)

    #stage3
    graph.add_node("budget_feasibility_router",budget_feasibility_router)

    #stage4
    graph.add_node("accommodation_recommender_low_budget",accommodation_recommender_low_budget_node)
    graph.add_node("accommodation_recommender_mid_budget",accommodation_recommender_mid_budget_node)
    graph.add_node("accommodation_recommender_high_budget",accommodation_recommender_high_budget_node)

    #stage5
    graph.add_node("trip_complexity_analyzer",trip_complexity_analyzer)

    #stage6
    graph.add_node("itinerary_generator",itinerary_generator_node)
    graph.add_node("itinerary_validator_and_reviser",itinerary_validator_and_reviser_node)

    #stage7
    graph.add_node("local_insights",local_insights_node)
    graph.add_node("booking_strategy",booking_strategy_node)

    #Entry point 
    graph.set_entry_point("input_parser")

    #sequential flow
    graph.add_edge("input_parser","input_normalizer")
    graph.add_edge("input_normalizer","budget_allocator")
    graph.add_edge("budget_allocator","budget_feasibility_router")

    #budeget routing 
    def route_by_budget(state: TravelPlanState):
        tier=state.get("daily_budget_tier","mid_budget_path")
        if tier=="low_budget_path":
            return "accommodation_recommender_low_budget"
        if tier =="high_budget_path":
            return "accommodation_recommender_high_budget"

        return "accommodation_recommender_mid_budget"
    graph.add_conditional_edges(
    "budget_feasibility_router",
            route_by_budget,
    {
        "accommodation_recommender_low_budget":"accommodation_recommender_low_budget",
        "accommodation_recommender_mid_budget":"accommodation_recommender_mid_budget",
        "accommodation_recommender_high_budget":"accommodation_recommender_high_budget",

    },

    )

    #Convergence 
    graph.add_edge("accommodation_recommender_low_budget","trip_complexity_analyzer")
    graph.add_edge("accommodation_recommender_mid_budget","trip_complexity_analyzer")
    graph.add_edge("accommodation_recommender_high_budget","trip_complexity_analyzer")

    #Remaining flow 
    graph.add_edge("trip_complexity_analyzer","itinerary_generator")
    graph.add_edge("itinerary_generator","itinerary_validator_and_reviser")
    graph.add_edge("itinerary_validator_and_reviser","local_insights")
    graph.add_edge("local_insights","booking_strategy")

    graph.set_finish_point("booking_strategy")
    return graph.compile()
def get_workflow_structure():
    return {
        "nodes":[
            "input_parser",
            "input_normalizer",
            "budget_allocator",
            "budget_feasibility_router",
            "accommodation_recommender_low_budget",
            "accommodation_recommender_mid_budget",
            "accommodation_recommender_high_budget",
            "trip_complexity_analyzer",
            "itinerary_generator",
            "itinerary_validator_and_reviser",
            "local_insights",
            "booking_strategy",
        ],
        "workflow":"Input -> Budget -> Accommodation -> Complexity -> Itinerary -> Insights -> Booking",
        "description":"LangGraph workflow  for AI-powered travel itinerary optimization",
    }
