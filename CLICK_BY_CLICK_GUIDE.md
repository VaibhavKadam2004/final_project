# 🖱️ CLICK-BY-CLICK INSTRUCTIONS

## SIMPLE 5-CLICK WORKFLOW

### **CLICK 1: Dashboard**
```
URL: http://127.0.0.1:8000/accounts/recruiter/dashboard/

You should see:
- "Your Job Postings" section
- Table with your posted jobs
```

---

### **CLICK 2: View Applications Button**
```
In the "Your Job Postings" table:

┌─────────────┬────────┬──────────┬─────────────┐
│ Job Title   │Package │ Deadline │ Actions     │
├─────────────┼────────┼──────────┼─────────────┤
│ Python Dev  │₹12 LPA │ Feb 01   │ [📄] 👁️ ✏️  │◄── CLICK HERE (📄)
│             │        │          │             │
└─────────────┴────────┴──────────┴─────────────┘

Click the 📄 icon (FILE ICON)
NOT the 👁️ (eye icon) or ✏️ (pencil icon)
```

**What happens:**
- New page loads showing "Applications for [Job Title]"
- Shows list of all students who applied

---

### **CLICK 3: Update Button**
```
In the Applications table:

┌──────────────┬──────────┬──────┬──────┬──────────┬──────┐
│ Student Name │ Email    │ CGPA │ BL   │ Status   │Action│
├──────────────┼──────────┼──────┼──────┼──────────┼──────┤
│ Raj Kumar    │ raj@...  │ 8.7  │ 0    │ Pending  │[Upd.]│◄── CLICK HERE
│ 2023CSE101   │          │      │      │          │      │
└──────────────┴──────────┴──────┴──────┴──────────┴──────┘

Click [Upd.] button on the candidate you want to update
```

**What happens:**
- Popup modal appears
- Shows candidate name at top
- Shows dropdown for status selection
- Shows text area for notes

---

### **CLICK 4: Select Status from Dropdown**
```
┌──────────────────────────────────────┐
│ Update Application Status            │
├──────────────────────────────────────┤
│ Raj Kumar                            │
│                                      │
│ New Status *                         │
│ ┌────────────────────────────────┐  │
│ │ -- Select Status --        ▼   │  │
│ │ Pending             ✓           │  │
│ │ Shortlisted                     │  │◄── CLICK & SELECT
│ │ Selected                        │  │
│ │ Rejected                        │  │
│ └────────────────────────────────┘  │
└──────────────────────────────────────┘

Click on the dropdown arrow ▼
Select one option:
- Shortlisted (for interview)
- Selected (give offer)
- Rejected (not selected)
```

**What happens:**
- Dropdown shows 4 options
- You select one
- Option is highlighted

---

### **CLICK 5: Add Note (Optional)**
```
┌──────────────────────────────────────┐
│ Update Application Status            │
├──────────────────────────────────────┤
│ New Status                           │
│ Shortlisted                          │
│                                      │
│ Add Note (Optional)                  │
│ ┌────────────────────────────────┐  │
│ │ Good resume, selected for R1   │  │◄── CLICK & TYPE
│ │                                │  │
│ │                                │  │
│ └────────────────────────────────┘  │
│                                      │
│        [Cancel] [Update Status]      │
└──────────────────────────────────────┘

Click in the text area
Type your note (optional)
Examples:
- "Good resume"
- "Selected for technical round"
- "Excellent coding skills"
- "Scheduled for interview on Jan 20"
```

**What happens:**
- Text area is focused
- You can type freely
- Any length is fine

---

### **CLICK 6: Update Status Button**
```
┌──────────────────────────────────────┐
│ Update Application Status            │
├──────────────────────────────────────┤
│ New Status                           │
│ Shortlisted                          │
│                                      │
│ Add Note                             │
│ Good resume, Round 1 on Jan 20       │
│                                      │
│        [Cancel] [Update Status] ◄────CLICK HERE
└──────────────────────────────────────┘

Click the blue [Update Status] button
```

**What happens:**
- Modal closes
- Page refreshes
- Success message shows: "✓ Application status updated to Shortlisted"
- Candidate's status changes in table
- Page stays on applications list

---

## 🎯 EXAMPLE: START TO FINISH

### **Initial View - Recruiter Dashboard**
```
Step 1: You see your jobs
┌─────────────────────────┐
│ Your Job Postings       │
├─────────────────────────┤
│ Python Dev     [📄] 👁️ ✏️ │◄── CLICK 📄
│ Data Science   [📄] 👁️ ✏️ │
│ DevOps Eng     [📄] 👁️ ✏️ │
└─────────────────────────┘
```

### **After CLICK 2 - Applications List**
```
Step 2: Applications load
┌────────────────────────────────┐
│ Applications for Python Dev    │
├────────────────────────────────┤
│ Total: 15                      │
├────────────────────────────────┤
│ Raj Kumar   Pending  [Upd.] ◄──CLICK [Upd.]
│ Priya S.   Pending  [Upd.]
│ Arjun V.   Pending  [Upd.]
└────────────────────────────────┘
```

### **After CLICK 3 - Modal Opens**
```
Step 3: Modal popup
┌─────────────────────────────┐
│ Update: Raj Kumar           │
├─────────────────────────────┤
│ Status: [-- Select --  ▼]◄──CLICK
│         Shortlisted
│         Selected
│         Rejected
│                             │
│ Note: [_________________]◄──TYPE
│       "Round 1 on Jan 20"    │
│                             │
│ [Cancel] [Update Status]◄──CLICK
└─────────────────────────────┘
```

