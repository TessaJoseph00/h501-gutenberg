# tt_gutenberg/helper.py

import pandas as pd
import os

def load_data():
    BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

    authors_df = pd.read_csv(os.path.join(BASE_DIR, "gutenberg_authors.csv"))
    languages_df = pd.read_csv(os.path.join(BASE_DIR, "gutenberg_languages.csv"))
    metadata_df = pd.read_csv(os.path.join(BASE_DIR, "gutenberg_metadata.csv"))

    return authors_df, languages_df, metadata_df
