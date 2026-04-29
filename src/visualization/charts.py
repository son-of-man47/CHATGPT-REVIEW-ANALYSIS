"""
visualization/charts.py
-----------------------
All Plotly chart-building functions for the ChatGPT Reviews Analysis.

Each function returns a ``plotly.graph_objects.Figure`` so it can be:
  - shown interactively  →  fig.show()
  - saved to HTML/PNG    →  fig.write_html("out.html")
  - embedded in a report →  pio.to_json(fig)
"""

from __future__ import annotations

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Colour palette
SENTIMENT_COLOURS = {
    "Positive": "#2ca02c",   # green
    "Neutral":  "#7f7f7f",   # grey
    "Negative": "#d62728",   # red
}


def plot_sentiment_distribution(sentiment_counts: pd.Series) -> go.Figure:
    """
    Bar chart of Positive / Neutral / Negative review counts.

    Parameters
    ----------
    sentiment_counts : pd.Series
        Output of ``df['Sentiment'].value_counts()``.

    Returns
    -------
    go.Figure
    """
    colours = [SENTIMENT_COLOURS.get(s, "#1f77b4") for s in sentiment_counts.index]
    fig = go.Figure(
        data=[
            go.Bar(
                x=sentiment_counts.index,
                y=sentiment_counts.values,
                marker_color=colours,
                text=sentiment_counts.values,
                textposition="outside",
            )
        ]
    )
    fig.update_layout(
        title="Sentiment Distribution of Reviews",
        xaxis_title="Sentiment",
        yaxis_title="Number of Reviews",
        template="plotly_white",
    )
    return fig


def plot_phrase_frequency(
    phrase_df: pd.DataFrame,
    title: str,
    colour: str = "#2ca02c",
) -> go.Figure:
    """
    Horizontal bar chart of phrase frequencies.

    Parameters
    ----------
    phrase_df : pd.DataFrame
        DataFrame with columns ['Phrase', 'Frequency'].
    title : str
        Chart title.
    colour : str
        Bar fill colour (hex).

    Returns
    -------
    go.Figure
    """
    top20 = phrase_df.head(20)   # keep chart readable
    fig = px.bar(
        top20,
        x="Frequency",
        y="Phrase",
        orientation="h",
        title=title,
        color_discrete_sequence=[colour],
        width=900,
        height=600,
        template="plotly_white",
    )
    fig.update_layout(
        xaxis_title="Frequency",
        yaxis_title="Phrase",
        yaxis={"categoryorder": "total ascending"},
    )
    return fig


def plot_problem_categories(problem_df: pd.DataFrame) -> go.Figure:
    """
    Bar chart mapping negative reviews to problem categories.

    Parameters
    ----------
    problem_df : pd.DataFrame
        Output of ``analysis.topic_modeling.categorise_problems``.

    Returns
    -------
    go.Figure
    """
    fig = px.bar(
        problem_df,
        x="Problem Category",
        y="Count",
        title="Common Problems Encountered with ChatGPT",
        color="Count",
        color_continuous_scale="Reds",
        template="plotly_white",
    )
    fig.update_layout(
        xaxis_title="Problem Category",
        yaxis_title="Frequency",
    )
    return fig


def plot_sentiment_over_time(monthly_df: pd.DataFrame) -> go.Figure:
    """
    Multi-line chart showing monthly sentiment trends.

    Parameters
    ----------
    monthly_df : pd.DataFrame
        Output of ``analysis.sentiment.sentiment_over_time``.
        Index → month (datetime), columns → sentiment labels, values → counts.

    Returns
    -------
    go.Figure
    """
    fig = go.Figure()
    for sentiment in monthly_df.columns:
        fig.add_trace(
            go.Scatter(
                x=monthly_df.index,
                y=monthly_df[sentiment],
                mode="lines+markers",
                name=sentiment,
                line=dict(color=SENTIMENT_COLOURS.get(sentiment)),
            )
        )
    fig.update_layout(
        title="Sentiment Trends Over Time",
        xaxis_title="Date",
        yaxis_title="Number of Reviews",
        legend_title="Sentiment",
        template="plotly_white",
        xaxis=dict(showgrid=True, gridcolor="lightgray"),
        yaxis=dict(showgrid=True, gridcolor="lightgray"),
    )
    return fig
