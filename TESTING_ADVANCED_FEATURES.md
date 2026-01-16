# 🧪 ADVANCED FEATURES - TEST SCENARIOS & VERIFICATION

Use this document to verify each feature works correctly before deployment.

---

## TEST SETUP

### Prerequisites
```bash
# 1. Create test database
python manage.py migrate

# 2. Create test users
python manage.py shell
```

In shell:
```python
from accounts.models import CustomUser, StudentProfile
from jobs.models import JobPost, Application, HistoricalHiringData, DreamCompany

# Create test users
admin_user = CustomUser.objects.create_superuser('admin', 'admin@test.com', 'admin123')

student1 = CustomUser.objects.create_user(
    username='student1', 
    email='student1@test.com', 
    password='pass123',
    role_type='STUDENT'
)

recruiter1 = CustomUser.objects.create_user(
    username='recruiter1',
    email='recruiter1@test.com',
    password='pass123',
    role_type='RECRUITER'
)

# Create student profiles
StudentProfile.objects.create(
    user=student1,
    cgpa=7.5,
    active_backlogs=0,
    skills="Python, Django, SQL",
    is_verified=True,
    roll_no="CS001",
    branch="Computer Science"
)

print("✅ Test users created")
```

---

## 🎯 FEATURE 1: Placement Credit Score (PCS) System

### Test 1.1: Initial PCS is 100
```python
from accounts.models import StudentProfile

profile = StudentProfile.objects.get(user__username='student1')
assert profile.credit_score == 100, f"Expected 100, got {profile.credit_score}"
assert profile.is_blocked == False, "Should not be blocked initially"
print("✅ Test 1.1 PASSED: Initial PCS is 100")
```

### Test 1.2: Penalty for Missed Interview
```python
from accounts.models import StudentProfile

profile = StudentProfile.objects.get(user__username='student1')
new_score = profile.update_pcs('missed_interview', 'Missed TCS interview')

assert new_score == 80, f"Expected 80, got {new_score}"
assert profile.credit_score == 80
print("✅ Test 1.2 PASSED: PCS decreased by 20 for missed interview")
```

### Test 1.3: Penalty for Rejected Offer
```python
from accounts.models import StudentProfile

profile = StudentProfile.objects.get(user__username='student1')
initial = profile.credit_score
new_score = profile.update_pcs('rejected_offer', 'Rejected Google offer')

assert new_score == (initial - 50), f"Expected {initial-50}, got {new_score}"
print("✅ Test 1.3 PASSED: PCS decreased by 50 for rejected offer")
```

### Test 1.4: Auto-block When Below Threshold
```python
from accounts.models import StudentProfile

profile = StudentProfile.objects.get(user__username='student1')

# Manually set to critical level
profile.credit_score = 45
profile.save()

# Apply penalty to trigger block
profile.update_pcs('missed_interview', 'Test')

assert profile.is_blocked == True, "Should be blocked when PCS < 50"
assert profile.blocked_until is not None, "Should have unblock date"
assert profile.block_reason != "", "Should have block reason"
print("✅ Test 1.4 PASSED: Auto-block triggered at PCS < 50")
```

### Test 1.5: Auto-unblock After Cooling Period
```python
from accounts.models import StudentProfile
from django.utils import timezone
from datetime import timedelta

profile = StudentProfile.objects.get(user__username='student1')

# Manually block with past unblock date
profile.is_blocked = True
profile.blocked_until = timezone.now() - timedelta(days=1)  # Past date
profile.save()

# Call unblock check
was_unblocked = profile.unblock_if_eligible()

assert was_unblocked == True, "Should have unblocked"
assert profile.is_blocked == False, "Should not be blocked anymore"
assert profile.blocked_until is None, "Unblock date should be cleared"
print("✅ Test 1.5 PASSED: Auto-unblock after cooling period")
```

### Test 1.6: Blocked Student Cannot Apply
```python
from accounts.models import StudentProfile

profile = StudentProfile.objects.get(user__username='student1')
profile.is_blocked = True
profile.save()

can_apply = profile.can_apply_for_jobs()

assert can_apply == False, "Blocked student should not be able to apply"
print("✅ Test 1.6 PASSED: Blocked student cannot apply for jobs")
```

### Test 1.7: PCS History is Recorded
```python
from accounts.models import StudentProfile
import json

profile = StudentProfile.objects.get(user__username='student1')

# Should have history
history = json.loads(profile.pcs_history or '[]')
assert len(history) > 0, "Should have history entries"
assert 'timestamp' in history[0], "Each entry should have timestamp"
assert 'type' in history[0], "Each entry should have penalty type"
print("✅ Test 1.7 PASSED: PCS history is recorded")
```

