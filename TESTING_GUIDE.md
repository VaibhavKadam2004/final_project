# End-to-End Testing Guide - Smart Internship & Placement Portal

## Overview
This guide provides comprehensive testing scenarios for all three user roles in the system: Students, Recruiters, and TPO.

---

## Part 1: Student Journey Testing

### 1.1 Student Registration
**Test Case: ST-001 - Successful Student Registration**
```
Precondition: Browser at http://127.0.0.1:8000/
Steps:
1. Click "Register (Student)" link
2. Fill form:
   - First Name: Aditya
   - Last Name: Singh
   - Email: aditya@student.com
   - Username: aditya_singh
   - Password: SecurePass@123
   - Roll Number: CS001
   - Branch: CS/IT
   - 10th %: 88.5
   - 12th %: 92.0
   - Upload Resume: [Select PDF file]
   - Skills: Python, Java, DSA
3. Click "Create Account"

Expected Results:
✓ Account created successfully
✓ Message: "Registration successful! Please complete your profile."
✓ Redirected to student dashboard
✓ StudentProfile object created in database
✓ Resume file uploaded to media/resumes/

Pass/Fail: _____
```

### 1.2 Student Profile Viewing
**Test Case: ST-002 - View Student Profile**
```
Precondition: Student logged in, viewing dashboard
Steps:
1. Observe "Academic Profile" card showing:
   - Roll No: CS001
   - Branch: CS/IT
   - CGPA: (empty until TPO verifies)
   - Active Backlogs: 0

2. Observe "Verification Status" card showing:
   - Status: ⏳ Pending Verification
   - Message: "Awaiting TPO verification"

3. Click [Edit Profile] button
4. Verify uneditable fields after verification

Expected Results:
✓ All profile fields display correctly
✓ Verification status shows correct state
✓ Edit profile button is accessible

Pass/Fail: _____
```

### 1.3 Browse Jobs with Eligibility Filtering
**Test Case: ST-003 - View Eligible Jobs**
```
Precondition: Student logged in, TPO has verified profile with CGPA: 3.8
Steps:
1. Click "Browse Jobs" in sidebar
2. Observe job cards displaying:
   - Company & Job Title
   - Job Type (Full-time/Internship/PPO)
   - Package range
   - Requirements (CGPA, Backlogs, Branch)
   - Eligibility status: ✓ "You are eligible"

3. Use filters:
   - CGPA Required: 3.5 → See filtered results
   - Backlogs: 0 → See filtered results
   - Package Range: 5-10 LPA → See filtered results

4. Find ineligible job (CGPA requirement: 4.0)
   - Observe eligibility message: "⚠ CGPA requirement not met"
   - Apply button should be disabled

Expected Results:
✓ Only eligible jobs show "Apply" button enabled
✓ Ineligible jobs show warning message
✓ Filters work correctly
✓ Eligibility checks are accurate

Pass/Fail: _____
```

### 1.4 Apply for Job
**Test Case: ST-004 - Submit Job Application**
```
Precondition: Student viewing eligible job, not yet applied
Steps:
1. Click [Apply Now] button on eligible job
2. Confirm application popup appears
3. Click [Confirm] button
4. Observe success message: "Application submitted successfully"

Expected Results:
✓ Application created with status: "Pending"
✓ Cannot apply again for same job
✓ Notification sent to student
✓ Application appears in dashboard
✓ Database record created in Application table

Pass/Fail: _____
```

### 1.5 Track Application Status
**Test Case: ST-005 - Monitor Application Progress**
```
Precondition: Student has applied for job
Steps:
1. Dashboard shows application with status: Pending
2. As recruiter changes status to "Shortlisted"
3. Refresh student dashboard
4. Observe status badge: ⭐ Shortlisted
5. Receive notification: "You have been shortlisted!"

Expected Results:
✓ Status updates reflect in real-time
✓ Correct status badge displays
✓ Notifications are sent
✓ Application history timeline shows all status changes

Pass/Fail: _____
```

