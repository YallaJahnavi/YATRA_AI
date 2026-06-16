"""Main ML training orchestrator.

Imports: typing.Dict, typing.Any, sys, pathlib.Path, ml.data_cleaning (clean_budget_data,
clean_accommodation_data), ml.train_model (train_budget_allocator, train_accommodation_recommender)

Orchestrates complete ML training pipeline with 4 steps:
1. Clean budget data
2. Clean accommodation data
3. Train budget allocator model (Regression)
4. Train accommodation recommender model (Classification)
"""

from typing import Dict, Any
import sys
from pathlib import Path
import os
import json

# Add parent directory to path when run as a script
if __name__ == "__main__":
    sys.path.insert(0, str(Path(__file__).parent.parent))

try:
    from ml.data_cleaning import clean_budget_data, clean_accommodation_data
    from ml.train_model import train_budget_allocator, train_accommodation_recommender
except ImportError:
    from .data_cleaning import clean_budget_data, clean_accommodation_data
    from .train_model import train_budget_allocator, train_accommodation_recommender


# TODO: Implement train_pipeline() function
# - Takes optional parameters: data_dir: str = "data", model_dir: str = "ml/models"
# - Returns Dict[str, Any]
# - Step 1: Call clean_budget_data() with input/output paths
# - Step 2: Call clean_accommodation_data() with input/output paths
# - Step 3: Call train_budget_allocator() with cleaned data and model_dir
# - Step 4: Call train_accommodation_recommender() with cleaned data and model_dir
# - Collect results from each step in results dict
# - Return dict with keys:
#   * status: "success" if all steps succeed, "error" otherwise
#   * steps: dict with results from each step


# TODO: Implement entry point
# - If __name__ == "__main__":
#   * Call train_pipeline()
#   * Print results as JSON with indent=2

def train_pipeline(data_dir:str="data",model_dir:str="ml/models") ->Dict[str,Any]:
    results={}
    try:
        training_dir=os.path.join(data_dir,"training_dataset")
        processed_dir=os.path.join(data_dir,"processed")

        os.makedirs(processed_dir,exist_ok=True)
        os.makedirs(model_dir,exist_ok=True)

        budget_input=os.path.join(training_dir,"budget_allocation_training.csv")
        budget_output=os.path.join(processed_dir,"budget_allocation_clean.csv")
        budget_clean_result=clean_budget_data(budget_input,budget_output)

        results["clean_budget_data"]=budget_clean_result

        accommodation_input=os.path.join(training_dir,"accommodation_recommender_training.csv")
        accommodation_output=os.path.join(processed_dir,"accommodation_recommender_clean.csv")

        accommodation_clean_result=clean_accommodation_data(
            accommodation_input,
            accommodation_output,
        )
        results["clean_accommodation_data"]=accommodation_clean_result

        train_budget_result=train_budget_allocator(
            budget_output,
            model_dir
        )
        results["train_budget_allocator"]=train_budget_result

        train_accommodation_result=train_accommodation_recommender(
            accommodation_output,
            model_dir
        )

        results["train_accommodation_recommender"]=train_accommodation_result

        status="success"
        
        for step in results.values():
            if step.get("status")=="error":
                status="error"
        
        return {
            "status":status,
            "steps":results,
        }
    except Exception as e:
        return {
            "status":"error",
            "error_message":str(e),
            "steps":results
        }
if __name__=="__main__":
    pipeline_result=train_pipeline()
    print(json.dumps(pipeline_result,indent=2))
