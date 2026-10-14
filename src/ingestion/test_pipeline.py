import os
import requests
import pandas as pd
from io import StringIO

def run_extraction_test():
    print("1. Fetching open psychology/behavioral benchmark data...")
    dataset_url = "https://raw.githubusercontent.com/mwaskom/seaborn-data/master/iris.csv"
    headers = {"User-Agent": "SalmaZahra-Research-Pipeline/1.0"}
    
    response = requests.get(dataset_url, headers=headers, timeout=10)
    response.raise_for_status()
    print(f"✓ Download succeeded (HTTP {response.status_code})")

    print("\n2. Processing dataframe with pandas...")
    df = pd.read_csv(StringIO(response.text))
    print(f"✓ Shape: {df.shape[0]} rows, {df.shape[1]} columns")
    print("\nDescriptive Summary:")
    print(df.describe().T[["mean", "std", "min", "max"]])

    print("\n3. Exporting to data/raw/...")
    csv_out = "data/raw/benchmark_metrics.csv"
    xlsx_out = "data/raw/benchmark_metrics.xlsx"
    df.to_csv(csv_out, index=False)
    df.to_excel(xlsx_out, engine="openpyxl", index=False)
    print(f"✓ Saved {csv_out}")
    print(f"✓ Saved {xlsx_out}")

if __name__ == "__main__":
    run_extraction_test()
