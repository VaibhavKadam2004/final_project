# Role-Based Access Control (RBAC) Implementation
## Smart Internship & Placement Portal

---

## Overview
This document describes the comprehensive RBAC system implemented in the placement portal. The system enforces strict access controls to ensure data security and process integrity across three primary roles: **Student**, **Recruiter**, and **TPO**.

---

## 1. STUDENT ROLE

### Allowed Operations ✅

#### 1.1 Register & Profile Building
- **View**: `student_register()`
- **Model**: `StudentProfile`
- **What they can do**:
  - Create account with username, email, password
  - Fill in academic details (10th %, 12th %, Branch, Skills)
  - Upload resume (PDF/DOC format)
  
#### 1.2 Resume Upload & Management
- **View**: `student_profile_view()`
- **What they can do**:
  - Upload initial resume
  - Update resume before TPO verification
  - Modify educational details before verification
  
#### 1.3 Search & Apply for Jobs
- **View**: `ApplyJobView`, `JobListView`, `JobDetailView`
- **Decorator**: `@student_can_apply`
- **What they can do**:
  - View eligible jobs (filtered by CGPA/backlogs)
  - Apply for jobs matching their criteria
  - View application status in real-time
  
#### 1.4 Track Application Status
- **View**: `StudentApplicationDetailView`, `student_dashboard`
- **What they can do**:
  - See application status updates (Pending → Shortlisted → Selected)
  - View interview schedules
  - Check rejection/acceptance status
  
#### 1.5 Receive Notifications
- **Mechanism**: Via Django signals and email
- **When they receive notifications**:
  - New job postings (matching criteria)
  - Shortlist notifications
  - Interview schedule confirmations
  - Final selection/rejection

---

### Restricted Operations ❌

#### 1.6 Cannot Edit Core Eligibility After TPO Verification
- **Protection**: Model validation in `student_profile_view()`
- **Protected fields**: `cgpa`, `active_backlogs`, `tenth_percent`, `twelfth_percent`
- **Why**: Ensures integrity - student cannot artificially inflate qualifications
- **Error message**: "Cannot modify academic details after TPO verification"

```python
if profile.is_verified:
    protected_fields = ['cgpa', 'active_backlogs', 'tenth_percent', 'twelfth_percent']
    # These fields are read-only after verification
```

#### 1.7 Cannot View Other Students
- **Protection**: Model queries filtered by `student=request.user`
- **Application filter**: `Application.objects.filter(student=self.request.user)`
- **Prevents**: Students cannot see peer profiles, resumes, or application history

#### 1.8 Cannot Post Jobs
- **Protection**: `recruiter_only` decorator
- **View restriction**: Only users with `role_type=RECRUITER` can access job creation
- **Error**: "Only recruiters can post jobs"

#### 1.9 Cannot Manually Change Application Status
- **Protection**: `can_change_status()` method in Application model
- **Restriction**: Only recruiter who posted the job can change status
- **Error**: "Only the recruiter who posted the job can update status"

#### 1.10 Cannot Contact HR Until Shortlisted
- **Protection**: Contact info only visible to shortlisted candidates
- **Implementation**: Template conditional rendering
- **Logic**: Only show recruiter contact if `status=SHORTLISTED`

---

## 2. RECRUITER ROLE

### Allowed Operations ✅

#### 2.1 Post Opportunities
- **View**: `JobCreateView`
- **Decorator**: `@recruiter_can_post`
- **What they can do**:
  - Create job/internship postings
  - Set eligibility criteria (min CGPA, max backlogs)
  - Define job type (Full-time, Internship, PPO)
  - Set application deadline
  
**Prerequisites**:
  - Must have `RecruiterProfile.is_approved=True`
  - Must NOT be blocked by TPO

#### 2.2 Filter & Shortlist Candidates
- **View**: `ApplicationShortlistView`
- **Decorator**: `@recruiter_can_update_application_status`
- **What they can do**:
  - View all applicants for their jobs
  - Access resumes of applicants
  - Shortlist candidates (mark as `SHORTLISTED`)
  - Reject candidates (mark as `REJECTED`)

