# 🖥️ ADMIN PANEL GUIDE - Opening Jobs

## Where to Find Everything

```
http://127.0.0.1:8000/admin/
          │
          ├─ Login Page (admin / Admin@123)
          │
          └─ Admin Dashboard
             │
             ├─ AUTHENTICATION AND AUTHORIZATION
             │  ├─ Groups
             │  └─ Users
             │
             ├─ JOBS  ← YOU ARE HERE
             │  ├─ Job posts  ← CLICK HERE
             │  └─ Applications
             │
             └─ Other sections...
```

---

## Detailed Click Path

### 1️⃣ OPEN ADMIN PANEL
```
Browser → Type: http://127.0.0.1:8000/admin/
```

### 2️⃣ LOGIN
```
Username field: admin
Password field: Admin@123
Click: [Log In] button
```

### 3️⃣ FIND JOB POSTS
```
Scroll down page
Find section labeled: "JOBS"
  │
  └─ Under JOBS, find: "Job posts"
     │
     └─ Click "Job posts" link
```

### 4️⃣ SELECT ALL JOBS
```
Admin table appears with your jobs:

┌─────────────────────────────────────────────┐
│ ☑️ ALL  │ Title           │ Company │ Status │
├─────────────────────────────────────────────┤
│ ☐      │ python full stack│ avcoe   │ Closed │
│ ☐      │ ghij             │ ghij    │ Closed │
│ ☐      │ S/W              │ abc     │ Closed │
│ ☐      │ data science     │ vrtec   │ Closed │
└─────────────────────────────────────────────┘

👆 Click this checkbox to select ALL jobs
```

### 5️⃣ CHOOSE ACTION
```
Scroll to BOTTOM of page

Find dropdown: "Action"  [Select action ▼]
Click dropdown
Select: "Open selected jobs"
```

### 6️⃣ EXECUTE
```
Find button: [Go]  (appears next to Action dropdown)
Click [Go]
```

### 7️⃣ SUCCESS!
```
Page shows green message:
"✅ Successfully changed 4 job posts."

OR

"✅ X job(s) have been opened."
```

---

## Visual Layout of Admin Table

```
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ Admin › Jobs › Job posts                                             ┃
┣━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┫
┃                                                                      ┃
┃  Search:  [______________]  [Search]                                ┃
┃                                                                      ┃
┃  Filter (right side):                                                ┃
┃    ├─ Status      → [Open] [Closed]                                 ┃
┃    ├─ Job type    → [Full-time] [Internship] [PPO]                  ┃
┃    └─ Deadline    → [Today] [Tomorrow] [This week]                  ┃
┃                                                                      ┃
┣━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┫
┃ ☑  │ Title             │ Company │ Posted By │ Status │ Deadline   ┃
┣━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┫
┃ ☐  │ python full stack │ avcoe   │ suraj     │ 🔴     │ Jan 15     ┃
┃ ☐  │ ghij              │ ghij    │ suraj     │ 🔴     │ Jan 14     ┃
┃ ☐  │ S/W               │ abc     │ suraj     │ 🔴     │ Jan 15     ┃
┃ ☐  │ data science      │ vrtec   │ suraj     │ 🔴     │ Jan 23     ┃
┣━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┫
┃                                                                      ┃
┃  Action: [Select action ▼]  [Go]                                    ┃
┃                                                                      ┃
┃  Results: 4 job posts (Page 1 of 1)                                 ┃
┃                                                                      ┃
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
```

---

## Action Dropdown Options

When you click the "Action" dropdown, you'll see:

```
[Select action ▼]
├─ Open selected jobs       ← USE THIS TO OPEN JOBS ✅
├─ Close selected jobs      ← USE THIS TO CLOSE JOBS
└─ Delete selected job posts
```

---

## Inline Editing (Alternative)

### Click Job Title to Edit

```
Click: "python full stack"  (the blue link)
                ↓
        Opens Edit Page
                ↓
Find: Status field
        │
        ├─ Current: [Closed ▼]
        │
        └─ Change to: [Open ▼]
                ↓
        Click: [SAVE] button (bottom)
                ↓
        Message: "Job updated successfully!"
                ↓
        Status now: [Open ✅]
```

---

## Status Color Legend

```
🔴 Closed  = Red dot or "Closed" text
🟢 Open    = Green dot or "Open" text
⚪ Default = Gray dot
```

---

## Filter Feature (Right Sidebar)

Use filters to quickly find jobs:

```
Filters:
├─ Status
│  ├─ Closed (4 jobs)     ← All your current jobs
│  └─ Open (0 jobs)
│
├─ Job type
│  ├─ Full-time (1 job)
│  ├─ Internship (2 jobs)
│  └─ PPO (1 job)
│
└─ Deadline
   ├─ This week (3 jobs)
   └─ Next week (1 job)
```

Click "Closed" filter to see only closed jobs
Then select all and open them

---

## Search Feature

```
Search box at top:
[_____________________]  [Search]

Type:
├─ Job title → "python"
├─ Company → "avcoe"
├─ Description keywords
└─ Posted by username → "suraj"

Press Enter or click [Search]
```

---

## Success Messages

After opening jobs, you'll see:

```
✅ Successfully changed 4 job posts.
```

OR

```
✅ 4 job(s) have been opened.
```

This confirms jobs are now OPEN!

---

## What Changes After Opening

### Before (Closed Status)
```
Status in admin: 🔴 Closed
Student view: Can't see job
Student action: Cannot apply
```

### After (Open Status)
```
Status in admin: 🟢 Open
Student view: See job (if eligible)
Student action: Can apply
Recruiter: Can shortlist
```

---

## Tips & Tricks

✅ **Select All** - Click checkbox in header to select all jobs at once  
✅ **Multi-select** - Hold Ctrl and click individual checkboxes  
✅ **Sort columns** - Click column header to sort  
✅ **Search first** - Find what you need before bulk actions  
✅ **Check before executing** - Verify selected items before clicking Go  

---

## Emergency Undo

If you accidentally closed all jobs:

1. Open admin
2. Go to Job posts
3. Select all jobs
4. Action: "Open selected jobs"
5. Click Go

**OR** use the command line:
```bash
python manage.py shell
from jobs.models import JobPost
JobPost.objects.all().update(status='Open')
exit()
```

---

## Performance Tips

- 🚀 Use **bulk actions** for multiple jobs
- 🚀 **Filters** help narrow down large lists
- 🚀 **Pagination** - don't overwhelm page with too many
- 🚀 **Search** when looking for specific jobs

---

**Version:** 1.0  
**Last Updated:** January 15, 2026
