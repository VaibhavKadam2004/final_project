# 🔧 MODEL CHANGES - COMPLETE CODE TO ADD

## This file contains exact code to add to your models.py files

---

## FILE 1: accounts/models.py - ADDITIONS TO StudentProfile

### Find this section in your StudentProfile:
```python
class StudentProfile(models.Model):
    """Student Profile - Tracks academic details and verification status"""
    # ... existing fields ...
    updated_at = models.DateTimeField(auto_now=True)
```

### Add AFTER updated_at this entire section:

```python
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
        from django.utils import timezone
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
        from django.utils import timezone
        
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
    
    def can_apply_for_jobs(self):
        """
        Check if student can apply for jobs.
        Updated from original - now includes PCS and auto-unblock checks.
        
        Returns:
            True if eligible, False otherwise
        """
        # Auto-unblock if cooling period ended
        self.unblock_if_eligible()
        
        # Check all blocking conditions
        if not self.is_verified:
            return False
        if self.is_blacklisted:
            return False
        if self.is_blocked:
            return False
        if self.cgpa is None or self.active_backlogs is None:
            return False
        
        return True
```

---

## FILE 2: jobs/models.py - ADDITIONS TO JobPost

### Find this section in your JobPost:
```python
    def can_be_closed_by(self, user):
        """Only recruiter who posted or TPO can close"""
        return user == self.posted_by or getattr(user, 'is_tpo', False)
```

### Add AFTER this entire section:

```python
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
```

---

## FILE 3: jobs/models.py - ADD NEW MODELS AT END

### Add at the END of jobs/models.py (after all existing models):

```python
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


# Add fields to Application model to track response times
# Insert in existing Application class:

# APPLICATION MODEL ADDITIONS - Add these fields to Application class:
"""
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
"""
```

---

## FILE 4: Create NEW FILE - jobs/signals.py

Create a new file: `c:\Users\Vaibhav\OneDrive\Documents\EY_4.0_AVCOE\Project3\jobs\signals.py`

Add this code:

```python
"""
Django signals for advanced features automation.
These run automatically when models are created/updated.
"""

from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.utils import timezone
from .models import Application, InterviewSchedule

@receiver(post_save, sender=Application)
def track_application_response_time(sender, instance, created, **kwargs):
    """
    When application status changes from Pending to anything else,
    record the response time (hours from deadline to update).
    
    This auto-populates the response_time_hours field.
    """
    if not created and instance.status != Application.STATUS_PENDING:
        # Status was changed
        if not instance.first_status_change_at:
            instance.first_status_change_at = timezone.now()
        
        # Calculate response time
        if instance.job.deadline:
            delta = instance.first_status_change_at - instance.job.deadline
            instance.response_time_hours = max(0, int(delta.total_seconds() / 3600))
        
        instance.status_last_updated_at = timezone.now()
        instance.save()
        
        # Recalculate recruiter rating
        try:
            recruiter_rating = instance.job.posted_by.response_rating
            recruiter_rating.calculate_rating()
        except AttributeError:
            pass  # Rating not created yet


@receiver(post_save, sender=InterviewSchedule)
def check_missed_interviews(sender, instance, created, **kwargs):
    """
    Periodically check if students missed scheduled interviews.
    
    If interview date has passed and application is still PENDING,
    apply PCS penalty for no-show.
    
    Note: In production, this should run as a background task (Celery).
    For now, it runs when InterviewSchedule is updated.
    """
    if instance.scheduled_date < timezone.now():
        app = instance.application
        
        # Check if status is still pending (student never responded)
        if app.status == Application.STATUS_PENDING:
            student_profile = app.student.student_profile
            
            # Apply no-show penalty
            if hasattr(student_profile, 'update_pcs'):
                student_profile.update_pcs(
                    'missed_interview',
                    f"No-show for {app.job.title} at {app.job.company} "
                    f"(Scheduled: {instance.scheduled_date.strftime('%Y-%m-%d %H:%M')})"
                )
```

---

## FILE 5: Update jobs/apps.py

Find your existing `jobs/apps.py` and update it:

```python
from django.apps import AppConfig

class JobsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'jobs'
    
    def ready(self):
        """
        Import signals when app starts so they're registered with Django.
        This makes all the automatic handlers work.
        """
        import jobs.signals
```

---

## MIGRATION COMMANDS

After adding all these models and fields, run:

```bash
# 1. Create migration file
python manage.py makemigrations accounts jobs

# 2. Check what will change (review before applying)
python manage.py migrate --plan

# 3. Apply the migrations
python manage.py migrate

# 4. Test that it worked
python manage.py shell
>>> from accounts.models import StudentProfile
>>> s = StudentProfile.objects.first()
>>> print(s.credit_score)  # Should print 100
>>> print(s.can_apply_for_jobs())  # Should print True/False
```

---

## CHECKLIST BEFORE MIGRATION

- [ ] Backed up db.sqlite3 (copy db.sqlite3 db.sqlite3.backup)
- [ ] Added all code from FILE 1 to accounts/models.py
- [ ] Added all code from FILE 2 to jobs/models.py (new methods on JobPost)
- [ ] Added all new model classes from FILE 3 to jobs/models.py
- [ ] Created jobs/signals.py with FILE 4 code
- [ ] Updated jobs/apps.py with FILE 5 code
- [ ] Installed new packages (pip install pandas openpyxl)
- [ ] No syntax errors in any file

---

**Everything is ready! Now run the migration commands above.** ✅
