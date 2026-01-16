# RBAC Implementation - Deployment & Migration Guide

## Phase 1: Database Migration

### Step 1.1: Create & Apply Migrations

```bash
# From project root directory
cd C:\Users\Vaibhav\OneDrive\Documents\EY_4.0_AVCOE\Project3

# Create migrations for new models
python manage.py makemigrations accounts
python manage.py makemigrations jobs

# Review migrations (optional but recommended)
cat accounts/migrations/000X_*.py
cat jobs/migrations/000X_*.py

# Apply migrations
python manage.py migrate accounts
python manage.py migrate jobs
```

### Step 1.2: Expected Database Changes

**New Tables:**
- accounts_recruiterprofile
- accounts_eligibilityrule
- jobs_interviewschedule

**Modified Tables:**
- accounts_studentprofile
  - ADD: is_verified (Boolean)
  - ADD: is_blacklisted (Boolean)
  - ADD: blacklist_reason (TextField)
  - ADD: verified_by_id (ForeignKey)
  - ADD: verified_at (DateTime)

- accounts_customuser
  - (role_type field already exists)

- jobs_jobpost
  - ADD: status (CharField, default='Open')
  - ADD: created_at (DateTime)
  - ADD: updated_at (DateTime)

- jobs_application
  - ADD: is_closed (Boolean)
  - ADD: closed_at (DateTime)

- jobs_applicationstatus
  - ADD: updated_by_id (ForeignKey)

---

## Phase 2: Create Initial Admin/TPO User

### Step 2.1: Create Superuser

```bash
# Create Django superuser (this is your TPO account)
python manage.py createsuperuser

# Follow prompts:
# Username: admin (or your choice)
# Email: admin@college.edu
# Password: (secure password)
# Superuser status: Yes
```

### Step 2.2: Set TPO Role

```bash
# Open Django shell
python manage.py shell

# In the Python shell:
from django.contrib.auth import get_user_model
from accounts.models import CustomUser

User = get_user_model()

# Get the admin user
admin_user = User.objects.get(username='admin')

# Set role to TPO
admin_user.role_type = CustomUser.TPO
admin_user.save()

# Verify
print(f"Role set to: {admin_user.role_type}")
print(f"Is TPO: {admin_user.is_tpo}")

# Exit shell
exit()
```

---

## Phase 3: Data Migration (If Migrating from Existing System)

### Step 3.1: Migrate Existing StudentProfiles

```bash
python manage.py shell
```

```python
from accounts.models import StudentProfile

# If you have existing students, they need verification
# You can batch verify them or mark for manual review

# Option 1: Mark all as pending verification
profiles = StudentProfile.objects.all()
for profile in profiles:
    profile.is_verified = False  # Default
    profile.save()

# Option 2: Auto-verify (only if data is clean)
# profiles = StudentProfile.objects.all()
# for profile in profiles:
#     if profile.cgpa and profile.active_backlogs is not None:
#         profile.is_verified = True
#         profile.save()

exit()
```

### Step 3.2: Migrate Existing RecruiterAccounts

```python
from django.contrib.auth import get_user_model
from accounts.models import RecruiterProfile

User = get_user_model()

# Find all recruiter users (if role_type is already set)
recruiters = User.objects.filter(role_type='RECRUITER')

for recruiter in recruiters:
    if not hasattr(recruiter, 'recruiter_profile'):
        # Create profile for this recruiter
        RecruiterProfile.objects.create(
            user=recruiter,
            company_name=recruiter.first_name or 'Company Name',
            company_email=recruiter.email,
            is_approved=True,  # Approve existing recruiters
        )
```

---

## Phase 4: Configure Settings

### Step 4.1: Update settings.py

