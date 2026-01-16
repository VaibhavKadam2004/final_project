# 📋 RECRUITER WORKFLOW - Complete Guide

## Overview
Recruiters can now manage student applications through a complete workflow system.

---

## 🚀 Step-by-Step Workflow

### **STEP 1: Login as Recruiter**
- Go to http://127.0.0.1:8000/accounts/login/
- Login with recruiter credentials
- Navigate to **Recruiter Dashboard**

---

### **STEP 2: View Job Postings**
On the Recruiter Dashboard, you'll see:
- **Your Job Postings** table with all your posted jobs
- Each job shows:
  - Job Title
  - Eligibility Criteria (CGPA, Backlogs)
  - Package (LPA)
  - Deadline
  - Status (Open/Closed)

---

### **STEP 3: Click "View Applications" Button**
In the **Actions** column for each job:
- 📄 **First Button (File icon)** = **View Applications** ← Click this
- 👁️ **Second Button (Eye icon)** = View Job Details
- ✏️ **Third Button (Edit icon)** = Edit Job

---

### **STEP 4: See All Applications**
After clicking "View Applications", you'll see:
- **Job Information** (Title, Company, Criteria, Package, Deadline)
- **Statistics** showing:
  - Total Applications
  - Pending Count
  - Shortlisted Count
  - Selected Count
  - Rejected Count
- **Applications Table** with all students who applied

---

### **STEP 5: View Student Details**
Each row in the Applications Table shows:
- **Student Name** (clickable if needed)
- **Email Address**
- **CGPA** (Student's academic score)
- **Active Backlogs** (Number of pending courses)
- **Applied On** (Date of application)
- **Current Status** (Pending/Shortlisted/Selected/Rejected)
- **Update Button** (Blue "Update" button)

---

### **STEP 6: Update Application Status**
Click the **"Update"** button to open a modal where you can:

#### **Change Status:**
Select from dropdown:
- ✋ **Pending** (Default - Under Review)
- ⭐ **Shortlisted** (Selected for interview)
- ✅ **Selected** (Offer given)
- ❌ **Rejected** (Not selected)

#### **Add Notes (Optional but Recommended):**
Examples of good notes:
- "Selected for technical round - Round 1"
- "Failed coding assessment"
- "Selected for HR round"
- "Excellent communication skills"
- "Passed technical, awaiting HR approval"

---

### **STEP 7: Submit Status Update**
Click **"Update Status"** button to save:
- ✅ Status is updated immediately
- ✅ Note is recorded in history
- ✅ Application is locked after final decision (Selected/Rejected)
- ✅ Success message appears

---

## 📊 Status Meanings

| Status | Meaning | Next Step |
|--------|---------|-----------|
| **Pending** | Under Review | Review resume, decide to shortlist or reject |
| **Shortlisted** | Selected for Interview | Schedule interview, send interview details |
| **Selected** | Offer Given | Send offer letter, arrange for joining |
| **Rejected** | Not Selected | Application closed, no further action |

---

## ⚠️ Important Rules

### **Who Can Update Status?**
✅ **Only the recruiter who posted the job**
❌ Students cannot update their own status
❌ Other recruiters cannot update your applications
❌ TPO cannot directly update status

### **When Can You Update?**
✅ Before application is closed
✅ While job posting is still open
✅ Anytime - Pending, Shortlisted, Selected, Rejected

### **What Happens When Closed?**
❌ Once an application reaches "Selected" or "Rejected", it may be locked
❌ No further modifications allowed
❌ History is preserved

---

## 🔍 View Application History

For each application, you can see:
- All status changes made
- When each status was set
- Notes added for each change
- Who made the change (your username)

---

## 📈 Dashboard Statistics

Your **Recruiter Dashboard** shows totals:
- **Total Applications** = All applications across all jobs
- **Total Shortlisted** = All shortlisted candidates
- **Total Selected** = All selected candidates

---

## 🎯 Common Workflow Example

```
1. Student applies for Data Science Internship
   ↓ (Status: Pending)

2. You review resume
   ↓ (Click "Update" → Change to "Shortlisted")
   ↓ Note: "Good resume, shortlisted for Round 1"

3. After technical interview
   ↓ (Click "Update" → Change to "Selected")
   ↓ Note: "Excellent performance, selected - offer letter sent"
   ↓ (Application now CLOSED)

4. Candidate accepted offer
   ↓ Final Status: Selected (Locked)
```

---

## 🚀 Quick Access URLs

| Action | URL | Method |
|--------|-----|--------|
| Recruiter Dashboard | `/accounts/recruiter/dashboard/` | GET |
| Post New Job | `/jobs/create/` | GET/POST |
| View Applications | `/jobs/recruiter/{job_id}/applications/` | GET/POST |
| Update Status | POST to same URL | POST |

---

## 💡 Tips for Better Management

1. **Add Detailed Notes** - Helps you remember why you made decisions
2. **Update Quickly** - Students want to know their status soon
3. **Review CGPA/Backlogs** - Ensure students meet your criteria
4. **Schedule Interviews** - After shortlisting, arrange interviews promptly
5. **Track Deadlines** - Check job deadline and respond before it passes

---

## ❓ Troubleshooting

### Problem: "Cannot modify closed applications"
**Solution:** Application is already finalized (Selected/Rejected). Cannot change.

### Problem: "You can only update applications for your own job postings"
**Solution:** You're trying to update another recruiter's job. Only the posting recruiter can update.

### Problem: "Cannot update applications for closed job postings"
**Solution:** The job posting itself is closed. Cannot accept new status changes.

### Problem: Button not appearing
**Solution:** Make sure you're logged in as the recruiter who posted the job.

---

## ✨ Features Implemented

✅ View all applications for your jobs
✅ See student details (Name, Email, CGPA, Backlogs)
✅ Update application status with dropdown
✅ Add notes for each status change
✅ View status history
✅ Statistics dashboard
✅ Sorted by application date (newest first)
✅ Restricted to job poster only
✅ Audit trail for compliance

---

**Last Updated:** January 15, 2026