---

## 🎯 FEATURE 2: Eligibility Gatekeeper

### Test 2.1: Eligible Student Shows Green
```python
from jobs.models import JobPost
from accounts.models import CustomUser

student = CustomUser.objects.get(username='student1')

# Create test job
job = JobPost.objects.create(
    title="Python Developer",
    company="Google",
    description="Test job",
    posted_by=CustomUser.objects.get(username='recruiter1'),
    min_cgpa=7.0,
    max_backlogs=0,
    deadline=timezone.now() + timedelta(days=7)
)

eligible, reasons = job.check_student_eligibility(student)
assert eligible == True, "Student should be eligible"
assert reasons == [], f"Should have no reasons, got {reasons}"

badge = job.get_eligibility_badge(student)
assert badge['can_apply'] == True
assert badge['icon'] == '✅'
print("✅ Test 2.1 PASSED: Eligible student shows green")
```

### Test 2.2: Low CGPA Shows Lock
```python
from jobs.models import JobPost
from accounts.models import StudentProfile, CustomUser

student = CustomUser.objects.get(username='student1')
profile = student.student_profile
profile.cgpa = 6.0  # Below 7.0 requirement
profile.save()

job = JobPost.objects.create(
    title="Python Developer",
    company="Microsoft",
    description="Test job",
    posted_by=CustomUser.objects.get(username='recruiter1'),
    min_cgpa=7.0,
    max_backlogs=0,
    deadline=timezone.now() + timedelta(days=7)
)

eligible, reasons = job.check_student_eligibility(student)
assert eligible == False, "Student should not be eligible"
assert any('CGPA' in reason for reason in reasons), "Should mention CGPA"

badge = job.get_eligibility_badge(student)
assert badge['can_apply'] == False
assert badge['icon'] == '🔒'
print("✅ Test 2.2 PASSED: Low CGPA shows lock")
```

### Test 2.3: Too Many Backlogs Shows Lock
```python
from jobs.models import JobPost
from accounts.models import StudentProfile, CustomUser

student = CustomUser.objects.get(username='student1')
profile = student.student_profile
profile.cgpa = 8.0  # Good CGPA
profile.active_backlogs = 3  # Too many
profile.save()

job = JobPost.objects.create(
    title="Backend Developer",
    company="Amazon",
    description="Test job",
    posted_by=CustomUser.objects.get(username='recruiter1'),
    min_cgpa=7.0,
    max_backlogs=1,  # Max 1 backlog
    deadline=timezone.now() + timedelta(days=7)
)

eligible, reasons = job.check_student_eligibility(student)
assert eligible == False
assert any('backlog' in reason.lower() for reason in reasons)

badge = job.get_eligibility_badge(student)
assert badge['can_apply'] == False
print("✅ Test 2.3 PASSED: Too many backlogs shows lock")
```

### Test 2.4: Branch Mismatch Shows Lock
```python
from jobs.models import JobPost
from accounts.models import StudentProfile, CustomUser

student = CustomUser.objects.get(username='student1')
profile = student.student_profile
profile.branch = "Electronics"
profile.save()

job = JobPost.objects.create(
    title="Data Engineer",
    company="Facebook",
    description="Test job",
    posted_by=CustomUser.objects.get(username='recruiter1'),
    branches="Computer Science, IT",  # Only CS and IT
    min_cgpa=7.0,
    max_backlogs=0,
    deadline=timezone.now() + timedelta(days=7)
)

eligible, reasons = job.check_student_eligibility(student)
assert eligible == False
assert any('branch' in reason.lower() for reason in reasons)
print("✅ Test 2.4 PASSED: Branch mismatch shows lock")
```

---

## 🎯 FEATURE 3: Recruiter SLA Tracking

### Test 3.1: RecruiterResponseRating Created
```python
from jobs.models import RecruiterResponseRating
from accounts.models import CustomUser

recruiter = CustomUser.objects.get(username='recruiter1')

# Create rating (usually auto-created)
rating, created = RecruiterResponseRating.objects.get_or_create(recruiter=recruiter)

assert rating is not None, "Rating should exist"
assert rating.avg_response_hours == 0, "Initial avg should be 0"
print("✅ Test 3.1 PASSED: RecruiterResponseRating created")
```

