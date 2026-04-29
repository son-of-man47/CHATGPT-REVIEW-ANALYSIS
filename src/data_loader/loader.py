"""
data_loader/loader.py
---------------------
Handles loading and initial validation of the ChatGPT reviews dataset.
"""

import pandas as pd
import logging
from pathlib import Path

logger = logging.getLogger(__name__)


def load_reviews(filepath: str | Path) -> pd.DataFrame:
    """
    Load the ChatGPT reviews CSV into a pandas DataFrame.

    Parameters
    ----------
    filepath : str or Path
        Path to the reviews CSV file.

    Returns
    -------
    pd.DataFrame
        Raw reviews DataFrame.

    Raises
    ------
    FileNotFoundError
        If the specified file does not exist.
    ValueError
        If required columns are missing from the CSV.
    """
    filepath = Path(filepath)

    if not filepath.exists():
        raise FileNotFoundError(f"Dataset not found at: {filepath}")

    logger.info(f"Loading dataset from {filepath}")
    df = pd.read_csv(filepath)

    required_columns = {"Review", "Review Date"}
    missing = required_columns - set(df.columns)
    if missing:
        raise ValueError(f"Missing required columns: {missing}")

    logger.info(f"Loaded {len(df):,} reviews with columns: {list(df.columns)}")
    return df