#### 2.3 Schedule Interviews
- **View**: `ScheduleInterviewView`
- **Model**: `InterviewSchedule`
- **What they can do**:
  - Create interview rounds (Round 1, 2, 3, HR, Final)
  - Set interview date/time
  - Add interview location or online link
  - Add interviewer notes

#### 2.4 Update Results
- **View**: `ApplicationShortlistView`
- **Status flow**: `Pending` → `Shortlisted` → `Selected/Rejected`
- **What they can do**:
  - Mark student as "Selected" after final round
  - Mark student as "Rejected" at any stage
  - Add notes to status updates

---

### Restricted Operations ❌

#### 2.5 Cannot Access All Student Data
- **Protection**: Query filtering
- **Implementation**: 
```python
applications = Application.objects.filter(job__posted_by=request.user)
```
- **Restriction**: Can only see students who applied to THEIR jobs
- **Prevents**: Cannot browse all student profiles or resumes

#### 2.6 Cannot See Students Who Haven't Applied
- **Query**: Only applicants appear in recruiter's view
- **Protection**: Direct access to student profile forbidden
- **Error**: 403 Forbidden if trying to access other recruiters' candidates

#### 2.7 Cannot Modify College Data
- **Protection**: No access to `EligibilityRule` or student profile fields
- **Restriction**: Read-only access to student academic details
- **Prevents**: Cannot change CGPA, backlogs, grades, or college settings

#### 2.8 Cannot Approve Other Companies
- **Protection**: `tpo_only` decorator
- **Restricts**: Recruiter cannot approve/block other recruiters
- **Only TPO can**: Manage recruiter approvals

#### 2.9 Cannot Override TPO Decisions
- **Protection**: Automatic filtering in `ApplyJobView`
```python
if profile.is_blacklisted:
    return JsonResponse({'error': 'You are blacklisted'}, status=403)
```
- **Restriction**: Cannot bypass TPO blacklist or block decisions
- **Enforcement**: Students blacklisted by TPO cannot apply to any job

#### 2.10 Cannot Modify Closed Applications
- **Protection**: `prevent_data_tampering` decorator
```python
if application.is_closed:
    return JsonResponse({'error': 'Cannot modify closed applications'}, status=403)
```
- **Prevents**: No status updates on closed/finalized applications

---

## 3. TPO / ADMIN ROLE

### Allowed Operations ✅

#### 3.1 Verify Student Data
- **View**: `verify_student()`
- **Decorator**: `@tpo_only`
- **What they can do**:
  - Review student profiles
  - Verify academic credentials (marks, transcripts)
  - Set `StudentProfile.is_verified=True`
  - Lock verified data from student editing

#### 3.2 Manage Recruiters
- **Views**: `approve_recruiter()`, `block_recruiter()`
- **Decorators**: `@tpo_only`
- **What they can do**:
  - Review recruiter registration
  - Approve companies to post jobs (`RecruiterProfile.is_approved=True`)
  - Block recruiters for malpractice (`RecruiterProfile.is_blocked=True`)
  - Add blocking reasons (audit trail)

#### 3.3 Handle Eligibility
- **Model**: `EligibilityRule`
- **What they can do**:
  - Set global minimum CGPA requirement
  - Set maximum active backlog limit
  - Create multiple eligibility rules for different batches
  - Enable/disable rules as needed

#### 3.4 Analytics & Reports
- **View**: `TPODashboardView`, `placement_stats()`
- **What they can do**:
  - Generate placement statistics
  - Calculate average package
  - View top recruiters (by placements)
  - Export placed students to Excel
  - Track placement percentage

#### 3.5 Communication Hub
- **Mechanism**: Bulk email system (future feature)
- **What they can do**:
  - Send bulk notifications to all students
  - Send targeted emails to specific batches
  - Schedule interview reminders
  - Announce placement updates

#### 3.6 Apply Global Rules
- **Model**: `EligibilityRule`
- **What they can do**:
  - Block students with >1 active backlog from applying
  - Require minimum CGPA for all placements
  - Override individual job eligibility if needed

---

### Restricted Operations ❌

#### 3.7 Cannot Apply for Jobs
- **Protection**: `is_student` check
- **Restriction**: TPO cannot enter student applicant flow
- **Why**: Prevents conflicts of interest and ensures impartiality

