"""
Company Health Analyser — Data Collection
Scrapes AmbitionBox reviews, LinkedIn job postings, and NewsAPI headlines
for any company. Demo: Infosys

Author: Your Name
"""

import requests
from bs4 import BeautifulSoup
import sqlite3
import pandas as pd
from datetime import datetime, timedelta
import time
import random
import re
import json
import os
from dotenv import load_dotenv

load_dotenv()

# ─────────────────────────────────────────────
# CONFIG — change company name here to analyse any company
# ─────────────────────────────────────────────
COMPANY_NAME = "Infosys"
AMBITIONBOX_SLUG = "infosys"       # as it appears in ambitionbox URL
LINKEDIN_KEYWORD = "Infosys"       # keyword for LinkedIn job search
NEWS_API_KEY = os.getenv("NEWS_API_KEY")  # get free key at newsapi.org
DB_PATH = "data/company_health.db"

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    )
}


# ─────────────────────────────────────────────
# DATABASE SETUP
# ─────────────────────────────────────────────
def init_db():
    """Create all 3 tables if they don't exist."""
    os.makedirs("data", exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.executescript("""
        CREATE TABLE IF NOT EXISTS reviews (
            id              INTEGER PRIMARY KEY AUTOINCREMENT,
            company         TEXT,
            date            TEXT,
            rating          REAL,
            department      TEXT,
            employment_type TEXT,
            pros            TEXT,
            cons            TEXT,
            work_life       REAL,
            skill_dev       REAL,
            salary          REAL,
            job_security    REAL,
            management      REAL,
            source          TEXT DEFAULT 'AmbitionBox',
            scraped_at      TEXT
        );

        CREATE TABLE IF NOT EXISTS job_postings (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            company     TEXT,
            date        TEXT,
            role        TEXT,
            seniority   TEXT,
            location    TEXT,
            department  TEXT,
            source      TEXT DEFAULT 'LinkedIn',
            scraped_at  TEXT
        );

        CREATE TABLE IF NOT EXISTS news (
            id              INTEGER PRIMARY KEY AUTOINCREMENT,
            company         TEXT,
            date            TEXT,
            headline        TEXT,
            description     TEXT,
            source          TEXT,
            url             TEXT,
            sentiment_score REAL,
            scraped_at      TEXT
        );
    """)

    conn.commit()
    conn.close()
    print("✓ Database initialised at", DB_PATH)


# ─────────────────────────────────────────────
# SCRAPER 1 — AMBITIONBOX REVIEWS
# ─────────────────────────────────────────────
def scrape_ambitionbox(company_slug: str, pages: int = 5) -> list[dict]:
    """
    Scrape employee reviews from AmbitionBox.
    Returns list of review dicts.
    """
    reviews = []
    base_url = f"https://www.ambitionbox.com/reviews/{company_slug}-reviews"

    print(f"\n── Scraping AmbitionBox: {company_slug} ({pages} pages)")

    for page in range(1, pages + 1):
        url = f"{base_url}?page={page}" if page > 1 else base_url

        try:
            response = requests.get(url, headers=HEADERS, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, "html.parser")

            # Each review card
            review_cards = soup.find_all("div", class_=re.compile(r"review-card|reviewCard"))

            if not review_cards:
                # Fallback: try alternate selectors
                review_cards = soup.select("div[data-testid='review-card']")

            for card in review_cards:
                review = parse_ambitionbox_card(card, company_slug)
                if review:
                    reviews.append(review)

            print(f"  Page {page}: {len(review_cards)} reviews found")
            time.sleep(random.uniform(2, 4))  # polite delay

        except requests.RequestException as e:
            print(f"  ✗ Page {page} failed: {e}")
            continue

    print(f"✓ AmbitionBox: {len(reviews)} reviews collected")
    return reviews


def parse_ambitionbox_card(card, company_slug: str) -> dict | None:
    """Parse a single AmbitionBox review card into a dict."""
    try:
        # Rating
        rating_el = card.find(class_=re.compile(r"rating|ratingBadge"))
        rating = float(rating_el.get_text(strip=True)) if rating_el else None

        # Department
        dept_el = card.find(class_=re.compile(r"designation|jobTitle|department"))
        department = dept_el.get_text(strip=True) if dept_el else "Unknown"

        # Employment type (current/former)
        emp_el = card.find(class_=re.compile(r"employment|empType"))
        employment_type = emp_el.get_text(strip=True) if emp_el else "Unknown"

        # Pros and cons
        pros_el = card.find(class_=re.compile(r"pros|good"))
        cons_el = card.find(class_=re.compile(r"cons|bad"))
        pros = pros_el.get_text(strip=True) if pros_el else ""
        cons = cons_el.get_text(strip=True) if cons_el else ""

        # Date
        date_el = card.find(class_=re.compile(r"date|time|posted"))
        date_str = date_el.get_text(strip=True) if date_el else str(datetime.now().date())

        # Sub-ratings (work-life, salary etc.)
        sub_ratings = card.find_all(class_=re.compile(r"subRating|categoryRating"))
        sub_vals = [float(r.get_text(strip=True)) for r in sub_ratings if r.get_text(strip=True).replace('.','').isdigit()]

        return {
            "company": company_slug,
            "date": date_str,
            "rating": rating,
            "department": clean_text(department),
            "employment_type": clean_text(employment_type),
            "pros": clean_text(pros),
            "cons": clean_text(cons),
            "work_life": sub_vals[0] if len(sub_vals) > 0 else None,
            "skill_dev": sub_vals[1] if len(sub_vals) > 1 else None,
            "salary": sub_vals[2] if len(sub_vals) > 2 else None,
            "job_security": sub_vals[3] if len(sub_vals) > 3 else None,
            "management": sub_vals[4] if len(sub_vals) > 4 else None,
            "scraped_at": datetime.now().isoformat()
        }
    except Exception:
        return None


# ─────────────────────────────────────────────
# SCRAPER 2 — LINKEDIN JOB POSTINGS
# ─────────────────────────────────────────────
def scrape_linkedin_jobs(company_name: str, pages: int = 3) -> list[dict]:
    """
    Scrape public LinkedIn job postings (no login needed for public listings).
    Returns list of job dicts.
    """
    jobs = []
    print(f"\n── Scraping LinkedIn jobs: {company_name} ({pages} pages)")

    for page in range(pages):
        start = page * 25
        url = (
            f"https://www.linkedin.com/jobs/search/"
            f"?keywords={company_name.replace(' ', '%20')}"
            f"&start={start}"
        )

        try:
            response = requests.get(url, headers=HEADERS, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, "html.parser")

            job_cards = soup.find_all("div", class_=re.compile(r"job-search-card|base-card"))

            for card in job_cards:
                job = parse_linkedin_card(card, company_name)
                if job:
                    jobs.append(job)

            print(f"  Page {page+1}: {len(job_cards)} jobs found")
            time.sleep(random.uniform(3, 5))

        except requests.RequestException as e:
            print(f"  ✗ Page {page+1} failed: {e}")
            continue

    print(f"✓ LinkedIn: {len(jobs)} job postings collected")
    return jobs


def parse_linkedin_card(card, company_name: str) -> dict | None:
    """Parse a single LinkedIn job card."""
    try:
        title_el = card.find(class_=re.compile(r"job-search-card__title|base-search-card__title"))
        role = title_el.get_text(strip=True) if title_el else "Unknown"

        location_el = card.find(class_=re.compile(r"job-search-card__location|base-search-card__metadata"))
        location = location_el.get_text(strip=True) if location_el else "Unknown"

        date_el = card.find("time")
        date_str = date_el.get("datetime", str(datetime.now().date())) if date_el else str(datetime.now().date())

        # Infer seniority from title
        seniority = infer_seniority(role)

        # Infer department from title
        department = infer_department(role)

        return {
            "company": company_name,
            "date": date_str,
            "role": clean_text(role),
            "seniority": seniority,
            "location": clean_text(location),
            "department": department,
            "scraped_at": datetime.now().isoformat()
        }
    except Exception:
        return None


def infer_seniority(role: str) -> str:
    """Infer seniority level from job title."""
    role_lower = role.lower()
    if any(w in role_lower for w in ["senior", "sr.", "lead", "principal"]):
        return "Senior"
    elif any(w in role_lower for w in ["manager", "head", "director", "vp", "chief"]):
        return "Management"
    elif any(w in role_lower for w in ["junior", "jr.", "associate", "trainee", "intern", "fresher"]):
        return "Junior"
    else:
        return "Mid-level"


def infer_department(role: str) -> str:
    """Infer department from job title."""
    role_lower = role.lower()
    if any(w in role_lower for w in ["data", "analyst", "analytics", "bi", "sql", "tableau"]):
        return "Data & Analytics"
    elif any(w in role_lower for w in ["software", "developer", "engineer", "sde", "backend", "frontend"]):
        return "Engineering"
    elif any(w in role_lower for w in ["hr", "human resource", "talent", "recruit"]):
        return "HR"
    elif any(w in role_lower for w in ["sales", "business development", "account"]):
        return "Sales"
    elif any(w in role_lower for w in ["finance", "accounting", "audit"]):
        return "Finance"
    elif any(w in role_lower for w in ["marketing", "content", "brand", "seo"]):
        return "Marketing"
    elif any(w in role_lower for w in ["product", "scrum", "agile"]):
        return "Product"
    else:
        return "Other"


# ─────────────────────────────────────────────
# SCRAPER 3 — NEWSAPI HEADLINES
# ─────────────────────────────────────────────
def fetch_news(company_name: str, days_back: int = 180) -> list[dict]:
    """
    Fetch last N days of news headlines via NewsAPI (free tier).
    Sign up at newsapi.org — 100 requests/day free.
    """
    print(f"\n── Fetching NewsAPI: {company_name} (last {days_back} days)")

    if not NEWS_API_KEY:
        print("  ✗ NEWS_API_KEY not set in .env — skipping news")
        return []

    from_date = (datetime.now() - timedelta(days=days_back)).strftime("%Y-%m-%d")
    url = "https://newsapi.org/v2/everything"
    params = {
        "q": f'"{company_name}"',
        "from": from_date,
        "sortBy": "publishedAt",
        "language": "en",
        "pageSize": 100,
        "apiKey": NEWS_API_KEY
    }

    articles = []
    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()

        for article in data.get("articles", []):
            articles.append({
                "company": company_name,
                "date": article.get("publishedAt", "")[:10],
                "headline": clean_text(article.get("title", "")),
                "description": clean_text(article.get("description", "")),
                "source": article.get("source", {}).get("name", ""),
                "url": article.get("url", ""),
                "sentiment_score": None,   # filled in Week 2 NLP step
                "scraped_at": datetime.now().isoformat()
            })

        print(f"✓ NewsAPI: {len(articles)} articles collected")

    except requests.RequestException as e:
        print(f"  ✗ NewsAPI failed: {e}")

    return articles


# ─────────────────────────────────────────────
# DATABASE — SAVE ALL DATA
# ─────────────────────────────────────────────
def save_to_db(reviews: list, jobs: list, news: list):
    """Save all scraped data into SQLite."""
    conn = sqlite3.connect(DB_PATH)

    if reviews:
        pd.DataFrame(reviews).to_sql("reviews", conn, if_exists="append", index=False)
        print(f"✓ Saved {len(reviews)} reviews to DB")

    if jobs:
        pd.DataFrame(jobs).to_sql("job_postings", conn, if_exists="append", index=False)
        print(f"✓ Saved {len(jobs)} job postings to DB")

    if news:
        pd.DataFrame(news).to_sql("news", conn, if_exists="append", index=False)
        print(f"✓ Saved {len(news)} news articles to DB")

    conn.close()


def export_csvs():
    """Export all tables to CSV for Power BI import."""
    os.makedirs("data", exist_ok=True)
    conn = sqlite3.connect(DB_PATH)

    for table in ["reviews", "job_postings", "news"]:
        try:
            df = pd.read_sql(f"SELECT * FROM {table}", conn)
            path = f"data/{table}.csv"
            df.to_csv(path, index=False)
            print(f"✓ Exported {len(df)} rows → {path}")
        except Exception as e:
            print(f"  ✗ Could not export {table}: {e}")

    conn.close()


# ─────────────────────────────────────────────
# UTILS
# ─────────────────────────────────────────────
def clean_text(text: str) -> str:
    """Remove extra whitespace and newlines."""
    if not text:
        return ""
    return re.sub(r'\s+', ' ', text).strip()


def print_summary():
    """Print row counts from all 3 tables."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    print("\n── Database summary")
    for table in ["reviews", "job_postings", "news"]:
        try:
            count = cursor.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]
            print(f"  {table:<20} {count} rows")
        except Exception:
            print(f"  {table:<20} table empty or missing")
    conn.close()


# ─────────────────────────────────────────────
# MAIN — RUN ALL 3 SCRAPERS
# ─────────────────────────────────────────────
if __name__ == "__main__":
    print("=" * 50)
    print(f"  Company Health Analyser — {COMPANY_NAME}")
    print(f"  Started: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print("=" * 50)

    # 1. Init database
    init_db()

    # 2. Scrape all 3 sources
    reviews = scrape_ambitionbox(AMBITIONBOX_SLUG, pages=5)
    jobs    = scrape_linkedin_jobs(LINKEDIN_KEYWORD, pages=3)
    news    = fetch_news(COMPANY_NAME, days_back=180)

    # 3. Save to SQLite
    save_to_db(reviews, jobs, news)

    # 4. Export CSVs (for Power BI)
    export_csvs()

    # 5. Summary
    print_summary()
    print("\n✓ Week 1 complete — data ready for SQL analysis in Week 2")