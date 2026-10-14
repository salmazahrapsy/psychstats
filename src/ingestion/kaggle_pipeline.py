import os
import sys
import zipfile
import pandas as pd
from kaggle.api.kaggle_api_extended import KaggleApi

def ingest_kaggle_dataset(dataset_slug: str, target_dir: str = "data/raw"):
    """
    Downloads and stages a dataset from Kaggle into data/raw/.
    Example slug: 'rakeshkapilavai/extrovert-vs-introvert-behavior-data'
    """
    print(f"--- Ingesting Kaggle Dataset: {dataset_slug} ---")
    
    # Initialize and authenticate API client
    api = KaggleApi()
    api.authenticate()
    print("✓ Authenticated with Kaggle API")

    os.makedirs(target_dir, exist_ok=True)
    
    # Download dataset archive
    print(f"Downloading files to {target_dir}...")
    api.dataset_download_files(dataset_slug, path=target_dir, unzip=True)
    print("✓ Download and unzipping complete")

    # Audit downloaded files
    extracted_files = [f for f in os.listdir(target_dir) if f.endswith(('.csv', '.json', '.xlsx'))]
    print(f"\nDiscovered {len(extracted_files)} data files in {target_dir}:")
    
    for filename in extracted_files:
        filepath = os.path.join(target_dir, filename)
        if filename.endswith('.csv'):
            try:
                df = pd.read_csv(filepath)
                print(f"  • {filename} — {df.shape[0]} rows, {df.shape[1]} columns")
            except Exception as e:
                print(f"  • {filename} (Error reading preview: {e})")
        else:
            print(f"  • {filename}")

if __name__ == "__main__":
    # Default to an open psychology dataset from your search if no argument passed
    slug = sys.argv[1] if len(sys.argv) > 1 else "rakeshkapilavai/extrovert-vs-introvert-behavior-data"
    ingest_kaggle_dataset(slug)
