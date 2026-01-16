from django.db import models
from django.conf import settings
from django.utils import timezone

class JobPost(models.Model):
    STATUS_OPEN = 'Open'
    STATUS_CLOSED = 'Closed'
    STATUS_CHOICES = [
        (STATUS_OPEN, 'Open'),
        (STATUS_CLOSED, 'Closed'),
    ]
    
    JOB_TYPE_CHOICES = [
        ('Full-time', 'Full-time'),
        ('Internship', 'Internship'),
        ('PPO', 'PPO')
    ]
    
    title = models.CharField(max_length=200)
    company = models.CharField(max_length=200)
    description = models.TextField()
    posted_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, 
                                  related_name='job_posts', limit_choices_to={'role_type': 'RECRUITER'})
    min_cgpa = models.DecimalField(max_digits=4, decimal_places=2, default=0.00)
    max_backlogs = models.IntegerField(default=0)
    branches = models.CharField(max_length=200, blank=True, help_text="Comma separated branch names")
    job_type = models.CharField(max_length=50, choices=JOB_TYPE_CHOICES, default='Internship')
    package = models.DecimalField(max_digits=9, decimal_places=2, null=True, blank=True)
    deadline = models.DateTimeField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_OPEN)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-deadline']
        indexes = [
            models.Index(fields=['status', 'deadline']),
            models.Index(fields=['posted_by']),
        ]

    def __str__(self):
        return f"{self.title} at {self.company}"

    def is_open_for_applications(self):
        """Check if job is open and deadline hasn't passed"""
        return self.status == self.STATUS_OPEN and timezone.now() <= self.deadline

    def can_be_closed_by(self, user):
        """Only recruiter who posted or TPO can close"""
        return user == self.posted_by or getattr(user, 'is_tpo', False)
    
    # ============================================================
    # ADVANCED FEATURES: Eligibility Gatekeeper (TIER 2)
    # ============================================================
    
    def check_student_eligibility(self, student):
        """
        Check if student meets ALL job requirements.
        
        Args:
            student: CustomUser instance
        
        Returns:
            Tuple: (is_eligible: bool, reasons: list)
                   reasons = [] if eligible
                   reasons = ["Reason 1", "Reason 2"] if not
        
        Example:
            >>> eligible, reasons = job.check_student_eligibility(student)
            >>> if not eligible:
            >>>     print(reasons[0])  # "Minimum CGPA required: 7.5..."
        """
        student_profile = student.student_profile
        reasons = []
        
        # 1. CGPA CHECK
        if student_profile.cgpa is None:
            reasons.append("❌ Profile incomplete: Please enter your CGPA")
        elif student_profile.cgpa < self.min_cgpa:
            reasons.append(
                f"❌ CGPA too low: Minimum required {self.min_cgpa} "
                f"(Your CGPA: {student_profile.cgpa})"
            )
        
        # 2. BACKLOG CHECK
        if student_profile.active_backlogs > self.max_backlogs:
            reasons.append(
                f"❌ Too many backlogs: Maximum allowed {self.max_backlogs} "
                f"(Your backlogs: {student_profile.active_backlogs})"
            )
        
        # 3. BRANCH CHECK
        if self.branches:
            allowed_branches = [b.strip() for b in self.branches.split(',')]
            if student_profile.branch not in allowed_branches:
                reasons.append(
                    f"❌ Branch not eligible: Your branch '{student_profile.branch}' "
                    f"is not in allowed branches: {', '.join(allowed_branches)}"
                )
        
        # 4. PCS CHECK (if PCS system is enabled)
        if hasattr(student_profile, 'is_blocked') and student_profile.is_blocked:
            reasons.append(
                f"❌ Blocked: {student_profile.block_reason} "
                f"Contact TPO at tpo@college.edu to appeal"
            )
        
        # 5. VERIFICATION CHECK
        if not student_profile.is_verified:
            reasons.append(
                "❌ Not verified: Your profile must be verified by TPO first. "
                "Contact TPO for verification."
            )
        
        # 6. BLACKLIST CHECK
        if student_profile.is_blacklisted:
            reasons.append(
                f"❌ Blacklisted: {student_profile.blacklist_reason} "
                f"You are permanently blocked from applying."
            )
        
        # 7. PROFILE COMPLETENESS CHECK
        if not student_profile.resume:
            reasons.append("❌ Missing resume: Upload your resume in profile settings")
        
        is_eligible = len(reasons) == 0
        return is_eligible, reasons
    
    def get_eligibility_badge(self, student):
        """
        Get badge info for eligibility display.
        
        Returns:
            dict: {
                'icon': '✅' or '🔒',
                'text': 'Eligible' or 'Locked',
                'color': 'success' or 'warning',
                'can_apply': True or False,
                'reasons': [] or [reasons]
            }
        
        Use in template:
            {% with badge=job.get_eligibility_badge request.user %}
                Icon: {{ badge.icon }}
                Text: {{ badge.text }}
                Can apply: {{ badge.can_apply }}
            {% endwith %}
        """
        is_eligible, reasons = self.check_student_eligibility(student)
        
        if is_eligible:
            return {
                'icon': '✅',
                'text': 'Eligible',
                'color': 'success',
                'can_apply': True,
                'reasons': []
            }
        else:
            return {
                'icon': '🔒',
                'text': 'Locked',
                'color': 'warning',
                'can_apply': False,
                'reasons': reasons
            }


