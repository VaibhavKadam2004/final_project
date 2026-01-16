# 🎬 VISUAL STEP-BY-STEP GUIDE - Recruiter Applications

## BEFORE YOU START
Make sure:
- ✅ Server is running: `python manage.py runserver`
- ✅ You're logged in as **Recruiter** (not Student, not TPO)
- ✅ You have posted at least one job

---

## 🎯 COMPLETE WORKFLOW WITH SCREENSHOTS

### **SCREEN 1: Recruiter Dashboard**

```
┌─────────────────────────────────────────────────────────┐
│ Welcome, John (Recruiter Name)                          │
│ Manage your job postings and candidate applications     │
│                                                    [Post New Job]
├─────────────────────────────────────────────────────────┤
│ Company Information                                      │
│ Company Name: Tech Corp                                 │
│ Email: hr@techcorp.com                                 │
│                                                         │
│ Approval Status: ✓ Approved                            │
│ You can now post jobs                                  │
├─────────────────────────────────────────────────────────┤
│ Statistics                                              │
│ ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐      │
│ │ 2 Jobs  │ │ 15 Apps │ │ 5 Short │ │ 2 Sel.  │      │
│ └─────────┘ └─────────┘ └─────────┘ └─────────┘      │
├─────────────────────────────────────────────────────────┤
│ Your Job Postings                                       │
│ ┌───────────┬────────────┬─────────┬───────┬──────┐   │
│ │ Job Title │ Criteria   │ Package │ Date  │Action│   │
├─────────────────────────────────────────────────────────┤
│ │ Python    │ CGPA: ≥7.5 │ ₹12 LPA │ Feb01 │ 📄✏️   │◄── CLICK 📄
│ │ Dev       │ BL: ≤0     │         │       │ 👁️ │   │    (View Apps)
├─────────────────────────────────────────────────────────┤
│ │ Data Sci  │ CGPA: ≥8.0 │ ₹15 LPA │ Feb15 │ 📄✏️   │
│ │ Int       │ BL: ≤1     │         │       │ 👁️ │   │
└───────────────────────────────────────────────────────┘
```

**ACTION:** Click 📄 button to "View Applications"

---

### **SCREEN 2: Applications List Page**

```
┌─────────────────────────────────────────────────────────┐
│ Applications for Python Developer                      │
│ Tech Corp • Manage candidate applications and update   │
│                                              [← Back to Dashboard]
├─────────────────────────────────────────────────────────┤
│ Job Information                                         │
│ Python Developer          Package: ₹12 LPA             │
│ CGPA: ≥7.5 • BL: ≤0     Deadline: Feb 1, 2026 14:00   │
├─────────────────────────────────────────────────────────┤
│ Statistics                                              │
│ ┌────────┐ ┌────────┐ ┌────────┐ ┌────────┐           │
│ │ 15     │ │ 8      │ │ 5      │ │ 2      │           │
│ │ Total  │ │Pending │ │Short.  │ │Select. │           │
│ └────────┘ └────────┘ └────────┘ └────────┘           │
├─────────────────────────────────────────────────────────┤
│ Candidates                                              │
│ ┌────────────┬───────────┬──────┬──────┬────────┬──────┤
│ │ Student    │ Email     │ CGPA │ BL   │ Status │Action│
├─────────────────────────────────────────────────────────┤
│ │ Raj Kumar  │ raj@...   │ 8.7  │ 0    │Pending │[Upd.]│◄── CLICK [Upd.]
│ │ 2023CSE101 │           │      │      │        │      │
├─────────────────────────────────────────────────────────┤
│ │ Priya S.   │ priya@... │ 8.9  │ 1    │Pending │[Upd.]│
│ │ 2023CSE102 │           │      │      │        │      │
├─────────────────────────────────────────────────────────┤
│ │ Arjun V.   │ arjun@... │ 7.8  │ 0    │Pending │[Upd.]│
│ │ 2023CSE103 │           │      │      │        │      │
├─────────────────────────────────────────────────────────┤
│ │ Ananya M.  │ ananya@.. │ 8.2  │ 2    │Pending │[Upd.]│
│ │ 2023CSE104 │           │      │      │        │      │
└───────────────────────────────────────────────────────┘
```

**ACTION:** Click [Upd.] button on any candidate

---

### **SCREEN 3: Update Status Modal (Popup)**

When you click the "Update" button, a popup appears:

```
┌───────────────────────────────────────┐
│ Update Application Status             │ [X]
├───────────────────────────────────────┤
│                                       │
│ Raj Kumar                             │
│                                       │
│ New Status *                          │
│ ┌─────────────────────────────────┐  │
│ │ -- Select Status --             ▼  │  ◄── DROPDOWN
│ │ Pending         ✓                  │      Select new
│ │ Shortlisted                        │      status
│ │ Selected                           │      here
│ │ Rejected                           │
│ └─────────────────────────────────┘  │
│                                       │
│ Add Note (Optional)                   │
│ ┌─────────────────────────────────┐  │
│ │                                 │  │
│ │ E.g., Selected for technical    │  │  ◄── TEXT AREA
│ │ round, Failed coding test, etc. │  │      Add reason
│ │                                 │  │      for change
│ │                                 │  │
│ └─────────────────────────────────┘  │
│                                       │
│          [Cancel]  [Update Status]    │
└───────────────────────────────────────┘
```

**ACTION:** 
1. Click dropdown, select "Shortlisted"
2. Type note: "Good resume, selected for Round 1"
3. Click [Update Status]

