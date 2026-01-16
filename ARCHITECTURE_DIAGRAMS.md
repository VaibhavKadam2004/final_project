# 🎨 RBAC System Architecture & Visual Diagrams

## 1. Role Hierarchy & Permissions

```
┌─────────────────────────────────────────────────────────────────┐
│                    RBAC Permission Model                        │
└─────────────────────────────────────────────────────────────────┘

                          ROOT SYSTEM
                               │
                ┌──────────────┼──────────────┐
                │              │              │
           STUDENT        RECRUITER          TPO
              │              │               │
              │              │               │
        ┌─────┴────┐    ┌────┴─────┐   ┌────┴────┐
        │           │    │          │   │         │
    View Own    Apply  Post Jobs  Accept   Full
    Apps        Jobs   View Apps  Reject  Access
                      Schedule    Verify
                      Interviews  Approve
                                  Block
```

---

## 2. Data Access by Role

```
                    DATA LAYER
              ┌─────────────────┐
              │  All System Data│
              └────────┬────────┘
                       │
        ┌──────────────┼──────────────┐
        │              │              │
     STUDENTS      RECRUITERS        TPO
        │              │              │
        ▼              ▼              ▼
   Own Data Only  Their Jobs     All Data
   (filtered by   (filtered by   (complete
    student_id)   posted_by)     access)
   
   Cannot see:    Cannot see:    Can see:
   ✗ Other        ✗ Other        ✓ Everything
     students       recruiters's  ✓ All students
   ✗ Other        ✗ All students ✓ All recruiters
     students's    ✗ All jobs    ✓ All jobs
     resumes                      ✓ All applications
```

---

## 3. Application Workflow with RBAC Enforcement

```
┌─────────────────────────────────────────────────────────────┐
│         COMPLETE JOB APPLICATION FLOW                       │
└─────────────────────────────────────────────────────────────┘

RECRUITER POSTS JOB:
    Post Job Request
        ↓
    [Is Authenticated?] ──NO──→ Redirect to Login
        │ YES
        ↓
    [Is Recruiter?] ──NO──→ 403 Forbidden
        │ YES
        ↓
    [Approved by TPO?] ──NO──→ 403 Forbidden (Awaiting Approval)
        │ YES
        ↓
    [Blocked by TPO?] ──YES──→ 403 Forbidden (Blocked)
        │ NO
        ↓
    [Job Data Valid?] ──NO──→ 400 Bad Request
        │ YES
        ↓
    ✅ Job Posted
        │
        └─→ Audit Log: "Recruiter X posted job Y"


STUDENT APPLIES FOR JOB:
    Apply Request
        ↓
    [Is Authenticated?] ──NO──→ Redirect to Login
        │ YES
        ↓
    [Is Student?] ──NO──→ 403 Forbidden
        │ YES
        ↓
    [Has Profile?] ──NO──→ 400 Bad Request
        │ YES
        ↓
    [Is Verified?] ──NO──→ 403 Forbidden (Verify First)
        │ YES
        ↓
    [Is Blacklisted?] ──YES──→ 403 Forbidden (Blacklisted)
        │ NO
        ↓
    [CGPA Eligible?] ──NO──→ 403 Forbidden (Low CGPA)
        │ YES
        ↓
    [Backlogs Eligible?] ──NO──→ 403 Forbidden (Too Many Backlogs)
        │ YES
        ↓
    [Deadline Passed?] ──YES──→ 400 Bad Request (Deadline Passed)
        │ NO
        ↓
    [Job Still Open?] ──NO──→ 403 Forbidden (Job Closed)
        │ YES
        ↓
    [Already Applied?] ──YES──→ 400 Bad Request (Duplicate)
        │ NO
        ↓
    ✅ Application Created
        │
        └─→ Audit Log: "Student X applied to Job Y"


RECRUITER SHORTLISTS STUDENT:
    Shortlist Request
        ↓
    [Is Authenticated?] ──NO──→ Redirect to Login
        │ YES
        ↓
    [Is Recruiter?] ──NO──→ 403 Forbidden
        │ YES
        ↓
    [Own This Job?] ──NO──→ 403 Forbidden
        │ YES
        ↓
    [App Still Open?] ──NO──→ 403 Forbidden (App Closed)
        │ YES
        ↓
    [Job Still Open?] ──NO──→ 403 Forbidden (Job Closed)
        │ YES
        ↓
    ✅ Status Updated to Shortlisted
        │
        └─→ Audit Log: "Recruiter X changed App Status"


TPO VERIFIES STUDENT:
    Verify Request
        ↓
    [Is Authenticated?] ──NO──→ Redirect to Login
        │ YES
        ↓
    [Is TPO?] ──NO──→ 403 Forbidden
        │ YES
        ↓
    ✅ Student Verified
        │
        └─→ Profile Lock: Student Data Now Read-Only (Academic Fields)
        └─→ Audit Log: "TPO verified Student X"
```