### 1.6 View Application Details
**Test Case: ST-006 - Application Detail View**
```
Precondition: Student has applications
Steps:
1. Dashboard → Click [View] on any application
2. Observe detailed view showing:
   - Company info
   - Job details
   - Current status
   - Application date
   - Status history/timeline

Expected Results:
✓ All application details display
✓ Timeline shows all status changes with dates
✓ Interview schedule displays (if scheduled)

Pass/Fail: _____
```

---

## Part 2: Recruiter Journey Testing

### 2.1 Recruiter Registration
**Test Case: RC-001 - Recruiter Registration**
```
Precondition: Browser at recruiter registration page
Steps:
1. Fill registration form:
   - Full Name: Priya Sharma
   - Email: recruiter@tcs.com
   - Password: SecurePass@123
   - Company Name: Tata Consultancy Services
   - Company Email: careers@tcs.com
   - Company Website: www.tcs.com
   - Contact Phone: +91-9876543210

2. Click [Register]

Expected Results:
✓ RecruiterProfile created
✓ Status: "Pending TPO Approval"
✓ Message: "Registration successful! Waiting for TPO approval."
✓ Redirected to recruiter dashboard

Pass/Fail: _____
```

### 2.2 Recruiter Approval by TPO
**Test Case: RC-002 - TPO Approves Recruiter**
```
Precondition: Recruiter registered, awaiting approval
Steps:
1. TPO Dashboard → "Approve Recruiters"
2. See unapproved recruiter in list
3. Click [Approve] button
4. Confirm approval

Expected Results:
✓ Recruiter status changed to: "Approved"
✓ Notification sent to recruiter
✓ Recruiter can now post jobs
✓ Status on recruiter dashboard updates to green: ✓ Approved

Pass/Fail: _____
```

### 2.3 Post a Job
**Test Case: RC-003 - Create Job Posting**
```
Precondition: Recruiter approved and logged in
Steps:
1. Click [Post New Job] button
2. Fill job form:
   - Job Title: Senior Software Engineer
   - Description: [Enter detailed description]
   - Job Type: Full-time
   - Min CGPA: 3.2
   - Max Backlogs: 1
   - Branches: CS, IT, ECE
   - Package: 8.5 LPA
   - Deadline: [Select future date]

3. Click [Post Job]

Expected Results:
✓ Job posted successfully
✓ Message: "Job posting created successfully!"
✓ Job appears in recruiter dashboard
✓ Status: 🟢 Open
✓ Students can view and apply

Pass/Fail: _____
```

### 2.4 Manage Applications
**Test Case: RC-004 - Review & Shortlist Applications**
```
Precondition: Job posted, students applied
Steps:
1. Job Dashboard → View job
2. Observe applications list with:
   - Candidate name
   - CGPA
   - Backlogs
   - Branch
   - Status: Pending

3. For promising candidate:
   - Click ★ (Shortlist button)
   - Change status to: "Shortlisted"
   - Observe status badge changes to ⭐

4. For another candidate:
   - Click ✓ (Select button)
   - Change status to: "Selected"
   - Observe status badge changes to ✓

Expected Results:
✓ Status changes update database
✓ Student receives notifications
✓ Status badges display correctly
✓ Audit trail records who made change and when

Pass/Fail: _____
```

### 2.5 Download Shortlisted Resumes
**Test Case: RC-005 - Batch Download Resumes as ZIP**
```
Precondition: Job has shortlisted candidates with resumes
Steps:
1. Job detail page → Shortlisted candidates section
2. Click [Download Shortlisted Resumes (ZIP)]
3. File downloaded to downloads folder

Expected Results:
✓ ZIP file created successfully
✓ Filename format: company_jobid_yyyy-mm-dd.zip
✓ Contains: company_name/candidate_name_resume.pdf
✓ All shortlisted resumes included
✓ File size reasonable (not empty)

Pass/Fail: _____
```

### 2.6 Schedule Interview
**Test Case: RC-006 - Schedule Interview**
```
Precondition: Candidate shortlisted
Steps:
1. Candidate row → Click [Schedule Interview]
2. Fill interview details:
   - Round: Technical (Round 1)
   - Date & Time: [Select future date/time]
   - Location: Zoom Link or Office Address
   - Interviewer Notes: [Optional notes]

3. Click [Schedule]

Expected Results:
✓ InterviewSchedule record created
✓ Notification sent to student
✓ Student sees interview in their dashboard
✓ Confirmation email with details

Pass/Fail: _____
```