#### 3.8 Cannot Fake Interview Results
- **Protection**: Immutable audit trail in `ApplicationStatus`
- **Restriction**: Cannot manually create false "Selected" records
- **Integrity**: All status changes logged with timestamp and updater
- **Audit**: Complete history prevents tampering

#### 3.9 Cannot Bypass Data Validation
- **Protection**: All operations go through models/views
- **Restriction**: No direct SQL access allowed
- **Why**: Maintains data integrity and audit trails

---

## 4. FORBIDDEN OPERATIONS (System-wide Security)

These operations are **blocked for ALL users** regardless of role:

### 4.1 Database Access - No Direct SQL
- **Prevention**: No raw SQL queries allowed
- **Enforcement**: Only ORM access through Django models
- **Why**: Prevents data corruption and maintains audit trail
- **Error**: Database access restricted at settings level

### 4.2 Identity Theft - Cannot Login As Another User
- **Protection**: `prevent_identity_theft` decorator
- **Exception**: TPO has optional "Login As" feature for support only
- **Implementation**:
```python
if str(request.user.id) != str(target_user_id):
    return JsonResponse({'error': 'You can only view your own data'}, status=403)
```

### 4.3 Data Tampering - Cannot Modify Closed Applications
- **Protection**: `prevent_data_tampering` decorator
- **Implementation**: Once `application.is_closed=True`, no modifications allowed
- **Enforcement**: Blocks POST, PUT, PATCH, DELETE on closed applications
- **Audit**: Enables TPO to review final application state without changes
- **Error Message**: "Cannot modify closed applications. Data is locked for audit purposes."

---

## 5. IMPLEMENTATION DETAILS

### 5.1 Decorators Overview

```
accounts/decorators.py contains:

ROLE-BASED DECORATORS:
- @student_only        → Only authenticated students
- @recruiter_only      → Only authenticated recruiters
- @tpo_only           → Only authenticated TPO

PERMISSION DECORATORS:
- @student_can_apply   → Checks verification, blacklist, profile
- @recruiter_can_post  → Checks approval, not blocked
- @recruiter_can_update_application_status → Checks ownership, not closed
- @student_cannot_modify_verified_data → Locks fields after verification
- @tpo_can_verify_student → TPO only
- @tpo_can_manage_recruiter → TPO only

SECURITY DECORATORS:
- @prevent_identity_theft → Block impersonation
- @prevent_data_tampering → Lock closed applications
```

### 5.2 Models Enhancement

#### CustomUser
```python
role_type: Student | Recruiter | TPO
is_student: @property
is_recruiter: @property
is_tpo: @property
```

#### StudentProfile (New Fields)
```python
is_verified: Boolean (TPO verification)
is_blacklisted: Boolean (TPO blacklist)
blacklist_reason: TextField
verified_by: ForeignKey → CustomUser (TPO)
verified_at: DateTime
```

#### RecruiterProfile (New)
```python
company_name: String
company_email: Email
company_website: URL
is_approved: Boolean (TPO approval required)
is_blocked: Boolean (TPO can block)
approved_by: ForeignKey → CustomUser (TPO)
approved_at: DateTime
blocked_reason: TextField
can_post_jobs(): Boolean method
```

#### EligibilityRule (New)
```python
name: String
min_cgpa: Decimal
max_active_backlogs: Integer
is_active: Boolean
created_by: ForeignKey → CustomUser (TPO)
```

#### JobPost (Enhanced)
```python
status: Open | Closed
created_at: DateTime
updated_at: DateTime
is_open_for_applications(): Boolean method
can_be_closed_by(user): Boolean method
```

#### Application (Enhanced)
```python
is_closed: Boolean (locks from modifications)
closed_at: DateTime
can_change_status(user): (Boolean, message) method
close_application(): locks application
add_status(new_status, user, note): updates with validation
```

#### ApplicationStatus (Enhanced)
```python
updated_by: ForeignKey → CustomUser (who made change)
# Immutable audit trail - created via add_status()
```

#### InterviewSchedule (New)
```python
application: ForeignKey
round: Round 1 | 2 | 3 | HR | Final
scheduled_date: DateTime
location: String
interviewer_notes: TextField
created_by: ForeignKey → CustomUser (Recruiter)
```

### 5.3 View-Level Access Control

