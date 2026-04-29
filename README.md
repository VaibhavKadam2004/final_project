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

## Advanced AI Features

### 1. OpenAI GPT Integration
- **Setup**: Copy `.env.example` to `.env` and add your `OPENAI_API_KEY`
- **Usage**: Access GPT-powered career recommendations via `/ai/gpt-recommendations/`
- **Features**: Personalized advice based on student skills and job requirements

### 2. Custom ML Model Training
- **Command**: `python manage.py train_models`
- **Purpose**: Trains RandomForest model on historical placement data for prediction
- **Output**: Model saved to `ai_models/placement_predictor.pkl`
- **Accuracy**: Displays training accuracy in console

### 3. Resume Parsing with PyResparser
- **Automatic**: Skills extracted when students upload resumes in profile
- **Integration**: Built into student profile update view
- **Fallback**: Manual skill entry still available if parsing fails

### Environment Setup
```bash
pip install python-dotenv
cp .env.example .env
# Edit .env with your API keys
```