class Application(models.Model):
    STATUS_PENDING = 'Pending'
    STATUS_SHORTLISTED = 'Shortlisted'
    STATUS_SELECTED = 'Selected'
    STATUS_REJECTED = 'Rejected'
    STATUS_CHOICES = [
        (STATUS_PENDING, 'Pending'),
        (STATUS_SHORTLISTED, 'Shortlisted'),
        (STATUS_SELECTED, 'Selected'),
        (STATUS_REJECTED, 'Rejected'),
    ]

    job = models.ForeignKey(JobPost, on_delete=models.CASCADE, related_name='applications')
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, 
                                limit_choices_to={'role_type': 'STUDENT'})
    applied_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_PENDING)
    is_closed = models.BooleanField(default=False, help_text="Application closed - no modifications allowed")
    closed_at = models.DateTimeField(null=True, blank=True)
    
    # ============================================================
    # ADVANCED FEATURES: SLA Tracking (TIER 1)
    # ============================================================
    status_last_updated_at = models.DateTimeField(
        null=True, 
        blank=True,
        help_text="When status was last changed by recruiter"
    )
    first_status_change_at = models.DateTimeField(
        null=True, 
        blank=True,
        help_text="When first moved from Pending status"
    )
    response_time_hours = models.IntegerField(
        null=True, 
        blank=True,
        help_text="Hours from deadline to first update"
    )

    class Meta:
        unique_together = ('job', 'student')
        indexes = [
            models.Index(fields=['student', 'status']),
            models.Index(fields=['job', 'status']),
        ]

    def __str__(self):
        return f"{self.student.username} - {self.job.title}"

    def can_change_status(self, user):
        """
        Only recruiter who posted the job can change status.
        Cannot change if application is closed.
        """
        if self.is_closed:
            return False, "Cannot modify closed applications"
        if self.job.posted_by != user:
            return False, "Only the recruiter who posted the job can update status"
        if self.job.status == JobPost.STATUS_CLOSED:
            return False, "Cannot update applications for closed jobs"
        return True, ""

    def close_application(self):
        """Close application - locks it from further modifications"""
        self.is_closed = True
        self.closed_at = timezone.now()
        self.save()

    def add_status(self, new_status, user, note=''):
        """Update status with validation"""
        can_change, message = self.can_change_status(user)
        if not can_change:
            raise PermissionError(message)
        
        self.status = new_status
        self.save()
        ApplicationStatus.objects.create(
            application=self, 
            status=new_status, 
            updated_by=user,
            note=note
        )


class ApplicationStatus(models.Model):
    """History of application status changes - immutable audit trail"""
    application = models.ForeignKey('Application', on_delete=models.CASCADE, related_name='status_history')
    status = models.CharField(max_length=20, choices=Application.STATUS_CHOICES)
    timestamp = models.DateTimeField(auto_now_add=True)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True,
                                   limit_choices_to={'role_type': 'RECRUITER'})
    note = models.TextField(blank=True)

    class Meta:
        ordering = ['timestamp']
        indexes = [
            models.Index(fields=['application', 'timestamp']),
        ]

    def __str__(self):
        return f"{self.application} - {self.status} @ {self.timestamp}"


class InterviewSchedule(models.Model):
    """Interview scheduling - Recruiter schedules, Student views"""
    ROUND_CHOICES = [
        ('Round 1', 'Round 1'),
        ('Round 2', 'Round 2'),
        ('Round 3', 'Round 3'),
        ('HR Round', 'HR Round'),
        ('Final', 'Final'),
    ]
    
    application = models.ForeignKey(Application, on_delete=models.CASCADE, related_name='interviews')
    round = models.CharField(max_length=20, choices=ROUND_CHOICES)
    scheduled_date = models.DateTimeField()
    location = models.CharField(max_length=200, blank=True, help_text="Interview location or online link")
    interviewer_notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, 
                                   null=True, limit_choices_to={'role_type': 'RECRUITER'})
    
    class Meta:
        ordering = ['-scheduled_date']
    
    def __str__(self):
        return f"{self.application.student.username} - {self.round}"