---

## 4. Permission Decision Tree (Student Applying)

```
                        START: APPLY FOR JOB
                              │
                              ▼
                    ┌─────────────────────┐
                    │ Authentication Check│
                    │ logged_in = True?   │
                    └─────────┬─────────┬─┘
                        YES  │         │ NO
                            ▼         ▼
                        CONTINUE   REDIRECT
                            │      (login)
                            ▼
                    ┌─────────────────────┐
                    │ Role Check          │
                    │ role == STUDENT?    │
                    └─────────┬─────────┬─┘
                        YES  │         │ NO
                            ▼         ▼
                        CONTINUE   403 ERROR
                            │      (Forbidden)
                            ▼
                    ┌─────────────────────┐
                    │ Profile Check       │
                    │ profile exists?     │
                    └─────────┬─────────┬─┘
                        YES  │         │ NO
                            ▼         ▼
                        CONTINUE   400 ERROR
                            │      (Profile Required)
                            ▼
                    ┌─────────────────────┐
                    │ Verification Check  │
                    │ is_verified = True? │
                    └─────────┬─────────┬─┘
                        YES  │         │ NO
                            ▼         ▼
                        CONTINUE   403 ERROR
                            │      (Not Verified)
                            ▼
                    ┌─────────────────────┐
                    │ Blacklist Check     │
                    │ is_blacklisted=False│
                    └─────────┬─────────┬─┘
                        YES  │         │ NO
                            ▼         ▼
                        CONTINUE   403 ERROR
                            │      (Blacklisted)
                            ▼
                    ┌─────────────────────┐
                    │ CGPA Check          │
                    │ cgpa >= min_cgpa?   │
                    └─────────┬─────────┬─┘
                        YES  │         │ NO
                            ▼         ▼
                        CONTINUE   403 ERROR
                            │      (Low CGPA)
                            ▼
                    ┌─────────────────────┐
                    │ Backlog Check       │
                    │ backlogs≤max_limit? │
                    └─────────┬─────────┬─┘
                        YES  │         │ NO
                            ▼         ▼
                        CONTINUE   403 ERROR
                            │      (Many Backlogs)
                            ▼
                    ┌─────────────────────┐
                    │ Deadline Check      │
                    │ now <= deadline?    │
                    └─────────┬─────────┬─┘
                        YES  │         │ NO
                            ▼         ▼
                        CONTINUE   400 ERROR
                            │      (Expired)
                            ▼
                    ┌─────────────────────┐
                    │ Job Status Check    │
                    │ status == OPEN?     │
                    └─────────┬─────────┬─┘
                        YES  │         │ NO
                            ▼         ▼
                        CONTINUE   403 ERROR
                            │      (Job Closed)
                            ▼
                    ┌─────────────────────┐
                    │ Duplicate Check     │
                    │ not already applied?│
                    └─────────┬─────────┬─┘
                        YES  │         │ NO
                            ▼         ▼
                        CONTINUE   400 ERROR
                            │      (Already Applied)
                            ▼
                    ┌─────────────────────┐
                    │ ✅ APPLICATION      │
                    │    CREATED          │
                    └─────────┬───────────┘
                              │
                              ▼
                    ┌─────────────────────┐
                    │ Log to Audit Trail  │
                    │ (user, timestamp)   │
                    └─────────────────────┘
```

---

## 5. Data Isolation Architecture

