"""Clean budget allocation training data.

Imports: pandas as pd, typing.Dict, typing.Any, typing.Tuple

Cleans budget allocation dataset: handles missing values, validates percentage constraints,
saves processed version to output file.
"""

import pandas as pd
from typing import Dict, Any, Tuple


# TODO: Implement clean_budget_data() function
# - Takes input_file: str and output_file: str parameters
# - Returns Dict[str, Any] with cleaning results
# - Load raw data from input_file using pd.read_csv()
# - Record original_rows count
# - Handle missing values:
#   * Categorical columns: destination, primary_interest, secondary_interest,
#     accommodation_preference, travel_season, transport_mode
#   * Fill with mode value (or "Unknown" if no mode)
# - Validate percentage constraints:
#   * Percentage columns: accommodation_budget_pct, food_dining_budget_pct,
#     activities_attractions_budget_pct, local_transport_budget_pct,
#     shopping_misc_budget_pct, contingency_budget_pct
#   * Keep only rows where each percentage is 0-100
#   * Keep only rows where sum of percentages is approximately 100
# - Save cleaned data to output_file
# - Return dict with keys:
#   * status: "success" or "error"
#   * rows_before: original count
#   * rows_after: count after cleaning
#   * rows_removed: count of removed rows
#   * error_message (if applicable)
def clean_budget_data(input_file:str,output_file:str)->Dict[str,Any]:
    try:
        df= pd.read_csv(input_file)

        original_rows = len(df)

        categorical_cols = [
            "destination",
            "primary_interest",
            "secondary_interest",
            "accommodation_preference",
            "travel_season",
            "transport_mode",
        ]
        for col in categorical_cols:
            if col in df.columns:
                mode_val=df[col].mode()
                fill_val=mode_val.iloc[0] if not mode_val.empty else "Unknown"
                df[col]=df[col].fillna(fill_val)
        
        pct_cols=[
            "accommodation_budget_pct",
            "food_dining_budget_pct",
            "activities_attractions_budget_pct",
            "local_transport_budget_pct",
            "shopping_misc_budget_pct",
            "contingency_budget_pct",
        ]

        for col in pct_cols:
            if col in df.columns:
                df=df[(df[col]>=0) & (df[col]<=100)]
        if all(col in df.columns for col in pct_cols):
            df["pct_sum"]=df[pct_cols].sum(axis=1)
            df=df[(df["pct_sum"]>=99)&(df["pct_sum"]<=101)]
            df=df.drop(columns=["pct_sum"])
        rows_after=len(df)
        rows_removed=original_rows-rows_after

        df.to_csv(output_file,index=False)
        return{
            "status":"success",
            "rows_before":original_rows,
            "rows_after":rows_after,
            "rows_removed":rows_removed
        }
    except Exception as e:
        return {
            "status":"error",
            "error_message":str(e),
            "rows_before":0,
            "rows_after":0,
            "rows_removed":0,
        }

if __name__ == "__main__":
    input_file = "data/training_dataset/budget_allocation_training.csv"
    output_file = "data/processed/budget_allocation_clean.csv"

    result = clean_budget_data(input_file, output_file)
    print(result)