---

## Part 3: TPO (Admin) Journey Testing

### 3.1 TPO Dashboard Overview
**Test Case: TPO-001 - Dashboard Statistics**
```
Precondition: TPO logged in
Steps:
1. Access TPO Dashboard
2. Verify statistics cards display:
   - Total Students: 45
   - Verified Students: 30
   - Total Companies: 8
   - Placements Made: 15

3. Verify charts:
   - Applications Trend: Line chart showing weekly data
   - Placement Status: Doughnut chart breakdown

Expected Results:
✓ All statistics display correctly
✓ Charts render with data
✓ Numbers are accurate
✓ Charts are interactive (hover shows data)

Pass/Fail: _____
```

### 3.2 Student Verification
**Test Case: TPO-002 - Verify Student**
```
Precondition: Unverified students in queue
Steps:
1. TPO Dashboard → "Pending Student Verifications"
2. See unverified student: Aditya Singh
3. Click [Verify] button
4. Verify student form shows:
   - Student details
   - Academic records
   - Resume preview
   - [Approve] and [Reject/Blacklist] buttons

5. Click [Approve]

Expected Results:
✓ Student profile marked is_verified = True
✓ verified_by = TPO user
✓ verified_at = current timestamp
✓ Student receives notification: "Your profile has been verified!"
✓ Student can now see all eligible jobs
✓ Non-eligible fields (CGPA, backlogs) become read-only

Pass/Fail: _____
```

### 3.3 Student Blacklisting
**Test Case: TPO-003 - Blacklist Student**
```
Precondition: TPO verifying student with misconduct record
Steps:
1. During verification, detect suspicious records
2. Click [Blacklist] button
3. Fill blacklist form:
   - Reason: "Fraudulent document submission"
   - [Confirm Blacklist]

Expected Results:
✓ Student is_blacklisted = True
✓ blacklist_reason recorded
✓ Student cannot apply for jobs
✓ All existing applications rejected
✓ Student notified with reason
✓ Shows in TPO dashboard as blacklisted

Pass/Fail: _____
```

### 3.4 Recruiter Approval
**Test Case: TPO-004 - Approve Recruiter**
```
Precondition: Unapproved recruiters in queue
Steps:
1. TPO Dashboard → "Pending Recruiter Approvals"
2. See recruiter: TCS
3. Click [Approve] button
4. Confirm approval

Expected Results:
✓ Recruiter is_approved = True
✓ approved_by = TPO user
✓ approved_at = current timestamp
✓ Recruiter notified: "Your company has been approved!"
✓ Recruiter can now post jobs
✓ Removed from pending queue

Pass/Fail: _____
```

### 3.5 Recruiter Blocking
**Test Case: TPO-005 - Block Recruiter**
```
Precondition: TPO reviewing recruiter with unfair practices
Steps:
1. During approval review, identify concerns
2. Click [Block] button
3. Fill block form:
   - Reason: "Discriminatory job criteria"
   - [Confirm Block]

Expected Results:
✓ Recruiter is_blocked = True
✓ blocked_reason recorded
✓ Recruiter cannot post new jobs
✓ Existing jobs unpublished
✓ Recruiter notified with reason
✓ Appears as blocked in TPO list

Pass/Fail: _____
```

### 3.6 Export Placement Report
**Test Case: TPO-006 - Generate & Export Report**
```
Precondition: Multiple placements made
Steps:
1. TPO Dashboard → [Export Report]
2. Select report type: "Placement Summary"
3. Select date range: [Start] [End]
4. Click [Generate]
5. File downloaded

Expected Results:
✓ PDF report generated
✓ Contains: Company names, Package details, Student names, Dates
✓ Summary statistics included
✓ File naming: placement_report_yyyy-mm-dd.pdf
✓ File opens correctly

Pass/Fail: _____
```

---

## Part 4: Security & Access Control Testing