```python
# settings.py

# ============================================
# AUTHENTICATION
# ============================================

AUTH_USER_MODEL = 'accounts.CustomUser'

LOGIN_URL = 'login'
LOGIN_REDIRECT_URL = 'home'
LOGOUT_REDIRECT_URL = 'home'

# ============================================
# SESSION & SECURITY
# ============================================

SESSION_COOKIE_SECURE = True  # Only HTTPS in production
SESSION_COOKIE_HTTPONLY = True
CSRF_COOKIE_SECURE = True  # Only HTTPS in production

# ============================================
# FILE UPLOAD
# ============================================

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Resume upload settings
FILE_UPLOAD_MAX_MEMORY_SIZE = 5242880  # 5MB
DATA_UPLOAD_MAX_MEMORY_SIZE = 5242880

# Allowed file types
ALLOWED_RESUME_EXTENSIONS = ['.pdf', '.doc', '.docx']

# ============================================
# LOGGING (for audit trail)
# ============================================

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': os.path.join(BASE_DIR, 'logs', 'rbac.log'),
        },
    },
    'loggers': {
        'placement_portal': {
            'handlers': ['file'],
            'level': 'INFO',
            'propagate': True,
        },
    },
}

# Create logs directory if not exists
import os
LOGS_DIR = os.path.join(BASE_DIR, 'logs')
os.makedirs(LOGS_DIR, exist_ok=True)
```

### Step 4.2: Create logs directory

```bash
# Create logs directory for audit trail
mkdir logs
```

---

## Phase 5: Run Tests

### Step 5.1: Check System Health

```bash
# Run Django checks
python manage.py check

# Run management commands
python manage.py makemigrations --check  # Should show no changes needed

# Test database connectivity
python manage.py dbshell
```

### Step 5.2: Start Development Server

```bash
# Start development server
python manage.py runserver

# Server should be running at http://localhost:8000
```

---

## Phase 6: Verification Checklist

