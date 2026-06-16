"""Clean accommodation recommender training data.

Imports: pandas as pd, typing.Dict, typing.Any

Cleans accommodation dataset: handles missing values, validates class distribution,
saves processed version to output file.
"""

import pandas as pd
from typing import Dict, Any


# TODO: Implement clean_accommodation_data() function
# - Takes input_file: str and output_file: str parameters
# - Returns Dict[str, Any] with cleaning results
# - Load raw data from input_file using pd.read_csv()
# - Record original_rows count
# - Handle missing values:
#   * Categorical columns: destination, primary_interest, travel_season
#   * Fill with mode value (or "Unknown" if no mode)
#   * Fill numeric columns with median
# - Validate accommodation_type:
#   * Keep only rows where accommodation_type is 0, 1, 2, or 3
# - Check class distribution:
#   * Record count for each class (0, 1, 2, 3)
# - Save cleaned data to output_file
# - Return dict with keys:
#   * status: "success" or "error"
#   * rows_before: original count
#   * rows_after: count after cleaning
#   * rows_removed: count of removed rows
#   * class_distribution: dict with counts for classes 0-3
#   * error_message (if applicable)
def clean_accommodation_data(input_file:str,output_file:str)->Dict[str,Any]:
    try:
        df=pd.read_csv(input_file)
        original_rows=len(df)
        categorical_cols=["destination","primary_interest","travel_season"]
        for col in categorical_cols:
            if col in df.columns:
                mode_val=df[col].mode()
                fill_val = mode_val.iloc[0] if not mode_val.empty else "Unknown"
                df[col] = df[col].fillna(fill_val)

        numeric_cols = df.select_dtypes(include=["number"]).columns

        for col in numeric_cols:
            median_val = df[col].median()
            df[col] = df[col].fillna(median_val)

        if "accommodation_type" in df.columns:
            df = df[df["accommodation_type"].isin([0,1,2,3])]

        class_distribution = {}

        if "accommodation_type" in df.columns:
            for cls in [0,1,2,3]:
                class_distribution[cls] = int((df["accommodation_type"]==cls).sum())
        rows_after = len(df)
        rows_removed = original_rows - rows_after

        df.to_csv(output_file,index=False)

        return {
            "status": "success",
            "rows_before": original_rows,
            "rows_after":rows_after,
            "rows_removed":rows_removed,
            "class_distribution":class_distribution,
        }

    except Exception as e:
        return {
            "status":"error",
            "error_message":str(e),
            "rows_before":0,
            "rows_after":0,
            "rows_removed":0,
            "class_distribution":{},

        }
    
if __name__ == "__main__":
    input_file = "data/training_dataset/accommodation_recommender_training.csv"
    output_file = "data/processed/accommodation_recommender_clean.csv"

    result = clean_accommodation_data(input_file, output_file)
    print(result)