### 4.1 Role-Based Access Control
**Test Case: SEC-001 - Student Cannot Access Recruiter Features**
```
Precondition: Student logged in
Steps:
1. Try to access /jobs/create/ directly
2. Try to access /recruiter/dashboard/
3. Try to access /tpo/dashboard/

Expected Results:
✓ Redirected to home with 403 Forbidden
✓ Message: "You don't have permission to access this page"
✓ Cannot access job creation
✓ Cannot access recruiter/TPO features

Pass/Fail: _____
```

### 4.2 Student Cannot Modify Verified Data
**Test Case: SEC-002 - Read-Only Fields After Verification**
```
Precondition: Student verified, CGPA set to 3.8
Steps:
1. Go to profile edit page
2. Try to modify CGPA field
3. Try to modify backlogs field
4. Try to modify 10th/12th percentages

Expected Results:
✓ Fields are disabled/read-only
✓ Message: "This field cannot be modified after verification"
✓ Values show correctly
✓ Only editable fields can be changed

Pass/Fail: _____
```

### 4.3 Prevent Duplicate Applications
**Test Case: SEC-003 - Cannot Apply Twice to Same Job**
```
Precondition: Student applied to job
Steps:
1. Try to apply to same job again
2. Click [Apply] button

Expected Results:
✓ Error message: "You have already applied for this job"
✓ Application not created
✓ Redirected to job detail

Pass/Fail: _____
```

---

## Part 5: Data Validation Testing

### 5.1 CGPA-Based Eligibility
**Test Case: DATA-001 - CGPA Filtering**
```
Precondition: Jobs with different CGPA requirements
Steps:
1. Student with CGPA 3.5 logged in
2. Browse jobs:
   - Job A: Min CGPA 3.0 → Eligible ✓
   - Job B: Min CGPA 3.8 → Not eligible ✗
   - Job C: Min CGPA 4.0 → Not eligible ✗

Expected Results:
✓ Only Job A shows [Apply] button
✓ Jobs B & C show eligibility warning
✓ Filtering logic correct

Pass/Fail: _____
```

### 5.2 Backlog Validation
**Test Case: DATA-002 - Backlog Limits**
```
Precondition: Student with 1 active backlog
Steps:
1. Browse jobs:
   - Job A: Max Backlogs 2 → Eligible ✓
   - Job B: Max Backlogs 0 → Not eligible ✗

Expected Results:
✓ Backlog check accurate
✓ Student cannot apply to Job B
✓ Warning message shown

Pass/Fail: _____
```

### 5.3 Deadline Validation
**Test Case: DATA-003 - Application Deadline**
```
Precondition: Job with deadline in past
Steps:
1. Try to apply to job with expired deadline
2. Click [Apply]

Expected Results:
✓ Error: "Application deadline has passed"
✓ [Apply] button disabled
✓ Job marked as closed

Pass/Fail: _____
```

---

## Part 6: Notification Testing

### 6.1 Status Change Notifications
**Test Case: NOTIF-001 - Status Update Alerts**
```
Precondition: Student applied, recruiter changing status
Steps:
1. Recruiter changes application status to "Shortlisted"
2. Student receives notification
3. Student sees in dashboard
4. Email received (check spam folder)

Expected Results:
✓ In-app notification appears
✓ Dashboard updates immediately
✓ Email sent with details
✓ Notification timestamp correct

Pass/Fail: _____
```

---

## Part 7: Performance Testing

### 7.1 Page Load Times
**Test Case: PERF-001 - Dashboard Load**
```
Steps:
1. Open student dashboard
2. Measure load time
3. Repeat for recruiter dashboard
4. Repeat for TPO dashboard

Expected Results:
✓ Student Dashboard: < 2 seconds
✓ Recruiter Dashboard: < 2 seconds
✓ TPO Dashboard with charts: < 3 seconds

Pass/Fail: _____
```

### 7.2 Large Dataset Handling
**Test Case: PERF-002 - Job Listing Performance**
```
Precondition: 500+ jobs in database
Steps:
1. Load job listing page
2. Apply multiple filters
3. Observe response time

Expected Results:
✓ Initial load: < 2 seconds
✓ Filter application: < 1 second
✓ No UI freezing
✓ Pagination working (20 items per page)

Pass/Fail: _____
```