# ============================================
# INTERNSHIP-SPECIFIC MODELS
# ============================================

class InternshipPost(models.Model):
    """Internship posting with detailed requirements"""
    STATUS_DRAFT = 'Draft'
    STATUS_APPROVED = 'Approved'
    STATUS_PUBLISHED = 'Published'
    STATUS_CLOSED = 'Closed'
    STATUS_CHOICES = [
        (STATUS_DRAFT, 'Draft'),
        (STATUS_APPROVED, 'Approved by Admin'),
        (STATUS_PUBLISHED, 'Published'),
        (STATUS_CLOSED, 'Closed'),
    ]
    
    title = models.CharField(max_length=200)
    company = models.CharField(max_length=200)
    description = models.TextField()
    skills_required = models.TextField(help_text="Comma separated skills")
    duration_weeks = models.IntegerField(help_text="Duration in weeks")
    stipend_per_month = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    is_paid = models.BooleanField(default=True)
    is_remote = models.BooleanField(default=False)
    location = models.CharField(max_length=200, blank=True)
    start_date = models.DateField()
    end_date = models.DateField()
    
    posted_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                  related_name='internship_posts', limit_choices_to={'role_type': 'RECRUITER'})
    approved_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True,
                                    related_name='approved_internships', limit_choices_to={'role_type': 'TPO'})
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_DRAFT)
    min_cgpa = models.DecimalField(max_digits=4, decimal_places=2, default=0.00)
    max_backlogs = models.IntegerField(default=0)
    branches = models.CharField(max_length=200, blank=True, help_text="Comma separated branches")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['status', 'start_date']),
            models.Index(fields=['posted_by']),
        ]
    
    def __str__(self):
        return f"{self.title} at {self.company}"


class InternshipApplication(models.Model):
    """Application for internship - extended with cover letter and resume"""
    STATUS_APPLIED = 'Applied'
    STATUS_SHORTLISTED = 'Shortlisted'
    STATUS_INTERVIEW = 'Interview'
    STATUS_SELECTED = 'Selected'
    STATUS_REJECTED = 'Rejected'
    STATUS_COMPLETED = 'Completed'
    STATUS_CANCELLED = 'Cancelled'
    
    STATUS_CHOICES = [
        (STATUS_APPLIED, 'Applied'),
        (STATUS_SHORTLISTED, 'Shortlisted'),
        (STATUS_INTERVIEW, 'Interview'),
        (STATUS_SELECTED, 'Selected'),
        (STATUS_REJECTED, 'Rejected'),
        (STATUS_COMPLETED, 'Completed'),
        (STATUS_CANCELLED, 'Cancelled'),
    ]
    
    internship = models.ForeignKey(InternshipPost, on_delete=models.CASCADE, related_name='applications')
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                related_name='internship_applications', limit_choices_to={'role_type': 'STUDENT'})
    resume = models.FileField(upload_to='internship_resumes/')
    cover_letter = models.TextField()
    applied_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_APPLIED)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ('internship', 'student')
        ordering = ['-applied_at']
        indexes = [
            models.Index(fields=['student', 'status']),
            models.Index(fields=['internship', 'status']),
        ]
    
    def __str__(self):
        return f"{self.student.username} - {self.internship.title}"


class InternshipInterview(models.Model):
    """Interview scheduling for internship applications"""
    TYPE_ONLINE = 'Online'
    TYPE_OFFLINE = 'Offline'
    TYPE_PHONE = 'Phone'
    TYPE_CHOICES = [
        (TYPE_ONLINE, 'Online'),
        (TYPE_OFFLINE, 'Offline'),
        (TYPE_PHONE, 'Phone'),
    ]
    
    STATUS_SCHEDULED = 'Scheduled'
    STATUS_COMPLETED = 'Completed'
    STATUS_CANCELLED = 'Cancelled'
    STATUS_CHOICES = [
        (STATUS_SCHEDULED, 'Scheduled'),
        (STATUS_COMPLETED, 'Completed'),
        (STATUS_CANCELLED, 'Cancelled'),
    ]
    
    application = models.ForeignKey(InternshipApplication, on_delete=models.CASCADE, related_name='interviews')
    scheduled_date = models.DateTimeField()
    interview_type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    interview_link = models.URLField(blank=True, help_text="For online interviews")
    location = models.CharField(max_length=200, blank=True, help_text="For offline interviews")
    notes = models.TextField(blank=True)
    
    conducted_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
                                    null=True, blank=True, limit_choices_to={'role_type': 'RECRUITER'})
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_SCHEDULED)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-scheduled_date']
    
    def __str__(self):
        return f"Interview - {self.application.student.username}"