### Test 3.2: Response Time Calculated
```python
from jobs.models import Application, JobPost, RecruiterResponseRating
from accounts.models import CustomUser, StudentProfile
from django.utils import timezone
from datetime import timedelta

student = CustomUser.objects.get(username='student1')
recruiter = CustomUser.objects.get(username='recruiter1')

# Create job with past deadline
job = JobPost.objects.create(
    title="QA Engineer",
    company="TCS",
    description="Test job",
    posted_by=recruiter,
    deadline=timezone.now() - timedelta(days=1),  # Past deadline
    min_cgpa=7.0,
    max_backlogs=0
)

# Create application
app = Application.objects.create(
    job=job,
    student=student
)

# Simulate 12 hours response time
app.first_status_change_at = job.deadline + timedelta(hours=12)
app.status = Application.STATUS_SHORTLISTED
app.save()

assert app.response_time_hours is not None, "Response time should be calculated"
print(f"✅ Test 3.2 PASSED: Response time calculated ({app.response_time_hours}h)")
```

### Test 3.3: Rating Label Correct
```python
from jobs.models import RecruiterResponseRating
from accounts.models import CustomUser

recruiter = CustomUser.objects.get(username='recruiter1')
rating = RecruiterResponseRating.objects.get(recruiter=recruiter)

# Calculate rating
rating.calculate_rating()

assert rating.rating_label is not None, "Should have label"
assert rating.responsiveness_rating > 0, "Should have rating"
print(f"✅ Test 3.3 PASSED: Rating label = {rating.rating_label}")
```

---

## 🎯 FEATURE 4: Dream Company Roadmap

### Test 4.1: Dream Company Created
```python
from jobs.models import DreamCompany
from accounts.models import CustomUser

student = CustomUser.objects.get(username='student1')

dream, created = DreamCompany.objects.get_or_create(
    student=student,
    defaults={
        'company_name': 'Google',
        'avg_cgpa_required': 8.5,
        'common_skills': 'Python, System Design, Algorithms'
    }
)

assert dream is not None
assert dream.company_name == 'Google'
print("✅ Test 4.1 PASSED: Dream company created")
```

### Test 4.2: Readiness Percentage Calculated
```python
from jobs.models import DreamCompany

dream = DreamCompany.objects.get(student__username='student1')

readiness = dream.get_readiness_percentage()

assert isinstance(readiness, int), "Should return int"
assert 0 <= readiness <= 100, f"Should be 0-100, got {readiness}"
print(f"✅ Test 4.2 PASSED: Readiness = {readiness}%")
```

### Test 4.3: Next Steps Listed
```python
from jobs.models import DreamCompany

dream = DreamCompany.objects.get(student__username='student1')
steps = dream.get_next_steps()

assert isinstance(steps, list), "Should return list"
# Steps might be empty if student is ready, or have items
print(f"✅ Test 4.3 PASSED: Next steps = {len(steps)} items")
```

---

## 🎯 FEATURE 5: Prep-Vault & Interview Experience

### Test 5.1: Interview Experience Created
```python
from jobs.models import InterviewExperience
from accounts.models import CustomUser

student = CustomUser.objects.get(username='student1')

exp = InterviewExperience.objects.create(
    student=student,
    company='Google',
    job_title='SDE',
    round_number=1,
    round_type='Coding',
    duration_minutes=90,
    difficulty='Hard',
    questions_asked='Design LRU Cache\nMerge K Sorted Arrays',
    your_experience='Solved in 45 mins, clean code',
    tips_for_others='Practice DP, use templates',
    selected_after=True,
    status='Pending'
)

assert exp is not None
assert exp.status == 'Pending'
print("✅ Test 5.1 PASSED: Interview experience created")
```

### Test 5.2: Experience Status Changed to Approved
```python
from jobs.models import InterviewExperience
from accounts.models import CustomUser

exp = InterviewExperience.objects.get(company='Google')
admin = CustomUser.objects.get(username='admin')

exp.status = 'Approved'
exp.approved_by = admin
exp.save()

assert exp.status == 'Approved'
assert exp.approved_by == admin
print("✅ Test 5.2 PASSED: Experience approved")
```

### Test 5.3: Prep Vault Shows Experience
```python
from jobs.models import PrepVault, HistoricalHiringData, InterviewExperience

# Ensure HistoricalHiringData exists
company_data, _ = HistoricalHiringData.objects.get_or_create(
    company_name='Google',
    defaults={
        'avg_cgpa': 8.5,
        'avg_backlogs': 0,
        'most_common_skills': 'Python, DSA',
        'students_hired': 5,
        'total_applicants': 100
    }
)

# Create prep vault
vault, _ = PrepVault.objects.get_or_create(company=company_data)

# Get approved experiences for this company
experiences = InterviewExperience.objects.filter(
    company='Google',
    status='Approved'
)

assert experiences.count() > 0
print(f"✅ Test 5.3 PASSED: Prep vault shows {experiences.count()} experiences")
```

