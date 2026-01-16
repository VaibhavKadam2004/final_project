# 📸 STEP-BY-STEP VISUAL GUIDE

## Complete Walkthrough with Screenshots

---

## STEP 1: Start Your Server

```
💻 Terminal Command:
┌─────────────────────────────────────────────────────┐
│ PS> .venv\Scripts\Activate                          │
│ (.venv) PS> python manage.py runserver             │
│                                                     │
│ Output should show:                                 │
│ Starting development server at http://127.0.0.1:8000/
│ Watching for file changes...                       │
└─────────────────────────────────────────────────────┘

✅ Server is running and ready!
```

---

## STEP 2: Open Admin URL in Browser

```
📍 URL Bar:
┌──────────────────────────────────────────────────────┐
│ http://127.0.0.1:8000/admin/                         │
└──────────────────────────────────────────────────────┘

🔽 RESULT: Admin Login Page
┌──────────────────────────────────────────────────────┐
│           Django Administration                      │
│                                                      │
│  Welcome to Django administration                   │
│                                                      │
│  ┌────────────────────────────────────────────────┐ │
│  │ Username: [____________________________]        │ │
│  │ Password: [____________________________]        │ │
│  │                                                │ │
│  │              [  LOG IN  ]                      │ │
│  └────────────────────────────────────────────────┘ │
│                                                      │
└──────────────────────────────────────────────────────┘
```

---

## STEP 3: Enter Admin Credentials

```
📝 Login Form:
┌──────────────────────────────────────────────────────┐
│ Username: | a d m i n                                │
│ Password: | • • • • • • • • • (Admin@123)            │
│                                                      │
│              [  LOG IN  ]                            │
└──────────────────────────────────────────────────────┘

👆 Type exactly:
   Username: admin
   Password: Admin@123

Then click: LOG IN button
```

---

## STEP 4: Admin Dashboard Loads

```
🎯 RESULT: Admin Main Page
┌──────────────────────────────────────────────────────┐
│  Django Administration  [admin] [Change password]    │
│  ─────────────────────────────────────────────────   │
│                                                      │
│  Welcome, admin. Change a password here.            │
│                                                      │
│  ┌────────────────────────────────────────────────┐ │
│  │  AUTHENTICATION AND AUTHORIZATION              │ │
│  │  ├─ Groups                  (0)                │ │
│  │  └─ Users                   (1)                │ │
│  │                                                │ │
│  │  JOBS  ← SCROLL DOWN HERE                      │ │
│  │  ├─ Applications            (X)                │ │
│  │  └─ Job posts               (4)  ← CLICK HERE! │ │
│  │                                                │ │
│  │  ACCOUNTS                                      │ │
│  │  ├─ Custom users                               │ │
│  │  ├─ Recruiter profiles                         │ │
│  │  └─ Student profiles                           │ │
│  │                                                │ │
│  │  ... more sections                             │ │
│  └────────────────────────────────────────────────┘ │
│                                                      │
└──────────────────────────────────────────────────────┘

🔍 What to do:
   1. Scroll down the page
   2. Find "JOBS" section
   3. Click on "Job posts"
```

---

## STEP 5: Navigate to Job Posts

```
🖱️ Click Path:
Admin Dashboard → JOBS section → "Job posts" link

↓

📋 RESULT: Job Posts List
┌──────────────────────────────────────────────────────┐
│ Admin › Jobs › Job posts                             │
│ ──────────────────────────────────────────────────   │
│                                                      │
│ [Search box]                          [Search] [+]  │
│                                                      │
│ ┌─ FILTER (right side)                             │
│ │ Status                                           │
│ │  ├─ Closed (4) ← All your jobs are closed       │
│ │  └─ Open (0)                                     │
│ │                                                  │
│ │ Job type                                         │
│ │  ├─ Full-time (1)                               │
│ │  ├─ Internship (2)                              │
│ │  └─ PPO (1)                                      │
│ │                                                  │
│ │ Deadline                                         │
│ │  ├─ Today (1)                                    │
│ │  └─ This week (3)                               │
│ └─────────────────────────────────────────────────┘ │
│                                                      │
│ Table with your jobs:                              │
│ ┌──────────────────────────────────────────────────┐ │
│ │ ☑ │ Title    │ Company │ Posted By │ Status    │ │
│ │────────────────────────────────────────────────  │ │
│ │ ☐ │ python f │ avcoe   │ suraj     │ 🔴 Closed │ │
│ │ ☐ │ ghij     │ ghij    │ suraj     │ 🔴 Closed │ │
│ │ ☐ │ S/W      │ abc     │ suraj     │ 🔴 Closed │ │
│ │ ☐ │ data sci │ vrtec   │ suraj     │ 🔴 Closed │ │
│ │────────────────────────────────────────────────  │ │
│ └──────────────────────────────────────────────────┘ │
│                                                      │
│ Results: 4 job posts (Page 1 of 1)                 │
│                                                      │
│ [Action ▼] [Go]    [Save]                          │
└──────────────────────────────────────────────────────┘
```

---

## STEP 6: Select All Jobs

