"""
main.py
-------
End-to-end pipeline for ChatGPT Reviews Analysis.

Usage
-----
    python main.py --data data/chatgpt_reviews.csv
    python main.py --data data/chatgpt_reviews.csv --save-html

The script runs every analysis step and either shows charts interactively
or saves them as HTML files in the ``outputs/`` directory.
"""

import argparse
import logging
import sys
from pathlib import Path

from src.data_loader.loader import load_reviews
from src.preprocessing.cleaner import clean_reviews
from src.analysis.sentiment import add_sentiment, sentiment_over_time
from src.analysis.topic_modeling import extract_phrases, categorise_problems
from src.visualization.charts import (
    plot_sentiment_distribution,
    plot_phrase_frequency,
    plot_problem_categories,
    plot_sentiment_over_time,
)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s  %(levelname)-8s  %(name)s – %(message)s",
    datefmt="%H:%M:%S",
)
logger = logging.getLogger(__name__)


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="ChatGPT Reviews Analysis Pipeline")
    parser.add_argument(
        "--data",
        default="data/chatgpt_reviews.csv",
        help="Path to the reviews CSV (default: data/chatgpt_reviews.csv)",
    )
    parser.add_argument(
        "--save-html",
        action="store_true",
        help="Save charts as HTML files in outputs/ instead of showing them",
    )
    # parse_known_args ignores Jupyter's -f kernel.json argument
    # so this module works both from the CLI and inside a notebook
    args, _ = parser.parse_known_args(argv)
    return args


def save_or_show(fig, name: str, save: bool, output_dir: Path) -> None:
    """Helper: either write the figure to HTML or display it interactively."""
    if save:
        output_dir.mkdir(parents=True, exist_ok=True)
        path = output_dir / f"{name}.html"
        fig.write_html(str(path))
        logger.info(f"Saved chart → {path}")
    else:
        fig.show()


def run(data_path: str, save_html: bool = False) -> None:
    output_dir = Path("outputs")

    # ── 1. Load ──────────────────────────────────────────────────────────
    df = load_reviews(data_path)

    # ── 2. Clean ─────────────────────────────────────────────────────────
    df = clean_reviews(df)

    # ── 3. Sentiment labelling ───────────────────────────────────────────
    df = add_sentiment(df)

    # ── 4. Sentiment distribution ────────────────────────────────────────
    fig = plot_sentiment_distribution(df["Sentiment"].value_counts())
    save_or_show(fig, "01_sentiment_distribution", save_html, output_dir)

    # ── 5. Positive phrase extraction ────────────────────────────────────
    positive_reviews = df[df["Sentiment"] == "Positive"]["Review"]
    pos_phrases = extract_phrases(positive_reviews)
    fig = plot_phrase_frequency(
        pos_phrases,
        title="Common Phrases in Positive Reviews",
        colour="#2ca02c",
    )
    save_or_show(fig, "02_positive_phrases", save_html, output_dir)

    # ── 6. Negative phrase extraction ────────────────────────────────────
    negative_reviews = df[df["Sentiment"] == "Negative"]["Review"]
    neg_phrases = extract_phrases(negative_reviews)
    fig = plot_phrase_frequency(
        neg_phrases,
        title="Common Phrases in Negative Reviews",
        colour="#d62728",
    )
    save_or_show(fig, "03_negative_phrases", save_html, output_dir)

    # ── 7. Problem categorisation ────────────────────────────────────────
    problem_df = categorise_problems(neg_phrases)
    fig = plot_problem_categories(problem_df)
    save_or_show(fig, "04_problem_categories", save_html, output_dir)

    # ── 8. Sentiment over time ───────────────────────────────────────────
    monthly = sentiment_over_time(df)
    fig = plot_sentiment_over_time(monthly)
    save_or_show(fig, "05_sentiment_over_time", save_html, output_dir)

    logger.info("Pipeline complete ✓")


if __name__ == "__main__":
    args = parse_args()
    try:
        run(data_path=args.data, save_html=args.save_html)
    except FileNotFoundError as exc:
        logger.error(exc)
        sys.exit(1)
