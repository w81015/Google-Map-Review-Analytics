[中文版 Chinese version](README_zh.md)

# Google Maps Restaurant Review Analysis System

📈 A web application built with Streamlit to help users analyze restaurant reviews on Google Maps through sentiment and topic classification.

---

## 🔧 Features

This system offers the following analysis modules:

- **Home**: Overview and instructions
- **Review Input**: Upload restaurant review data for processing
- **Review Summary**: Displays general trends and statistics
- **Rating Analysis**: Visualize star ratings distribution
- **Keyword Analysis**: Extract popular keywords and related reviews
- **Topic Analysis**: Discover discussion topics through topic modeling

---

## 🖥️ Technical Architecture

### 📦 Frontend

- **Streamlit**: For building interactive web UI
- **streamlit-option-menu**: Provides elegant navigation menu

### 🧪 Backend

- **Data Collection** (`utils/get_reviews.py`):
  - Uses Selenium to scrape restaurant reviews from Google Maps
  - Automatically searches, scrolls, and loads all available reviews
  - Extracts review text and ratings, stores results in a pandas DataFrame

- **Data Processing & Analysis** (`utils/process_reviews.py`):
  - Uses `jieba` and TextRank for keyword extraction
  - Performs sentiment analysis via `SnowNLP`
  - Classifies sentences based on predefined keywords (e.g. Food, Service, Environment)
  - Splits reviews into sentences for detailed analysis

---

## 🗂️ Project Structure

```
📁 your_project/
│
├── app.py                     # Main Streamlit app and navigation
├── page/                      # Page modules
│   ├── input_page.py
│   ├── summary_page.py
│   ├── rating_analysis.py
│   ├── keyword_analysis.py
│   └── topic_analysis.py
│
├── utils/                     # Functional modules
│   ├── get_reviews.py         # Scraping logic for Google reviews
│   └── process_reviews.py     # NLP processing and analysis
│
├── userdict.txt               # Custom dictionary for jieba
├── stopwords.txt              # Stopword list
```

---

## ▶️ Usage

### Install dependencies

```bash
pip install -r requirements.txt
```

Or manually:

```bash
pip install streamlit streamlit-option-menu selenium webdriver-manager snownlp jieba pandas
```

### Run the app

```bash
streamlit run app.py
```

---

## 📌 Notes

- Chrome and a compatible ChromeDriver are required to run the scraper (`webdriver-manager` automates installation).
- Classification rules are defined in `process_reviews.py` and can be customized.
- Sentiment analysis is based on `SnowNLP`. You may replace it with a more robust model like BERT if needed for Traditional Chinese.

---

## 🙋‍♂️ Developer Info

- Developer: Jared Lin
- GitHub: [https://github.com/w81015](https://github.com/w81015)

---

This system aims to help restaurant owners, data analysts, and researchers quickly understand review trends and hidden insights.