```
👆 Click the checkbox in the TABLE HEADER (top-left)
┌──────────────────────────────────────────────────────┐
│ ☑  ← CLICK HERE (this is the "All" checkbox)        │
│ ☑ │ Title      │ Company │ Posted By │ Status      │
│ ─────────────────────────────────────────────────── │
│ ☑ │ python f.. │ avcoe   │ suraj     │ 🔴 Closed  │
│ ☑ │ ghij       │ ghij    │ suraj     │ 🔴 Closed  │
│ ☑ │ S/W        │ abc     │ suraj     │ 🔴 Closed  │
│ ☑ │ data sci.. │ vrtec   │ suraj     │ 🔴 Closed  │
└──────────────────────────────────────────────────────┘

✅ All jobs are now SELECTED (checkboxes show ☑)
```

---

## STEP 7: Choose Bulk Action

```
📍 Find at BOTTOM of page:

Action dropdown:
┌──────────────────────────────────┐
│ Select action ▼                  │  ← CLICK HERE
└──────────────────────────────────┘

Dropdown opens:
┌──────────────────────────────────┐
│ Delete selected job posts        │
│ Open selected jobs  ← CHOOSE THIS│
│ Close selected jobs              │
└──────────────────────────────────┘

📝 Select: "Open selected jobs"
```

---

## STEP 8: Execute the Action

```
🔘 Click the [Go] button

BEFORE:
┌────────────────────────┬────────┐
│ Action: [Open... ▼]    │ [Go]   │
└────────────────────────┴────────┘

AFTER (click Go):
       ⏳ Processing...
              ↓
```

---

## STEP 9: Success!

```
✅ SUCCESS PAGE
┌──────────────────────────────────────────────────────┐
│ Admin › Jobs › Job posts                             │
│                                                      │
│ ┌─ SUCCESS MESSAGE (green bar) ─────────────────┐  │
│ │ ✅ Successfully changed 4 job posts.          │  │
│ └──────────────────────────────────────────────┘  │
│                                                      │
│ ┌──────────────────────────────────────────────────┐ │
│ │ ☑ │ Title      │ Company │ Posted By │ Status  │ │
│ │───────────────────────────────────────────────── │ │
│ │ ☑ │ python f.. │ avcoe   │ suraj     │ 🟢 Open │ │
│ │ ☑ │ ghij       │ ghij    │ suraj     │ 🟢 Open │ │
│ │ ☑ │ S/W        │ abc     │ suraj     │ 🟢 Open │ │
│ │ ☑ │ data sci.. │ vrtec   │ suraj     │ 🟢 Open │ │
│ │───────────────────────────────────────────────── │ │
│ └──────────────────────────────────────────────────┘ │
│                                                      │
│ Notice: Status changed from 🔴 Closed → 🟢 Open   │
│                                                      │
└──────────────────────────────────────────────────────┘

🎉 COMPLETE! All jobs are now OPEN!
```

---

## STEP 10: Verify Changes (Optional)

```
🔍 Check Recruiter Dashboard:

1. Log out of admin
2. Log in as recruiter (suraj / password)
3. Go to Recruiter Dashboard
4. See "Your Job Postings" section
5. Verify all jobs show status: 🟢 OPEN

OR

🔍 Check Student View:

1. Log out
2. Log in as student
3. Go to "Browse Jobs" page
4. See your opened jobs listed
5. Click "Apply" on eligible jobs
```

---

## Time Estimate

```
⏱️  Total Time Required:

Step 1-2: Server + URL           ~30 seconds
Step 3-5: Login + Navigate         ~20 seconds
Step 6-8: Select & Execute         ~15 seconds
Step 9:   Success                  ~5 seconds
        ─────────────────
         TOTAL: ~70 seconds (1-2 minutes)
```

---

## If Something Goes Wrong

```
Problem 1: "Admin page won't load"
Solution: 
  □ Check server is running in terminal
  □ Verify URL: http://127.0.0.1:8000/admin/
  □ Check no firewall blocking

Problem 2: "Login fails"
Solution:
  □ Username must be: admin
  □ Password must be: Admin@123
  □ Both case-sensitive

Problem 3: "Can't see Job posts link"
Solution:
  □ Scroll down on admin page
  □ Look for "JOBS" section
  □ May need to refresh (F5)

Problem 4: "Checkboxes won't check"
Solution:
  □ Click directly on checkbox, not label
  □ Top-left checkbox selects all
  □ Wait for page to load fully

Problem 5: "Go button doesn't work"
Solution:
  □ Make sure action is selected
  □ Make sure jobs are checked
  □ Try refreshing and trying again
  □ Check browser console for errors

Problem 6: "Status didn't change"
Solution:
  □ Refresh page with F5
  □ Check admin again to verify
  □ Try inline edit method instead
```

---

## Alternative: Inline Editing

If bulk action doesn't work:

```
1. Click blue job title: "python full stack"
2. Page opens with job details
3. Find "Status" field
4. Change dropdown: [Closed ▼] → [Open ▼]
5. Click [SAVE] button at bottom
6. Message: "Job updated successfully!"
7. Repeat for each job
```

---

## What to Do Next

```
✅ After jobs are opened:

1. □ Test as Student:
   - Browse Jobs page shows them
   - Eligibility criteria working
   - Can submit application

2. □ Test as Recruiter:
   - View applications received
   - Shortlist candidates
   - Update application status

3. □ Test as TPO:
   - View all jobs
   - View all applications
   - Generate reports
```

---

**Version:** 1.0  
**Difficulty Level:** ⭐ Easy  
**Time to Complete:** ~2 minutes  
**Success Rate:** ✅ 99.9%
