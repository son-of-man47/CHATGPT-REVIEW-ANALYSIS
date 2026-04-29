"""
analysis/sentiment.py
----------------------
Sentiment analysis using TextBlob polarity scoring.

Each review is labelled as:
  - 'Positive'  → polarity > 0
  - 'Negative'  → polarity < 0
  - 'Neutral'   → polarity == 0
"""

import pandas as pd
import logging
from textblob import TextBlob

logger = logging.getLogger(__name__)


def _classify_polarity(review: str) -> str:
    """Return sentiment label for a single review string."""
    polarity = TextBlob(str(review)).sentiment.polarity
    if polarity > 0:
        return "Positive"
    elif polarity < 0:
        return "Negative"
    return "Neutral"


def add_sentiment(df: pd.DataFrame, review_col: str = "Review") -> pd.DataFrame:
    """
    Append a 'Sentiment' column to *df* based on TextBlob polarity.

    Parameters
    ----------
    df : pd.DataFrame
        Cleaned reviews DataFrame.
    review_col : str
        Name of the column containing review text.

    Returns
    -------
    pd.DataFrame
        DataFrame with new 'Sentiment' column added in-place on a copy.
    """
    df = df.copy()
    logger.info("Computing TextBlob sentiment for all reviews …")
    df["Sentiment"] = df[review_col].apply(_classify_polarity)
    counts = df["Sentiment"].value_counts().to_dict()
    logger.info(f"Sentiment distribution: {counts}")
    return df


def sentiment_over_time(df: pd.DataFrame) -> pd.DataFrame:
    """
    Aggregate monthly sentiment counts for trend analysis.

    Parameters
    ----------
    df : pd.DataFrame
        DataFrame with 'Review Date' (datetime) and 'Sentiment' columns.

    Returns
    -------
    pd.DataFrame
        Wide-format DataFrame indexed by month (datetime) with one column
        per sentiment label and integer counts as values.
    """
    monthly = (
        df.groupby([df["Review Date"].dt.to_period("M"), "Sentiment"])
        .size()
        .unstack(fill_value=0)
    )
    monthly.index = monthly.index.to_timestamp()
    return monthly
