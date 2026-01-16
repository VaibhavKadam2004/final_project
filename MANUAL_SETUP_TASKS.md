# 🔧 MANUAL TASKS - FOLLOW EXACTLY

## ⚠️ CRITICAL: These steps MUST be done in terminal

---

## **STEP 1: Activate Virtual Environment**

```bash
.venv\Scripts\Activate
```

✅ **Verify it worked:** Prompt should show `(.venv) PS ...`

---

## **STEP 2: Create Database Migrations**

```bash
python manage.py makemigrations accounts
```

**Expected Output:**
```
Migrations for 'accounts':
  accounts/migrations/0003_studentprofile_email_verified.py
    - Add field email_verified to studentprofile
    - Add field phone_verified to studentprofile
    - Add field phone_number to studentprofile
    - Add field portfolio_url to studentprofile
    - Add field cover_letter_template to studentprofile
    - Add field created_at to studentprofile
    - Add field updated_at to studentprofile
    - Alter field recruiter_profile..., etc.
```

### If error occurs:
```bash
# Clear Python cache
python -Bc "import py_compile; py_compile.compile('accounts/models.py', doraise=True)"

# Try again
python manage.py makemigrations accounts --dry-run
```

---

## **STEP 3: Create Jobs App Migrations**

```bash
python manage.py makemigrations jobs
```

**Expected Output:**
```
Migrations for 'jobs':
  jobs/migrations/0003_*.py
    - Create model InternshipPost
    - Create model InternshipApplication
    - Create model InternshipInterview
    - Create model InternshipCompletion
    - Create model Notification
    - Create model StudentFeedback
    - Create model StudentSkill
    - Create model OTPVerification
    - Create model AdminAnnouncement
    - Alter application...
```

---

## **STEP 4: View All Pending Migrations**

```bash
python manage.py migrate --plan
```

**Check Output:** Should show all pending migrations for accounts and jobs

---

## **STEP 5: Apply All Migrations**

```bash
python manage.py migrate
```

**Expected Output:**
```
Operations to perform:
  Apply all migrations: accounts, admin, auth, contenttypes, jobs, sessions
Running migrations:
  Applying accounts.0003_... OK
  Applying jobs.0003_... OK
  ...
Operations completed successfully. All models are now in database.
```

---

## **STEP 6: Verify Database (Optional)**

```bash
python manage.py dbshell
```

Then type:
```sql
.tables
```

**Should see tables like:**
- `jobs_internshippost`
- `jobs_internshipapplication`
- `jobs_internshipinterview`
- `jobs_internshipcompletion`
- `jobs_notification`
- `jobs_studentskill`
- `jobs_otpverification`
- `jobs_adminannouncement`

Exit with: `.quit`

---

## **STEP 7: Start Server and Test**

```bash
python manage.py runserver
```

**Expected Output:**
```
Watching for file changes with StatReloader
Performing system checks...
System check identified no issues (0 silenced).
January 15, 2026 - 04:35:00
Django version 6.0.1, using settings 'placement_portal.settings'
Starting development server at http://127.0.0.1:8000/
Quit the server with CTRL-BREAK.
```

---

## **STEP 8: Access Portal**

Open browser and go to:
```
http://127.0.0.1:8000/
```

---

## **STEP 9: Access Admin Panel** (Optional)

```
http://127.0.0.1:8000/admin/

Login with:
Username: admin
Password: Admin@123
```

---

## ⚡ Complete Command Sequence (Copy & Paste)

```bash
# Activate environment
.venv\Scripts\Activate

# Create all migrations
python manage.py makemigrations accounts jobs

# Apply migrations
python manage.py migrate

# Start server
python manage.py runserver
```

---

## ✅ Success Indicators

After running migrations, you should see:
- ✅ No errors in terminal
- ✅ "Operations completed successfully" message
- ✅ Server starts without errors
- ✅ Website loads at http://127.0.0.1:8000/
- ✅ New database tables created

---

## ❌ If Something Goes Wrong

### Migration Errors:

```bash
# Check what's pending
python manage.py migrate --plan

# Check for issues
python manage.py check

# Reset (CAUTION - clears database)
python manage.py migrate accounts zero
python manage.py migrate jobs zero
python manage.py migrate
```

### Server won't start:

```bash
# Check for syntax errors
python manage.py check

# Clear Python cache
python -Bc "import compileall; compileall.compile_dir('.')"

# Try starting again
python manage.py runserver
```

### Database issues:

```bash
# Backup current database
copy db.sqlite3 db.sqlite3.backup

# Delete and recreate
del db.sqlite3
python manage.py migrate
python manage.py createsuperuser
```

---

## 📋 Checklist Before Running

- [ ] Virtual environment activated (`.venv\Scripts\Activate`)
- [ ] In correct directory (`EY_4.0_AVCOE\Project3`)
- [ ] Python 3.12+ installed (`python --version`)
- [ ] Django 6.0.1 installed (`pip show django`)
- [ ] No unsaved files in VS Code
- [ ] Read through all 9 steps above

---

## 🎯 Final Step

After migrations succeed:

1. **Test Student Registration**
   - Go to http://127.0.0.1:8000/accounts/register/
   - Register a test student account
   - Verify OTP functionality

2. **Test Recruiter Registration**
   - Go to http://127.0.0.1:8000/accounts/register/recruiter/
   - Register a test company account
   - Wait for TPO approval

3. **Test Admin Functions**
   - Login as admin: admin/Admin@123
   - Approve recruiter
   - Verify student
   - Send announcement

---

## 📞 If Stuck

Try these debug commands:

```bash
# Check all models
python manage.py inspectdb

# List installed apps
python manage.py shell
>>> from django.apps import apps
>>> for app in apps.get_app_configs(): print(app.name)

# Exit shell
>>> exit()
```

---

## ✨ Expected Results After Migration

```
Database File: db.sqlite3
├── CustomUser table (enhanced)
├── StudentProfile table (with 6 new fields)
├── RecruiterProfile table (with 8 new fields)
├── InternshipPost table (NEW)
├── InternshipApplication table (NEW)
├── InternshipInterview table (NEW)
├── InternshipCompletion table (NEW)
├── Notification table (NEW)
├── StudentSkill table (NEW)
├── OTPVerification table (NEW)
└── AdminAnnouncement table (NEW)
```

---

## 🎉 Congratulations!

If everything ran successfully, you now have:
- ✅ 9 new database tables
- ✅ 14 new fields in existing tables
- ✅ Complete internship workflow schema
- ✅ Ready for next feature development

**Next Phase:** Create Forms and Views for each workflow

---

**RUN THESE COMMANDS NOW:**

```bash
.venv\Scripts\Activate
python manage.py makemigrations accounts jobs
python manage.py migrate
python manage.py runserver
```