### **After CLICK 6 - Success!**
```
Step 4: Status updated
┌────────────────────────────────┐
│ ✓ Application status updated   │
│   to Shortlisted               │
├────────────────────────────────┤
│ Raj Kumar   ⭐ Shortlisted [Upd.]
│ Priya S.   ⏳ Pending      [Upd.]
│ Arjun V.   ⏳ Pending      [Upd.]
└────────────────────────────────┘
```

---

## 📍 WHERE TO FIND BUTTONS

### **Recruiter Dashboard Page**
```
Location of "View Applications" button:

┌──────────────────────────────────┐
│ Recruiter Dashboard              │
├──────────────────────────────────┤
│ [Post New Job]                   │
├──────────────────────────────────┤
│ Your Job Postings                │
│ ┌────────────────────────────┐   │
│ │ Job Title   | Actions      │   │
│ ├────────────────────────────┤   │
│ │ Python Dev │ [📄] 👁️ ✏️    │   │ ◄──RIGHT SIDE
│ │ Data Sci   │ [📄] 👁️ ✏️    │   │   OF TABLE
│ │ DevOps     │ [📄] 👁️ ✏️    │   │
│ └────────────────────────────┘   │
└──────────────────────────────────┘

The 📄 icon is what you need!
```

### **Applications List Page**
```
Location of "Update" buttons:

┌─────────────────────────────────────┐
│ Applications for Python Developer   │
├─────────────────────────────────────┤
│ [Statistics cards]                  │
├─────────────────────────────────────┤
│ Candidates                          │
│ ┌─────────────────────────────────┐ │
│ │ Name | Email | CGPA | Action    │ │
│ ├─────────────────────────────────┤ │
│ │ Raj  | ...   │ 8.7  │ [Upd.] ◄───RIGHT SIDE
│ │ Priya| ...   │ 8.9  │ [Upd.]     │ OF ROW
│ │ Arjun| ...   │ 7.8  │ [Upd.]     │
│ └─────────────────────────────────┘ │
└─────────────────────────────────────┘

Each row has an [Upd.] button!
```

---

## ⌨️ KEYBOARD SHORTCUTS

Not needed, but good to know:

```
Tab key → Move between fields
Enter → Select from dropdown (if open)
Ctrl+Enter → Submit form (may work)
Escape → Close modal
```

---

## 🔍 HOW TO TELL IF IT'S WORKING

### ✅ You'll know it's working when:

1. **After CLICK 1 (Dashboard):**
   - [ ] URL shows: `http://127.0.0.1:8000/accounts/recruiter/dashboard/`
   - [ ] You see "Your Job Postings" section
   - [ ] You see a table with your jobs

2. **After CLICK 2 (View Apps):**
   - [ ] URL shows: `http://127.0.0.1:8000/jobs/recruiter/1/applications/`
   - [ ] Page title says "Applications for [Job Title]"
   - [ ] You see list of students who applied

3. **After CLICK 3 (Update):**
   - [ ] A popup modal appears
   - [ ] Modal shows student name
   - [ ] Modal has status dropdown
   - [ ] Modal has notes text area

4. **After CLICK 4 (Select Status):**
   - [ ] Dropdown shows 4 options
   - [ ] Selected option is highlighted
   - [ ] You can see the option you selected

5. **After CLICK 5 (Add Note):**
   - [ ] Cursor is in text area (blinking line)
   - [ ] Your text appears as you type
   - [ ] Text is visible in the box

6. **After CLICK 6 (Update):**
   - [ ] Modal closes
   - [ ] Success message appears at top
   - [ ] Candidate's status in table changes
   - [ ] You're still on the same page

---

## ❌ TROUBLESHOOTING BY SYMPTOM

### **Symptom: Can't find 📄 button**
```
Solution:
1. Check you're logged in as RECRUITER
2. Check page shows "Your Job Postings"
3. Scroll right if buttons are cut off
4. If nothing works, refresh page (F5)
```

### **Symptom: Modal doesn't open when click Update**
```
Solution:
1. Refresh page (F5)
2. Try clicking the [Upd.] button again
3. Check browser console for errors (F12)
4. Try different candidate
```

### **Symptom: Update button is disabled/greyed out**
```
Solution:
1. Application might be closed
2. Job might be closed
3. You might not own this job
4. Try selecting different status
```

### **Symptom: Note didn't save**
```
Solution:
1. Make sure you clicked [Update Status]
2. Don't click [Cancel]
3. Check success message appeared
4. Refresh to see if it was saved
```

### **Symptom: Wrong page shows**
```
Solution:
1. Check URL is correct
2. Scroll down to see all content
3. Page might be loading, wait a moment
4. Refresh page (F5)
```

---

## 📱 MOBILE/RESPONSIVE DESIGN

Same workflow works on:
- ✅ Desktop
- ✅ Tablet
- ✅ Mobile

Just adjust your viewport!

---

## 🎓 PRACTICE EXERCISE

1. Login as recruiter
2. Find a job with "Pending" applications
3. Click 📄 View Applications
4. Click [Upd.] on first candidate
5. Select "Shortlisted"
6. Add note: "Good resume"
7. Click [Update Status]
8. Verify status changed
9. Repeat with different status
10. Verify statistics updated

**Estimated time:** 5-10 minutes

---

**You're ready! Let's go manage those applications! 🚀**
