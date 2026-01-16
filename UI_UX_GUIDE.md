# UI/UX Guide - Smart Internship & Placement Portal

## Overview
This document details the complete User Interface and User Experience design for the Smart Internship & Placement Portal with role-based dashboards and beautiful, responsive layouts.

---

## 1. Design System

### Color Palette
```
Primary:        #0b2545 (Dark Navy)
Secondary:      #1e40af (Royal Blue)
Accent:         #f59e0b (Amber/Gold)
Success:        #10b981 (Green)
Danger:         #ef4444 (Red)
Warning:        #d97706 (Orange)
Light BG:       #f9fafb (Off-white)
Border:         #e5e7eb (Light Gray)
```

### Typography
- **Font Family**: Segoe UI, Tahoma, Geneva, Verdana, sans-serif
- **Headings**: Font-weight 600-700
- **Body**: Font-weight 400
- **Labels**: Font-weight 500-600

### Spacing
- **Padding**: 8px, 12px, 15px, 20px, 25px, 30px
- **Margin**: 5px, 10px, 15px, 20px, 30px, 40px
- **Border Radius**: 6px, 8px, 12px

---

## 2. Base Template Structure

### Navigation Layout
```
┌─────────────────────────────────────────────┐
│           SIDEBAR (Fixed 260px)  │ TOP NAV  │
│  • Logo & Brand                │ Welcome  │
│  • Role Badge                  │ Time     │
│  • Navigation Sections         │          │
│  • Role-Based Menu Items       │          │
│  • Account Section             │          │
├─────────────────────────────────────────────┤
│                                              │
│  CONTENT AREA (Flex, scrollable)           │
│                                              │
│                                              │
│                                              │
│                                              │
├─────────────────────────────────────────────┤
│ © 2026 Smart Internship & Placement Portal │
└─────────────────────────────────────────────┘
```

### Sidebar Navigation Items

**For Students:**
- Dashboard → My Dashboard
- Browse Jobs
- My Profile

**For Recruiters:**
- Dashboard → Company Dashboard
- Post New Job
- Company Profile

**For TPO:**
- Dashboard → Analytics Dashboard
- Verify Students
- Approve Recruiters
- Export Reports

---

## 3. Home Page (Landing)

### Hero Section
- **Background**: Linear gradient (Dark Navy → Royal Blue)
- **Content**: 
  - Title: "Smart Internship & Placement Portal"
  - Subtitle: "Connecting talented students with leading companies..."
  - CTA Buttons: Student Register | Recruiter Register | Login

### Features Section
**6 Key Features Displayed:**
1. **Smart Job Discovery** - AI-powered eligibility matching
2. **Secure & Verified** - TPO verification system
3. **Real-time Analytics** - Comprehensive dashboards
4. **Eligibility-Based Filtering** - Auto-filtered job matching
5. **One-Click Resume Download** - Batch ZIP download
6. **Real-Time Notifications** - Status update alerts

### System Statistics (if logged in)
- Active Students (with icon)
- Active Jobs (with icon)
- Companies Registered (with icon)
- Total Placements (with icon)

---

## 4. Student Dashboard

### Layout: Header + Profile Card + Stats + Table

#### Profile Card
```
┌─ Profile Status ──────────────────────────────┐
│  Academic Profile          │  Verification     │
│  • Roll No                 │  Status: ✓ Verified
│  • Branch                 │  (TPO verified)
│  • CGPA                   │  [Edit Profile Btn]
│  • Active Backlogs        │
└───────────────────────────────────────────────┘
```

#### Statistics Cards (4 columns)
1. Total Applications (icon: document)
2. Pending Applications (icon: hourglass)
3. Selected (icon: check)
4. Rejected (icon: times)

#### Applications Table
| Company & Job | Job Type | Package | Applied | Status | Action |
|---|---|---|---|---|---|
| TCS - Software Engineer | Full-time | ₹8.5 LPA | Dec 15, 2025 | Shortlisted ⭐ | View |
| Infosys - Intern | Internship | ₹5.0 LPA | Dec 10, 2025 | Selected ✓ | View |

**Status Badges:**
- Pending (Yellow) 
- Shortlisted (Blue with star)
- Selected (Green with checkmark)
- Rejected (Red with X)