class InternshipCompletion(models.Model):
    """Track internship completion, feedback, and certificates"""
    STATUS_IN_PROGRESS = 'In Progress'
    STATUS_SUBMITTED = 'Submitted'
    STATUS_REVIEWED = 'Reviewed'
    STATUS_COMPLETED = 'Completed'
    STATUS_CHOICES = [
        (STATUS_IN_PROGRESS, 'In Progress'),
        (STATUS_SUBMITTED, 'Submitted'),
        (STATUS_REVIEWED, 'Reviewed'),
        (STATUS_COMPLETED, 'Completed'),
    ]
    
    application = models.OneToOneField(InternshipApplication, on_delete=models.CASCADE,
                                      related_name='completion')
    
    # Work submission
    work_submission = models.TextField(blank=True, help_text="Work completed during internship")
    submission_date = models.DateTimeField(null=True, blank=True)
    
    # Feedback
    recruiter_feedback = models.TextField(blank=True)
    student_feedback = models.TextField(blank=True)
    
    # Ratings
    recruiter_rating = models.IntegerField(null=True, blank=True, choices=[(i, f"{i} Stars") for i in range(1, 6)])
    student_rating = models.IntegerField(null=True, blank=True, choices=[(i, f"{i} Stars") for i in range(1, 6)])
    
    # Certificate
    certificate = models.FileField(upload_to='certificates/', null=True, blank=True)
    certificate_issued_date = models.DateTimeField(null=True, blank=True)
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_IN_PROGRESS)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Completion - {self.application.student.username}"


# ============================================
# NOTIFICATION & FEEDBACK MODELS
# ============================================

class Notification(models.Model):
    """System notifications for users"""
    TYPE_APPLICATION = 'Application'
    TYPE_INTERVIEW = 'Interview'
    TYPE_SELECTION = 'Selection'
    TYPE_REJECTION = 'Rejection'
    TYPE_CERTIFICATE = 'Certificate'
    TYPE_ANNOUNCEMENT = 'Announcement'
    TYPE_CHOICES = [
        (TYPE_APPLICATION, 'Application'),
        (TYPE_INTERVIEW, 'Interview'),
        (TYPE_SELECTION, 'Selection'),
        (TYPE_REJECTION, 'Rejection'),
        (TYPE_CERTIFICATE, 'Certificate'),
        (TYPE_ANNOUNCEMENT, 'Announcement'),
    ]
    
    CHANNEL_EMAIL = 'Email'
    CHANNEL_SMS = 'SMS'
    CHANNEL_INAPP = 'In-App'
    CHANNEL_CHOICES = [
        (CHANNEL_EMAIL, 'Email'),
        (CHANNEL_SMS, 'SMS'),
        (CHANNEL_INAPP, 'In-App'),
    ]
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='notifications')
    notification_type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    title = models.CharField(max_length=200)
    message = models.TextField()
    channel = models.CharField(max_length=20, choices=CHANNEL_CHOICES, default=CHANNEL_INAPP)
    
    is_read = models.BooleanField(default=False)
    is_sent = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(auto_now_add=True)
    read_at = models.DateTimeField(null=True, blank=True)
    sent_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', 'is_read']),
        ]
    
    def __str__(self):
        return f"{self.title} - {self.user.username}"


class StudentFeedback(models.Model):
    """Student feedback on internship experience"""
    internship_application = models.OneToOneField(InternshipApplication, on_delete=models.CASCADE,
                                                 related_name='feedback')
    rating = models.IntegerField(choices=[(i, f"{i} Stars") for i in range(1, 6)])
    feedback_text = models.TextField()
    would_recommend = models.BooleanField(default=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Feedback - {self.internship_application.student.username}"


class StudentSkill(models.Model):
    """Track student skills and proficiency"""
    PROFICIENCY_BEGINNER = 'Beginner'
    PROFICIENCY_INTERMEDIATE = 'Intermediate'
    PROFICIENCY_ADVANCED = 'Advanced'
    PROFICIENCY_EXPERT = 'Expert'
    PROFICIENCY_CHOICES = [
        (PROFICIENCY_BEGINNER, 'Beginner'),
        (PROFICIENCY_INTERMEDIATE, 'Intermediate'),
        (PROFICIENCY_ADVANCED, 'Advanced'),
        (PROFICIENCY_EXPERT, 'Expert'),
    ]
    
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                               related_name='skills', limit_choices_to={'role_type': 'STUDENT'})
    skill_name = models.CharField(max_length=100)
    proficiency_level = models.CharField(max_length=20, choices=PROFICIENCY_CHOICES)
    years_of_experience = models.DecimalField(max_digits=3, decimal_places=1, default=0)
    
    added_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('student', 'skill_name')
    
    def __str__(self):
        return f"{self.student.username} - {self.skill_name}"


