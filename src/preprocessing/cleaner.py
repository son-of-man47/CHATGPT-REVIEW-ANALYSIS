"""
preprocessing/cleaner.py
------------------------
Data cleaning pipeline for the ChatGPT reviews dataset.

Steps:
  1. Fill missing reviews with a placeholder string.
  2. Parse and normalise the 'Review Date' column to datetime.
  3. Strip leading/trailing whitespace from text columns.
"""

import pandas as pd
import logging

logger = logging.getLogger(__name__)

PLACEHOLDER_REVIEW = "NO REVIEWS"


def clean_reviews(df: pd.DataFrame) -> pd.DataFrame:
    """
    Apply the full cleaning pipeline to the raw reviews DataFrame.

    Parameters
    ----------
    df : pd.DataFrame
        Raw DataFrame as returned by ``data_loader.loader.load_reviews``.

    Returns
    -------
    pd.DataFrame
        Cleaned DataFrame with:
        - Null reviews replaced by ``PLACEHOLDER_REVIEW``
        - 'Review Date' parsed to ``datetime64``
        - Text columns stripped of whitespace
    """
    df = df.copy()

    # ── 1. Fill missing reviews ──────────────────────────────────────────
    null_count = df["Review"].isna().sum()
    if null_count:
        logger.info(f"Filling {null_count} null reviews with '{PLACEHOLDER_REVIEW}'")
    df["Review"] = df["Review"].fillna(PLACEHOLDER_REVIEW)

    # ── 2. Parse review date ─────────────────────────────────────────────
    df["Review Date"] = pd.to_datetime(df["Review Date"], errors="coerce")
    invalid_dates = df["Review Date"].isna().sum()
    if invalid_dates:
        logger.warning(f"{invalid_dates} rows have unparseable dates and will have NaT.")

    # ── 3. Strip whitespace from text columns ────────────────────────────
    text_cols = df.select_dtypes(include="object").columns
    for col in text_cols:
        df[col] = df[col].str.strip()

    logger.info("Cleaning complete.")
    return df
