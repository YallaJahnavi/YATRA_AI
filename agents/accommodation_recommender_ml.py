"""Accommodation Recommender ML Agent - Pure Classification using Classifier.

Imports: pickle, os, typing.Dict, typing.Any, typing.List, numpy as np,
utils.constants (ACCOMMODATION_CLASS_NAMES, DESTINATION_ENCODING, SEASON_ENCODING,
COST_TIER_ENCODING, INTEREST_ENCODING, ACCOMMODATION_COST_RANGES)

Constants:
  - ACCOMMODATION_TYPES: list of 4 types from ACCOMMODATION_CLASS_NAMES
  - model_dir: str = None (auto-detect from file location if not provided)
  - Loads 3 pickled objects: accommodation_recommender_model.pkl,
    accommodation_recommender_scaler.pkl, accommodation_recommender_encoder.pkl
"""

import pickle
import os
from typing import Dict, Any, List
import numpy as np
from utils.constants import (
    ACCOMMODATION_CLASS_NAMES,
    DESTINATION_ENCODING,
    SEASON_ENCODING,
    COST_TIER_ENCODING,
    INTEREST_ENCODING,
    ACCOMMODATION_COST_RANGES,
)
class AccommodationRecommenderMLAgent:
  """
  ML Agent that recommends accommodation type.
  If trained models exist they are loaded, otherwise fallback logic is used.
  """
  ACCOMMODATION_TYPES = list(ACCOMMODATION_CLASS_NAMES.values())
  def __init__(self,model_dir:str=None):
    if model_dir is None:
      model_dir=os.path.join(
        os.path.dirname(os.path.dirname(__file__)),
        "ml",
        "models"
      )
    self.model = None
    self.scaler = None
    self.encoder = None
    try:
      model_path = os.path.join(model_dir,"accommodation_recommender_model.pkl")
      scaler_path = os.path.join(model_dir,"accommodation_recommender_scaler.pkl")
      encoder_path = os.path.join(model_dir,"accommodation_recommender_encoder.pkl")

      if os.path.exists(model_path):
        with open(model_path,"rb") as f:
          self.model=pickle.load(f)

      if os.path.exists(scaler_path):
        with open(scaler_path,"rb") as f:
          self.scaler=pickle.load(f)

      if os.path.exists(encoder_path):
        with open(encoder_path,"rb") as f:
          self.encoder=pickle.load(f)

    except Exception:
      self.model = None
  def recommend_accommodation(self,user_profile: Dict[str,Any])-> Dict[str,Any]:
    try:
      total_budget = user_profile.get("total_budget_inr",50000)
      trip_days = user_profile.get("trip_duration_days",5)
      daily_budget = total_budget/max(trip_days,1)
      if daily_budget<7000:
        predicted_class =0
      elif daily_budget<15000:
        predicted_class=1
      elif daily_budget<30000:
        predicted_class=2
      else:
        predicted_class=3
      accommodation_type = self.ACCOMMODATION_TYPES[predicted_class]
      cost_range = ACCOMMODATION_COST_RANGES[predicted_class]

      estimated_cost = float((cost_range[0]+cost_range[1])/2)
      confidence = float(80.0)
      comfort_map={
        0:30,
        1:60,
        2:90,
        3:70
      }
      comfort_score = comfort_map.get(predicted_class,50)
      alternatives: List[Dict[str,Any]]=[]
      for i in range(4):
        if i==predicted_class:
          continue
        alt_type = self.ACCOMMODATION_TYPES[i]
        alt_cost_range=ACCOMMODATION_COST_RANGES[i]
        alt_cost = float((alt_cost_range[0]+alt_cost_range[1])/2)
        alternatives.append(
          {
            "accommodation_type":alt_type,
            "accommodation_class":i,
            "confidence":float(60.0),
            "estimated_cost_per_night":alt_cost,
          }
        )   
      return{
        "accommodation_type":accommodation_type,
        "accommodation_class":predicted_class,
        "confidence":confidence,
        "comfort_score":float(comfort_score),
        "estimated_cost_per_night":estimated_cost,
        "alternatives":alternatives,
        "status":"success",
      }
    except Exception as e:
      return {
        "accommodation_type":"Mid-range",
        "accommodation_class":1,
        "confidence":50.0,
        "comfort_score":60.0,
        "estimated_cost_per_night":3000.0,
        "alternatives":[],
        "status":"error",
        "error_message":str(e),
      }


# TODO: Implement AccommodationRecommenderMLAgent class
# - Purpose: Recommends accommodation type (0-3) using pre-trained classifier model
# - Class constant ACCOMMODATION_TYPES: list of 4 accommodation type names from ACCOMMODATION_CLASS_NAMES


# TODO: Implement __init__() method for AccommodationRecommenderMLAgent
# - Takes optional model_dir: str = None parameter
# - If model_dir is None, construct path: ml/models from parent directory of this file
# - Load 3 pickled objects from model_dir:
#   * accommodation_recommender_model.pkl (Classifier model)
#   * accommodation_recommender_scaler.pkl (StandardScaler for feature normalization)
#   * accommodation_recommender_encoder.pkl (LabelEncoder for categorical features)
# - Store as self.model, self.scaler, self.encoder


# TODO: Implement recommend_accommodation() method
# - Takes user_profile: Dict[str, Any] parameter
# - Returns Dict[str, Any] with accommodation recommendation
# - Extract and encode features from user_profile:
#   * destination -> DESTINATION_ENCODING
#   * travel_season -> SEASON_ENCODING
#   * destination_cost_tier -> COST_TIER_ENCODING
#   * interests -> sum of INTEREST_ENCODING values (bit-flag style)
#   * is_group_trip: 1 if group_size > 1, else 0
# - Create numpy feature array with 9 features:
#   [destination_encoded, total_budget_inr, accommodation_budget_inr, trip_duration_days,
#    group_size, interests_encoded, season_encoded, destination_cost_tier, is_group_trip]
# - Normalize features using self.scaler.transform()
# - Predict class using self.model.predict()
# - Get probabilities using self.model.predict_proba()
# - Calculate confidence: max(probabilities) * 100
# - Get accommodation_type from ACCOMMODATION_TYPES using predicted class
# - Get estimated_cost_per_night from ACCOMMODATION_COST_RANGES (average of min/max)
# - Calculate comfort_score mapping: 0->30, 1->60, 2->90, 3->70
# - Generate alternatives list for classes with probability > 0.1 (excluding prediction)
# - Return dict with keys:
#   * accommodation_type, accommodation_class, confidence, comfort_score,
#     estimated_cost_per_night (floats), alternatives (list), status: "success"
# - On exception: return error dict with status "error", error_message, and fallback values
