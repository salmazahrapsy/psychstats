import os
import pandas as pd
import numpy as np
import pytest
from src.processing.normalize_features import normalize_dataset

def test_normalization_math(tmp_path):
    # Create synthetic test dataset
    raw_csv = tmp_path / "test_raw.csv"
    processed_csv = tmp_path / "test_norm.csv"
    meta_json = tmp_path / "test_meta.json"

    df = pd.DataFrame({
        "trait_score": [10.0, 20.0, 30.0, 40.0, 50.0],
        "category": ["A", "B", "A", "B", "A"]
    })
    df.to_csv(raw_csv, index=False)

    normalize_dataset(
        input_file=str(raw_csv),
        output_file=str(processed_csv),
        metadata_file=str(meta_json)
    )

    result = pd.read_csv(processed_csv)
    
    # Verify Z-score properties (mean ~ 0, std ~ 1)
    z_scores = result["trait_score_zscore"]
    assert np.isclose(z_scores.mean(), 0.0, atol=1e-5)
    assert np.isclose(z_scores.std(ddof=1), 1.0, atol=1e-5)

    # Verify Min-Max range [0, 1]
    minmax = result["trait_score_minmax"]
    assert minmax.min() == 0.0
    assert minmax.max() == 1.0

def test_wiki_table_generation():
    from src.utils.sync_to_wiki import dataframe_to_wikitable
    df = pd.DataFrame({"Construct": ["Working Memory"], "Reliability_Alpha": [0.89]})
    wikitext = dataframe_to_wikitable(df, title="Test Table")
    
    assert '{| class="wikitable sortable"' in wikitext
    assert "Working Memory" in wikitext
    assert "0.89" in wikitext
