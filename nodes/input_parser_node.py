"""Input Parser Node - validates user input.

Imports: state.TravelPlanState

Constants:
  - valid_destinations: List of 17 supported destination names
  - Budget range: 5,000 - 500,000 INR
  - Trip duration: 2 - 30 days
  - Group size: 1 - 10 people
"""

from state import TravelPlanState


# TODO: Implement input_parser_node() function
# - Takes state: TravelPlanState parameter
# - Returns TravelPlanState
# - Define valid_destinations list with 17 supported destinations
# - Validate input fields:
#   * destination: must be in valid_destinations
#   * total_budget_inr: must be between 5,000 and 500,000
#   * trip_duration_days: must be between 2 and 30
#   * group_size: must be between 1 and 10
# - Collect errors in list for each validation failure
# - Set state fields:
#   * validation_errors: list of error strings
#   * parsing_complete: True if no errors, False otherwise
# - If errors exist:
#   * Extend state["error_messages"] with errors
#   * Set error_occurred = True
# - Return modified state
# - On exception: append error message, set error_occurred=True, parsing_complete=False

def input_parser_node(state: TravelPlanState)-> TravelPlanState:
  try:
    valid_destinations=[
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
    errors=[]

    destination = state.get("destination")
    total_budget = state.get("total_budget_inr",0)
    duration = state.get("trip_duration_days",0)
    group_size = state.get("group_size",1)

    if destination not in valid_destinations:
      errors.append("Invalid destination selected")

    if not (5000 <= total_budget <= 500000):
      errors.append("Total budget must be between 5000 and 500000 INR")
    
    if not (2 <= duration <=30):
      errors.append("Trip duration must be between 2 and 30 days")
    
    if not (1<= group_size<=10):
      errors.append("Group size must be between 1 and 10")
    
    state["validation_errors"]=errors

    if errors:
      state["parsing_complete"]=False
      state.setdefault("error_messages",[]).extend(errors)
      state["error_occurred"]=True

    else:
      state["parsing_complete"]=True
    
    return state
  
  except Exception as e:
    state.setdefault("error_messages",[]).append(str(e))
    state["error_occurred"]=True
    state["parsing_complete"]=False

    return state
