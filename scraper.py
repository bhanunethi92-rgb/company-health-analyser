import requests
import sqlite3
import pandas as pd
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

COMPANY_NAME = "Infosys"
NEWS_API_KEY = os.getenv("NEWS_API_KEY")
DB_PATH = "data/company_health.db"

def fetch_news():
    url = f"https://newsapi.org/v2/everything?q={COMPANY_NAME}&language=en&pageSize=30&apiKey={NEWS_API_KEY}"
    response = requests.get(url)
    data = response.json()
    
    articles = []
    for article in data.get("articles", []):
        articles.append({
            "company": COMPANY_NAME,
            "date": article.get("publishedAt", "")[:10],
            "headline": article.get("title", ""),
            "description": article.get("description", ""),
            "source": article.get("source", {}).get("name", ""),
            "url": article.get("url", ""),
            "sentiment_score": 0,
            "scraped_at": datetime.now().isoformat()
        })
    
    df = pd.DataFrame(articles)
    df.to_csv("data/news.csv", index=False)
    print(f"✓ Saved {len(df)} news articles")

fetch_news()