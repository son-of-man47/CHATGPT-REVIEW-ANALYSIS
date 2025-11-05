# 🧠 ChatGPT App Reviews Analysis

> Turning real user feedback into actionable insights with Python, NLP, and interactive data visualization.

---

## 📘 Project Overview
This project analyzes user reviews of the **ChatGPT mobile app** to uncover sentiment trends, identify major review themes, and provide data-driven insights on user experience. Using a combination of text preprocessing, topic modeling, and sentiment scoring, the analysis transforms raw app feedback into meaningful patterns and visual stories.

---

## 🚀 Key Steps
1. **Data Loading & Cleaning**  
   - Imported CSV of ChatGPT app reviews  
   - Filled missing values (“No Review”) for consistent processing  
   - Removed punctuation, stopwords, and redundant spaces  

2. **Exploratory Analysis**  
   - Visualized review distribution by sentiment  
   - Identified frequently used words using token frequency counts  

3. **Topic Modeling (LDA)**  
   - Used `CountVectorizer` to extract common review themes  
    

4. **Sentiment Analysis**  
   - Classified reviews into **Positive**, **Neutral**, and **Negative** sentiments  
   

5. **Visualization**  
   - Built interactive visualizations with **Plotly** for clarity and engagement  
   - Created bar charts and line plots

---

## 🧰 Tools & Libraries
- **Python** — Core analysis and scripting  
- **Pandas** — Data manipulation  
- **Scikit-learn** — LDA topic modeling  
- **Plotly Express & Graph Objects** — Interactive visualizations  
- **NLTK / Text Processing** — Tokenization, cleaning, and stopword removal  

---

## 📊 Key Findings
- Majority of users expressed **positive sentiment**, appreciating ChatGPT’s **accuracy, usability, and creativity**.  
- **Negative reviews** often mentioned **bad app** and **wrong or inaccurate responses**.  
- Common problem encountered was with the responses 

---

## 📈 Example Visuals
- **Sentiment Distribution** — Bar chart comparing positive, neutral, and negative feedback.  
- **Sentiment Distribution Over Time** - Line graph showing positive, neutral, and negative feedback over time
- **Common Positive and Negative Phrases** - Bar charts showing common phrases associated with positive and negative reviews
- **Common Problems Encountered Whilst Using the App** - Bar chart showing different categories of problems or issues associated with the app

> All figures are generated using Plotly and displayed interactively within the notebook.