- [ ] Database migrations applied successfully
- [ ] TPO user created and role set
- [ ] Django admin accessible (http://localhost:8000/admin)
- [ ] Media folder created for resume uploads
- [ ] Static files collected (if in production)
- [ ] Logs directory created
- [ ] Settings.py updated with AUTH_USER_MODEL
- [ ] Development server running without errors

---

## Phase 7: Post-Deployment Configuration

### Step 7.1: Configure Admin Interface

```python
# accounts/admin.py

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, StudentProfile, RecruiterProfile, EligibilityRule

class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'role_type', 'is_staff', 'is_active')
    list_filter = ('role_type', 'is_staff', 'is_active')
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name', 'email')}),
        ('Role', {'fields': ('role_type',)}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
    )

class StudentProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'roll_no', 'cgpa', 'is_verified', 'is_blacklisted')
    list_filter = ('is_verified', 'is_blacklisted', 'branch')
    search_fields = ('user__username', 'roll_no')
    readonly_fields = ('verified_by', 'verified_at')

class RecruiterProfileAdmin(admin.ModelAdmin):
    list_display = ('company_name', 'user', 'is_approved', 'is_blocked')
    list_filter = ('is_approved', 'is_blocked')
    search_fields = ('company_name', 'user__username')
    readonly_fields = ('approved_by', 'approved_at')

class EligibilityRuleAdmin(admin.ModelAdmin):
    list_display = ('name', 'min_cgpa', 'max_active_backlogs', 'is_active')
    list_filter = ('is_active',)

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(StudentProfile, StudentProfileAdmin)
admin.site.register(RecruiterProfile, RecruiterProfileAdmin)
admin.site.register(EligibilityRule, EligibilityRuleAdmin)
```

### Step 7.2: Create Initial Eligibility Rules

```bash
python manage.py shell
```

```python
from accounts.models import EligibilityRule, CustomUser

# Get TPO user
tpo = CustomUser.objects.get(role_type='TPO')

# Create default eligibility rule
rule = EligibilityRule.objects.create(
    name='Default Eligibility',
    description='Default minimum requirements for all students',
    min_cgpa=2.5,
    max_active_backlogs=2,
    is_active=True,
    created_by=tpo
)

print(f"Created rule: {rule.name}")
exit()
```

---

## Phase 8: Troubleshooting

### Issue: "AUTH_USER_MODEL" not recognized

**Solution**: Ensure AUTH_USER_MODEL is set in settings.py BEFORE running migrations

```python
AUTH_USER_MODEL = 'accounts.CustomUser'
```

### Issue: Migration errors

**Solution**: Clear and recreate migrations (only for development)

```bash
# WARNING: Only in development, not production
rm accounts/migrations/000X_*.py  # Keep only __init__.py
python manage.py makemigrations accounts
python manage.py migrate accounts
```

### Issue: Recruiter cannot post jobs after approval

**Solution**: Ensure RecruiterProfile.is_approved = True and is_blocked = False

```python
python manage.py shell
from accounts.models import RecruiterProfile
profile = RecruiterProfile.objects.get(user__username='recruiter1')
profile.is_approved = True
profile.is_blocked = False
profile.save()
exit()
```

### Issue: Students cannot apply

**Solution**: Check StudentProfile verification status and ensure profile is complete

```python
python manage.py shell
from accounts.models import StudentProfile
profile = StudentProfile.objects.get(user__username='student1')
print(f"Verified: {profile.is_verified}")
print(f"Blacklisted: {profile.is_blacklisted}")
print(f"CGPA: {profile.cgpa}")
print(f"Backlogs: {profile.active_backlogs}")
exit()
```

---

## Phase 9: Backup Strategy

### Before Going Live

```bash
# Backup database
python manage.py dumpdata > backup_$(date +%Y%m%d).json

# Backup media files
cp -r media/ media_backup_$(date +%Y%m%d)/

# Backup logs
cp -r logs/ logs_backup_$(date +%Y%m%d)/
```

### Recovery

```bash
# Restore database
python manage.py loaddata backup_YYYYMMDD.json

# Restore media files
cp -r media_backup_YYYYMMDD/* media/
```

---

## Phase 10: Performance Optimization

### Database Indexes

Already included in models:

```python
# JobPost
indexes = [
    models.Index(fields=['status', 'deadline']),
    models.Index(fields=['posted_by']),
]

# Application
indexes = [
    models.Index(fields=['student', 'status']),
    models.Index(fields=['job', 'status']),
]

# ApplicationStatus
indexes = [
    models.Index(fields=['application', 'timestamp']),
]
```

### Query Optimization

Use `select_related()` and `prefetch_related()`:

```python
# Good: Single query with JOINs
applications = Application.objects.select_related(
    'student', 'job'
).prefetch_related('status_history')

# Bad: Multiple queries (N+1 problem)
applications = Application.objects.all()
for app in applications:
    print(app.student.username)  # Extra query per app
```

---

## Summary Commands

```bash
# Complete setup from scratch:

# 1. Create/Apply migrations
python manage.py makemigrations
python manage.py migrate

# 2. Create TPO user
python manage.py createsuperuser

# 3. Set TPO role (via shell)
python manage.py shell
# Then set role_type

# 4. Create initial eligibility rules
python manage.py shell
# Then create EligibilityRule

# 5. Start server
python manage.py runserver

# Access at:
# - Home: http://localhost:8000/
# - Admin: http://localhost:8000/admin
# - Student Register: http://localhost:8000/accounts/register/student/
# - Recruiter Register: http://localhost:8000/accounts/register/recruiter/
```

---

## Post-Deployment Monitoring

### Key Metrics to Track

1. **Login Attempts**: Monitor for brute force
2. **Authorization Failures**: Track 403 errors
3. **Data Access**: Audit trail of who accessed what
4. **Job Postings**: Count and status
5. **Applications**: Status distribution (Pending, Shortlisted, Selected)
6. **Placement Rate**: Selected / Total Applications

### Setup Monitoring

```python
# Logging important events
import logging

logger = logging.getLogger('placement_portal')

# Example: Log status changes
logger.info(f'User {user.username} changed application {app.id} status to {new_status}')
```

---

**Document Version**: 1.0
**Last Updated**: January 2026
**For Questions**: Refer to RBAC_IMPLEMENTATION.md
