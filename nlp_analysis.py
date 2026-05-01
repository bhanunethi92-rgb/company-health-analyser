import sqlite3
import csv
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

analyzer = SentimentIntensityAnalyzer()

conn = sqlite3.connect("data/company_health.db")
cursor = conn.cursor()

# Get all job postings
cursor.execute("SELECT role, department, seniority FROM job_postings;")
jobs = cursor.fetchall()

results = []

for job in jobs:
    role, department, seniority = job
    text = f"{role} {department} {seniority}"
    score = analyzer.polarity_scores(text)
    sentiment = "Positive" if score['compound'] > 0.05 else "Negative" if score['compound'] < -0.05 else "Neutral"
    results.append([role, department, seniority, score['compound'], sentiment])

# Save to CSV
with open("data/nlp_sentiment.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["role", "department", "seniority", "compound_score", "sentiment"])
    writer.writerows(results)

print(f"Analysed {len(results)} jobs!")
print("Saved: data/nlp_sentiment.csv")
# Quick summary
positive = sum(1 for r in results if r[4] == "Positive")
negative = sum(1 for r in results if r[4] == "Negative")
neutral = sum(1 for r in results if r[4] == "Neutral")

print(f"\nSentiment Summary:")
print(f"Positive: {positive}")
print(f"Negative: {negative}")
print(f"Neutral:  {neutral}")

conn.close()