class OTPVerification(models.Model):
    """OTP-based email and phone verification"""
    TYPE_EMAIL = 'Email'
    TYPE_PHONE = 'Phone'
    TYPE_CHOICES = [
        (TYPE_EMAIL, 'Email'),
        (TYPE_PHONE, 'Phone'),
    ]
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='otp_verifications')
    verification_type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    otp_code = models.CharField(max_length=6)
    is_verified = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    verified_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"OTP - {self.user.username} ({self.verification_type})"
    
    def is_expired(self):
        """Check if OTP has expired"""
        return timezone.now() > self.expires_at
    
    def is_valid(self):
        """Check if OTP is valid"""
        return not self.is_expired() and not self.is_verified


class AdminAnnouncement(models.Model):
    """TPO announcements for students and companies"""
    AUDIENCE_ALL = 'All'
    AUDIENCE_STUDENTS = 'Students'
    AUDIENCE_COMPANIES = 'Companies'
    AUDIENCE_CHOICES = [
        (AUDIENCE_ALL, 'All Users'),
        (AUDIENCE_STUDENTS, 'Students Only'),
        (AUDIENCE_COMPANIES, 'Companies Only'),
    ]
    
    title = models.CharField(max_length=200)
    description = models.TextField()
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
                                  null=True, limit_choices_to={'role_type': 'TPO'})
    target_audience = models.CharField(max_length=20, choices=AUDIENCE_CHOICES, default=AUDIENCE_ALL)
    
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return self.title
    
    def is_active_now(self):
        """Check if announcement is currently active"""
        now = timezone.now()
        if not self.is_active:
            return False
        if self.expires_at and now > self.expires_at:
            return False
        return True


# ============================================================
# ADVANCED FEATURES: Eligibility Gatekeeper (TIER 2)
# ============================================================

# ADD THESE METHODS TO JobPost CLASS (after can_be_closed_by method):
"""
    def check_student_eligibility(self, student):
        \"\"\"
        Check if student meets ALL job requirements.
        
        Args:
            student: CustomUser instance
        
        Returns:
            Tuple: (is_eligible: bool, reasons: list)
                   reasons = [] if eligible
                   reasons = ["Reason 1", "Reason 2"] if not
        
        Example:
            >>> eligible, reasons = job.check_student_eligibility(student)
            >>> if not eligible:
            >>>     print(reasons[0])  # "Minimum CGPA required: 7.5..."
        \"\"\"
        student_profile = student.student_profile
        reasons = []
        
        # 1. CGPA CHECK
        if student_profile.cgpa is None:
            reasons.append("❌ Profile incomplete: Please enter your CGPA")
        elif student_profile.cgpa < self.min_cgpa:
            reasons.append(
                f"❌ CGPA too low: Minimum required {self.min_cgpa} "
                f"(Your CGPA: {student_profile.cgpa})"
            )
        
        # 2. BACKLOG CHECK
        if student_profile.active_backlogs > self.max_backlogs:
            reasons.append(
                f"❌ Too many backlogs: Maximum allowed {self.max_backlogs} "
                f"(Your backlogs: {student_profile.active_backlogs})"
            )
        
        # 3. BRANCH CHECK
        if self.branches:
            allowed_branches = [b.strip() for b in self.branches.split(',')]
            if student_profile.branch not in allowed_branches:
                reasons.append(
                    f"❌ Branch not eligible: Your branch '{student_profile.branch}' "
                    f"is not in allowed branches: {', '.join(allowed_branches)}"
                )
        
        # 4. PCS CHECK (if PCS system is enabled)
        if hasattr(student_profile, 'is_blocked') and student_profile.is_blocked:
            reasons.append(
                f"❌ Blocked: {student_profile.block_reason} "
                f"Contact TPO at tpo@college.edu to appeal"
            )
        
        # 5. VERIFICATION CHECK
        if not student_profile.is_verified:
            reasons.append(
                "❌ Not verified: Your profile must be verified by TPO first. "
                "Contact TPO for verification."
            )
        
        # 6. BLACKLIST CHECK
        if student_profile.is_blacklisted:
            reasons.append(
                f"❌ Blacklisted: {student_profile.blacklist_reason} "
                f"You are permanently blocked from applying."
            )
        
        # 7. PROFILE COMPLETENESS CHECK
        if not student_profile.resume:
            reasons.append("❌ Missing resume: Upload your resume in profile settings")
        
        is_eligible = len(reasons) == 0
        return is_eligible, reasons
    
    def get_eligibility_badge(self, student):
        \"\"\"
        Get badge info for eligibility display.
        
        Returns:
            dict: {
                'icon': '✅' or '🔒',
                'text': 'Eligible' or 'Locked',
                'color': 'success' or 'warning',
                'can_apply': True or False,
                'reasons': [] or [reasons]
            }
        
        Use in template:
            {% with badge=job.get_eligibility_badge request.user %}
                Icon: {{ badge.icon }}
                Text: {{ badge.text }}
                Can apply: {{ badge.can_apply }}
            {% endwith %}
        \"\"\"
        is_eligible, reasons = self.check_student_eligibility(student)
        
        if is_eligible:
            return {
                'icon': '✅',
                'text': 'Eligible',
                'color': 'success',
                'can_apply': True,
                'reasons': []
            }
        else:
            return {
                'icon': '🔒',
                'text': 'Locked',
                'color': 'warning',
                'can_apply': False,
                'reasons': reasons
            }
"""


