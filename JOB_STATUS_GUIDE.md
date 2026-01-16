# How to View Job Application Status

## Quick Navigation

### For Students:

#### **Option 1: From Student Dashboard** ✨
1. Log in to your student account
2. You'll be redirected to the **Student Dashboard**
3. Click the blue button: **"View Full Application Status & Timeline"**
4. This takes you to `/jobs/student/applications/` - your dedicated applications tracking page

#### **Option 2: Direct URL**
Navigate directly to: `http://localhost:8000/jobs/student/applications/`

---

## Application Status Tracking Page Features

### **Dashboard Statistics**
At the top, you'll see 4 key metrics:
- 📋 **Total Applications** - How many jobs you've applied for
- ⏳ **Shortlisted** - Count of jobs where you've been shortlisted
- ✅ **Selected** - Count of jobs where you've been selected
- ❌ **Rejected** - Count of rejected applications

### **Applications Table**
A comprehensive table showing:
- **Company** - Name of the hiring company
- **Position** - Job title you applied for
- **Applied Date** - When you submitted your application
- **Status** - Current application status (with color-coded badges)
- **Actions** - "View Details" button to see full job posting

### **Application Status Levels**

| Status | Icon | Color | Meaning |
|--------|------|-------|---------|
| **Applied** | 📄 | Blue | Your application is under review |
| **Shortlisted** | ⭐ | Orange | You've passed initial screening |
| **Interviewing** | 📞 | Purple | Interview scheduled or in progress |
| **Selected** | ✅ | Green | Congratulations! You're hired |
| **Rejected** | ❌ | Red | Application not selected |

---

## Real-Time Updates

### Auto-Refresh Feature
- The page **automatically refreshes every 30 seconds**
- No need to manually refresh to see status updates
- You'll get the latest information in real-time

### Manual Refresh
- Press **F5** or **Ctrl+R** (Windows) / **Cmd+R** (Mac) to manually refresh
- Or click your browser's refresh button

---

## How Status Updates Work

### 1. **When You Apply**
- Status = **"Applied"** (immediately)
- Your application enters the recruiter's queue

### 2. **After Initial Screening**
- Status = **"Shortlisted"** (recruiter marks you eligible)
- You pass resume/profile screening

### 3. **Interview Scheduling**
- Status = **"Interviewing"** (interview scheduled)
- Recruiter will update this after scheduling

### 4. **Final Decision**
- Status = **"Selected"** ✅ - You got the job!
- OR Status = **"Rejected"** ❌ - Application not selected

---

## API Endpoint (For Developers)

### Check Individual Application Status
**Endpoint:** `GET /jobs/api/application/<app_id>/status/`

**Example Response:**
```json
{
    "id": 42,
    "job": {
        "id": 5,
        "title": "Software Engineer",
        "company": "TechCorp"
    },
    "status": "Shortlisted",
    "applied_at": "2026-01-15T10:30:00Z"
}
```

### Example Usage (JavaScript/AJAX):
```javascript
// Fetch status of application with ID 42
fetch('/jobs/api/application/42/status/')
    .then(response => response.json())
    .then(data => console.log(data))
    .catch(error => console.error('Error:', error));
```

---

## Filter & Pagination

### View Multiple Pages
- Applications are shown **10 per page**
- Use pagination buttons at the bottom to navigate
- First, Previous, Next, Last page navigation available

### View by Status
- The statistics cards help you quickly see how many applications are in each status
- Click on individual applications to see full details

---

## Troubleshooting

### ❓ "No Applications Yet" Message
- You haven't applied for any jobs yet
- Click **"Browse Jobs"** button to see available positions
- Make sure your profile is verified by TPO first

### ❓ Eligibility Restrictions
Students can only see and apply for jobs where:
- ✅ Your CGPA >= Job's Minimum CGPA requirement
- ✅ Your Active Backlogs <= Job's Maximum Allowed Backlogs
- ✅ Your profile is **verified by TPO**
- ✅ You are **not blacklisted**

### ❓ Status Not Updating?
- Reload the page with **F5**
- Check if recruiter has updated your status
- Contact TPO if status is stuck for a week

---

## Important Notes

1. **Profile Verification Required**: You must have a verified profile before applying for jobs
2. **Automatic Filtering**: Only eligible jobs are shown based on your CGPA and backlogs
3. **Unique Applications**: You can only apply once per job (no duplicate applications)
4. **Eligibility Check**: System automatically verifies eligibility before allowing your application

---

## Contact & Support

For issues or questions about your application status:
- Contact: **TPO Office** 
- Email: Check your dashboard for contact details
- In-person: Visit during office hours

---

**Last Updated:** January 15, 2026  
**Version:** 1.0