---

### **SCREEN 4: Success & Updated List**

After clicking [Update Status]:

```
┌─────────────────────────────────────────────────────────┐
│ ✓ Application status updated to Shortlisted             │ ◄── SUCCESS MSG
├─────────────────────────────────────────────────────────┤
│ Candidates                                              │
│ ┌────────────┬───────────┬──────┬──────┬──────────┬─────┤
│ │ Student    │ Email     │ CGPA │ BL   │ Status   │Action
├─────────────────────────────────────────────────────────┤
│ │ Raj Kumar  │ raj@...   │ 8.7  │ 0    │⭐Short   │[Upd.]│ ◄── STATUS CHANGED
│ │ 2023CSE101 │           │      │      │          │      │
├─────────────────────────────────────────────────────────┤
│ │ Priya S.   │ priya@... │ 8.9  │ 1    │⏳Pending │[Upd.]│
│ │ 2023CSE102 │           │      │      │          │      │
└───────────────────────────────────────────────────────┘
```

**RESULT:** 
- ✅ Raj Kumar's status changed to "Shortlisted" (⭐)
- ✅ Note saved to database
- ✅ Timestamp recorded
- ✅ Success message shown

---

## 📊 STATUS COLOR CODING

```
Status Badge Colors:

Pending      - Yellow background (⏳ Under Review)
Shortlisted  - Blue background (⭐ Selected for Interview)
Selected     - Green background (✅ Offer Given)
Rejected     - Red background (❌ Not Selected)
```

---

## 🔄 COMPLETE APPLICATION JOURNEY

```
1. STUDENT APPLIES
   ↓
   Status: Pending 🟡
   Dashboard shows: 1 Pending

2. YOU REVIEW (Day 1)
   ↓ [Click Update]
   → Select "Shortlisted"
   → Add note: "Good CGPA and skills"
   → [Update Status]
   ↓
   Status: Shortlisted 🔵
   Dashboard shows: 5 Shortlisted

3. AFTER TECHNICAL INTERVIEW (Day 3)
   ↓ [Click Update]
   → Select "Selected"
   → Add note: "Excellent performance, offer sent"
   → [Update Status]
   ↓
   Status: Selected 🟢
   Dashboard shows: 2 Selected
   (Application now LOCKED - Cannot modify)

4. CANDIDATE ACCEPTS OFFER
   ↓
   Final Status: Selected 🟢
   (Ready for onboarding)
```

---

## ⚡ QUICK REFERENCE - BUTTONS & ACTIONS

| Location | Button | Purpose |
|----------|--------|---------|
| **Dashboard** | 📄 | View Applications for this job |
| **Dashboard** | 👁️ | View Job Details |
| **Dashboard** | ✏️ | Edit Job (Title, Description, etc.) |
| **Applications List** | [Update] | Open modal to change status |
| **Modal** | [Cancel] | Close without saving |
| **Modal** | [Update Status] | Save status change and note |
| **Modal** | [← Back] | Return to dashboard |

---

## 💡 TIPS & TRICKS

**Tip 1: Use Descriptive Notes**
```
Good: "Shortlisted for technical round 1 - Strong coding skills"
Bad: "ok"
```

**Tip 2: Quick Status Updates**
```
Instead of reviewing one-by-one:
1. Open applications list
2. Quickly scan CVs/GPA
3. Click Update on good candidates
4. Select "Shortlisted" and note "Shortlist for Round 1"
5. Repeat for all
```

**Tip 3: Track Your Progress**
```
Statistics at top show:
- How many still Pending
- How many Shortlisted
- How many Selected
- How many Rejected
```

**Tip 4: Notes Become Communication**
```
Student sees: "Shortlisted for Round 1"
So they know exactly why they advanced
```

---

## ❌ COMMON MISTAKES

### Mistake 1: Can't find "View Applications" button
**Solution:** You need to be logged in as the RECRUITER who posted the job

### Mistake 2: "Cannot modify closed applications"
**Solution:** Application already finalized. Status is Locked.

### Mistake 3: Lost modal when clicked Cancel
**Solution:** Normal - Modal closes. Application not updated.

### Mistake 4: Forgot to save note
**Solution:** Click [Update Status] button to save note

### Mistake 5: Can't update another recruiter's job
**Solution:** You can only update applications for YOUR jobs

---

## 🎓 LEARNING PATH

### Day 1: Learn to Update Status
- [ ] Login as Recruiter
- [ ] Go to Dashboard
- [ ] Click View Applications
- [ ] Update 1 application from Pending → Shortlisted
- [ ] Add a note
- [ ] See status change

### Day 2: Manage Multiple Applications
- [ ] Update 5 applications
- [ ] Use different statuses (Shortlisted, Rejected)
- [ ] Add descriptive notes
- [ ] Check statistics

### Day 3: Full Workflow
- [ ] Review all pending applications
- [ ] Shortlist candidates with high CGPA
- [ ] Schedule interviews
- [ ] Update to "Selected" after interviews
- [ ] Track hiring metrics

---

## 📞 NEED HELP?

Check these documents:
1. [RECRUITER_APPLICATION_GUIDE.md](RECRUITER_APPLICATION_GUIDE.md) - Detailed guide
2. [IMPLEMENTATION_SUMMARY_RECRUITER_APPLICATIONS.md](IMPLEMENTATION_SUMMARY_RECRUITER_APPLICATIONS.md) - Technical details
3. This file - Visual walkthrough

---

**Ready to manage applications? Let's go! 🚀**
