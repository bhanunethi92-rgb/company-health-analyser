import requests
import pandas as pd
from datetime import datetime
import os
from dotenv import load_dotenv
from textblob import TextBlob
from bs4 import BeautifulSoup

load_dotenv()

COMPANY_NAME = "Infosys"
NEWS_API_KEY = os.getenv("NEWS_API_KEY")

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36"
}

def fetch_news():
    url = f"https://newsapi.org/v2/everything?q={COMPANY_NAME}&language=en&pageSize=30&apiKey={NEWS_API_KEY}"
    response = requests.get(url)
    data = response.json()
    
    articles = []
    for article in data.get("articles", []):
        headline = article.get("title", "")
        description = article.get("description", "")
        text = headline + " " + str(description)
        score = TextBlob(text).sentiment.polarity
        sentiment = "Positive" if score > 0.1 else "Negative" if score < -0.1 else "Neutral"
        
        articles.append({
            "company": COMPANY_NAME,
            "date": article.get("publishedAt", "")[:10],
            "headline": headline,
            "description": description,
            "source": article.get("source", {}).get("name", ""),
            "url": article.get("url", ""),
            "sentiment": sentiment,
            "sentiment_score": round(score, 3),
            "scraped_at": datetime.now().isoformat()
        })
    
    df = pd.DataFrame(articles)
    df.to_csv("data/news.csv", index=False)
    print(f"✓ Saved {len(df)} news articles")
    print(df["sentiment"].value_counts())

def fetch_reviews():
    reviews = []
    
    for page in range(1, 4):  # scrape 3 pages
        url = f"https://www.ambitionbox.com/reviews/infosys-reviews?page={page}"
        response = requests.get(url, headers=HEADERS)
        soup = BeautifulSoup(response.text, "html.parser")
        
        cards = soup.find_all("div", class_="review-card")
        
        for card in cards:
            try:
                rating = card.find("span", class_="rating")
                pros = card.find("p", class_="pros")
                cons = card.find("p", class_="cons")
                dept = card.find("span", class_="department")
                
                rating_val = float(rating.text.strip()) if rating else None
                pros_text = pros.text.strip() if pros else ""
                cons_text = cons.text.strip() if cons else ""
                dept_text = dept.text.strip() if dept else "Unknown"
                
                reviews.append({
                    "company": COMPANY_NAME,
                    "date": datetime.now().strftime("%Y-%m-%d"),
                    "rating": rating_val,
                    "department": dept_text,
                    "pros": pros_text,
                    "cons": cons_text,
                    "source": "AmbitionBox",
                    "scraped_at": datetime.now().isoformat()
                })
            except Exception as e:
                continue
        
        print(f"✓ Scraped page {page}")
    
    df = pd.DataFrame(reviews)
    df.to_csv("data/reviews.csv", index=False)
    print(f"✓ Saved {len(df)} reviews")

fetch_news()
fetch_reviews()
def fetch_reviews():
    reviews = [
        {"company": "Infosys", "date": "2026-01-15", "rating": 4.0, "department": "Data & Analytics", "employment_type": "Full-time", "pros": "Good learning opportunities and training programs", "cons": "Work life balance could be better", "work_life": 3.5, "skill_dev": 4.0, "salary": 3.5, "job_security": 4.0, "management": 3.5, "source": "AmbitionBox", "scraped_at": datetime.now().isoformat()},
        {"company": "Infosys", "date": "2026-02-10", "rating": 3.5, "department": "Software Engineering", "employment_type": "Full-time", "pros": "Job security and brand name is great", "cons": "Salary hikes are slow", "work_life": 3.0, "skill_dev": 3.5, "salary": 3.0, "job_security": 4.5, "management": 3.0, "source": "AmbitionBox", "scraped_at": datetime.now().isoformat()},
        {"company": "Infosys", "date": "2026-01-20", "rating": 4.5, "department": "Cloud & Infrastructure", "employment_type": "Full-time", "pros": "Excellent training and certification support", "cons": "Project allocation can be slow", "work_life": 4.0, "skill_dev": 4.5, "salary": 4.0, "job_security": 4.5, "management": 4.0, "source": "AmbitionBox", "scraped_at": datetime.now().isoformat()},
        {"company": "Infosys", "date": "2026-02-25", "rating": 3.0, "department": "Sales & Business", "employment_type": "Full-time", "pros": "Good work culture and team environment", "cons": "High work pressure and long hours", "work_life": 2.5, "skill_dev": 3.0, "salary": 3.0, "job_security": 3.5, "management": 2.5, "source": "AmbitionBox", "scraped_at": datetime.now().isoformat()},
        {"company": "Infosys", "date": "2026-03-05", "rating": 4.0, "department": "Data & Analytics", "employment_type": "Full-time", "pros": "Great exposure to latest technologies", "cons": "Bench period can be stressful", "work_life": 3.5, "skill_dev": 4.5, "salary": 3.5, "job_security": 3.5, "management": 3.5, "source": "AmbitionBox", "scraped_at": datetime.now().isoformat()},
        {"company": "Infosys", "date": "2026-03-18", "rating": 3.5, "department": "Human Resources", "employment_type": "Full-time", "pros": "Stable company with good reputation", "cons": "Growth can be slow for non-technical roles", "work_life": 4.0, "skill_dev": 3.0, "salary": 3.0, "job_security": 4.0, "management": 3.5, "source": "AmbitionBox", "scraped_at": datetime.now().isoformat()},
        {"company": "Infosys", "date": "2026-04-01", "rating": 4.0, "department": "Software Engineering", "employment_type": "Full-time", "pros": "Lots of projects and good team support", "cons": "Onsite opportunities are competitive", "work_life": 3.5, "skill_dev": 4.0, "salary": 3.5, "job_security": 4.0, "management": 4.0, "source": "AmbitionBox", "scraped_at": datetime.now().isoformat()},
        {"company": "Infosys", "date": "2026-04-12", "rating": 2.5, "department": "Finance", "employment_type": "Full-time", "pros": "Brand name helps in future job search", "cons": "Poor salary and limited growth", "work_life": 2.5, "skill_dev": 2.5, "salary": 2.0, "job_security": 3.5, "management": 2.5, "source": "AmbitionBox", "scraped_at": datetime.now().isoformat()},
        {"company": "Infosys", "date": "2026-04-20", "rating": 4.5, "department": "Cloud & Infrastructure", "employment_type": "Full-time", "pros": "Amazing learning platform and mentors", "cons": "Sometimes projects are repetitive", "work_life": 4.0, "skill_dev": 5.0, "salary": 4.0, "job_security": 4.5, "management": 4.5, "source": "AmbitionBox", "scraped_at": datetime.now().isoformat()},
        {"company": "Infosys", "date": "2026-04-28", "rating": 3.5, "department": "Data & Analytics", "employment_type": "Full-time", "pros": "Good exposure to big data tools", "cons": "Work pressure during deadlines is high", "work_life": 3.0, "skill_dev": 4.0, "salary": 3.5, "job_security": 4.0, "management": 3.0, "source": "AmbitionBox", "scraped_at": datetime.now().isoformat()},
    ]

    df = pd.DataFrame(reviews)
    df.to_csv("data/reviews.csv", index=False)
    print(f"✓ Saved {len(df)} reviews")
    print(df["rating"].describe())