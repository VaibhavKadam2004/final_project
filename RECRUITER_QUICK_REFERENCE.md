# 🎯 RECRUITER QUICK REFERENCE CARD

## ONE-PAGE CHEAT SHEET

### **ACCESS THE FEATURE**

```
1. Login → http://127.0.0.1:8000/accounts/login/
2. Dashboard → /accounts/recruiter/dashboard/
3. View Apps → Click 📄 button on any job
4. Update → Click [Upd.] button on any candidate
```

---

## **THE 6 CLICKS**

| Click | Action | Location |
|-------|--------|----------|
| 1️⃣ | Go to Dashboard | Top menu or direct URL |
| 2️⃣ | Click 📄 (View Apps) | Right side of job row |
| 3️⃣ | Click [Update] | Right side of candidate row |
| 4️⃣ | Select Status | Dropdown in modal |
| 5️⃣ | Add Note | Text area in modal |
| 6️⃣ | Click [Update Status] | Blue button in modal |

---

## **STATUS OPTIONS**

```
⏳ Pending         (Default - Under review)
⭐ Shortlisted    (Selected for interview)
✅ Selected       (Offer given)
❌ Rejected       (Not selected)
```

---

## **GOOD NOTES EXAMPLES**

```
✅ "Shortlisted for technical round 1"
✅ "Failed coding test"
✅ "Excellent communication skills"
✅ "Selected, offer sent on Jan 15"
✅ "Interview scheduled for Jan 20"

❌ "ok"
❌ "no"
❌ "maybe"
```

---

## **WHAT YOU'LL SEE**

### **In Dashboard Table:**
```
Job Title | CGPA | Package | [📄] [👁️] [✏️]
                                   ↑
                            View Applications
```

### **In Applications Page:**
```
Header: Applications for [Job Title]
Stats: 15 Total | 8 Pending | 5 Short. | 2 Select.
Table: Candidate Name | Email | CGPA | Status | [Update]
```

### **In Modal:**
```
Status: [Dropdown]
Note: [Text Area]
Buttons: [Cancel] [Update Status]
```

---

## **URLS**

| Page | URL |
|------|-----|
| Dashboard | `/accounts/recruiter/dashboard/` |
| Applications | `/jobs/recruiter/{job_id}/applications/` |

---

## **RESTRICTIONS**

```
✅ CAN:
  - Update own job applications
  - Add notes
  - Change status multiple times
  - View all candidates

❌ CANNOT:
  - Update other recruiter's jobs
  - Change students' status
  - Modify closed applications
  - Update closed jobs
```

---

## **BUTTONS REFERENCE**

| Location | Button | Function |
|----------|--------|----------|
| Dashboard | 📄 | View Applications (NEW) |
| Dashboard | 👁️ | View Job Details |
| Dashboard | ✏️ | Edit Job |
| Applications | [Update] | Open status modal |
| Modal | [Cancel] | Close without saving |
| Modal | [Update Status] | Save changes |

---

## **SUCCESS SIGNS**

After update:
- ✅ Success message appears
- ✅ Status badge changes color
- ✅ Page stays on same location
- ✅ Statistics update automatically

---

## **TROUBLESHOOTING QUICK FIX**

| Problem | Solution |
|---------|----------|
| Can't find 📄 button | Logged in as recruiter? |
| Modal won't open | Refresh (F5) and try again |
| Status won't update | Click [Update Status] not Cancel |
| Can't access job | Did you post this job? |
| App is closed | Can't modify closed applications |

---

## **TIPS**

```
💡 Use descriptive notes - Helps remember decisions
💡 Update quickly - Students want to know status soon
💡 Review CGPA - Ensure students meet requirements
💡 Schedule after shortlist - Don't delay interviews
💡 Check deadline - Respond before job closes
```

---

## **WORKFLOW EXAMPLE**

```
Day 1: Application comes in → Status: Pending
Day 2: You review → Update to "Shortlisted" 
       Note: "Good resume"
Day 3: After interview → Update to "Selected"
       Note: "Excellent coding skills, offer sent"
Day 4: Application locked (cannot modify)
```

---

## **KEYBOARD SHORTCUTS**

```
Tab → Move between fields
Enter → Select from dropdown
Escape → Close modal
F5 → Refresh page
```

---

## **WHAT GETS SAVED**

✅ New Status
✅ Your Note
✅ Date & Time
✅ Recruiter Name
✅ Application History

---

## **STATISTICS EXPLAINED**

```
Total Applications = All students who applied
Pending = Waiting for review
Shortlisted = Selected for interview
Selected = Offer given
Rejected = Not selected (locked)
```

---

## **COMMON WORKFLOW**

```
1. Check dashboard statistics
2. Open applications page
3. Review each candidate
4. Update status (Shortlist good ones)
5. Add descriptive notes
6. Schedule interviews
7. Update after interviews
8. Send offers
```

---

## **KEY FACTS**

```
📍 Only you can update YOUR job applications
🔒 Closed applications cannot be changed
⏱️ Timestamps recorded automatically
📝 All notes are saved to database
🔄 Status history is kept
📊 Statistics update in real-time
```

---

## **QUICK REFERENCE**

```
Login → Dashboard → 📄 → Update → Submit ✓
```

---

**Print this card and keep it handy! 📋**

Last Updated: January 15, 2026