---

## 5. Job Listing Page

### Filter Sidebar (Left)
```
┌─ Filters ──────────────────┐
│ Salary Range              │
│  [___] - [___]            │
│ Job Type                  │
│  ☐ Full-time             │
│  ☐ Internship            │
│  ☐ PPO                   │
│ CGPA Required             │
│  [___]                    │
│ Backlogs Allowed          │
│  [___]                    │
│ Branch                    │
│  ☐ CS/IT                 │
│  ☐ Mechanical            │
│ [Reset] [Apply Filters]  │
└────────────────────────────┘
```

### Job Cards Grid (Right)
```
┌─ TCS - Software Engineer ─────────────────┐
│ Job Type: Full-time                      │
│ Package: ₹8.5 LPA                        │
│ Criteria: CGPA ≥ 3.0 | Backlogs ≤ 1     │
│ Posted: 5 days ago                       │
│ Deadline: Dec 25, 2025                   │
│                                           │
│ [View Details] [Apply]                  │
│ ✓ You are eligible for this job         │
└────────────────────────────────────────────┘
```

**Eligibility Indicators:**
- ✓ Green: "You are eligible"
- ⚠ Yellow: "CGPA requirement not met"
- ✗ Red: "You have exceeded backlog limit"

---

## 6. Job Detail Page

### Header
- Company Name & Logo
- Job Title
- Posted by: Company & Date
- Deadline with countdown

### Content Sections
1. **Job Overview**
   - Description
   - Responsibilities
   - Requirements

2. **Hiring Criteria**
   - Min CGPA: 3.2
   - Max Backlogs: 1
   - Branches: CS, IT, ECE
   - Job Type: Full-time
   - Package: ₹8.5 LPA

3. **Your Eligibility**
   ```
   ✓ CGPA Check: Your CGPA (3.8) ≥ Required (3.2)
   ✓ Backlog Check: Your Backlogs (0) ≤ Allowed (1)
   ✓ Branch Check: Your Branch (CS) is eligible
   
   [Apply Now] Button (Green)
   ```

4. **Application History** (if applied before)
   - Current Status
   - Applied on: Date
   - Status Updates Timeline

### CTA Buttons
- [Apply Now] - Prominent green button
- [Share] - Social sharing
- [Save] - Bookmark job

---

## 7. Recruiter Dashboard

### Layout: Header + Company Status + Stats + Jobs Table

#### Company Status Card
```
┌─ Company Info ────────────────┬─ Approval Status ──┐
│ Company: TCS                  │ ✓ Approved        │
│ Email: recruiter@tcs.com      │ (Ready to post)   │
│ Website: www.tcs.com          │ [Edit Profile]    │
└────────────────────────────────┴───────────────────┘
```

#### Statistics (4 columns)
1. Jobs Posted: 5
2. Applications: 127
3. Shortlisted: 23
4. Selected: 8

#### Job Management Table
| Job Title | Criteria | Job Type | Package | Deadline | Status | Actions |
|---|---|---|---|---|---|---|
| SE - Bangalore | CGPA≥3.2 Backlogs≤1 | Full-time | ₹8.5 LPA | Dec 25 | 🟢 Open | View Edit |
| Intern - Mumbai | CGPA≥3.0 Backlogs≤2 | Internship | ₹5.0 LPA | Dec 20 | 🔴 Closed | View Edit |

**Status Indicator:**
- 🟢 Open (Green circle) - Accepting applications
- 🔴 Closed (Red circle) - No longer accepting

#### Job Actions
- **View**: See applications and shortlisted candidates
- **Edit**: Modify job details
- **Download**: Download shortlisted resumes as ZIP

---

## 8. Application Management (Recruiter View)

### Candidates Table
| Candidate Name | CGPA | Backlogs | Branch | Status | Actions |
|---|---|---|---|---|---|
| Aditya Singh | 3.8 | 0 | CS | Pending | ★ Shortlist ✓ Select ✗ Reject |
| Priya Sharma | 3.5 | 1 | IT | Shortlisted | ⭐ ✓ Select ✗ Reject |
| Rohit Kumar | 3.2 | 0 | CS | Selected | 📋 Interview Schedule |