#### Mixins Used:
```python
class StudentRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    - Ensures only students access the view
    - Returns 403 on unauthorized access

class RecruiterRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    - Ensures only recruiters (must be approved) access the view
    
class TPORequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    - Ensures only TPO users access admin views
```

### 5.4 Validation Layers

```
Request → Authentication → Authorization (Decorator/Mixin) → 
View Logic → Model Validation → Database Operation
```

**Example Flow for Job Application:**

1. **Authentication**: Is user logged in?
2. **Authorization**: Is user a student? (@student_only decorator)
3. **Profile Check**: Does student have complete profile?
4. **Verification Check**: Is profile verified by TPO?
5. **Blacklist Check**: Is student blacklisted?
6. **Eligibility Check**: Does student meet job criteria?
7. **Deadline Check**: Is deadline not passed?
8. **Job Status Check**: Is job still open?
9. **Duplicate Check**: Already applied?
10. **Save Application**: If all checks pass

---

## 6. SECURITY BEST PRACTICES IMPLEMENTED

✅ **Defense in Depth**: Multiple layers of validation
✅ **Immutable Audit Trail**: All changes logged with timestamps
✅ **Fail Secure**: Default deny, explicit allow
✅ **Principle of Least Privilege**: Users get minimum necessary access
✅ **Separation of Duties**: Different roles have distinct responsibilities
✅ **Data Integrity**: Core data locked after verification
✅ **Tamper Detection**: Closed applications prevent modification
✅ **Access Logging**: Track who made changes and when

---

## 7. MIGRATION STEPS

After implementing these changes, run:

```bash
# Create migrations for new models
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Create a TPO user (superuser)
python manage.py createsuperuser

# Set role_type to 'TPO' for admin user
# Then access admin panel to manage system
```

---

## 8. TESTING CHECKLIST

### Student Role Tests
- [ ] Cannot register as recruiter or TPO
- [ ] Cannot see other student profiles
- [ ] Cannot apply after blacklisting
- [ ] Cannot change CGPA after TPO verification
- [ ] Can only view their own applications
- [ ] Cannot manually change application status

### Recruiter Role Tests
- [ ] Cannot post jobs until TPO approval
- [ ] Cannot see candidates from other recruiters
- [ ] Cannot access all student data
- [ ] Cannot unblock themselves if TPO blocks them
- [ ] Cannot update closed applications
- [ ] Can only update applications for their jobs

### TPO Role Tests
- [ ] Can verify student profiles
- [ ] Can blacklist students (prevents all applications)
- [ ] Can approve/block recruiters
- [ ] Can access all analytics
- [ ] Can export placement reports
- [ ] Cannot apply for jobs themselves

### System Security Tests
- [ ] No SQL injection possible
- [ ] Cannot impersonate other users
- [ ] Cannot modify closed applications
- [ ] All status changes are audited
- [ ] Decorators properly block unauthorized access

---

## 9. ERROR CODES & MESSAGES

| Code | Message | When |
|------|---------|------|
| 400 | Profile incomplete | Student missing CGPA/backlogs |
| 401 | Unauthorized | Not logged in or wrong role |
| 403 | Access Denied | Insufficient permissions |
| 403 | Cannot modify closed applications | Application is_closed=True |
| 403 | You are blacklisted | StudentProfile.is_blacklisted=True |
| 403 | Profile not verified | StudentProfile.is_verified=False |
| 403 | Company must be approved | RecruiterProfile.is_approved=False |
| 403 | Account is blocked | RecruiterProfile.is_blocked=True |

---

## 10. AUDIT TRAIL

Every important action is logged:

```python
ApplicationStatus: 
- application_id
- old_status → new_status
- timestamp
- updated_by (recruiter)
- note (reason)

StudentProfile.verified_at, verified_by
RecruiterProfile.approved_at, approved_by
```

This enables full compliance auditing and dispute resolution.

---

## Summary

The RBAC system is designed with **security, integrity, and accountability** as core principles:

- **Students** have limited, role-appropriate access while being protected from unauthorized data access
- **Recruiters** can manage their jobs and candidates while respecting TPO oversight
- **TPO** has administrative privileges with complete audit capabilities
- **System-wide protections** prevent tampering and ensure data integrity

All validations occur at multiple levels to prevent bypass attempts.
