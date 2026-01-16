# Enhanced Internship & Placement Portal - Database Schema Updates

## New Models & Fields to Add

This document outlines all database models needed for the complete internship workflow.

### 1. StudentProfile Enhancements (EXISTING - MINOR UPDATES)
```
- Add: email_verified (Boolean) - OTP/email verification status
- Add: phone_verified (Boolean) - Phone verification status
- Add: cover_letter_template (TextField) - Default cover letter
- Add: portfolio_url (URLField) - Portfolio/LinkedIn URL
```

### 2. InternshipPost (NEW MODEL)
Extends JobPost specifically for internships with more details:
```
- title: CharField - Internship title
- company: ForeignKey to RecruiterProfile
- description: TextField
- skills_required: TextField - comma separated
- duration_weeks: IntegerField - duration in weeks
- stipend_per_month: DecimalField - monthly stipend
- location: CharField - internship location
- is_paid: Boolean
- is_remote: Boolean
- start_date: DateField
- end_date: DateField
- posted_by: ForeignKey to User (Recruiter)
- approved_by_admin: Boolean
- status: Choices (Draft, Approved, Published, Closed)
- created_at: DateTimeField
- updated_at: DateTimeField
```

### 3. InternshipApplication (NEW MODEL)
Replaces Application for internships:
```
- internship: ForeignKey to InternshipPost
- student: ForeignKey to User (Student)
- resume: FileField - uploaded resume
- cover_letter: TextField
- applied_at: DateTimeField
- status: Choices (Applied, Shortlisted, Interview, Selected, Rejected, Completed)
- interview_schedule: ForeignKey to InterviewSchedule
- created_at: DateTimeField
- updated_at: DateTimeField
```

### 4. InterviewSchedule (NEW MODEL)
```
- application: ForeignKey to InternshipApplication
- scheduled_date: DateTimeField
- interview_type: Choices (Online, Offline, Phone)
- interview_link: URLField (for online)
- location: CharField (for offline)
- notes: TextField
- conducted_by: ForeignKey to User (Recruiter/HR)
- status: Choices (Scheduled, Completed, Cancelled)
- created_at: DateTimeField
```

### 5. InternshipCompletion (NEW MODEL)
Tracks internship completion and feedback:
```
- internship_application: ForeignKey to InternshipApplication
- work_submission: TextField - work completed
- submission_date: DateTimeField
- recruiter_feedback: TextField
- student_rating: IntegerField - 1-5 stars
- company_rating: IntegerField - 1-5 stars (student rates company)
- certificate_url: FileField - issued certificate
- certificate_issued_date: DateTimeField
- status: Choices (In Progress, Submitted, Reviewed, Completed)
- created_at: DateTimeField
```

### 6. Notification (NEW MODEL)
For email/SMS notifications:
```
- user: ForeignKey to User
- notification_type: Choices (Application, Interview, Selection, Certificate)
- title: CharField
- message: TextField
- is_read: Boolean
- is_sent: Boolean
- sent_via: Choices (Email, SMS, InApp)
- created_at: DateTimeField
- read_at: DateTimeField (nullable)
```

### 7. StudentFeedback (NEW MODEL)
For feedback and ratings:
```
- student: ForeignKey to User (Student)
- internship: ForeignKey to InternshipPost
- rating: IntegerField (1-5)
- feedback_text: TextField
- created_at: DateTimeField
```

### 8. StudentSkills (NEW MODEL)
Tracks student skills:
```
- student: ForeignKey to User
- skill_name: CharField
- proficiency_level: Choices (Beginner, Intermediate, Advanced, Expert)
- years_of_experience: DecimalField
- added_at: DateTimeField
```

### 9. OTPVerification (NEW MODEL)
For OTP-based email/phone verification:
```
- user: ForeignKey to User
- verification_type: Choices (Email, Phone)
- otp_code: CharField
- is_verified: Boolean
- created_at: DateTimeField
- expires_at: DateTimeField
- verified_at: DateTimeField (nullable)
```

### 10. AdminAnnouncement (NEW MODEL)
For admin notifications:
```
- title: CharField
- description: TextField
- created_by: ForeignKey to User (TPO)
- target_audience: Choices (All, Students, Companies)
- is_active: Boolean
- created_at: DateTimeField
- expires_at: DateTimeField
```

## Migration Steps:

1. Add new models to jobs/models.py
2. Create and apply migrations
3. Run database migrations
4. Create forms for all new models
5. Create views and templates
6. Update URL routing
