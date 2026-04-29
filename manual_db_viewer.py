import sqlite3
import os

# Database path
db_path = 'db.sqlite3'

# Check if database exists
if not os.path.exists(db_path):
    print(f"Database file '{db_path}' not found!")
    exit(1)

# Connect to database
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

print("=== DATABASE VIEWER ===\n")

# Get all tables
cursor.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name;")
tables = cursor.fetchall()

print(f"Found {len(tables)} tables:")
for table in tables:
    print(f"  - {table[0]}")

print("\n" + "="*50)

# Show student data
print("\n=== STUDENT PROFILES ===")
cursor.execute("""
    SELECT sp.id, u.username, sp.roll_no, sp.branch, sp.cgpa, sp.is_verified
    FROM accounts_studentprofile sp
    JOIN accounts_customuser u ON sp.user_id = u.id
    ORDER BY sp.id
""")
students = cursor.fetchall()

if students:
    print(f"Total students: {len(students)}")
    print("ID | Username | Roll No | Branch | CGPA | Verified")
    print("-" * 60)
    for student in students:
        roll_no = student[2] if student[2] else "N/A"
        branch = student[3] if student[3] else "N/A"
        cgpa = f"{student[4]}" if student[4] else "N/A"
        verified = "Yes" if student[5] else "No"
        print(f"{student[0]} | {student[1]} | {roll_no} | {branch} | {cgpa} | {verified}")
else:
    print("No student profiles found.")

print("\n" + "="*50)

# Show recruiter data
print("\n=== RECRUITER PROFILES ===")
cursor.execute("""
    SELECT rp.id, u.username, rp.company_name, rp.industry, rp.is_approved
    FROM accounts_recruiterprofile rp
    JOIN accounts_customuser u ON rp.user_id = u.id
    ORDER BY rp.id
""")
recruiters = cursor.fetchall()

if recruiters:
    print(f"Total recruiters: {len(recruiters)}")
    print("ID | Username | Company | Industry | Approved")
    print("-" * 60)
    for recruiter in recruiters:
        industry = recruiter[3] if recruiter[3] else "N/A"
        approved = "Yes" if recruiter[4] else "No"
        print(f"{recruiter[0]} | {recruiter[1]} | {recruiter[2]} | {industry} | {approved}")
else:
    print("No recruiter profiles found.")

print("\n" + "="*50)

# Show jobs data
print("\n=== JOBS ===")
cursor.execute("PRAGMA table_info(jobs_jobpost);")
columns = cursor.fetchall()
print("Job table columns:")
for col in columns:
    print(f"  {col[1]} ({col[2]})")

cursor.execute("""
    SELECT j.id, j.title, j.company, u.username as posted_by, j.status, j.created_at
    FROM jobs_jobpost j
    JOIN accounts_customuser u ON j.posted_by_id = u.id
    ORDER BY j.created_at DESC
    LIMIT 5
""")
jobs = cursor.fetchall()

if jobs:
    print(f"\nRecent jobs (showing last {len(jobs)}):")
    print("ID | Title | Company | Posted By | Status | Created")
    print("-" * 80)
    for job in jobs:
        created = job[5][:10] if job[5] else "N/A"  # Show only date
        print(f"{job[0]} | {job[1]} | {job[2]} | {job[3]} | {job[4]} | {created}")
else:
    print("No jobs found.")

# Close connection
conn.close()

print("\n=== END OF DATABASE VIEW ===")