# 🛒 Jumia AI Review Summarizer

A Python-based AI tool that scrapes customer reviews from **Jumia Kenya** and uses **Google Gemini 1.5 Flash** to provide a "Buy/Skip" verdict.

## 🚀 How it Works

1. **Scrape:** Uses Selenium to bypass Jumia's frontend and extract raw reviews.
2. **Analyze:** Feeds reviews into Gemini AI to filter out "fake" feedback and summarize pros/cons.
3. **Verdict:** Delivers a clear recommendation based on real customer sentiment.

## 🛠️ Tech Stack

- Python 3.12+
- Selenium & Webdriver-Manager
- Google Generative AI (Gemini API)
- Python-Dotenv (Security)

## 📦 Setup

1. Clone the repo.
2. `pip install -r requirements.txt`
3. Add your `GEMINI_API_KEY` to a `.env` file.
4. Run `python main.py`.
