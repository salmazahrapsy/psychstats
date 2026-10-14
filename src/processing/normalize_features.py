import os
import sys
import json
import pandas as pd
import numpy as np

def normalize_dataset(
    input_file: str = "data/raw/benchmark_metrics.csv",
    output_file: str = "data/processed/normalized_metrics.csv",
    metadata_file: str = "data/processed/transformation_metadata.json"
):
    print(f"=== Starting Feature Normalization ===")
    print(f"Reading input: {input_file}")
    
    if not os.path.exists(input_file):
        print(f"Error: {input_file} not found. Ensure raw data exists first.")
        sys.exit(1)
        
    df = pd.read_csv(input_file)
    print(f"Loaded raw shape: {df.shape[0]} rows, {df.shape[1]} columns")

    # Separate numeric behavioral traits from categorical identifiers
    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    categorical_cols = [c for c in df.columns if c not in numeric_cols]
    print(f"Identified {len(numeric_cols)} numeric metric columns: {numeric_cols}")

    processed_df = df.copy()
    metadata = {"columns": {}}

    for col in numeric_cols:
        series = processed_df[col].dropna()
        mean_val = float(series.mean())
        std_val = float(series.std(ddof=1))
        min_val = float(series.min())
        max_val = float(series.max())
        
        # 1. Z-Score Standardization: (x - mean) / std
        if std_val > 0:
            processed_df[f"{col}_zscore"] = (processed_df[col] - mean_val) / std_val
        else:
            processed_df[f"{col}_zscore"] = 0.0

        # 2. Min-Max Normalization: (x - min) / (max - min)
        denom = max_val - min_val
        if denom > 0:
            processed_df[f"{col}_minmax"] = (processed_df[col] - min_val) / denom
        else:
            processed_df[f"{col}_minmax"] = 0.0

        # 3. IQR Outlier Detection
        q25 = float(series.quantile(0.25))
        q75 = float(series.quantile(0.75))
        iqr = q75 - q25
        lower_bound = q25 - (1.5 * iqr)
        upper_bound = q75 + (1.5 * iqr)
        outlier_count = int(((series < lower_bound) | (series > upper_bound)).sum())

        metadata["columns"][col] = {
            "mean": round(mean_val, 4),
            "std": round(std_val, 4),
            "min": round(min_val, 4),
            "max": round(max_val, 4),
            "iqr_outliers": outlier_count
        }

    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    processed_df.to_csv(output_file, index=False)
    print(f"✓ Saved processed metrics to: {output_file}")

    with open(metadata_file, "w", encoding="utf-8") as f:
        json.dump(metadata, f, indent=2)
    print(f"✓ Saved transformation metadata to: {metadata_file}")

    print("\nSample Transformed Columns:")
    preview_cols = [c for c in processed_df.columns if "_zscore" in c or "_minmax" in c][:4]
    print(processed_df[preview_cols].head(3))

if __name__ == "__main__":
    src = sys.argv[1] if len(sys.argv) > 1 else "data/raw/benchmark_metrics.csv"
    normalize_dataset(input_file=src)