```
┌──────────────────────────────────────────────────────────────┐
│                    DATABASE                                  │
│                                                              │
│  ┌───────────────┐  ┌───────────────┐  ┌───────────────┐   │
│  │ StudentProfile│  │ RecruiterProf │  │   JobPost     │   │
│  │               │  │               │  │               │   │
│  │ User 1        │  │ Company A     │  │ Job 1 (CompA) │   │
│  │ - CGPA: 3.5   │  │ - Approved    │  │ Job 2 (CompA) │   │
│  │ - Verified    │  │               │  │ Job 3 (CompB) │   │
│  │               │  │ Company B     │  │               │   │
│  │ User 2        │  │ - Blocked     │  └───────────────┘   │
│  │ - CGPA: 3.2   │  │               │                       │
│  │ - Verified    │  │ TPO           │  ┌───────────────┐   │
│  │               │  │ (Admin)       │  │ Application   │   │
│  │ User 3        │  │               │  │               │   │
│  │ - CGPA: 2.8   │  └───────────────┘  │ App 1: User1→ │   │
│  │ - Blacklisted │                     │ Job1, Pending │   │
│  │               │                     │               │   │
│  └───────────────┘                     │ App 2: User2→ │   │
│                                        │ Job2, Shortl. │   │
│                                        │               │   │
│                                        │ App 3: User1→ │   │
│                                        │ Job3, Rejected│   │
│                                        │               │   │
│                                        └───────────────┘   │
└──────────────────────────────────────────────────────────────┘

                    QUERY FILTERING

┌─────────────┐         ┌──────────────┐         ┌──────────┐
│ Student 1   │         │ Recruiter A  │         │   TPO    │
│  Sees:      │         │  Sees:       │         │  Sees:   │
│ • Own       │         │ • Own jobs   │         │ • All    │
│   Profile   │         │ • Applicants │         │   Users  │
│ • Own Apps  │   AND   │   for own    │   AND   │ • All    │
│             │         │   jobs only  │         │   Data   │
│ Cannot See: │         │ • Cannot see │         │ • All    │
│ ✗ Other     │         │   other      │         │   Jobs   │
│   Students  │         │   recruiters │         │ • All    │
│ ✗ Any Job   │         │   data       │         │   Apps   │
│   Apps      │         │ • Cannot see │         │ • Can    │
│ ✗ Recruiter │         │   all        │         │   verify │
│   Info      │         │   students   │         │ • Can    │
│             │         │              │         │   block  │
└─────────────┘         └──────────────┘         └──────────┘
```

---

## 6. Validation Layers Visualization

```
                    REQUEST ARRIVES
                          │
                          ▼
              ┌────────────────────────┐
              │  LAYER 1: AUTH         │
              │ Is user logged in?     │
              │ .is_authenticated      │
              └────────┬───────┬───────┘
                   YES │       │ NO
                       ▼       ▼
                   CONTINUE  REJECT (401)
                       │
                       ▼
              ┌────────────────────────┐
              │  LAYER 2: ROLE         │
              │ Does role match?       │
              │ @student_only, etc.    │
              └────────┬───────┬───────┘
                   YES │       │ NO
                       ▼       ▼
                   CONTINUE  REJECT (403)
                       │
                       ▼
              ┌────────────────────────┐
              │  LAYER 3: STATUS       │
              │ Verified? Approved?    │
              │ Blacklisted? Blocked?  │
              │ @student_can_apply     │
              └────────┬───────┬───────┘
                   YES │       │ NO
                       ▼       ▼
                   CONTINUE  REJECT (403)
                       │
                       ▼
              ┌────────────────────────┐
              │  LAYER 4: OWNERSHIP    │
              │ Do you own this?       │
              │ job.posted_by==user?   │
              └────────┬───────┬───────┘
                   YES │       │ NO
                       ▼       ▼
                   CONTINUE  REJECT (403)
                       │
                       ▼
              ┌────────────────────────┐
              │  LAYER 5: ELIGIBILITY  │
              │ Meet criteria?         │
              │ CGPA, deadlines, etc.  │
              └────────┬───────┬───────┘
                   YES │       │ NO
                       ▼       ▼
                   CONTINUE  REJECT (400/403)
                       │
                       ▼
              ┌────────────────────────┐
              │  MODEL VALIDATION      │
              │ Business logic check   │
              │ can_change_status()    │
              └────────┬───────┬───────┘
                   YES │       │ NO
                       ▼       ▼
                   CONTINUE  REJECT (403)
                       │
                       ▼
              ┌────────────────────────┐
              │  DATABASE UPDATE       │
              │ Save to database       │
              └────────┬───────────────┘
                       │
                       ▼
              ┌────────────────────────┐
              │  AUDIT LOGGING         │
              │ Log: user, timestamp   │
              │ what changed           │
              └────────┬───────────────┘
                       │
                       ▼
              ┌────────────────────────┐
              │  ✅ SUCCESS            │
              │ Return result to user  │
              └────────────────────────┘
```

