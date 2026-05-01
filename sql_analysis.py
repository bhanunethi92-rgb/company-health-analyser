import sqlite3

conn = sqlite3.connect("data/company_health.db")
cursor = conn.cursor()

# Query 1 - Total job postings
print("=== Query 1: Total Job Postings ===")
cursor.execute("SELECT COUNT(*) FROM job_postings;")
print("Total jobs:", cursor.fetchone()[0])

# Query 2 - Jobs by department
print("\n=== Query 2: Jobs by Department ===")
cursor.execute("SELECT department, COUNT(*) as total FROM job_postings GROUP BY department ORDER BY total DESC;")
for row in cursor.fetchall():
    print(row)

# Query 3 - Jobs by seniority
print("\n=== Query 3: Jobs by Seniority ===")
cursor.execute("SELECT seniority, COUNT(*) as total FROM job_postings GROUP BY seniority ORDER BY total DESC;")
for row in cursor.fetchall():
    print(row)

# Query 4 - Most recent 5 jobs
print("\n=== Query 4: Most Recent 5 Jobs ===")
cursor.execute("SELECT role, department, date FROM job_postings ORDER BY date DESC LIMIT 5;")
for row in cursor.fetchall():
    print(row)

# Query 5 - Jobs by month
print("\n=== Query 5: Jobs by Month ===")
cursor.execute("SELECT strftime('%Y-%m', date) as month, COUNT(*) as total FROM job_postings GROUP BY month ORDER BY month DESC;")
for row in cursor.fetchall():
    print(row)
    # Query 6 - Top 5 most hired roles
print("\n=== Query 6: Top 5 Most Hired Roles ===")
cursor.execute("SELECT role, COUNT(*) as total FROM job_postings GROUP BY role ORDER BY total DESC LIMIT 5;")
for row in cursor.fetchall():
    print(row)

# Query 7 - Data & Analytics jobs only
print("\n=== Query 7: Data & Analytics Jobs ===")
cursor.execute("SELECT role, seniority, date FROM job_postings WHERE department = 'Data & Analytics' ORDER BY date DESC;")
for row in cursor.fetchall():
    print(row)

# Query 8 - Senior and Management jobs
print("\n=== Query 8: Senior + Management Jobs ===")
cursor.execute("SELECT role, department, seniority FROM job_postings WHERE seniority IN ('Senior', 'Management') ORDER BY department;")
for row in cursor.fetchall():
    print(row)
    import csv

# Save Query 2 results to CSV
print("\n=== Saving Results to CSV ===")

# Jobs by department
cursor.execute("SELECT department, COUNT(*) as total FROM job_postings GROUP BY department ORDER BY total DESC;")
rows = cursor.fetchall()
with open("data/jobs_by_department.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["department", "total"])
    writer.writerows(rows)
print("Saved: jobs_by_department.csv")

# Jobs by seniority
cursor.execute("SELECT seniority, COUNT(*) as total FROM job_postings GROUP BY seniority ORDER BY total DESC;")
rows = cursor.fetchall()
with open("data/jobs_by_seniority.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["seniority", "total"])
    writer.writerows(rows)
print("Saved: jobs_by_seniority.csv")

# Top roles
cursor.execute("SELECT role, COUNT(*) as total FROM job_postings GROUP BY role ORDER BY total DESC LIMIT 10;")
rows = cursor.fetchall()
with open("data/top_roles.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["role", "total"])
    writer.writerows(rows)
print("Saved: top_roles.csv")

conn.close()