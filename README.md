# Smart Internship and Placement Portal

This repository contains a Django-based implementation of a Smart Internship and Placement Portal with RBAC (Student, Recruiter, TPO).

Basic setup (Windows, VS Code):

1. Install Python 3.10+ and MySQL Server. Install MySQL Workbench to create DB.
2. Clone repo (or use workspace). Open terminal in `Project3`.
3. Create virtualenv and activate (PowerShell):

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install --upgrade pip
pip install -r requirements.txt
```

4. Create a MySQL database and user (example using Workbench): create database `placement_db` and grant privileges.
5. Update `placement_portal/settings.py` DATABASES with your MySQL `USER` and `PASSWORD`.
6. Run migrations and create superuser:

```powershell
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

7. Open `http://127.0.0.1:8000/`.

Advanced features and notes:
- Resume parsing: use `pyresparser` to parse uploaded resumes and populate `skills`. See `README` sections below.
- Export to Excel: use `pandas`/`openpyxl` to export placed students.
- Zip resumes: TPO or Recruiter can download shortlisted resumes as a .zip file.

Security and RBAC:
- `CustomUser.role_type` controls access. Add decorators and checks in views for stricter RBAC.
