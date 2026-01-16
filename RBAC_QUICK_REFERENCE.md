# RBAC Quick Reference Guide

## Quick Access Decision Tree

### For Students
```
Endpoint → Is Authenticated? 
    NO → Redirect to login
    YES → Is role_type = STUDENT?
        NO → 403 Forbidden
        YES → Is StudentProfile.is_verified?
            NO → Cannot perform action
            YES → Is StudentProfile.is_blacklisted?
                NO → Check action-specific rules
                YES → 403 Forbidden
```

### For Recruiters
```
Endpoint → Is Authenticated?
    NO → Redirect to login
    YES → Is role_type = RECRUITER?
        NO → 403 Forbidden
        YES → Is RecruiterProfile.is_approved?
            NO → 403 Forbidden (awaiting TPO approval)
            YES → Is RecruiterProfile.is_blocked?
                YES → 403 Forbidden (blocked by TPO)
                NO → Check action-specific rules
```

### For TPO
```
Endpoint → Is Authenticated?
    NO → Redirect to login
    YES → Is role_type = TPO?
        NO → 403 Forbidden
        YES → Grant admin access
```

---

## Decorator Usage

### Protecting Views

```python
# At view level
from accounts.decorators import student_only, recruiter_only, tpo_only

@student_only
def student_dashboard(request):
    # Automatically checks role
    pass

@recruiter_only  
def recruiter_dashboard(request):
    # Automatically checks role and approval
    pass

@tpo_only
def tpo_dashboard(request):
    # Automatically checks role
    pass
```

### Protecting Operations

```python
from accounts.decorators import (
    student_can_apply,
    recruiter_can_post,
    recruiter_can_update_application_status,
    prevent_data_tampering
)

@student_can_apply
def apply_job(request):
    # Checks: verified, not blacklisted, profile complete, eligible
    pass

@recruiter_can_post
def post_job(request):
    # Checks: approved by TPO, not blocked
    pass

@recruiter_can_update_application_status
def update_status(request):
    # Checks: owns job, app not closed, job still open
    pass

@prevent_data_tampering
def modify_application(request):
    # Blocks: if application is closed
    pass
```

---

## Common Query Patterns

### Students Can Only See Their Own Applications
```python
# Correct
apps = Application.objects.filter(student=request.user)

# Wrong (leaks other students' data)
apps = Application.objects.all()
```

### Recruiters Can Only See Their Posted Jobs
```python
# Correct
jobs = JobPost.objects.filter(posted_by=request.user)

# Wrong (leaks other recruiters' jobs)
jobs = JobPost.objects.all()
```

### Recruiters Can Only Update Their Own Applications
```python
# Always verify ownership
job = app.job
if job.posted_by != request.user:
    return HttpResponseForbidden("You can only update your own applications")
```

### Prevent Modification of Closed Applications
```python
# Always check before updating
if application.is_closed:
    raise PermissionError("Cannot modify closed applications")
```

---

## Field Access Restrictions

### Student-Level Restrictions
| Field | Before Verification | After Verification |
|-------|:-----------------:|:-----------------:|
| cgpa | ✏️ Editable | 🔒 Read-only |
| active_backlogs | ✏️ Editable | 🔒 Read-only |
| 10th percent | ✏️ Editable | 🔒 Read-only |
| 12th percent | ✏️ Editable | 🔒 Read-only |
| resume | ✏️ Editable | ✏️ Can Update |
| skills | ✏️ Editable | ✏️ Editable |

### Implementation
```python
if profile.is_verified:
    protected_fields = ['cgpa', 'active_backlogs']
    if any(field in request.POST for field in protected_fields):
        raise PermissionError("Cannot modify verified data")
```

---

## Status Update Rules

### Who Can Update?
- Only recruiter who posted the job
- Not after application is closed
- Not after job posting is closed

### Allowed Status Transitions
```
Pending   → Shortlisted (recruiter)
Pending   → Rejected (recruiter)
Shortlisted → Selected (recruiter)
Shortlisted → Rejected (recruiter)
```

### Preventing Unauthorized Updates
```python
# Model validation
def can_change_status(self, user):
    if self.is_closed:
        return False, "Application is closed"
    if self.job.posted_by != user:
        return False, "You don't own this job"
    if self.job.status == JobPost.STATUS_CLOSED:
        return False, "Job posting is closed"
    return True, ""

# View usage
can_change, msg = application.can_change_status(request.user)
if not can_change:
    return JsonResponse({'error': msg}, status=403)
```

---

## Audit Trail

### What Gets Logged
- **StudentProfile**: verified_by, verified_at
- **RecruiterProfile**: approved_by, approved_at
- **ApplicationStatus**: updated_by, timestamp, note
- **Application**: is_closed, closed_at

### Querying Audit Trail
```python
# See all status changes for an application
history = app.status_history.all()  # Ordered by timestamp

# See who verified a student
student_profile.verified_by  # TPO user
student_profile.verified_at  # DateTime

# See who approved a recruiter
recruiter_profile.approved_by  # TPO user
recruiter_profile.approved_at  # DateTime
```

