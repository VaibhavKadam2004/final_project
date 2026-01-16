# 📌 SUMMARY: How to Open Your Closed Jobs

## The Problem
All your jobs are showing **"Closed"** status in the recruiter dashboard. Students cannot see or apply for closed jobs.

## The Solution
Change job status from **"Closed"** → **"Open"** using the Admin Panel.

---

## ⚡ FASTEST METHOD (1 minute)

### Step-by-Step:

**Step 1:** Open Admin Panel
```
URL: http://127.0.0.1:8000/admin/
Username: admin
Password: Admin@123
```

**Step 2:** Navigate to Jobs
```
Scroll down to "JOBS" section → Click "Job posts"
```

**Step 3:** Select All Jobs
```
Check the checkbox at TOP-LEFT next to "All"
(This selects ALL jobs on the page)
```

**Step 4:** Open All Jobs
```
Bottom of page: Action dropdown → Select "Open selected jobs"
Click "Go" button
```

**Step 5:** Confirm Success
```
Green message: "X job(s) have been opened."
✅ ALL JOBS NOW OPEN!
```

---

## ✅ What Happens After

| For Students | For Recruiters |
|---|---|
| See open jobs in "Browse Jobs" | View applications |
| Apply if eligible | Shortlist candidates |
| Track status in Dashboard | Accept/Reject applicants |

---

## 🎯 Eligibility Rules

Students will ONLY see your jobs if:
- ✅ Job status = **OPEN**
- ✅ Deadline = **FUTURE date**
- ✅ Student's CGPA ≥ Job's Min CGPA
- ✅ Student's Backlogs ≤ Job's Max Backlogs
- ✅ Student's profile = **VERIFIED** (by TPO)

---

## 📚 Detailed Guides

For more detailed information, see:
- **`HOW_TO_OPEN_JOBS.md`** - Complete step-by-step guide with screenshots
- **`QUICK_OPEN_JOBS.md`** - Quick reference card

---

## 🔧 Alternative Methods

### Method 2: Edit Individual Job
1. Admin → Job posts
2. Click job title
3. Change Status: "Closed" → "Open"
4. Click SAVE

### Method 3: Command Line (Advanced)
```bash
python manage.py shell
from jobs.models import JobPost
JobPost.objects.filter(status='Closed').update(status='Open')
exit()
```

---

## ⚠️ Troubleshooting

| Issue | Fix |
|-------|-----|
| Admin page won't load | Make sure Django server is running |
| Can't login to admin | Username: admin, Password: Admin@123 |
| Changes not saving | Click SAVE button (important!) |
| Jobs still showing Closed | Refresh browser with F5 |

---

## 🎓 Verification Checklist

After opening jobs:

- [ ] Server is running (`python manage.py runserver`)
- [ ] Jobs status changed to "Open" in admin
- [ ] Deadlines are future dates
- [ ] Student profiles verified by TPO
- [ ] Student CGPA meets job requirements
- [ ] Test: Login as student and browse jobs
- [ ] Test: Apply for a job as student
- [ ] Check: Applications appear in recruiter dashboard

---

## 📞 Quick Links

| Link | Purpose |
|------|---------|
| http://127.0.0.1:8000/ | Home page |
| http://127.0.0.1:8000/admin/ | Admin panel (opens jobs here) |
| http://127.0.0.1:8000/jobs/ | Browse jobs page |
| http://127.0.0.1:8000/accounts/login/ | Login page |

---

**Last Updated:** January 15, 2026  
**Status:** ✅ Ready to Use
