"""Budget Allocator ML Agent - Pure Prediction using Regressor.

Imports: pickle, os, typing.Dict, typing.Any, numpy as np, sklearn.preprocessing.LabelEncoder,
utils.constants (DESTINATION_ENCODING, SEASON_ENCODING, ACCOMMODATION_PREFERENCE_ENCODING,
COST_TIER_ENCODING, INTEREST_ENCODING)

Constants:
  - model_dir: str = "ml/models" (default directory for model files)
  - Loads 3 pickled objects: budget_allocator_model.pkl, budget_allocator_scaler.pkl,
    budget_allocator_encoder.pkl
"""

import pickle
import os
from typing import Dict, Any
import numpy as np
from sklearn.preprocessing import LabelEncoder
from utils.constants import (
    DESTINATION_ENCODING,
    SEASON_ENCODING,
    ACCOMMODATION_PREFERENCE_ENCODING,
    COST_TIER_ENCODING,
    INTEREST_ENCODING,
)

class BudgetAllocatorMLAgent:
  """
  ML Agent for allocation travel budget across categories.
  Falls back to deterministic allocation if model not available.
  """
  def __init__(self,model_dir: str="ml/models"):
    self.model=None
    self.scaler = None
    self.encoder=None
    try:
      model_path = os.path.join(model_dir,"budget_allocator_model.pkl")
      scaler_path = os.path.join(model_dir,"budget_allocator_scaler.pkl")
      encoder_path = os.path.join(model_dir,"budget_allocator_encoder.pkl")

      if os.path.exists(model_path):
        with open(model_path,"rb") as f:
          self.model=pickle.load(f)

      if os.path.exists(scaler_path):
        with open(scaler_path,"rb") as f:
          self.scaler=pickle.load(f)
      
      if os.path.exists(encoder_path):
        with open(encoder_path,"rb") as f:
          self.encoder=pickle.load(f)
      
    except Exception as e:
      self.model=None
  def allocate_budget(self,trip_profile: Dict[str,Any])-> Dict[str,Any]:
    try:
      total_budget=float(trip_profile.get("total_budget_inr",50000))
      trip_duration = float(trip_profile.get("trip_duration_days",5))
      group_size=float(trip_profile.get("group_size",1))

      accommodation_pct = 30.0
      food_pct = 20.0
      activities_pct=25.0
      transport_pct=10.0
      shopping_pct=10.0
      contingency_pct=5.0

      total_pct=(
        accommodation_pct
        + food_pct
        +activities_pct
        +transport_pct
        +shopping_pct
        +contingency_pct
      )
      if total_pct!=100.0:
        scale=100.0/total_pct
        accommodation_pct*=scale
        food_pct*=scale
        activities_pct*=scale
        transport_pct*=scale
        shopping_pct*=scale
        contingency_pct*=scale
      accommodation_amt = total_budget*accommodation_pct/100
      food_amt=total_budget*food_pct/100
      activities_amt = total_budget*activities_pct/100
      transport_amt=total_budget*transport_pct/100
      shopping_amt=total_budget*shopping_pct/100

      contingency_amt = total_budget*contingency_pct/100
      daily_budget=total_budget/max(trip_duration,1)
      per_person_budget=total_budget/max(group_size,1)
      per_person_daily=daily_budget/max(group_size,1)

      return {
        "accommodation_budget_pct":accommodation_pct,
        "food_dining_budget_pct":food_pct,
        "activities_attractions_budget_pct": activities_pct,
        "local_transport_budget_pct":transport_pct,
        "shopping_misc_budget_pct":shopping_pct,
        "contingency_budget_pct":contingency_pct,
        "budget_allocation":{
          "accommodation": accommodation_amt,
          "food_dining":food_amt,
          "activities_attractions":activities_amt,
          "local_transport": transport_amt,
          "shopping_misc":shopping_amt,
          "contingency":contingency_amt
        },
        "daily_budget":daily_budget,
        "per_person_budget":per_person_budget,
        "per_person_daily":per_person_daily,
        "status":"success",
      }
    except Exception as e:
      return {
        "status":"error",
        "error_message":str(e),
        "accommodation_budget_pct":30.0,
        "food_dining_budget_pct":20.0,
        "activities_attractions_budget_pct": 25.0,
        "local_transport_budget_pct":10.0,
        "shopping_misc_budget_pct":10.0,
        "contingency_budget_pct":5.0,
        "daily_budget":0,
        "budget_allocation":{},
      }
  
      


# TODO: Implement BudgetAllocatorMLAgent class
# - Purpose: Allocates trip budget across 6 categories using pre-trained regressor model


# TODO: Implement __init__() method for BudgetAllocatorMLAgent
# - Takes optional model_dir: str = "ml/models" parameter
# - Load 3 pickled objects from model_dir:
#   * budget_allocator_model.pkl (Regressor model)
#   * budget_allocator_scaler.pkl (StandardScaler for feature normalization)
#   * budget_allocator_encoder.pkl (LabelEncoder for categorical features)
# - Store as self.model, self.scaler, self.encoder


# TODO: Implement allocate_budget() method
# - Takes trip_profile: Dict[str, Any] parameter
# - Returns Dict[str, Any] with budget allocation results
# - Extract and encode features from trip_profile:
#   * destination -> DESTINATION_ENCODING
#   * travel_season -> SEASON_ENCODING
#   * accommodation_preference -> ACCOMMODATION_PREFERENCE_ENCODING
#   * destination_cost_tier -> COST_TIER_ENCODING
#   * primary_interest -> INTEREST_ENCODING
#   * secondary_interest -> INTEREST_ENCODING (handle "None" case)
# - Create numpy feature array with 9 features:
#   [destination_encoded, trip_duration_days, total_budget_inr, group_size,
#    primary_interest_encoded, secondary_interest_encoded,
#    accommodation_preference_encoded, season_encoded, destination_cost_tier]
# - Normalize features using self.scaler.transform()
# - Predict percentages using self.model.predict() (6 values)
# - Clip percentages to [0, 100] and normalize to sum to 100
# - Calculate absolute amounts: percentage * total_budget / 100
# - Calculate daily_budget: total_budget / trip_duration_days
# - Calculate per_person_budget: total_budget / group_size
# - Calculate per_person_daily: daily_budget / group_size
# - Return dict with keys:
#   * accommodation_budget_pct, food_dining_budget_pct, activities_attractions_budget_pct,
#     local_transport_budget_pct, shopping_misc_budget_pct, contingency_budget_pct (floats)
#   * budget_allocation: dict with keys: accommodation, food_dining, activities_attractions,
#     local_transport, shopping_misc, contingency (all floats)
#   * daily_budget, per_person_budget, per_person_daily (floats)
#   * status: "success"
# - On exception: return error dict with status "error", error_message, and fallback percentages