# ============================================================
# ADVANCED FEATURES: NEW MODELS
# ============================================================

class DreamCompany(models.Model):
    """
    Student's selected dream company for career planning (TIER 2 FEATURE).
    
    Each student has ONE dream company at a time.
    Shows personalized roadmap based on historical hiring data.
    """
    student = models.OneToOneField(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE,
        related_name='dream_company', 
        limit_choices_to={'role_type': 'STUDENT'}
    )
    company_name = models.CharField(max_length=200)
    
    # Historical hiring requirements (populated from HistoricalHiringData)
    avg_cgpa_required = models.DecimalField(
        max_digits=4, 
        decimal_places=2, 
        default=7.0
    )
    common_skills = models.TextField(
        help_text="Comma separated skills (e.g., 'Python, Django, REST API')"
    )
    typical_interview_rounds = models.IntegerField(default=3)
    typical_feedback_days = models.IntegerField(default=5)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name_plural = "Dream Companies"
    
    def __str__(self):
        return f"{self.student.username} → {self.company_name}"
    
    def get_readiness_percentage(self):
        """
        Calculate how ready student is for dream company (0-100%).
        
        Scoring:
        - CGPA match: 40 points
        - Skills match: 40 points
        - Resume present: 10 points
        - Portfolio present: 10 points
        
        Returns:
            int: 0-100
        
        Example:
            >>> readiness = dream.get_readiness_percentage()
            >>> print(f"You are {readiness}% ready!")
        """
        student = self.student.student_profile
        score = 0
        
        # CGPA check (40 points)
        if student.cgpa and student.cgpa >= self.avg_cgpa_required:
            score += 40
        elif student.cgpa:
            ratio = float(student.cgpa) / float(self.avg_cgpa_required)
            score += int(40 * min(ratio, 1.0))
        
        # Skills check (40 points)
        required_skills = set(s.strip().lower() for s in self.common_skills.split(',') if s.strip())
        student_skills = set(s.strip().lower() for s in (student.skills or '').split(',') if s.strip())
        
        if required_skills:
            matched = len(required_skills.intersection(student_skills))
            score += int(40 * (matched / len(required_skills)))
        
        # Resume present (10 points)
        if student.resume:
            score += 10
        
        # Portfolio present (10 points)
        if student.portfolio_url:
            score += 10
        
        return min(100, score)
    
    def get_next_steps(self):
        """
        Return list of recommended next steps to prepare for dream company.
        
        Returns:
            list of dicts:
            [
                {
                    'priority': 'HIGH',
                    'task': 'Improve CGPA to 8.5',
                    'current': 7.8,
                    'target': 8.5
                },
                {
                    'priority': 'HIGH',
                    'task': 'Learn skills: Docker, Kubernetes',
                    'resources': 'Udemy, Coursera'
                }
            ]
        """
        student = self.student.student_profile
        steps = []
        
        # Step 1: CGPA improvement
        if not student.cgpa or student.cgpa < self.avg_cgpa_required:
            steps.append({
                'priority': 'HIGH',
                'task': f"Improve CGPA to {self.avg_cgpa_required}",
                'current': float(student.cgpa) if student.cgpa else 0,
                'target': float(self.avg_cgpa_required),
                'type': 'academic'
            })
        
        # Step 2: Missing skills
        required_skills = set(s.strip().lower() for s in self.common_skills.split(',') if s.strip())
        student_skills = set(s.strip().lower() for s in (student.skills or '').split(',') if s.strip())
        missing_skills = required_skills - student_skills
        
        if missing_skills:
            steps.append({
                'priority': 'HIGH',
                'task': f"Learn skills: {', '.join(missing_skills)}",
                'resources': 'LinkedIn Learning, Coursera, Udemy',
                'type': 'skills'
            })
        
        # Step 3: Resume
        if not student.resume:
            steps.append({
                'priority': 'MEDIUM',
                'task': "Upload or update your resume",
                'resources': 'Check sample resumes in portal resources',
                'type': 'resume'
            })
        
        # Step 4: Portfolio
        if not student.portfolio_url:
            steps.append({
                'priority': 'MEDIUM',
                'task': "Build and share your portfolio",
                'resources': 'GitHub, personal website, portfolio.dev',
                'type': 'portfolio'
            })
        
        return steps