---

## Security Checklist

Before deploying any new endpoint:

- [ ] Is authentication checked? (@login_required or mixin)
- [ ] Is role validated? (@student_only, @recruiter_only, @tpo_only)
- [ ] Are ownership checks done? (job.posted_by == request.user)
- [ ] Are closed applications locked? (prevent_data_tampering)
- [ ] Are query filters applied? (filter by request.user)
- [ ] Is sensitive data protected? (no leaking student/job data)
- [ ] Are error messages generic? (don't reveal system details)
- [ ] Is the action audited? (logged with user/timestamp)

---

## Common Mistakes & Fixes

### ❌ Mistake 1: Leaking Student Data
```python
# WRONG - Returns all students
students = StudentProfile.objects.all()

# CORRECT - Only if TPO
if request.user.is_tpo:
    students = StudentProfile.objects.all()
```

### ❌ Mistake 2: Allowing Modifications on Closed Apps
```python
# WRONG - No check for closed status
def update_status(request, app_id):
    app = Application.objects.get(pk=app_id)
    app.status = request.POST['status']
    app.save()

# CORRECT - Check is_closed
def update_status(request, app_id):
    app = Application.objects.get(pk=app_id)
    if app.is_closed:
        raise PermissionError("Cannot modify closed applications")
    app.status = request.POST['status']
    app.save()
```

### ❌ Mistake 3: Trusting Frontend for Authorization
```python
# WRONG - User can change role_type in form
user.role_type = request.POST.get('role_type')

# CORRECT - Set role_type server-side
if request.POST.get('register_type') == 'student':
    user.role_type = CustomUser.STUDENT
```

### ❌ Mistake 4: Missing Ownership Validation
```python
# WRONG - Any recruiter can update any application
app.status = request.POST['status']
app.save()

# CORRECT - Verify recruiter owns the job
if app.job.posted_by != request.user:
    raise PermissionError("Not your job")
```

---

## Testing RBAC

### Unit Test Template
```python
from django.test import TestCase, Client
from django.contrib.auth import get_user_model

User = get_user_model()

class StudentRBACTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.student = User.objects.create_user(
            username='student1',
            password='pass123',
            role_type=User.STUDENT
        )
        self.recruiter = User.objects.create_user(
            username='recruiter1',
            password='pass123',
            role_type=User.RECRUITER
        )
    
    def test_student_cannot_access_recruiter_dashboard(self):
        self.client.login(username='student1', password='pass123')
        response = self.client.get('/recruiter/dashboard/')
        self.assertEqual(response.status_code, 403)
    
    def test_student_cannot_see_other_student_apps(self):
        # Create another student
        student2 = User.objects.create_user(
            username='student2',
            password='pass123',
            role_type=User.STUDENT
        )
        # Login as student1
        self.client.login(username='student1', password='pass123')
        # Try to access student2's application (should fail)
        response = self.client.get(f'/applications/{student2.id}/')
        self.assertEqual(response.status_code, 403)
```

---

## API Response Codes

| Code | Meaning | When to Use |
|------|---------|-----------|
| 200 | OK | Successful operation |
| 400 | Bad Request | Missing/invalid data |
| 401 | Unauthorized | Not authenticated |
| 403 | Forbidden | Authenticated but no permission |
| 404 | Not Found | Resource doesn't exist |

---

## Performance Notes

### Indexed Queries (for performance)
```python
# These queries are indexed:
JobPost.objects.filter(status='Open', deadline__gte=now)
Application.objects.filter(student_id=X, status__in=statuses)
Application.objects.filter(job_id=X, status='Shortlisted')
```

### Use select_related for JOINs
```python
# SLOW - N+1 queries
apps = Application.objects.all()
for app in apps:
    print(app.student.username)  # Extra query per app

# FAST - Single query
apps = Application.objects.select_related('student', 'job')
for app in apps:
    print(app.student.username)  # No extra queries
```

---

## Role Transition Rules

Students/Recruiters CANNOT change their own role:
```
✅ Student  → (Fixed)
✅ Recruiter → (Fixed)
✅ TPO → (Fixed, set during user creation)
```

Only admins can change roles via Django management commands.

---

## Summary Flowchart

```
User Request
    ↓
[Authentication Check]
    ├─ Not logged in? → Redirect to login
    └─ Logged in? → Continue
    ↓
[Role Check]
    ├─ Wrong role? → 403 Forbidden
    └─ Correct role? → Continue
    ↓
[Status Check]
    ├─ Student blacklisted? → 403 Forbidden
    ├─ Recruiter blocked? → 403 Forbidden
    └─ Verified/Approved? → Continue
    ↓
[Ownership Check]
    ├─ Own the resource? → Continue
    └─ Don't own it? → 403 Forbidden
    ↓
[Data Validation]
    ├─ Data valid? → Continue
    └─ Invalid? → 400 Bad Request
    ↓
[Execute Action]
    ↓
[Log to Audit Trail]
    ↓
[Return Success]
```

---

**Last Updated**: January 2026
**System Version**: 1.0
**Security Level**: High