---

## 7. Audit Trail Flow

```
                    USER ACTION
                          │
                          ▼
              ┌──────────────────────┐
              │ Check Permissions    │
              └──────────┬───────────┘
                         │
                         ▼
              ┌──────────────────────┐
              │ Perform Action       │
              └──────────┬───────────┘
                         │
                         ▼
          ┌──────────────────────────────┐
          │ CREATE AUDIT LOG ENTRY       │
          │                              │
          │ ✓ User ID: request.user      │
          │ ✓ Action: "Changed Status"   │
          │ ✓ Timestamp: timezone.now()  │
          │ ✓ Old Value: "Pending"       │
          │ ✓ New Value: "Shortlisted"   │
          │ ✓ Note: "Meeting criteria"   │
          │ ✓ IP Address (optional)      │
          │ ✓ User Agent (optional)      │
          └──────────┬───────────────────┘
                     │
                     ▼
         ┌──────────────────────────┐
         │ SAVE TO APPLICATIONSTATUS│
         │ (Immutable Record)       │
         │ Cannot be edited or      │
         │ deleted after creation   │
         └──────────┬───────────────┘
                    │
                    ▼
         ┌──────────────────────────┐
         │ Audit Trail Complete     │
         │ Available for:           │
         │ • TPO Review             │
         │ • Dispute Resolution     │
         │ • Compliance Report      │
         │ • Security Investigation │
         └──────────────────────────┘
```

---

## 8. User Journey Maps

### Student Journey
```
STUDENT JOURNEY:

New User
  │
  ├─→ Register
  │   └─→ Create Profile
  │
  ├─→ Wait for TPO Verification
  │   └─→ TPO reviews and verifies
  │
  ├─→ Search Jobs
  │   └─→ System filters by CGPA/backlogs
  │
  ├─→ Apply
  │   └─→ 10-point validation
  │   └─→ Application Created
  │
  ├─→ Track Status
  │   ├─ Pending
  │   ├─ Shortlisted (get interview invite)
  │   ├─ Selected (got job!)
  │   └─ Rejected
  │
  ├─ Update Resume
  │  └─ Can update any time
  │
  └─ Profile Locked
     └─ Cannot edit CGPA after verification
```

### Recruiter Journey
```
RECRUITER JOURNEY:

New Company
  │
  ├─→ Register Company
  │   └─→ Create RecruiterProfile
  │
  ├─→ Wait for TPO Approval
  │   └─→ TPO reviews and approves
  │
  ├─→ Post Jobs
  │   └─→ Approval check passes
  │   └─→ Job Posted
  │
  ├─→ View Applicants
  │   └─→ See only applicants for their jobs
  │
  ├─→ Shortlist/Reject
  │   ├─ Mark as Shortlisted
  │   ├─ Send interview invite
  │   └─ Mark as Rejected
  │
  ├─→ Schedule Interviews
  │   └─→ Set date, time, location
  │
  ├─→ Download Resumes
  │   └─→ Bulk download as ZIP
  │
  ├─→ Final Status
  │   └─→ Mark as Selected
  │
  └─ Cannot:
     ├─ See other recruiter's data
     ├─ Override TPO decisions
     ├─ Modify closed applications
     └─ Access non-applicants
```

### TPO Journey
```
TPO JOURNEY:

Initial Setup
  │
  ├─→ Create TPO Account
  │   └─→ Set role_type = 'TPO'
  │
  ├─→ Set Eligibility Rules
  │   └─→ Min CGPA, Max Backlogs
  │
  ├─→ Review Students
  │   ├─ Verify profiles
  │   ├─ Blacklist if needed
  │   └─ Lock verified data
  │
  ├─→ Review Recruiters
  │   ├─ Approve companies
  │   ├─ Block if issues
  │   └─ Manage approvals
  │
  ├─→ Monitor Placements
  │   ├─ Track applications
  │   ├─ Monitor status changes
  │   └─ Export reports
  │
  ├─→ Analytics & Reports
  │   ├─ Placement rate
  │   ├─ Average package
  │   ├─ Top recruiters
  │   └─ Excel export
  │
  └─ Cannot:
     ├─ Apply for jobs as student
     ├─ Fake interview results
     ├─ Modify closed applications
     └─ Bypass their own audit logs
```

---

## 9. State Transition Diagram