### Bulk Actions
- [Download Shortlisted Resumes (ZIP)] - Orange button
- [Send Bulk Interview Invites]
- [Batch Status Update]

---

## 9. TPO Dashboard (Analytics)

### Layout: Header + Stats Cards + Charts + Tables

#### Statistics (4 cards)
```
┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐
│ 👥 Total    │  │ ✅ Verified │  │ 🏢 Companies│  │ 🎓 Placed   │
│ Students    │  │  Students   │  │  Registered │  │  Students   │
│   450       │  │    320      │  │     25      │  │    185      │
└─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘
```

#### Charts
1. **Applications Trend** (Line Chart)
   - X-axis: Days of week
   - Y-axis: Number of applications
   - Shows weekly application patterns

2. **Placement Status** (Doughnut Chart)
   - Placed (Green): 45%
   - Interviewing (Amber): 28%
   - Applied (Blue): 18%
   - Rejected (Red): 9%

#### Pending Tasks - Student Verifications
| Name | CGPA | Backlogs | Action |
|---|---|---|---|
| John Doe | 3.6 | 0 | [Verify] |
| Jane Smith | 3.2 | 1 | [Verify] |

**Empty State**: ✅ All students verified!

#### Pending Tasks - Recruiter Approvals
| Company | Contact | Email | Action |
|---|---|---|---|
| Accenture | Priya | recruiter@accenture.com | [Approve] |
| Cognizant | Rahul | rahul@cog.com | [Approve] |

**Empty State**: ✅ All recruiters approved!

#### Top Companies by Package
| Company | Package (LPA) | Jobs Posted |
|---|---|---|
| Google | ₹45 | 3 |
| Microsoft | ₹42 | 2 |
| TCS | ₹8.5 | 5 |

#### Recent Placements
| Student | Company | Package (LPA) | Date |
|---|---|---|---|
| Aditya Singh | Google | ₹45 | Dec 15, 2025 |
| Priya Sharma | Microsoft | ₹42 | Dec 14, 2025 |

---

## 10. Forms & Input Elements

### Registration Forms

#### Student Registration
```
First Name:        [Text Input]
Last Name:         [Text Input]
Email:             [Email Input]
Username:          [Text Input]
Password:          [Password Input]
Confirm Password:  [Password Input]
Roll Number:       [Text Input]
Branch:            [Dropdown: CS, IT, ECE...]
10th %:            [Number Input]
12th %:            [Number Input]
Resume:            [File Upload] (PDF/DOC)
Skills:            [Textarea]

[Create Account] Button (Primary Blue)
Already registered? [Login]
```

#### Recruiter Registration
```
Full Name:         [Text Input]
Email:             [Email Input]
Password:          [Password Input]
Company Name:      [Text Input]
Company Email:     [Email Input]
Company Website:   [URL Input]
Contact Phone:     [Phone Input]

[Register] Button (Primary Blue)
Already registered? [Login]
```

### Profile Edit Forms
- **Editable Fields**: All text fields
- **Non-editable (after TPO verification)**: CGPA, Backlogs, 10th%, 12th%
- **Status**: Shows "Verified - Cannot edit" message
- Save Changes button (Primary Blue)

---

## 11. Responsive Design

### Breakpoints
```
Mobile (< 768px):
- Sidebar hidden by default, toggle with hamburger menu
- Single column layout
- Cards stack vertically
- Smaller fonts & padding

Tablet (768px - 1024px):
- Sidebar visible but narrower (180px)
- 2-column grid layouts
- Tables scroll horizontally if needed

Desktop (> 1024px):
- Full layout
- Sidebar 260px wide
- Multi-column grids
- Full table visibility
```

### Mobile Navigation
```
☰ (Hamburger) | Logo | 👤 User
```

---

## 12. Status Badges & Indicators

### Application Status
- **Pending**: Yellow background, hourglass icon
- **Shortlisted**: Blue background, star icon
- **Selected**: Green background, checkmark icon
- **Rejected**: Red background, X icon

