from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
import json
from datetime import timedelta

class CustomUser(AbstractUser):
    STUDENT = 'STUDENT'
    RECRUITER = 'RECRUITER'
    TPO = 'TPO'
    ROLE_CHOICES = [
        (STUDENT, 'Student'),
        (RECRUITER, 'Recruiter'),
        (TPO, 'TPO'),
    ]
    role_type = models.CharField(max_length=20, choices=ROLE_CHOICES, default=STUDENT)

    @property
    def is_student(self):
        return self.role_type == self.STUDENT

    @property
    def is_recruiter(self):
        return self.role_type == self.RECRUITER

    @property
    def is_tpo(self):
        return self.role_type == self.TPO or self.is_superuser

class StudentProfile(models.Model):
    """Student Profile - Tracks academic details and verification status"""
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='student_profile')
    roll_no = models.CharField(max_length=30, unique=True, null=True, blank=True)
    branch = models.CharField(max_length=100, blank=True)
    tenth_percent = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    twelfth_percent = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    cgpa = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True)
    active_backlogs = models.IntegerField(default=0)
    skills = models.TextField(blank=True, help_text="Comma separated skills")
    resume = models.FileField(upload_to='resumes/', null=True, blank=True)
    profile_photo = models.ImageField(upload_to='profile_photos/', null=True, blank=True, help_text="Your profile photo")
    portfolio_url = models.URLField(blank=True, help_text="Portfolio or LinkedIn URL")
    cover_letter_template = models.TextField(blank=True)
    
    # Verification
    is_verified = models.BooleanField(default=False)
    is_blacklisted = models.BooleanField(default=False, help_text="Blacklisted by TPO - cannot apply")
    blacklist_reason = models.TextField(blank=True)
    verified_by = models.ForeignKey(CustomUser, null=True, blank=True, on_delete=models.SET_NULL, 
                                    related_name='verified_students', limit_choices_to={'role_type': 'TPO'})
    verified_at = models.DateTimeField(null=True, blank=True)
    
    # Email & Phone verification
    email_verified = models.BooleanField(default=False)
    phone_verified = models.BooleanField(default=False)
    phone_number = models.CharField(max_length=20, blank=True)
    
    created_at = models.DateTimeField(null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # ============================================================
    # ADVANCED FEATURES: Placement Credit Score System (TIER 1)
    # ============================================================
    credit_score = models.IntegerField(
        default=100, 
        help_text="Placement Credit Score: 0-100. Starts at 100. Decreases with penalties."
    )
    is_blocked = models.BooleanField(
        default=False, 
        help_text="Blocked from applying due to low PCS (< 50)"
    )
    blocked_until = models.DateTimeField(
        null=True, 
        blank=True, 
        help_text="Cooling period end date (15 days)"
    )
    block_reason = models.CharField(
        max_length=500, 
        blank=True,
        help_text="Reason for blocking (shows to student)"
    )
    pcs_history = models.TextField(
        blank=True, 
        help_text="JSON history of all PCS changes"
    )
    
    # PCS Configuration (DO NOT MODIFY)
    PCS_THRESHOLDS = {
        'CRITICAL': 50,      # Block if below this
        'WARNING': 70,       # Show warning
        'GOOD': 85,          # Good standing
        'EXCELLENT': 95      # Excellent
    }
    
    PCS_PENALTIES = {
        'missed_interview': 20,
        'rejected_offer': 50,
        'ghosted_interview': 15,
        'rejected_after_accepted': 40
    }
    
    COOLING_PERIOD_DAYS = 15

    def __str__(self):
        return f"{self.user.username} Profile"

    def can_apply_for_jobs(self):
        """Check if student can apply for jobs"""
        # Auto-unblock if cooling period ended
        self.unblock_if_eligible()
        
        # Check all blocking conditions
        if not self.is_verified or self.is_blacklisted:
            return False
        if self.cgpa is None or self.active_backlogs is None:
            return False
        if self.is_blocked:
            return False
        return True
    
    def update_pcs(self, penalty_type, reason=""):
        """
        Update PCS and check for blocking
        
        Args:
            penalty_type: Key from PCS_PENALTIES dict
            reason: Additional reason text (e.g., "Missed TCS interview")
        
        Returns:
            new_pcs_score (int)
        
        Example:
            >>> student.student_profile.update_pcs('missed_interview', 'TCS Round 1')
            80
        """
        import json
        from datetime import timedelta
        
        # Validate penalty type
        if penalty_type not in self.PCS_PENALTIES:
            raise ValueError(f"Invalid penalty type: {penalty_type}. "
                           f"Must be one of: {list(self.PCS_PENALTIES.keys())}")
        
        # Calculate new score
        penalty = self.PCS_PENALTIES[penalty_type]
        old_score = self.credit_score
        self.credit_score = max(0, self.credit_score - penalty)
        
        # Record in history (JSON)
        history = json.loads(self.pcs_history or '[]')
        history.append({
            'timestamp': timezone.now().isoformat(),
            'type': penalty_type,
            'penalty': penalty,
            'old_score': old_score,
            'new_score': self.credit_score,
            'reason': reason
        })
        self.pcs_history = json.dumps(history)
        
        # Check if blocking is needed
        if self.credit_score < self.PCS_THRESHOLDS['CRITICAL']:
            self.is_blocked = True
            self.blocked_until = timezone.now() + timedelta(days=self.COOLING_PERIOD_DAYS)
            self.block_reason = (f"Low Placement Credit Score ({self.credit_score}/100). "
                               f"Blocked until {self.blocked_until.date()}. "
                               f"Reason: {reason}")
        
        self.save()
        return self.credit_score
    
    def unblock_if_eligible(self):
        """
        Check and remove block if cooling period is over.
        Called automatically before apply checks.
        
        Returns:
            True if unblocked, False otherwise
        """
        if self.is_blocked and self.blocked_until:
            if timezone.now() >= self.blocked_until:
                self.is_blocked = False
                self.blocked_until = None
                self.block_reason = ""
                self.save()
                return True
        return False
    
    def get_pcs_status(self):
        """
        Return human-readable PCS status.
        
        Returns:
            'Excellent' (95+) | 'Good' (85+) | 'Warning' (70+) | 'Critical' (<70)
        """
        if self.credit_score >= self.PCS_THRESHOLDS['EXCELLENT']:
            return 'Excellent'
        elif self.credit_score >= self.PCS_THRESHOLDS['GOOD']:
            return 'Good'
        elif self.credit_score >= self.PCS_THRESHOLDS['WARNING']:
            return 'Warning'
        else:
            return 'Critical'


class RecruiterProfile(models.Model):
    """Recruiter Profile - Tracks company and recruiter details"""
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='recruiter_profile')
    company_name = models.CharField(max_length=200)
    company_website = models.URLField(blank=True)
    company_email = models.EmailField()
    contact_phone = models.CharField(max_length=20, blank=True)
    description = models.TextField(blank=True, help_text="Company description")
    industry = models.CharField(max_length=100, blank=True)
    
    # HR Contact
    hr_contact_email = models.EmailField(blank=True)
    hr_contact_phone = models.CharField(max_length=20, blank=True)
    
    # Approval Status
    is_approved = models.BooleanField(default=False, help_text="Approved by TPO to post jobs")
    is_blocked = models.BooleanField(default=False, help_text="Blocked by TPO from posting")
    approved_by = models.ForeignKey(CustomUser, null=True, blank=True, on_delete=models.SET_NULL,
                                    related_name='approved_recruiters', limit_choices_to={'role_type': 'TPO'})
    approved_at = models.DateTimeField(null=True, blank=True)
    blocked_reason = models.TextField(blank=True)
    block_reason = models.TextField(blank=True)
    
    created_at = models.DateTimeField(null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.company_name} - {self.user.username}"

    def can_post_jobs(self):
        """Check if recruiter can post jobs"""
        return self.is_approved and not self.is_blocked


class EligibilityRule(models.Model):
    """Global eligibility rules set by TPO"""
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    min_cgpa = models.DecimalField(max_digits=4, decimal_places=2, default=0.0)
    max_active_backlogs = models.IntegerField(default=2)
    is_active = models.BooleanField(default=True)
    created_by = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True,
                                   limit_choices_to={'role_type': 'TPO'})
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