---

## 🎯 FEATURE 6: TPO Master-Sheet Generator

### Test 6.1: Export Data Structure
```python
from jobs.models import Application, JobPost
from accounts.models import CustomUser
import pandas as pd

recruiter = CustomUser.objects.get(username='recruiter1')

# Get job
job = JobPost.objects.filter(posted_by=recruiter).first()

if job:
    applications = Application.objects.filter(job=job)
    
    # Build data (simulate export logic)
    data = []
    for app in applications:
        student = app.student
        profile = student.student_profile
        
        data.append({
            'Name': f"{student.first_name} {student.last_name}",
            'Email': student.email,
            'CGPA': profile.cgpa,
            'Status': app.status
        })
    
    df = pd.DataFrame(data)
    assert len(df) > 0, "Should have data"
    print(f"✅ Test 6.1 PASSED: Export has {len(df)} rows")
else:
    print("⚠️ Test 6.1 SKIPPED: No job data")
```

---

## 🔧 INTEGRATION TESTS

### Test 7.1: Complete Student Journey
```python
from django.utils import timezone
from datetime import timedelta

print("\n=== INTEGRATION TEST: Complete Student Journey ===\n")

# 1. Student applies for job
student = CustomUser.objects.get(username='student1')
job = JobPost.objects.first()
app = Application.objects.create(job=job, student=student)
print("✅ Step 1: Student applied")

# 2. Recruiter schedules interview
from jobs.models import InterviewSchedule
interview = InterviewSchedule.objects.create(
    application=app,
    round='Round 1',
    scheduled_date=timezone.now() + timedelta(days=3)
)
print("✅ Step 2: Interview scheduled")

# 3. Recruiter updates status after interview
from jobs.models import ApplicationStatus
app.status = 'Shortlisted'
app.save()
status_record = ApplicationStatus.objects.create(
    application=app,
    status='Shortlisted',
    updated_by=job.posted_by
)
print("✅ Step 3: Status updated")

# 4. Student shares experience
exp = InterviewExperience.objects.create(
    student=student,
    company=job.company,
    job_title=job.title,
    round_number=1,
    round_type='Technical',
    duration_minutes=60,
    difficulty='Medium',
    questions_asked='Q1\nQ2\nQ3',
    your_experience='Good discussion',
    tips_for_others='Practice DSA',
    selected_after=True
)
print("✅ Step 4: Experience submitted")

# 5. TPO approves experience
exp.status = 'Approved'
exp.save()
print("✅ Step 5: Experience approved")

print("\n✅ Integration test PASSED!")
```

---

## 📊 TEST SUMMARY TEMPLATE

After running tests, fill this in:

```
FEATURE TESTING SUMMARY
=======================

Date: ___________
Tester: ___________

TIER 1 FEATURES
[ ] PCS System - All tests passed
    - Initial PCS: 100
    - Penalties applied correctly
    - Auto-blocking works
    - Auto-unblocking works
    - History recorded
    
[ ] Eligibility Gate - All tests passed
    - CGPA check works
    - Backlog check works
    - Branch check works
    - Shows lock icon correctly
    
[ ] SLA Tracking - All tests passed
    - Response time calculated
    - Rating label correct
    - Shows on job cards

TIER 2 FEATURES
[ ] Dream Company - All tests passed
    - Readiness % calculated
    - Next steps listed
    
[ ] Prep Vault - All tests passed
    - Experiences created
    - TPO approval works
    - Shows in vault

TIER 3 FEATURES
[ ] TPO Export - All tests passed
    - Excel generated
    - Data complete

INTEGRATION
[ ] Complete student journey works end-to-end

ISSUES FOUND:
_________________________________
_________________________________

STATUS: ☐ Ready to Deploy  ☐ Needs Fixes
```

---

## 🚀 PRODUCTION CHECKLIST

Before deploying to production:

- [ ] All tests passed ✅
- [ ] No console errors
- [ ] Database backed up
- [ ] Migrations tested on fresh database
- [ ] User documentation created
- [ ] Admin trained on new features
- [ ] Rollback plan prepared

---

**Happy testing! Let me know if you find any issues.** 🧪✨
