import pandas as pd
from datetime import datetime

reviews = [
    {"company": "Infosys", "date": "2026-01-15", "rating": 4.0, "department": "Data & Analytics", "employment_type": "Full-time", "pros": "Good learning opportunities and training programs", "cons": "Work life balance could be better", "work_life": 3.5, "skill_dev": 4.0, "salary": 3.5, "job_security": 4.0, "management": 3.5, "source": "AmbitionBox"},
    {"company": "Infosys", "date": "2026-02-10", "rating": 3.5, "department": "Software Engineering", "employment_type": "Full-time", "pros": "Job security and brand name is great", "cons": "Salary hikes are slow", "work_life": 3.0, "skill_dev": 3.5, "salary": 3.0, "job_security": 4.5, "management": 3.0, "source": "AmbitionBox"},
    {"company": "Infosys", "date": "2026-01-20", "rating": 4.5, "department": "Cloud & Infrastructure", "employment_type": "Full-time", "pros": "Excellent training and certification support", "cons": "Project allocation can be slow", "work_life": 4.0, "skill_dev": 4.5, "salary": 4.0, "job_security": 4.5, "management": 4.0, "source": "AmbitionBox"},
    {"company": "Infosys", "date": "2026-02-25", "rating": 3.0, "department": "Sales & Business", "employment_type": "Full-time", "pros": "Good work culture and team environment", "cons": "High work pressure and long hours", "work_life": 2.5, "skill_dev": 3.0, "salary": 3.0, "job_security": 3.5, "management": 2.5, "source": "AmbitionBox"},
    {"company": "Infosys", "date": "2026-03-05", "rating": 4.0, "department": "Data & Analytics", "employment_type": "Full-time", "pros": "Great exposure to latest technologies", "cons": "Bench period can be stressful", "work_life": 3.5, "skill_dev": 4.5, "salary": 3.5, "job_security": 3.5, "management": 3.5, "source": "AmbitionBox"},
    {"company": "Infosys", "date": "2026-03-18", "rating": 3.5, "department": "Human Resources", "employment_type": "Full-time", "pros": "Stable company with good reputation", "cons": "Growth can be slow for non-technical roles", "work_life": 4.0, "skill_dev": 3.0, "salary": 3.0, "job_security": 4.0, "management": 3.5, "source": "AmbitionBox"},
    {"company": "Infosys", "date": "2026-04-01", "rating": 4.0, "department": "Software Engineering", "employment_type": "Full-time", "pros": "Lots of projects and good team support", "cons": "Onsite opportunities are competitive", "work_life": 3.5, "skill_dev": 4.0, "salary": 3.5, "job_security": 4.0, "management": 4.0, "source": "AmbitionBox"},
    {"company": "Infosys", "date": "2026-04-12", "rating": 2.5, "department": "Finance", "employment_type": "Full-time", "pros": "Brand name helps in future job search", "cons": "Poor salary and limited growth", "work_life": 2.5, "skill_dev": 2.5, "salary": 2.0, "job_security": 3.5, "management": 2.5, "source": "AmbitionBox"},
    {"company": "Infosys", "date": "2026-04-20", "rating": 4.5, "department": "Cloud & Infrastructure", "employment_type": "Full-time", "pros": "Amazing learning platform and mentors", "cons": "Sometimes projects are repetitive", "work_life": 4.0, "skill_dev": 5.0, "salary": 4.0, "job_security": 4.5, "management": 4.5, "source": "AmbitionBox"},
    {"company": "Infosys", "date": "2026-04-28", "rating": 3.5, "department": "Data & Analytics", "employment_type": "Full-time", "pros": "Good exposure to big data tools", "cons": "Work pressure during deadlines is high", "work_life": 3.0, "skill_dev": 4.0, "salary": 3.5, "job_security": 4.0, "management": 3.0, "source": "AmbitionBox"},
]

df = pd.DataFrame(reviews)
df.to_csv("data/reviews.csv", index=False)
print(f"✓ Saved {len(df)} reviews")
print(df.head())