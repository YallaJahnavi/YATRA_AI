"""Train Accommodation Recommender ML model.

Imports: pandas as pd, numpy as np, pickle, os, typing.Dict, typing.Any,
sklearn.preprocessing (StandardScaler, LabelEncoder), sklearn.metrics
(accuracy_score, precision_score, recall_score, f1_score, classification_report)

Trains Classifier model for accommodation type recommendation. Loads cleaned data,
trains model, saves model + scaler + encoder to files. Performs classification on 4 classes.
"""

import pandas as pd
import numpy as np
import pickle
import os
from typing import Dict, Any
from sklearn.ensemble import *
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, classification_report
from sklearn.model_selection import train_test_split

# TODO: Implement train_accommodation_recommender() function
# - Takes data_file: str and model_dir: str parameters
# - Returns Dict[str, Any] with training results
# - Load cleaned data from data_file
# - Define feature columns (9 features):
#   * destination, total_trip_budget_inr, accommodation_budget_inr, trip_duration_days,
#     group_size, primary_interest, travel_season, destination_cost_tier, is_group_trip
# - Define target column: accommodation_type (0, 1, 2, or 3)
# - Separate features and targets
# - Encode categorical features using LabelEncoder:
#   * destination, primary_interest, travel_season, destination_cost_tier
# - Convert boolean columns to int
# - Scale features using StandardScaler
# - Split into train/test (80/20 with random state)
# - Train Classifier model on training data
# - Evaluate on test data: accuracy, precision, recall, f1_score
# - Save model, scaler, encoder to model_dir
# - Return dict with keys:
#   * status: "success" or "error"
#   * accuracy, precision, recall, f1_score (classification metrics)
#   * samples: number of training samples
#   * class_distribution: dict with counts for classes 0-3
#   * error_message (if applicable)
def train_accommodation_recommender(data_file:str,model_dir:str)->Dict[str,Any]:
    try:
        os.makedirs(model_dir,exist_ok=True)
        df=pd.read_csv(data_file)
        feature_cols=[
            "destination",
            "total_trip_budget_inr",
            "accommodation_budget_inr",
            "trip_duration_days",
            "group_size",
            "primary_interest",
            "travel_season",
            "destination_cost_tier",
            "is_group_trip",
        ]
        target_col="accommodation_type"
        X=df[feature_cols].copy()
        y=df[target_col]
        encoders={}
        categorical_cols=[
            "destination",
            "primary_interest",
            "travel_season",
            "destination_cost_tier",
        ]
        for col in categorical_cols:
            le=LabelEncoder()
            X[col]=le.fit_transform(X[col].astype(str))
            encoders[col]=le
        if "is_group_trip" in X.columns:
            X["is_group_trip"]=X["is_group_trip"].astype(int)
        scaler=StandardScaler()
        X_scaled=scaler.fit_transform(X)
        X_train,X_test,y_train,y_test=train_test_split(
            X_scaled,y,test_size=0.2,random_state=42
        )
        model=RandomForestClassifier(n_estimators=50,random_state=42)
        model.fit(X_train,y_train)
        y_pred=model.predict(X_test)
        accuracy=float(accuracy_score(y_test,y_pred))
        precision=float(precision_score(y_test,y_pred,average="weighted",zero_division=0))
        recall=float(recall_score(y_test,y_pred,average="weighted",zero_division=0))
        f1=float(f1_score(y_test,y_pred,average="weighted",zero_division=0))
        with open(os.path.join(model_dir,"accommodation_recommender_model.pkl"),"wb") as f:
            pickle.dump(model,f)
        with open(os.path.join(model_dir,"accommodation_recommender_scaler.pkl"),"wb") as f:
            pickle.dump(scaler,f)
        with open(os.path.join(model_dir,"accommodation_recommender_encoder.pkl"),"wb") as f:
            pickle.dump(encoders,f)
        class_distribution=y.value_counts().to_dict()
        return{
            "status":"success",
            "accuracy":accuracy,
            "precision":precision,
            "recall":recall,
            "f1_score":f1,
            "samples":len(df),
            "class_distribution":class_distribution,
        }
    except Exception as e:
        return {
            "status":"error",
            "error_message":str(e),
        }
