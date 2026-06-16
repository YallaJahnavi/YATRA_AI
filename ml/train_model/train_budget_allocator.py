"""Train Budget Allocator ML model.

Imports: pandas as pd, numpy as np, pickle, os, typing.Dict, typing.Any,
sklearn.preprocessing (StandardScaler, LabelEncoder), sklearn.model_selection.train_test_split,
sklearn.metrics (r2_score, mean_squared_error, mean_absolute_error)

Trains Regressor model for budget allocation. Loads cleaned data, trains model,
saves model + scaler + encoder to files. Performs regression on 6 budget percentage targets.
"""

import pandas as pd
import numpy as np
import pickle
import os
from typing import Dict, Any
from sklearn.ensemble import *
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score, mean_squared_error, mean_absolute_error


# TODO: Implement train_budget_allocator() function
# - Takes data_file: str and model_dir: str parameters
# - Returns Dict[str, Any] with training results
# - Load cleaned data from data_file
# - Define feature columns (9 features):
#   * destination, trip_duration_days, total_budget_inr, group_size,
#     primary_interest, secondary_interest, accommodation_preference,
#     travel_season, destination_cost_tier
# - Define target columns (6 budget percentages):
#   * accommodation_budget_pct, food_dining_budget_pct,
#     activities_attractions_budget_pct, local_transport_budget_pct,
#     shopping_misc_budget_pct, contingency_budget_pct
# - Separate features and targets
# - Encode categorical features using LabelEncoder (or similar)
# - Scale features using StandardScaler
# - Split into train/test (80/20 with random state)
# - Train Regressor model on training data
# - Evaluate on test data: R² score, RMSE, MAE
# - Save model, scaler, encoder to model_dir
# - Return dict with keys:
#   * status: "success" or "error"
#   * r2_score, rmse, mae (regression metrics)
#   * samples: number of training samples
#   * error_message (if applicable)
def train_budget_allocator(data_file:str,model_dir:str)->Dict[str,Any]:
    try:
        os.makedirs(model_dir,exist_ok=True)
        df=pd.read_csv(data_file)
        feature_cols=[
            "destination",
            "trip_duration_days",
            "total_budget_inr",
            "group_size",
            "primary_interest",
            "secondary_interest",
            "accommodation_preference",
            "travel_season",
            "destination_cost_tier",
        ]
        target_cols=[
            "accommodation_budget_pct",
            "food_dining_budget_pct",
            "activities_attractions_budget_pct",
            "local_transport_budget_pct",
            "shopping_misc_budget_pct",
            "contingency_budget_pct",
        ]
        X=df[feature_cols].copy()
        y=df[target_cols].copy()

        encoders={}
        categorical_cols=[
            "destination",
            "primary_interest",
            "secondary_interest",
            "accommodation_preference",
            "travel_season",
            "destination_cost_tier",
        ]
        for col in categorical_cols:
            le=LabelEncoder()
            X[col]=le.fit_transform(X[col].astype(str))
            encoders[col]=le
        scaler=StandardScaler()
        X_scaled=scaler.fit_transform(X)
        X_train,X_test,y_train,y_test=train_test_split(
            X_scaled,y,test_size=0.2,random_state=42
        )
        model=RandomForestRegressor(
            n_estimators=50,
            random_state=42,
        )
        model.fit(X_train,y_train)
        y_pred=model.predict(X_test)
        r2=float(r2_score(y_test,y_pred))
        rmse=float(np.sqrt(mean_squared_error(y_test,y_pred)))
        mae=float(mean_absolute_error(y_test,y_pred))
        
        with open(os.path.join(model_dir,"budget_allocator_model.pkl"),"wb") as f:
            pickle.dump(model,f)
        
        with open(os.path.join(model_dir,"budget_allocator_scaler.pkl"),"wb") as f:
            pickle.dump(scaler,f)
            
        with open(os.path.join(model_dir,"budget_allocator_encoder.pkl"),"wb") as f:
            pickle.dump(encoders,f)
        
        return {
            "status":"success",
            "r2_score":r2,
            "rmse":rmse,
            "mae":mae,
            "samples":len(df),
        }
    except Exception as e:
        return {
            "status":"error",
            "error_message":str(e)
        }
