import requests
import sqlite3
import pandas as pd
from datetime import datetime
import os
from dotenv import load_dotenv
from textblob import TextBlob

load_dotenv()

COMPANY_NAME = "Infosys"
NEWS_API_KEY = os.getenv("NEWS_API_KEY")

def fetch_news():
    url = f"https://newsapi.org/v2/everything?q={COMPANY_NAME}&language=en&pageSize=30&apiKey={NEWS_API_KEY}"
    response = requests.get(url)
    data = response.json()
    
    articles = []
    for article in data.get("articles", []):
        headline = article.get("title", "")
        description = article.get("description", "")
        
        # sentiment scoring
        text = headline + " " + str(description)
        score = TextBlob(text).sentiment.polarity
        if score > 0.1:
            sentiment = "Positive"
        elif score < -0.1:
            sentiment = "Negative"
        else:
            sentiment = "Neutral"
        
        articles.append({
            "company": COMPANY_NAME,
            "date": article.get("publishedAt", "")[:10],
            "headline": headline,
            "description": description,
            "source": article.get("source", {}).get("name", ""),
            "url": article.get("url", ""),
            "sentiment": sentiment,
            "sentiment_score": score,
            "scraped_at": datetime.now().isoformat()
        })
    
    df = pd.DataFrame(articles)
    df.to_csv("data/news.csv", index=False)
    print(f"✓ Saved {len(df)} news articles")
    print(df["sentiment"].value_counts())

fetch_news()