import sqlite3

# Connect to the database
conn = sqlite3.connect('db.sqlite3')
cursor = conn.cursor()

# Get all table names
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()

print("Database Tables:")
for table in tables:
    print(table[0])

# Show some data from key tables
print("\n--- Student Profiles ---")
cursor.execute("SELECT user_id, roll_no FROM accounts_studentprofile LIMIT 10;")
students = cursor.fetchall()
for student in students:
    print(f"User ID: {student[0]}, Roll No: {student[1]}")

print("\n--- Recruiter Profiles ---")
cursor.execute("SELECT user_id, company_name FROM accounts_recruiterprofile LIMIT 10;")
recruiters = cursor.fetchall()
for recruiter in recruiters:
    print(f"User ID: {recruiter[0]}, Company: {recruiter[1]}")

conn.close()