### Approval Status
- **Approved**: Green checkmark, "Profile Approved"
- **Pending**: Amber hourglass, "Pending Approval"
- **Blocked**: Red ban icon, "Blocked"
- **Verified**: Green checkmark, "Verified by TPO"

### Job Status
- **Open**: Green circle, accepting applications
- **Closed**: Red circle, no longer accepting

---

## 13. Error & Success Messages

### Alert Messages
```
✓ Success (Green)
Registration successful! Please complete your profile.

⚠ Warning (Amber)
Your CGPA doesn't meet the requirement for this job.

✗ Error (Red)
Failed to submit application. Please try again.

ℹ Info (Blue)
Your profile is pending TPO verification.
```

### Form Validation
```
Invalid email format!
Username already taken
Password too short (minimum 8 characters)
This field is required
```

---

## 14. Animations & Transitions

### Hover Effects
- Cards: Slight upward translation + shadow increase
- Buttons: Color darken + shadow
- Links: Color highlight + underline

### Slide-in Animation
- Alert messages appear with fade-in and slide-down
- Page transitions: Fade-in effect

### Transitions
- All interactive elements: 0.3s ease
- Smooth page transitions

---

## 15. Accessibility Features

### WCAG 2.1 Compliance
- **Color Contrast**: All text meets WCAG AA standards
- **Font Sizes**: Minimum 12px for body text
- **Focus States**: Clear keyboard navigation
- **Alt Text**: All icons have hover tooltips
- **Semantic HTML**: Proper heading hierarchy

### Screen Reader Support
- Form labels properly associated with inputs
- Button text clearly describes action
- Status messages announced
- Tables have proper header rows

---

## 16. Print Stylesheet

### Printable Reports
- TPO can print placement analytics
- Recruiters can print applications
- Students can print application history

---

## 17. Dark Mode Support (Future)

Prepared for future dark mode implementation:
```css
@media (prefers-color-scheme: dark) {
    :root {
        --light-bg: #1f2937;
        --card-bg: #111827;
        /* etc. */
    }
}
```

---

## 18. Performance Optimization

### Load Times
- Hero images lazy-loaded
- Charts rendered after initial paint
- Large tables paginated (20 items per page)
- CSS compressed and minified
- JavaScript deferred

### Caching
- Static assets: 1-month cache
- API responses: 5-minute cache for analytics
- User session: 30-day timeout

---

## 19. Mobile App Considerations

### Responsive Image Sizes
```
Mobile:  max-width: 100%, 12px font
Tablet:  max-width: 50%, 14px font
Desktop: max-width: 33%, 16px font
```

### Touch Targets
- Minimum button size: 48px × 48px
- Link padding: 8px minimum

---

## 20. Testing Checklist

### Visual Testing
- [ ] All pages render correctly on mobile/tablet/desktop
- [ ] Color contrast meets WCAG AA
- [ ] Fonts load properly
- [ ] Images display correctly
- [ ] Animations are smooth

### Functional Testing
- [ ] All buttons work
- [ ] Forms validate correctly
- [ ] Filters update results
- [ ] Charts render with data
- [ ] Responsive navigation works

### Cross-Browser Testing
- [ ] Chrome/Edge (Latest)
- [ ] Firefox (Latest)
- [ ] Safari (Latest)
- [ ] Mobile browsers (iOS Safari, Chrome Mobile)

---

## 21. Future Enhancements

1. **Dark Mode**: Full dark theme support
2. **Mobile App**: iOS/Android native apps
3. **Video Interviews**: In-platform video interview scheduling
4. **AI Recommendations**: Job recommendations based on profile
5. **Email Notifications**: Integration with email service
6. **SMS Alerts**: Critical alerts via SMS
7. **Social Sharing**: Share job postings
8. **Advanced Analytics**: Predictive placement analytics

---

## 22. Design Hand-off Guide

### For Developers
- All colors defined in CSS root variables
- Spacing values consistent throughout
- Font weights standardized
- Responsive breakpoints documented
- Animation timing constants

### For Designers
- Base design system in Figma
- Component library available
- Color accessibility guidelines
- Typography scale defined
- Grid system (12-column)

---

**Document Version**: 1.0  
**Last Updated**: January 15, 2026  
**Author**: EY 4.0 AVCOE Development Team
