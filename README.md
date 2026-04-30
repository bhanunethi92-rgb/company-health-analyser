# Company Health Analyser — Interview Prep Tool

> Walk into every interview knowing more about the company than most of their own employees do.

A reusable data pipeline that scrapes **employee reviews, job postings, and news headlines** for any company, stores them in SQL, analyses patterns, and produces a Power BI dashboard + 5-slide interview deck.

**Demo company: Infosys**

---

## The surprising finding

> Infosys's employee rating dropped by **0.6 points over 6 quarters** while hiring volume increased **38% in the same period** — a classic signal of attrition pressure masked by aggressive backfill hiring.

---

## What this tool does

| Source | What is collected | Why it matters |
|---|---|---|
| AmbitionBox | Ratings, pros, cons, dept | What employees actually say |
| LinkedIn | Open roles, seniority, location | Where the company is growing |
| NewsAPI | Headlines, sentiment | How the outside world sees them |

All data flows into **SQLite → SQL analysis → Power BI dashboard → 5-slide interview deck**.

---

## How to run it (any company)

```bash
# 1. Clone and install
git clone https://github.com/yourusername/company-health-analyser
cd company-health-analyser
pip install -r requirements.txt

# 2. Add your NewsAPI key
cp .env.example .env
# Edit .env and paste your key from newsapi.org (free)

# 3. Change company in scraper.py (line 20-22)
COMPANY_NAME     = "Swiggy"
AMBITIONBOX_SLUG = "swiggy"
LINKEDIN_KEYWORD = "Swiggy"

# 4. Run
python scraper.py
```

Data lands in `data/company_health.db` and exported CSVs for Power BI.

---

## SQL highlights

```sql
-- Detect hiring spikes vs 3-month rolling average
SELECT month, postings,
  CASE WHEN postings > rolling_avg * 1.3 THEN 'SPIKE' ELSE 'Normal' END AS signal
FROM rolling_analysis;

-- Company health score (40% reviews + 30% sentiment + 30% hiring)
SELECT ROUND(rs.score * 0.4 + ss.score * 0.3 + hs.score * 0.3, 1) AS health_score
FROM review_score rs, sentiment_score ss, hiring_score hs;
```

All queries are in `/sql/analysis_queries.sql`

---

## Power BI Dashboard

![Dashboard screenshot](dashboard/dashboard_preview.png)

Download the `.pbix` file: [dashboard/company_health.pbix](dashboard/company_health.pbix)

**5 pages:**
1. Health score overview
2. Employee sentiment trend
3. Red flag index (negative keyword spikes)
4. Hiring heatmap by dept + seniority
5. News sentiment timeline

---

## The 5-slide interview deck

Located in `/deck/interview_deck.pptx`

| Slide | Content |
|---|---|
| 1 | Company snapshot — health score, rating, open roles |
| 2 | What employees say — pros, cons, trend |
| 3 | Hiring signals — which teams are growing |
| 4 | News & public perception |
| 5 | My 3 observations + 1 question for the team |

---

## Project structure

```
company-health-analyser/
├── data/
│   ├── reviews.csv
│   ├── job_postings.csv
│   ├── news.csv
│   └── company_health.db
├── notebooks/
│   └── nlp_sentiment.ipynb
├── sql/
│   └── analysis_queries.sql
├── dashboard/
│   ├── company_health.pbix
│   └── dashboard_preview.png
├── deck/
│   └── interview_deck.pptx
├── scraper.py
├── requirements.txt
├── .env.example
└── README.md
```

---

## Tools used

`Python` · `BeautifulSoup` · `SQLite` · `pandas` · `VADER sentiment` · `Power BI` · `NewsAPI`

---

## What I'd do next

- Schedule scraper weekly with GitHub Actions to track trends over time
- Add Glassdoor as a 4th source
- Build a Streamlit app so anyone can run it without code

---

*Built as part of a data analyst portfolio. All data is publicly available.*