```
APPLICATION STATE MACHINE:

                    ┌────────────┐
                    │   PENDING  │
                    └──────┬─────┘
                           │
              ┌────────────┼────────────┐
              │            │           │
              ▼            ▼           ▼
        ┌─────────┐  ┌──────────────┐ ┌────────┐
        │REJECTED │  │SHORTLISTED   │ │ CUSTOM │
        └─────────┘  │(Interview1)  │ │ STATUS │
              │      └──────┬───────┘ └────────┘
              │             │
              │    ┌────────┴─────────┐
              │    │                  │
              │    ▼                  ▼
              │ ┌────────┐      ┌──────────┐
              │ │REJECTED│      │  SELECTED│
              │ └────────┘      └──────────┘
              │    │                  │
              └────┼──────────────────┘
                   │
                   ▼ (Close Application)
            ┌────────────┐
            │   CLOSED   │ ← Immutable, Cannot Change
            │ (Locked)   │
            └────────────┘

STATUS CHANGE RULES:
✓ Can change: Pending → Shortlisted
✓ Can change: Pending → Rejected
✓ Can change: Shortlisted → Selected
✓ Can change: Shortlisted → Rejected
✗ Cannot:    Any Status → Any Status (if closed)
✗ Cannot:    Change without permission
✗ Cannot:    If job is closed
```

---

## 10. Complete System Flow

```
┌──────────────────────────────────────────────────────────────┐
│             COMPLETE SYSTEM ARCHITECTURE                     │
└──────────────────────────────────────────────────────────────┘

                    STUDENTS
                   (n=1000s)
                       │
        ┌──────────────┼──────────────┐
        │              │              │
    Register         TPO           Search
        │          Verifies          Jobs
        ▼              │              │
    ┌───────┐          ▼              ▼
    │Profile├─→ ┌──────────┐    ┌──────────┐
    │Create │   │Verified? │    │Job Filter│
    └───────┘   └──────────┘    │by Criteria
                     │           └──────┬──┘
                     ▼                  │
                ┌──────────┐            │
                │Lock Data │            │
                │Save Audit│            │
                └──────────┘            │
                                        ▼
                                   ┌─────────┐
                                   │ Apply   │
                                   │ 10-Point│
                                   │Validation
                                   └────┬────┘
                                        │
                                        ▼
                            ┌──────────────────────┐
                            │ Application Created  │
                            │ Status: Pending      │
                            │ Audit Log Entry      │
                            └──────────┬───────────┘
                                       │
                    ┌──────────────────┼──────────────────┐
                    │                  │                  │
                    ▼                  ▼                  ▼
            ┌──────────────┐   ┌──────────────┐   ┌──────────────┐
            │  RECRUITERS  │   │    EMAIL     │   │    TPO       │
            │(n=100s)      │   │ NOTIFICATION │   │ ANALYTICS    │
            │              │   │              │   │              │
            │ Shortlist    │   │ Job Posted   │   │ Reports      │
            │ Reject       │   │ Shortlisted  │   │ Export Data  │
            │ Schedule     │   │ Selected     │   │ Verify Users │
            │ Interviews   │   │ Rejected     │   │ Blacklist    │
            └──────────────┘   └──────────────┘   └──────────────┘
                    │                  │                  │
                    └──────────────────┼──────────────────┘
                                       │
                                       ▼
                       ┌──────────────────────────┐
                       │   IMMUTABLE AUDIT TRAIL  │
                       │                          │
                       │ ApplicationStatus Table  │
                       │ • Who made change        │
                       │ • When change made       │
                       │ • What status changed to │
                       │ • Why (note)             │
                       │                          │
                       │ Cannot be deleted        │
                       │ Cannot be edited         │
                       │ Complete compliance      │
                       └──────────────────────────┘
```

---

## Summary of Diagrams

1. **Role Hierarchy** - Shows 3 roles and their main permissions
2. **Data Access** - Shows what each role can see
3. **Application Workflow** - Complete flow with RBAC at each step
4. **Decision Tree** - 10-point validation for job applications
5. **Data Isolation** - Query filtering by role
6. **Validation Layers** - 5-layer defense in depth
7. **Audit Trail** - How actions are logged
8. **User Journeys** - Individual role workflows
9. **State Machine** - Application status transitions
10. **System Flow** - Complete architecture overview

**All diagrams show**: Security enforcement at every step, complete audit capability, and strict role separation.
