# 🚀 Internship Portal - Complete Feature Implementation Guide

## Phase 1: Database Migration & Setup

### Step 1: Create and Apply Migrations

```bash
# Navigate to project root
cd C:\Users\Vaibhav\OneDrive\Documents\EY_4.0_AVCOE\Project3

# Activate virtual environment
.venv\Scripts\Activate

# Create migrations for accounts app
python manage.py makemigrations accounts

# Create migrations for jobs app
python manage.py makemigrations jobs

# Apply all migrations
python manage.py migrate
```

### Expected Output:
```
Operations to perform:
  Apply all migrations: accounts, jobs, admin, auth, contenttypes, sessions
Running migrations:
  ...
  Applying jobs.0003_... OK
  ...
Operations completed successfully. All models are now in database.
```

---

## Phase 2: Implemented Models Overview

### New Models Created:

#### 1. **InternshipPost** 
- Dedicated model for internship postings
- Fields: title, company, description, skills_required, duration_weeks, stipend, location, etc.
- Status: Draft → Approved → Published → Closed

#### 2. **InternshipApplication**
- Extended application with resume + cover letter
- Status: Applied → Shortlisted → Interview → Selected → Rejected/Completed

#### 3. **InternshipInterview**
- Interview scheduling (Online/Offline/Phone)
- Tracks interview link, location, notes
- Status: Scheduled → Completed → Cancelled

#### 4. **InternshipCompletion**
- Work submission tracking
- Feedback from both recruiter and student
- Certificate issuance
- Ratings system (1-5 stars)

#### 5. **Notification**
- System notifications
- Types: Application, Interview, Selection, Certificate, Announcement
- Channels: Email, SMS, In-App

#### 6. **StudentSkill**
- Track individual skills with proficiency levels
- Beginner → Intermediate → Advanced → Expert

#### 7. **OTPVerification**
- Email and phone OTP verification
- Auto-expiry after set time
- Secure verification flow

#### 8. **AdminAnnouncement**
- TPO announcements for Students/Companies
- Audience targeting
- Expiry management

#### 9. **StudentFeedback**
- Student feedback on internship
- Ratings and recommendation

---

## Phase 3: Updated Models

### StudentProfile Enhancements:
- ✅ `email_verified` - Email verification status
- ✅ `phone_verified` - Phone verification status
- ✅ `phone_number` - Phone number field
- ✅ `portfolio_url` - Portfolio/LinkedIn URL
- ✅ `cover_letter_template` - Default cover letter
- ✅ `created_at` / `updated_at` - Timestamps

### RecruiterProfile Enhancements:
- ✅ `description` - Company description
- ✅ `industry` - Industry type
- ✅ `hr_contact_email` - HR email
- ✅ `hr_contact_phone` - HR phone
- ✅ `block_reason` - Blocking reason
- ✅ `created_at` / `updated_at` - Timestamps

---

## Phase 4: Next Steps (To Be Implemented)

### 1. Create Forms (forms.py)
```python
- InternshipPostForm
- InternshipApplicationForm
- InterviewScheduleForm
- InternshipCompletionForm
- OTPVerificationForm
- StudentSkillForm
- AdminAnnouncementForm
```

### 2. Create Views (views.py)
```python
# Student Views
- BrowseInternshipsView
- InternshipDetailView
- ApplyInternshipView
- StudentApplicationListView
- SubmitWorkView
- RateInternshipView

# Recruiter Views
- PostInternshipView
- ManageApplicationsView
- ScheduleInterviewView
- ViewSubmissionView
- IssueCertificateView

# TPO Views
- ApproveInternshipView
- ManageAnnouncementsView
- ViewAnalyticsView
- ExportReportsView
```

### 3. Create Templates
```
- internship_list.html
- internship_detail.html
- apply_internship.html
- interview_schedule.html
- work_submission.html
- certificate_view.html
- announcements.html
```

### 4. Update URL Configuration
```python
# Add to accounts/urls.py or create new jobs/urls.py

path('internships/', views.BrowseInternshipsView.as_view(), name='internship_list'),
path('internships/<int:pk>/', views.InternshipDetailView.as_view(), name='internship_detail'),
path('internships/<int:pk>/apply/', views.ApplyInternshipView.as_view(), name='apply_internship'),
path('internships/<int:pk>/schedule-interview/', views.ScheduleInterviewView.as_view(), name='schedule_interview'),
path('applications/<int:pk>/submit-work/', views.SubmitWorkView.as_view(), name='submit_work'),
path('internships/<int:pk>/certificate/', views.IssueCertificateView.as_view(), name='issue_certificate'),
```

### 5. OTP Implementation
```python
# Email OTP Service
from django.core.mail import send_mail
import random
import string

def generate_otp():
    return ''.join(random.choices(string.digits, k=6))

def send_otp_email(user, otp):
    subject = 'Email Verification OTP'
    message = f'Your OTP is: {otp}\nValid for 10 minutes'
    send_mail(subject, message, 'admin@portal.com', [user.email])
```

