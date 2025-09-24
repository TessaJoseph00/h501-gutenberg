# tt_gutenberg/util.py

import pandas as pd
import os

def load_data():
    """Load the three CSVs and return (authors_df, languages_df, metadata_df)."""
    BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

    authors_df = pd.read_csv(os.path.join(BASE_DIR, "gutenberg_authors.csv"))
    languages_df = pd.read_csv(os.path.join(BASE_DIR, "gutenberg_languages.csv"))
    metadata_df = pd.read_csv(os.path.join(BASE_DIR, "gutenberg_metadata.csv"))

    return authors_df, languages_df, metadata_df

def flatten_list(nested_list):
    """Flatten a list of lists into one list (simple, readable loop)."""
    flat = []
    for sub in nested_list:
        for item in sub:
            flat.append(item)
    return flat