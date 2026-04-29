"""
analysis/topic_modeling.py
--------------------------
Phrase extraction and problem categorisation for positive/negative reviews.

Uses scikit-learn's CountVectorizer to surface the most common bi-grams
and tri-grams in each sentiment group.  Negative phrases are then bucketed
into four problem categories using keyword matching.
"""

from __future__ import annotations

import pandas as pd
import logging
from sklearn.feature_extraction.text import CountVectorizer

logger = logging.getLogger(__name__)

# ── Default problem taxonomy ─────────────────────────────────────────────────
PROBLEM_CATEGORIES: dict[str, list[str]] = {
    "Responses and Answers Quality": [
        "wrong answer", "gives wrong", "incorrect", "inaccurate",
        "wrong", "bad response", "irrelevant", "useless", "poor",
    ],
    "App Performance": [
        "bad", "lag", "freeze", "crash", "bug", "loading", "glitch",
    ],
    "User Interface": [
        "poor", "interface", "ui", "layout", "difficult", "confusing",
    ],
    "General Features": [
        "network", "feature missing", "poor", "not working",
        "not available", "poor network", "no network",
    ],
}


def extract_phrases(
    reviews: pd.Series,
    ngram_range: tuple[int, int] = (2, 3),
    max_features: int = 100,
) -> pd.DataFrame:
    """
    Extract the most frequent n-grams from a Series of review strings.

    Parameters
    ----------
    reviews : pd.Series
        Series of review text strings.
    ngram_range : tuple[int, int]
        Min and max n-gram size (default bi- and tri-grams).
    max_features : int
        Maximum vocabulary size for the CountVectorizer.

    Returns
    -------
    pd.DataFrame
        Columns: ['Phrase', 'Frequency'], sorted descending by frequency.
    """
    if reviews.empty:
        logger.warning("Empty reviews Series; returning empty phrase DataFrame.")
        return pd.DataFrame(columns=["Phrase", "Frequency"])

    vectorizer = CountVectorizer(
        stop_words="english",
        ngram_range=ngram_range,
        max_features=max_features,
    )
    X = vectorizer.fit_transform(reviews.astype(str))
    phrase_counts = X.sum(axis=0).A1          # convert matrix row → 1-D array
    phrases = vectorizer.get_feature_names_out()

    phrase_df = (
        pd.DataFrame({"Phrase": phrases, "Frequency": phrase_counts})
        .sort_values("Frequency", ascending=False)
        .reset_index(drop=True)
    )
    return phrase_df


def categorise_problems(
    phrase_df: pd.DataFrame,
    categories: dict[str, list[str]] | None = None,
) -> pd.DataFrame:
    """
    Map negative phrases to problem categories via keyword matching.

    Parameters
    ----------
    phrase_df : pd.DataFrame
        Output of ``extract_phrases`` for negative reviews.
    categories : dict, optional
        Custom category → keyword-list mapping.  Defaults to
        ``PROBLEM_CATEGORIES``.

    Returns
    -------
    pd.DataFrame
        Columns: ['Problem Category', 'Count'], one row per category.
    """
    if categories is None:
        categories = PROBLEM_CATEGORIES

    problem_counts: dict[str, int] = {cat: 0 for cat in categories}

    for _, row in phrase_df.iterrows():
        phrase = row["Phrase"].lower()
        freq = int(row["Frequency"])
        for category, keywords in categories.items():
            if any(kw in phrase for kw in keywords):
                problem_counts[category] += freq
                break  # assign to the first matching category only

    return pd.DataFrame(
        list(problem_counts.items()),
        columns=["Problem Category", "Count"],
    ).sort_values("Count", ascending=False).reset_index(drop=True)