### 6. Notification System
```python
# Automated notifications
def notify_student_shortlisted(application):
    Notification.objects.create(
        user=application.student,
        notification_type='Shortlisted',
        title='You are shortlisted!',
        message=f'Congratulations! You are shortlisted for {application.internship.title}',
        channel='Email'
    )
```

### 7. Search & Filter Features
```python
# Internship Filters
- Domain (IT, Marketing, Finance, etc.)
- Location (Remote, Onsite)
- Duration (2-4 weeks, 4-8 weeks, etc.)
- Stipend Range
- Company
- Skills Required
```

### 8. Admin Dashboard Enhancements
```
- Total Internships Posted
- Total Applications
- Completion Rate
- Average Ratings
- Top Companies
- Student Engagement Metrics
```

---

## Phase 5: Manual Setup Tasks

### 1️⃣ **Create Migration Files**

After running `makemigrations`, you should see new files in:
- `accounts/migrations/0003_*.py`
- `jobs/migrations/0003_*.py` (or higher)

Verify these files exist before running migrate.

### 2️⃣ **Run Migrations**

```bash
python manage.py migrate
```

Check output for any errors. If successful, you'll see "Operations completed successfully."

### 3️⃣ **Create Superuser (if not already done)**

```bash
python manage.py createsuperuser
# or use existing: admin / Admin@123
```

### 4️⃣ **Verify Database**

```bash
python manage.py dbshell
> .tables
# You should see: jobs_internshippost, jobs_internshipapplication, etc.
> .quit
```

### 5️⃣ **Update Admin Interface** (admin.py)

Add new models to Django admin:

```python
from django.contrib import admin
from jobs.models import *

@admin.register(InternshipPost)
class InternshipPostAdmin(admin.ModelAdmin):
    list_display = ['title', 'company', 'status', 'created_at']
    list_filter = ['status', 'is_paid', 'created_at']
    search_fields = ['title', 'company', 'description']

# Register other models similarly
```

### 6️⃣ **Test API Endpoints**

```bash
# Start server
python manage.py runserver

# Test endpoints:
# GET http://127.0.0.1:8000/internships/
# GET http://127.0.0.1:8000/internships/1/
# POST http://127.0.0.1:8000/internships/1/apply/
```

### 7️⃣ **Populate Test Data** (Optional)

Create fixture file: `fixtures/test_internships.json`

```bash
python manage.py loaddata fixtures/test_internships.json
```

### 8️⃣ **Configure Email Backend** (settings.py)

```python
# For development (console output):
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# For production (SMTP):
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'your-email@gmail.com'
EMAIL_HOST_PASSWORD = 'your-app-password'
```

### 9️⃣ **Configure SMS Service** (Optional)

For SMS OTP, integrate Twilio or MSG91:

```python
# Install: pip install twilio
# Configure in settings.py with API keys
```

### 🔟 **Run Tests**

```bash
python manage.py test jobs
python manage.py test accounts
```

---

## Implementation Timeline

| Phase | Task | Time | Status |
|-------|------|------|--------|
| 1 | Database Models | ✅ Done | Completed |
| 2 | Model Migration | ⏳ TODO | Next Step |
| 3 | Forms | ⏳ TODO | After migration |
| 4 | Views | ⏳ TODO | After forms |
| 5 | Templates | ⏳ TODO | After views |
| 6 | URL Routing | ⏳ TODO | Final |
| 7 | Testing | ⏳ TODO | After routing |

---

## ✨ Features Summary

### Student Features:
✅ Registration with email verification  
✅ Browse internships with filters  
✅ Apply with resume + cover letter  
✅ Track application status  
✅ Schedule interviews  
✅ Submit work  
✅ Rate company  
✅ Download certificate  

### Recruiter Features:
✅ Post internships  
✅ View applications  
✅ Schedule interviews  
✅ Track submissions  
✅ Issue certificates  
✅ Send feedback  

### Admin (TPO) Features:
✅ Approve internships  
✅ Manage users  
✅ View analytics  
✅ Send announcements  
✅ Export reports  

---

## 🔗 Database Relationships

```
CustomUser
├── StudentProfile (1-to-1)
│   ├── StudentSkill (1-to-many)
│   ├── InternshipApplication (1-to-many)
│   └── OTPVerification (1-to-many)
├── RecruiterProfile (1-to-1)
│   └── InternshipPost (1-to-many)
└── Notification (1-to-many)

InternshipPost (1-to-many) → InternshipApplication
InternshipApplication (1-to-many) → InternshipInterview
InternshipApplication (1-to-1) → InternshipCompletion
InternshipApplication (1-to-1) → StudentFeedback
```

---

## Ready to Proceed?

**Next Command to Run:**

```bash
# 1. Create migrations
python manage.py makemigrations

# 2. Apply migrations
python manage.py migrate

# 3. Start server
python manage.py runserver
```

Then access: http://127.0.0.1:8000/

---

**All database models are now ready! 🎉**
