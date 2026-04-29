# CHATGPT-REVIEW-ANALYSIS

# 📊 ChatGPT Reviews Analysis

> **NLP-powered sentiment analysis, topic modelling, and trend visualisation of real-world ChatGPT app-store reviews.**

[![Python 3.10+](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/yourusername/chatgpt-reviews-analysis/blob/main/notebooks/chatgpt_reviews_analysis.ipynb)

---

## 🔍 Overview

Millions of users share their experiences with ChatGPT on app stores every day. This project turns that raw, unstructured feedback into actionable intelligence — automatically classifying sentiment, surfacing the most common praise and complaints, categorising product problems, and tracking how public perception has evolved over time.

Whether you're a product manager, researcher, or ML engineer, this pipeline gives you a reproducible, production-ready framework for understanding how users feel about any conversational AI product — not just ChatGPT.

---

## ✨ Features

| Feature | Description |
|---|---|
| 🧹 **Data Cleaning Pipeline** | Handles nulls, date parsing, and text normalisation automatically |
| 😊 **Sentiment Analysis** | TextBlob polarity scoring labels every review as Positive / Neutral / Negative |
| 🔤 **Phrase Extraction** | n-gram analysis (bi/tri-grams) surfaces what users actually say in their own words |
| 🗂️ **Problem Categorisation** | Negative phrases are bucketed into 4 product problem categories via keyword matching |
| 📈 **Trend Analysis** | Monthly aggregation shows how sentiment has shifted over the product lifecycle |
| 📊 **Interactive Charts** | All visualisations built with Plotly — hover, zoom, and export ready |
| 🧪 **Full Test Suite** | pytest unit tests for every module with fixture-based isolation |
| 🖥️ **CLI Entry Point** | Run the full pipeline with a single command; optionally save charts as HTML |

---

## 📁 Project Structure

```
chatgpt-reviews-analysis/
│
├── src/                          # Core application logic
│   ├── data_loader/
│   │   └── loader.py             # CSV loading & schema validation
│   ├── preprocessing/
│   │   └── cleaner.py            # Null filling, date parsing, whitespace stripping
│   ├── analysis/
│   │   ├── sentiment.py          # TextBlob sentiment labelling & time aggregation
│   │   └── topic_modeling.py     # n-gram extraction & problem categorisation
│   └── visualization/
│       └── charts.py             # Plotly chart builders (all return go.Figure)
│
├── data/
│   ├── sample/
│   │   └── chatgpt_reviews_sample.csv   
│
├── notebooks/
│   └── chatgpt_reviews_analysis.ipynb   
│
│
├── main.py                       # CLI pipeline entry point
├── requirements.txt              # Pinned runtime dependencies
├── .gitignore
└── README.md
```

---

## 📦 Dataset Description

The dataset is a collection of user-submitted reviews for the ChatGPT mobile application, sourced from app-store platforms.

| Column | Type | Description |
|---|---|---|
| `Review` | `string` | Raw review text written by the user |
| `Review Date` | `datetime` | Date the review was submitted |
| `Rating` | `int` | Star rating 1–5 (optional column) |

**Source:** [Kaggle – ChatGPT Reviews Dataset](https://www.kaggle.com/datasets/)
**Size:** ~10,000+ reviews spanning late 2022 to mid-2024

> Place your `chatgpt_reviews.csv` in the `data/` directory before running. See `data/README.md` for details.

---

## 🛠️ Installation

**Prerequisites:** Python 3.10 or higher

```bash
# 1. Clone the repository
git clone https://github.com/yourusername/chatgpt-reviews-analysis.git
cd chatgpt-reviews-analysis

# 2. Create and activate a virtual environment (recommended)
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Download TextBlob corpora (one-time setup)
python -m textblob.download_corpora
```

---

## 🚀 Usage

### Option 1 — Command Line (recommended)

```bash
# Run with interactive Plotly charts
python main.py --data data/chatgpt_reviews.csv

# Run with charts saved as HTML files in outputs/
python main.py --data data/chatgpt_reviews.csv --save-html

# Quick test with the included sample data
python main.py --data data/sample/chatgpt_reviews_sample.csv
```

### Option 2 — Jupyter Notebook

```bash
jupyter notebook notebooks/chatgpt_reviews_analysis.ipynb
```

Or open directly in Google Colab using the badge at the top of this README.

### Option 3 — Import as a Library

```python
from src.data_loader.loader import load_reviews
from src.preprocessing.cleaner import clean_reviews
from src.analysis.sentiment import add_sentiment
from src.visualization.charts import plot_sentiment_distribution

df = load_reviews("data/chatgpt_reviews.csv")
df = clean_reviews(df)
df = add_sentiment(df)

fig = plot_sentiment_distribution(df["Sentiment"].value_counts())
fig.show()
```

---



## 📊 Example Outputs

### 1. Sentiment Distribution
*A bar chart showing the proportion of Positive (green), Neutral (grey), and Negative (red) reviews.*
> **Finding:** The majority of reviews are positive, indicating strong overall user satisfaction.

### 2. Common Phrases in Positive Reviews
*Horizontal bar chart of the top 20 bi/tri-grams from positive reviews.*
> **Finding:** Users frequently describe ChatGPT as a "great app", "good ai", "amazing app", and "user friendly" — highlighting perceived quality and ease of use.

### 3. Common Phrases in Negative Reviews
*Horizontal bar chart of top negative phrases.*
> **Finding:** Negative reviews cluster around "wrong answer", "network error", and "app crash" — pointing to reliability and accuracy concerns.

### 4. Problem Category Breakdown
*Bar chart mapping negative phrases to four product problem areas.*
> **Finding:** "Response and Answer Quality" is the most cited problem category, followed by "App Performance".

### 5. Sentiment Over Time
*Multi-line trend chart aggregated by month.*
> **Finding:** Positive reviews trended sharply upward from Feb 2024, with all sentiment categories peaking before a partial dip in May 2024 — correlating with major product updates.

---

## 🧠 Key Insights & Business Analysis

### What Users Love
- ChatGPT is widely praised for its **accessibility and student utility** ("good app for students", "user friendly")
- Users value the **quality and breadth of responses** across tasks
- The app earns consistent praise as a reliable AI assistant

### What Frustrates Users
- **Response accuracy** is the #1 concern — users are sensitive to incorrect or irrelevant answers
- **App stability** (crashes, freezes, bugs) drives significant negative sentiment
- **Network-dependent performance** is a recurring frustration, particularly in regions with unreliable connectivity

### Trend Signal
- The sharp upward trajectory in positive reviews from February 2024 onwards suggests that a product release or capability update meaningfully shifted user perception
- The partial dip in May 2024 warrants investigation — may correlate with a service outage or controversial update

### Business Recommendation
> Prioritise accuracy and reliability improvements over new feature launches. User trust is built on consistency — the data shows users are highly sensitive to wrong answers and crashes. Improving the offline/low-connectivity experience would also address a recurring complaint theme.

---

## 🧩 Technologies Used

| Library | Version | Purpose |
|---|---|---|
| `pandas` | ≥ 2.0 | Data loading, cleaning, aggregation |
| `textblob` | ≥ 0.18 | Lexicon-based sentiment analysis |
| `scikit-learn` | ≥ 1.4 | CountVectorizer for n-gram extraction |
| `plotly` | ≥ 5.20 | Interactive visualisations |
| `pytest` | ≥ 8.0 | Unit testing framework |

---

## 🔮 Future Improvements

- [ ] **Upgrade to transformer-based sentiment** (e.g. `cardiffnlp/twitter-roberta-base-sentiment`) for higher accuracy
- [ ] **LDA topic modelling** using `sklearn.decomposition.LatentDirichletAllocation` to auto-discover themes
- [ ] **Rating-weighted sentiment** — incorporate star-rating as a ground truth label for model validation
- [ ] **Word cloud visualisation** for a quick qualitative snapshot of each sentiment group
- [ ] **Streamlit dashboard** for non-technical stakeholders to explore results interactively
- [ ] **CI/CD pipeline** with GitHub Actions running `pytest` on every push

---

## 👤 Author

**David Iroanya**