---

## Part 8: Mobile Responsiveness Testing

### 8.1 Mobile Layout
**Test Case: RESP-001 - Mobile Dashboard**
```
Precondition: Browser at 375x812 (iPhone size)
Steps:
1. Access student dashboard
2. Verify layout:
   - Hamburger menu visible
   - Navigation slides out
   - Content area full width
   - Cards stack vertically
   - Tables scroll horizontally

Expected Results:
✓ All elements visible and accessible
✓ Text readable without zoom
✓ Touch targets >= 48x48px
✓ No horizontal scroll at 375px width

Pass/Fail: _____
```

---

## Part 9: Integration Testing

### 9.1 End-to-End Student Journey
**Test Case: INT-001 - Complete Student Workflow**
```
Steps:
1. Student registers
2. TPO verifies student
3. Student browses jobs
4. Student applies to job
5. Recruiter shortlists student
6. Recruiter schedules interview
7. Student attends interview
8. Recruiter selects student
9. TPO exports placement report

Expected Results:
✓ All steps complete successfully
✓ Data consistent across system
✓ No errors or data loss
✓ All notifications sent

Pass/Fail: _____
```

---

## Part 10: Database Testing

### 10.1 Audit Trail
**Test Case: DB-001 - ApplicationStatus Audit Log**
```
Precondition: Application status changed by recruiter
Steps:
1. Check ApplicationStatus table
2. Verify fields:
   - status = new status
   - updated_by = recruiter user
   - application = correct application
   - timestamp = accurate

Expected Results:
✓ All audit fields populated
✓ Timestamp is accurate
✓ Updated_by correctly identifies user
✓ Cannot be modified after creation

Pass/Fail: _____
```

---

## Regression Test Suite

After each update, run these critical tests:

```
☐ ST-001: Student registration
☐ ST-004: Apply for job
☐ RC-003: Post job
☐ RC-004: Manage applications
☐ TPO-002: Verify student
☐ SEC-001: RBAC access control
☐ DATA-001: CGPA eligibility
☐ INT-001: End-to-end workflow
```

---

## Test Results Summary

| Test Case ID | Description | Pass/Fail | Notes |
|---|---|---|---|
| ST-001 | Student Registration | ☐ | |
| ST-002 | View Profile | ☐ | |
| ST-003 | Browse Eligible Jobs | ☐ | |
| ST-004 | Apply for Job | ☐ | |
| ST-005 | Track Application | ☐ | |
| ST-006 | View App Details | ☐ | |
| RC-001 | Recruiter Registration | ☐ | |
| RC-002 | TPO Approval | ☐ | |
| RC-003 | Post Job | ☐ | |
| RC-004 | Manage Applications | ☐ | |
| RC-005 | Download Resumes | ☐ | |
| RC-006 | Schedule Interview | ☐ | |
| TPO-001 | Dashboard Stats | ☐ | |
| TPO-002 | Verify Student | ☐ | |
| TPO-003 | Blacklist Student | ☐ | |
| TPO-004 | Approve Recruiter | ☐ | |
| TPO-005 | Block Recruiter | ☐ | |
| TPO-006 | Export Report | ☐ | |
| SEC-001 | RBAC Access | ☐ | |
| SEC-002 | Read-Only Fields | ☐ | |
| SEC-003 | Duplicate Prevention | ☐ | |
| DATA-001 | CGPA Filtering | ☐ | |
| DATA-002 | Backlog Validation | ☐ | |
| DATA-003 | Deadline Validation | ☐ | |
| NOTIF-001 | Status Notifications | ☐ | |
| PERF-001 | Load Times | ☐ | |
| PERF-002 | Large Datasets | ☐ | |
| RESP-001 | Mobile Layout | ☐ | |
| INT-001 | End-to-End | ☐ | |
| DB-001 | Audit Trail | ☐ | |

---

**Test Plan Version**: 1.0  
**Date**: January 15, 2026  
**Tester**: QA Team

