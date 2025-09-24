# tt_gutenberg/authors.py
from .util import load_data, flatten_list
import pandas as pd

def list_authors(by_languages=False, alias=False, language_filter=None):
    """
    Return a list of author aliases (or names). If by_languages=True,
    returns aliases ordered by translation count (distinct language count).
    alias=True => use alias column; otherwise use the author name.
    language_filter: list of languages to consider (e.g., ['en'] or ['English'])
    """
    authors_df, languages_df, metadata_df = load_data()  # loads CSVs at call time

    # Build a column all_names (list per author) depending on alias flag
    if alias:
        # keep alias only if present (not NaN / not empty)
        authors_df['all_names'] = authors_df.apply(
            lambda r: [r['alias'].strip()] if pd.notna(r.get('alias')) and str(r['alias']).strip() else [],
            axis=1
        )
    else:
        authors_df['all_names'] = authors_df['author'].apply(lambda x: [x] if pd.notna(x) else [])

    # If filtering/sorting by language translations:
    if by_languages:
        # Merge metadata and languages
        merged = metadata_df.merge(languages_df, on="gutenberg_id", suffixes=("_meta", "_lang"))
        # Filter by language if requested
        if language_filter:
            merged = merged[merged["language_lang"].isin(language_filter)]
        # Count distinct languages per author (translation count)
        lang_counts = merged.groupby("gutenberg_author_id")["language_lang"].nunique()

        # map counts back to authors_df (set index to gutenberg_author_id)
        authors_df = authors_df.set_index('gutenberg_author_id')
        authors_df['translation_count'] = lang_counts
        authors_df['translation_count'] = authors_df['translation_count'].fillna(0).astype(int)

        # Keep only authors who have an alias (non-empty) and sort by translation_count desc
        authors_with_alias = authors_df[authors_df['all_names'].map(lambda x: len(x) > 0)].copy()
        authors_with_alias = authors_with_alias.sort_values('translation_count', ascending=False)

        # Extract alias values (flatten)
        alias_lists = authors_with_alias['all_names'].tolist()  # list of lists
        aliases = flatten_list(alias_lists)
        # final cleaning: strip and drop tiny/malformed values
        aliases = [a.strip() for a in aliases if isinstance(a, str) and len(a.strip()) > 1]
        return aliases

    # If not by_languages: just return flat list of names/aliases (no sorting)
    all_names_lists = authors_df['all_names'].tolist()
    result = flatten_list(all_names_lists)
    result = [r.strip() for r in result if isinstance(r, str) and len(r.strip()) > 1]
    return result