class HistoricalHiringData(models.Model):
    """
    Aggregated hiring data from previous placements (TIER 2 FEATURE).
    
    TPO populates this by analyzing past placement drives.
    Used by Dream Company feature to set realistic targets.
    """
    company_name = models.CharField(max_length=200, unique=True)
    
    # Requirements
    avg_cgpa = models.DecimalField(max_digits=4, decimal_places=2)
    avg_backlogs = models.DecimalField(max_digits=4, decimal_places=2)
    most_common_skills = models.TextField(help_text="Comma separated")
    
    # Interview info
    avg_interview_rounds = models.IntegerField(default=3)
    avg_response_time_days = models.IntegerField(default=7)
    
    # Success metrics
    students_hired = models.IntegerField(default=0)
    total_applicants = models.IntegerField(default=1)
    success_rate = models.DecimalField(
        max_digits=5, 
        decimal_places=2, 
        default=0,
        help_text="(hired / applicants) * 100"
    )
    
    last_visited_date = models.DateField(auto_now=True)
    
    class Meta:
        ordering = ['-success_rate']
        verbose_name_plural = "Historical Hiring Data"
    
    def __str__(self):
        return f"{self.company_name} ({self.success_rate}% success, {self.students_hired} hired)"


class InterviewExperience(models.Model):
    """
    Student shares their interview experience (TIER 2 FEATURE).
    
    After interview result, student posts:
    - Questions asked in each round
    - Tips for preparation
    - Whether they were selected
    
    TPO approves before adding to Prep Vault.
    """
    # Status choices
    STATUS_PENDING = 'Pending'
    STATUS_APPROVED = 'Approved'
    STATUS_REJECTED = 'Rejected'
    STATUS_CHOICES = [
        (STATUS_PENDING, 'Pending TPO Approval'),
        (STATUS_APPROVED, 'Approved - Visible to Students'),
        (STATUS_REJECTED, 'Rejected by TPO'),
    ]
    
    # Round type choices
    ROUND_TYPE_CHOICES = [
        ('Online Test', 'Online Test / Assessment'),
        ('Technical', 'Technical Interview'),
        ('Coding', 'Coding Round'),
        ('HR', 'HR Round'),
        ('Case Study', 'Case Study'),
        ('Group Discussion', 'Group Discussion'),
        ('Aptitude', 'Aptitude Test'),
    ]
    
    DIFFICULTY_CHOICES = [
        ('Easy', 'Easy'),
        ('Medium', 'Medium'),
        ('Hard', 'Hard'),
    ]
    
    # Company & Job Info
    company = models.CharField(max_length=200)
    job_title = models.CharField(max_length=200)
    
    # Student who submitted
    student = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE,
        related_name='interview_experiences',
        limit_choices_to={'role_type': 'STUDENT'}
    )
    
    # Round details
    round_number = models.IntegerField()
    round_type = models.CharField(max_length=100, choices=ROUND_TYPE_CHOICES)
    duration_minutes = models.IntegerField(help_text="How long was the round?")
    difficulty = models.CharField(
        max_length=20, 
        choices=DIFFICULTY_CHOICES, 
        default='Medium'
    )
    
    # Experience details
    questions_asked = models.TextField(
        help_text="List each question on a new line"
    )
    your_experience = models.TextField(
        help_text="What did you discuss? What did you solve? Any challenges?"
    )
    tips_for_others = models.TextField(
        help_text="Advice for future candidates: what to study, what to prepare"
    )
    
    # Result
    selected_after = models.BooleanField(
        help_text="Were you selected/moved to next round after this?"
    )
    
    # Approval by TPO
    status = models.CharField(
        max_length=20, 
        choices=STATUS_CHOICES, 
        default=STATUS_PENDING
    )
    
    approved_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.SET_NULL,
        null=True, 
        blank=True, 
        related_name='approved_experiences',
        limit_choices_to={'role_type': 'TPO'}
    )
    
    # Stats
    created_at = models.DateTimeField(auto_now_add=True)
    views_count = models.IntegerField(default=0, help_text="How many students viewed this")
    helpful_count = models.IntegerField(default=0, help_text="How many marked as helpful")
    
    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = "Interview Experiences"
    
    def __str__(self):
        return f"{self.student.username} - {self.company} Round {self.round_number}"


