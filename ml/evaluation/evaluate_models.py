"""Evaluate trained ML models.

Imports: pandas as pd, numpy as np, pickle, os, sys, pathlib.Path, typing.Dict,
typing.Any, sklearn.preprocessing (StandardScaler, LabelEncoder), sklearn.metrics
(r2_score, mean_squared_error, mean_absolute_error, mean_absolute_percentage_error,
accuracy_score, precision_score, recall_score, f1_score, confusion_matrix, classification_report)

Evaluates trained ML models on evaluation datasets and returns metrics.
"""

import pandas as pd
import numpy as np
import pickle
import os
import sys
from pathlib import Path
from typing import Dict, Any
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.metrics import (
    r2_score, mean_squared_error, mean_absolute_error,
    mean_absolute_percentage_error,
    accuracy_score, precision_score, recall_score, f1_score,
    confusion_matrix, classification_report
)


# TODO: Implement evaluate_all_models() function
# - Takes optional project_root: str = None parameter
# - Returns Dict[str, Any] with evaluation results
# - If project_root is None, use current working directory
# - Construct paths to evaluation dataset and model directories
# - Call evaluate_models() with paths
# - Return evaluation results dict


# TODO: Implement evaluate_models() function
# - Takes eval_data_dir: str and model_dir: str parameters
# - Returns Dict[str, Any] with evaluation results
# - Load budget allocation evaluation CSV
# - Load accommodation recommender evaluation CSV
# - Evaluate budget allocator model:
#   * Load model, scaler, encoder from model_dir
#   * Extract features and target from evaluation data
#   * Predict using model
#   * Calculate metrics: MAPE, RMSE, MAE, R² score, samples count
# - Evaluate accommodation recommender model:
#   * Load model, scaler, encoder from model_dir
#   * Extract features and target from evaluation data
#   * Predict using model
#   * Calculate metrics: accuracy, precision, recall, f1_score, samples count
# - Return dict with structure:
#   * status: "success" or "error"
#   * budget_allocator: dict with MAPE, RMSE, MAE, samples
#   * accommodation_recommender: dict with accuracy, precision, recall, samples
#   * error_message (if applicable)
def evaluate_all_models(project_root:str=None)->Dict[str,Any]:
    try:
        if project_root is None:
            project_root=os.getcwd()
        eval_data_dir=os.path.join(project_root,"data","processed")
        model_dir=os.path.join(project_root,"ml","models")
        return evaluate_models(eval_data_dir,model_dir)
    except Exception as e:
        return {
            "status":"error",
            "error_message":str(e),
        }
    
def evaluate_models(eval_data_dir: str, model_dir: str) -> Dict[str, Any]:
    try:
        results = {
            "status": "success",
            "budget_allocator": {},
            "accommodation_recommender": {},
        }

        # =========================
        # ✅ BUDGET MODEL EVALUATION
        # =========================
        budget_file = os.path.join(eval_data_dir, "budget_allocation_clean.csv")

        if os.path.exists(budget_file):
            df = pd.read_csv(budget_file)

            feature_cols = [
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

            target_cols = [
                "accommodation_budget_pct",
                "food_dining_budget_pct",
                "activities_attractions_budget_pct",
                "local_transport_budget_pct",
                "shopping_misc_budget_pct",
                "contingency_budget_pct",
            ]

            X = df[feature_cols].copy()
            y_true = df[target_cols].values

            # Load artifacts
            model = pickle.load(open(os.path.join(model_dir, "budget_allocator_model.pkl"), "rb"))
            scaler = pickle.load(open(os.path.join(model_dir, "budget_allocator_scaler.pkl"), "rb"))
            encoders = pickle.load(open(os.path.join(model_dir, "budget_allocator_encoder.pkl"), "rb"))

            # Encode
            for col, le in encoders.items():
                X[col] = le.transform(X[col].astype(str))

            # Scale
            X_scaled = scaler.transform(X)

            # Predict
            y_pred = model.predict(X_scaled)

            # Metrics
            mape = float(mean_absolute_percentage_error(y_true, y_pred))
            rmse = float(np.sqrt(mean_squared_error(y_true, y_pred)))
            mae = float(mean_absolute_error(y_true, y_pred))
            r2 = float(r2_score(y_true, y_pred))

            results["budget_allocator"] = {
                "MAPE": mape,
                "RMSE": rmse,
                "MAE": mae,
                "R2": r2,
                "samples": len(df),
            }

        # =========================
        # ✅ ACCOMMODATION MODEL
        # =========================
        acc_file = os.path.join(eval_data_dir, "accommodation_recommender_clean.csv")

        if os.path.exists(acc_file):
            df = pd.read_csv(acc_file)

            feature_cols = [
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

            target_col = "accommodation_type"

            X = df[feature_cols].copy()
            y_true = df[target_col].values

            # Load artifacts
            model = pickle.load(open(os.path.join(model_dir, "accommodation_recommender_model.pkl"), "rb"))
            scaler = pickle.load(open(os.path.join(model_dir, "accommodation_recommender_scaler.pkl"), "rb"))
            encoders = pickle.load(open(os.path.join(model_dir, "accommodation_recommender_encoder.pkl"), "rb"))

            # Encode
            for col, le in encoders.items():
                X[col] = le.transform(X[col].astype(str))

            # Boolean fix
            if "is_group_trip" in X.columns:
                X["is_group_trip"] = X["is_group_trip"].astype(int)

            # Scale
            X_scaled = scaler.transform(X)

            # Predict
            y_pred = model.predict(X_scaled)

            # Metrics
            acc = float(accuracy_score(y_true, y_pred))
            precision = float(precision_score(y_true, y_pred, average="weighted", zero_division=0))
            recall = float(recall_score(y_true, y_pred, average="weighted", zero_division=0))
            f1 = float(f1_score(y_true, y_pred, average="weighted", zero_division=0))

            results["accommodation_recommender"] = {
                "accuracy": acc,
                "precision": precision,
                "recall": recall,
                "f1_score": f1,
                "samples": len(df),
            }

        return results

    except Exception as e:
        return {
            "status": "error",
            "error_message": str(e)
        }