class PrepVault(models.Model):
    """
    Aggregated prep material for a specific company (TIER 2 FEATURE).
    
    When student applies for a company, they can access:
    - All interview experiences from that company
    - Most commonly asked questions
    - Preparation tips from seniors
    """
    company = models.OneToOneField(
        HistoricalHiringData, 
        on_delete=models.CASCADE,
        related_name='prep_vault'
    )
    
    # Statistics
    total_experiences = models.IntegerField(
        default=0,
        help_text="Number of approved interview experiences"
    )
    most_asked_questions = models.TextField(
        blank=True,
        help_text="Top 10 questions (JSON array)"
    )
    difficulty_distribution = models.TextField(
        blank=True,
        help_text="Easy/Medium/Hard counts (JSON)"
    )
    
    # Recommendations
    recommended_topics = models.TextField(
        blank=True,
        help_text="Comma separated topics to study"
    )
    avg_interview_rounds = models.IntegerField(default=3)
    avg_selection_rate = models.DecimalField(
        max_digits=5, 
        decimal_places=2, 
        default=0,
        help_text="Percentage of students selected"
    )
    
    last_updated = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name_plural = "Prep Vaults"
    
    def __str__(self):
        return f"{self.company.company_name} Prep Vault"
    
    def get_approval_pending_count(self):
        """Count experiences awaiting TPO approval"""
        return InterviewExperience.objects.filter(
            company=self.company.company_name,
            status=InterviewExperience.STATUS_PENDING
        ).count()


class RecruiterResponseRating(models.Model):
    """
    Recruiter response time rating (TIER 1 FEATURE).
    
    Tracks how quickly each recruiter responds to applications.
    Displays "⭐⭐⭐⭐⭐ Very Fast Responder" on job postings.
    """
    recruiter = models.OneToOneField(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE,
        related_name='response_rating',
        limit_choices_to={'role_type': 'RECRUITER'}
    )
    
    # Response statistics
    avg_response_hours = models.IntegerField(default=0)
    total_jobs_posted = models.IntegerField(default=0)
    total_applications = models.IntegerField(default=0)
    responses_given = models.IntegerField(default=0)
    
    # Rating
    responsiveness_rating = models.DecimalField(
        max_digits=2, 
        decimal_places=1, 
        default=3.0,
        help_text="1.0 to 5.0 stars"
    )
    rating_label = models.CharField(max_length=50, default='Average')
    
    last_updated = models.DateTimeField(auto_now=True)
    
    # Rating thresholds (DO NOT MODIFY)
    RATING_THRESHOLDS = {
        (0, 24): ('⭐⭐⭐⭐⭐', 'Very Fast Responder', 5.0),
        (24, 72): ('⭐⭐⭐⭐', 'Fast Responder', 4.0),
        (72, 168): ('⭐⭐⭐', 'Average Responder', 3.0),
        (168, 336): ('⭐⭐', 'Slow Responder', 2.0),
        (336, float('inf')): ('⭐', 'Very Slow Responder', 1.0),
    }
    
    class Meta:
        verbose_name_plural = "Recruiter Response Ratings"
    
    def __str__(self):
        return f"{self.recruiter.recruiter_profile.company_name} - {self.rating_label}"
    
    def calculate_rating(self):
        """
        Calculate responsiveness rating from application data.
        
        Call this after applications are created/updated to recalculate ratings.
        
        Example:
            >>> rating = RecruiterResponseRating.objects.first()
            >>> rating.calculate_rating()
            >>> print(rating.rating_label)  # "Very Fast Responder"
        """
        from django.db.models import Avg
        
        # Get all applications for this recruiter
        applications = Application.objects.filter(
            job__posted_by=self.recruiter
        ).exclude(response_time_hours__isnull=True)
        
        if not applications.exists():
            self.avg_response_hours = 0
            self.responsiveness_rating = 3.0
            self.rating_label = 'No Data Yet'
            self.save()
            return
        
        # Calculate average response time
        avg_hours = int(
            applications.aggregate(Avg('response_time_hours'))
            ['response_time_hours__avg'] or 0
        )
        self.avg_response_hours = avg_hours
        self.total_applications = applications.count()
        self.responses_given = applications.filter(
            response_time_hours__isnull=False
        ).count()
        
        # Determine rating based on thresholds
        for (min_h, max_h), (emoji, label, rating) in self.RATING_THRESHOLDS.items():
            if min_h <= avg_hours < max_h:
                self.rating_label = label
                self.responsiveness_rating = rating
                break
        
        self.save()