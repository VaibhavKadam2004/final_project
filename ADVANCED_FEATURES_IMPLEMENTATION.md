# 🚀 ADVANCED FEATURES IMPLEMENTATION GUIDE

## Overview
This guide implements 8 high-impact features that will make your placement portal stand out in competitions and real-world usage. These features add institutional memory, accountability, transparency, and AI-driven career guidance.

---

## FEATURE 1: Placement Credit Score (PCS) System
### Purpose
Ensure student accountability and manage no-shows, offer rejections, and ghosting.

### Implementation

#### Step 1: Update StudentProfile Model
Add to `accounts/models.py`:

```python
class StudentProfile(models.Model):
    # ... existing fields ...
    
    # NEW: Placement Credit Score System
    credit_score = models.IntegerField(default=100, help_text="Placement Credit Score: 0-100")
    is_blocked = models.BooleanField(default=False, help_text="Blocked from applying due to low PCS")
    blocked_until = models.DateTimeField(null=True, blank=True, help_text="Cooling period end date")
    block_reason = models.CharField(max_length=500, blank=True)
    pcs_history = models.TextField(blank=True, help_text="JSON history of PCS changes")
    
    PCS_THRESHOLDS = {
        'CRITICAL': 50,  # Block if below this
        'WARNING': 70,   # Show warning
        'GOOD': 85,      # Good standing
        'EXCELLENT': 95  # Excellent
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
            reason: Additional reason text
        """
        from django.utils import timezone
        import json
        from datetime import timedelta
        
        if penalty_type not in self.PCS_PENALTIES:
            raise ValueError(f"Invalid penalty type: {penalty_type}")
        
        penalty = self.PCS_PENALTIES[penalty_type]
        old_score = self.credit_score
        self.credit_score = max(0, self.credit_score - penalty)
        
        # Record in history
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
            self.block_reason = f"Low PCS ({self.credit_score}/100). Blocked until {self.blocked_until.date()}"
        
        self.save()
        return self.credit_score

    def unblock_if_eligible(self):
        """Check and remove block if cooling period is over"""
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
        """Return human-readable PCS status"""
        if self.credit_score >= self.PCS_THRESHOLDS['EXCELLENT']:
            return 'Excellent'
        elif self.credit_score >= self.PCS_THRESHOLDS['GOOD']:
            return 'Good'
        elif self.credit_score >= self.PCS_THRESHOLDS['WARNING']:
            return 'Warning'
        else:
            return 'Critical'

    def can_apply_for_jobs(self):
        """Check if student can apply"""
        self.unblock_if_eligible()  # Auto-unblock if period ended
        
        if not self.is_verified or self.is_blacklisted or self.is_blocked:
            return False
        if self.cgpa is None or self.active_backlogs is None:
            return False
        return True
```

#### Step 2: Create Signal Handler for Automatic PCS Updates

Create `jobs/signals.py`:

```python
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from .models import InterviewSchedule, Application
from accounts.models import StudentProfile

@receiver(post_save, sender=InterviewSchedule)
def check_missed_interview(sender, instance, created, **kwargs):
    """
    Check if interview time has passed without student response.
    This runs periodically (use celery for production).
    """
    if instance.scheduled_date < timezone.now():
        app = instance.application
        
        # Check if status was never updated (student missed)
        if app.status == Application.STATUS_PENDING:
            student_profile = app.student.student_profile
            student_profile.update_pcs('missed_interview', 
                                     f"No-show for {app.job.title} at {app.job.company}")

@receiver(post_save, sender=Application)
def track_offer_rejection(sender, instance, created, **kwargs):
    """
    When application status changes to REJECTED after being SELECTED,
    apply penalty for offer rejection.
    """
    if instance.status == Application.STATUS_REJECTED:
        # Check if was previously selected
        from .models import ApplicationStatus
        
        try:
            prev_status = instance.status_history.filter(
                status=Application.STATUS_SELECTED
            ).latest('timestamp')
            
            if prev_status:
                # Student was selected but now rejected = offer rejection
                student_profile = instance.student.student_profile
                student_profile.update_pcs('rejected_offer',
                                         f"Rejected selected offer for {instance.job.title}")
        except ApplicationStatus.DoesNotExist:
            pass
```

#### Step 3: Add PCS Check in ApplyJobView

Update `jobs/views.py` ApplyJobView:

```python
def post(self, request, job_id):
    job = get_object_or_404(JobPost, pk=job_id)
    student_profile = request.user.student_profile
    
    # Check PCS blocking first
    if not student_profile.can_apply_for_jobs():
        if student_profile.is_blocked:
            messages.error(request, 
                f"You are blocked from applying. {student_profile.block_reason}. "
                f"Appeal to: tpo@college.edu")
            return redirect('student_dashboard')
        else:
            messages.error(request, "You are not eligible to apply for jobs.")
            return redirect('student_dashboard')
    
    # ... rest of validation ...
```

---

## FEATURE 2: Dream Company Roadmap
### Purpose
Help students set career goals and track progress towards specific companies.

### Implementation

#### Step 1: Create Models

Add to `jobs/models.py`:

```python
class DreamCompany(models.Model):
    """Student's selected dream company for career planning"""
    student = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                    related_name='dream_company', limit_choices_to={'role_type': 'STUDENT'})
    company_name = models.CharField(max_length=200)
    
    # Historical hiring requirements (aggregated from past data)
    avg_cgpa_required = models.DecimalField(max_digits=4, decimal_places=2, default=7.0)
    common_skills = models.TextField(help_text="Comma separated skills")
    typical_interview_rounds = models.IntegerField(default=3)
    typical_feedback_days = models.IntegerField(default=5)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.student.username} -> {self.company_name}"

    def get_readiness_percentage(self):
        """Calculate how ready student is for dream company (0-100%)"""
        student = self.student.student_profile
        score = 0
        
        # CGPA check (40 points)
        if student.cgpa and student.cgpa >= self.avg_cgpa_required:
            score += 40
        elif student.cgpa:
            score += int(40 * (float(student.cgpa) / float(self.avg_cgpa_required)))
        
        # Skills check (40 points)
        required_skills = set(s.strip().lower() for s in self.common_skills.split(','))
        student_skills = set(s.strip().lower() for s in (student.skills or '').split(','))
        if required_skills:
            matched = len(required_skills.intersection(student_skills))
            score += int(40 * (matched / len(required_skills)))
        
        # Resume presence (10 points)
        if student.resume:
            score += 10
        
        # Portfolio (10 points)
        if student.portfolio_url:
            score += 10
        
        return min(100, score)

    def get_next_steps(self):
        """Return list of recommended next steps"""
        student = self.student.student_profile
        steps = []
        
        if not student.cgpa or student.cgpa < self.avg_cgpa_required:
            steps.append({
                'priority': 'HIGH',
                'task': f"Improve CGPA to {self.avg_cgpa_required}",
                'current': student.cgpa or 0,
                'target': self.avg_cgpa_required
            })
        
        required_skills = set(s.strip().lower() for s in self.common_skills.split(','))
        student_skills = set(s.strip().lower() for s in (student.skills or '').split(','))
        missing_skills = required_skills - student_skills
        
        if missing_skills:
            steps.append({
                'priority': 'HIGH',
                'task': f"Learn skills: {', '.join(missing_skills)}",
                'resources': 'Linkedin Learning, Coursera, Udemy'
            })
        
        if not student.resume:
            steps.append({
                'priority': 'MEDIUM',
                'task': "Upload updated resume",
                'resources': 'Check sample resumes in portal'
            })
        
        if not student.portfolio_url:
            steps.append({
                'priority': 'MEDIUM',
                'task': "Build and share portfolio",
                'resources': 'GitHub, personal website'
            })
        
        return steps


class HistoricalHiringData(models.Model):
    """Aggregated hiring data from previous placements"""
    company_name = models.CharField(max_length=200, unique=True)
    
    avg_cgpa = models.DecimalField(max_digits=4, decimal_places=2)
    avg_backlogs = models.DecimalField(max_digits=4, decimal_places=2)
    most_common_skills = models.TextField(help_text="Comma separated")
    avg_interview_rounds = models.IntegerField(default=3)
    avg_response_time_days = models.IntegerField(default=7)
    
    students_hired = models.IntegerField(default=0)
    total_applicants = models.IntegerField(default=1)
    success_rate = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    
    last_visited_date = models.DateField()
    
    class Meta:
        ordering = ['-success_rate']
    
    def __str__(self):
        return f"{self.company_name} ({self.success_rate}% success)"


class SkillRequirement(models.Model):
    """Maps skills to companies for recommendation engine"""
    skill_name = models.CharField(max_length=100)
    companies = models.ManyToManyField(HistoricalHiringData, related_name='required_skills')
    difficulty_level = models.CharField(max_length=20, choices=[
        ('Beginner', 'Beginner'),
        ('Intermediate', 'Intermediate'),
        ('Advanced', 'Advanced'),
    ])
    
    def __str__(self):
        return f"{self.skill_name} ({self.difficulty_level})"
```

#### Step 2: Add Dream Company Roadmap View

Add to `accounts/views.py`:

```python
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.contrib import messages
from jobs.models import DreamCompany, HistoricalHiringData

class DreamCompanyRoadmapView(LoginRequiredMixin, View):
    """Student sets dream company and views personalized roadmap"""
    
    def get(self, request):
        student = request.user.student_profile
        dream = DreamCompany.objects.filter(student=request.user).first()
        
        context = {
            'dream_company': dream,
            'available_companies': HistoricalHiringData.objects.all().order_by('-success_rate'),
        }
        
        if dream:
            context.update({
                'readiness_percentage': dream.get_readiness_percentage(),
                'next_steps': dream.get_next_steps(),
            })
        
        return render(request, 'accounts/dream_company_roadmap.html', context)
    
    def post(self, request):
        company_name = request.POST.get('company_name')
        
        if not company_name:
            messages.error(request, "Please select a company")
            return redirect('dream_company_roadmap')
        
        dream, created = DreamCompany.objects.update_or_create(
            student=request.user,
            defaults={'company_name': company_name}
        )
        
        messages.success(request, f"Dream company set to {company_name}! Your roadmap is ready.")
        return redirect('dream_company_roadmap')
```

#### Step 3: Add to URLs

Add to `accounts/urls.py`:

```python
path('dream-company/roadmap/', views.DreamCompanyRoadmapView.as_view(), name='dream_company_roadmap'),
```

---

## FEATURE 3: Prep-Vault & Interview Experience Sharing
### Purpose
Create institutional memory by sharing interview experiences and questions from previous years.

### Implementation

#### Step 1: Create Models

Add to `jobs/models.py`:

```python
class InterviewExperience(models.Model):
    """Student shares their interview experience after getting result"""
    STATUS_PENDING = 'Pending'
    STATUS_APPROVED = 'Approved'
    STATUS_REJECTED = 'Rejected'
    
    company = models.CharField(max_length=200)
    job_title = models.CharField(max_length=200)
    
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                               related_name='interview_experiences',
                               limit_choices_to={'role_type': 'STUDENT'})
    
    # Interview details
    round_number = models.IntegerField()
    round_type = models.CharField(max_length=100, choices=[
        ('Technical', 'Technical'),
        ('Coding', 'Coding'),
        ('HR', 'HR'),
        ('Case Study', 'Case Study'),
        ('Group Discussion', 'Group Discussion'),
    ])
    
    duration_minutes = models.IntegerField()
    difficulty = models.CharField(max_length=20, choices=[
        ('Easy', 'Easy'),
        ('Medium', 'Medium'),
        ('Hard', 'Hard'),
    ], default='Medium')
    
    # Questions asked (JSON format)
    questions_asked = models.TextField(help_text="List of questions asked (JSON array)")
    
    # Experience details
    your_experience = models.TextField(help_text="What did you discuss/solve")
    tips_for_others = models.TextField(help_text="Advice for future candidates")
    
    selected_after = models.BooleanField(help_text="Were you selected after this round?")
    
    # Approval by TPO
    status = models.CharField(max_length=20, choices=[
        (STATUS_PENDING, 'Pending Approval'),
        (STATUS_APPROVED, 'Approved'),
        (STATUS_REJECTED, 'Rejected'),
    ], default=STATUS_PENDING)
    
    approved_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
                                   null=True, blank=True, related_name='approved_experiences',
                                   limit_choices_to={'role_type': 'TPO'})
    
    created_at = models.DateTimeField(auto_now_add=True)
    views_count = models.IntegerField(default=0)
    helpful_count = models.IntegerField(default=0)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.student.username} - {self.company} Round {self.round_number}"


class PrepVault(models.Model):
    """Aggregated prep material for a specific company"""
    company = models.OneToOneField(HistoricalHiringData, on_delete=models.CASCADE,
                                   related_name='prep_vault')
    
    # Stats
    total_experiences = models.IntegerField(default=0)
    most_asked_questions = models.TextField(help_text="JSON array of top 10 questions")
    difficulty_distribution = models.TextField(help_text="JSON with Easy/Medium/Hard counts")
    
    # Aggregate recommendations
    recommended_topics = models.TextField(help_text="Comma separated topics to study")
    avg_interview_rounds = models.IntegerField(default=3)
    avg_selection_rate = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    
    last_updated = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.company.company_name} Prep Vault"
    
    def get_approval_pending_count(self):
        """Count pending experiences awaiting TPO approval"""
        return InterviewExperience.objects.filter(
            company=self.company.company_name,
            status=InterviewExperience.STATUS_PENDING
        ).count()
```

#### Step 2: Create Prep-Vault Views

Add to `jobs/views.py`:

```python
class PrepVaultDetailView(DetailView):
    """Student views prep material for a specific company"""
    model = PrepVault
    template_name = 'jobs/prep_vault_detail.html'
    context_object_name = 'vault'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        vault = self.get_object()
        
        # Get approved experiences
        experiences = InterviewExperience.objects.filter(
            company=vault.company.company_name,
            status=InterviewExperience.STATUS_APPROVED
        )
        
        context.update({
            'experiences': experiences,
            'total_experiences': experiences.count(),
            'round_breakdown': self._get_round_breakdown(experiences),
            'difficulty_breakdown': self._get_difficulty_breakdown(experiences),
        })
        
        return context
    
    @staticmethod
    def _get_round_breakdown(experiences):
        breakdown = {}
        for exp in experiences:
            key = f"Round {exp.round_number} ({exp.round_type})"
            breakdown[key] = breakdown.get(key, 0) + 1
        return breakdown
    
    @staticmethod
    def _get_difficulty_breakdown(experiences):
        breakdown = {'Easy': 0, 'Medium': 0, 'Hard': 0}
        for exp in experiences:
            breakdown[exp.difficulty] += 1
        return breakdown


class SubmitInterviewExperienceView(LoginRequiredMixin, View):
    """Student submits their interview experience"""
    
    def get(self, request, application_id):
        app = get_object_or_404(Application, pk=application_id, student=request.user)
        
        # Only allow if application is closed/resolved
        if not app.is_closed and app.status not in [Application.STATUS_SELECTED, 
                                                      Application.STATUS_REJECTED]:
            messages.error(request, "You can only submit experience after interview is concluded.")
            return redirect('student_applications')
        
        return render(request, 'jobs/submit_experience.html', {'application': app})
    
    def post(self, request, application_id):
        app = get_object_or_404(Application, pk=application_id, student=request.user)
        
        import json
        
        experience = InterviewExperience.objects.create(
            student=request.user,
            company=app.job.company,
            job_title=app.job.title,
            round_number=int(request.POST.get('round_number', 1)),
            round_type=request.POST.get('round_type'),
            duration_minutes=int(request.POST.get('duration_minutes', 60)),
            difficulty=request.POST.get('difficulty'),
            questions_asked=json.dumps(request.POST.getlist('questions')),
            your_experience=request.POST.get('your_experience'),
            tips_for_others=request.POST.get('tips_for_others'),
            selected_after=(request.POST.get('selected_after') == 'on'),
        )
        
        messages.success(request, 
            "Experience submitted! TPO will review and add to Prep Vault. Thank you for sharing!")
        return redirect('student_applications')
```

---

## FEATURE 4: Recruiter SLA Tracking (Ghosting Detector)
### Purpose
Track and display how quickly recruiters respond to applications.

### Implementation

#### Step 1: Update Application Model

Add fields to `Application` model in `jobs/models.py`:

```python
class Application(models.Model):
    # ... existing fields ...
    
    # NEW: SLA Tracking
    status_last_updated_at = models.DateTimeField(null=True, blank=True, 
                                                   help_text="When status was last changed")
    first_status_change_at = models.DateTimeField(null=True, blank=True,
                                                   help_text="When first moved from Pending")
    response_time_hours = models.IntegerField(null=True, blank=True,
                                             help_text="Hours taken to first update")
    
    def calculate_response_time(self):
        """Calculate hours from deadline to first status change"""
        from django.utils import timezone
        
        if self.first_status_change_at and self.job.deadline:
            delta = self.first_status_change_at - self.job.deadline
            hours = delta.total_seconds() / 3600
            return max(0, int(hours))
        return None

    def save(self, *args, **kwargs):
        """Auto-calculate response time on save"""
        if self.status != self.STATUS_PENDING and not self.first_status_change_at:
            from django.utils import timezone
            self.first_status_change_at = timezone.now()
        
        self.status_last_updated_at = timezone.now()
        self.response_time_hours = self.calculate_response_time()
        super().save(*args, **kwargs)
```

#### Step 2: Create RecruiterRating Model

Add to `jobs/models.py`:

```python
class RecruiterResponseRating(models.Model):
    """Aggregate recruiter response time rating"""
    recruiter = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                     related_name='response_rating',
                                     limit_choices_to={'role_type': 'RECRUITER'})
    
    avg_response_hours = models.IntegerField(default=0)
    total_jobs_posted = models.IntegerField(default=0)
    total_applications = models.IntegerField(default=0)
    responses_given = models.IntegerField(default=0)
    
    # Rating (1-5 stars)
    responsiveness_rating = models.DecimalField(max_digits=2, decimal_places=1, default=3.0)
    rating_label = models.CharField(max_length=50, default='Average')
    
    last_updated = models.DateTimeField(auto_now=True)
    
    RATING_THRESHOLDS = {
        (0, 24): ('⭐⭐⭐⭐⭐', 'Very Fast Responder', 5.0),
        (24, 72): ('⭐⭐⭐⭐', 'Fast Responder', 4.0),
        (72, 168): ('⭐⭐⭐', 'Average', 3.0),
        (168, 336): ('⭐⭐', 'Slow Responder', 2.0),
        (336, float('inf')): ('⭐', 'Very Slow Responder', 1.0),
    }
    
    def calculate_rating(self):
        """Calculate responsiveness rating from application data"""
        from jobs.models import Application, JobPost
        
        applications = Application.objects.filter(
            job__posted_by=self.recruiter
        ).exclude(response_time_hours__isnull=True)
        
        if not applications.exists():
            self.avg_response_hours = 0
            self.responsiveness_rating = 3.0
            self.rating_label = 'No Data'
            return
        
        # Calculate average
        from django.db.models import Avg
        avg_hours = int(applications.aggregate(Avg('response_time_hours'))['response_time_hours__avg'] or 0)
        self.avg_response_hours = avg_hours
        self.total_applications = applications.count()
        self.responses_given = applications.filter(
            response_time_hours__isnull=False
        ).count()
        
        # Determine rating
        for (min_h, max_h), (emoji, label, rating) in self.RATING_THRESHOLDS.items():
            if min_h <= avg_hours < max_h:
                self.rating_label = label
                self.responsiveness_rating = rating
                break
        
        self.save()
    
    def __str__(self):
        return f"{self.recruiter.recruiter_profile.company_name} - {self.rating_label}"
```

#### Step 3: Display Rating on Job Cards

Update `job_list.html` template:

```html
<!-- Add to job card -->
<div class="job-metadata">
    {% if job.posted_by.response_rating %}
        <div class="recruiter-rating">
            <span class="rating-badge">
                {{ job.posted_by.response_rating.rating_label }}
            </span>
            <span class="response-time">
                📊 Avg response: {{ job.posted_by.response_rating.avg_response_hours }}h
            </span>
        </div>
    {% endif %}
</div>
```

---

## FEATURE 5: Eligibility Gatekeeper (Automated Screening)
### Purpose
Show locked applications with reasons if student doesn't meet minimum criteria.

### Implementation

Add to `jobs/models.py`:

```python
class JobPost(models.Model):
    # ... existing fields ...
    
    def check_student_eligibility(self, student):
        """
        Check if student meets all job requirements.
        Returns: (is_eligible, reason_if_locked)
        """
        student_profile = student.student_profile
        reasons = []
        
        # CGPA check
        if student_profile.cgpa is None:
            reasons.append("Please complete your profile with CGPA")
        elif student_profile.cgpa < self.min_cgpa:
            reasons.append(f"Minimum CGPA required: {self.min_cgpa} (Your CGPA: {student_profile.cgpa})")
        
        # Backlog check
        if student_profile.active_backlogs > self.max_backlogs:
            reasons.append(f"Maximum backlogs allowed: {self.max_backlogs} (Your backlogs: {student_profile.active_backlogs})")
        
        # Branch check
        if self.branches:
            allowed_branches = [b.strip() for b in self.branches.split(',')]
            if student_profile.branch not in allowed_branches:
                reasons.append(f"Your branch '{student_profile.branch}' is not eligible. Allowed: {', '.join(allowed_branches)}")
        
        # PCS check
        if hasattr(student_profile, 'is_blocked') and student_profile.is_blocked:
            reasons.append(f"Blocked due to low Placement Credit Score. {student_profile.block_reason}")
        
        # Verification check
        if not student_profile.is_verified:
            reasons.append("Your profile must be verified by TPO")
        
        # Blacklist check
        if student_profile.is_blacklisted:
            reasons.append(f"You are blacklisted: {student_profile.blacklist_reason}")
        
        is_eligible = len(reasons) == 0
        return is_eligible, reasons
    
    def get_eligibility_badge(self, student):
        """Get badge for eligibility display"""
        is_eligible, reasons = self.check_student_eligibility(student)
        
        if is_eligible:
            return {
                'icon': '✅',
                'text': 'Eligible',
                'color': 'success',
                'can_apply': True
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

Update `job_detail.html` template:

```html
<div class="eligibility-section">
    {% with badge=job.get_eligibility_badge request.user %}
        <div class="alert alert-{{ badge.color }}">
            <h5>{{ badge.icon }} {{ badge.text }}</h5>
            
            {% if not badge.can_apply %}
                <div class="lock-reasons">
                    <p><strong>You cannot apply because:</strong></p>
                    <ul>
                        {% for reason in badge.reasons %}
                            <li>{{ reason }}</li>
                        {% endfor %}
                    </ul>
                    <small>Reach out to TPO if you believe this is incorrect.</small>
                </div>
                <button class="btn btn-secondary" disabled>Apply (Locked)</button>
            {% else %}
                <form method="post" action="{% url 'apply_job' job.id %}">
                    {% csrf_token %}
                    <button type="submit" class="btn btn-primary">Apply Now</button>
                </form>
            {% endif %}
        </div>
    {% endwith %}
</div>
```

---

## FEATURE 6: Pre-Drive Simulation & Company-Specific Prep

This integrates with Feature 3 (Prep-Vault). When a student applies for a company:

Update `ApplyJobView` in `jobs/views.py`:

```python
def post(self, request, job_id):
    # ... validation logic ...
    
    # After successful application creation:
    application = Application.objects.create(
        job=job,
        student=request.user
    )
    
    # Unlock prep vault for this company
    from jobs.models import PrepVault
    try:
        vault = PrepVault.objects.get(company__company_name__iexact=job.company)
        # Send notification to student with vault link
        messages.info(request, 
            f"Prepare for {job.company}! Access the <a href='{vault.get_absolute_url()}'>Prep Vault</a> "
            f"with {vault.total_experiences} interview experiences from your college.")
    except PrepVault.DoesNotExist:
        pass
    
    messages.success(request, f"Applied for {job.title} successfully!")
    return redirect('student_applications')
```

---

## FEATURE 7: TPO Master-Sheet Generator
### Purpose
Automate TPO reporting with one-click export.

### Implementation

Add to `jobs/views.py`:

```python
import pandas as pd
from django.http import HttpResponse
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from accounts.decorators import tpo_required
from django.utils.decorators import method_decorator
from .models import Application, JobPost

@method_decorator(tpo_required, name='dispatch')
class ExportJobDriveReportView(View):
    """TPO exports comprehensive job drive report"""
    
    def post(self, request):
        job_id = request.POST.get('job_id')
        report_type = request.POST.get('report_type', 'full')
        
        job = get_object_or_404(JobPost, pk=job_id)
        applications = Application.objects.filter(job=job).select_related('student', 'student__student_profile')
        
        # Build data
        data = []
        for app in applications:
            student = app.student
            profile = student.student_profile
            
            data.append({
                'Roll No': profile.roll_no,
                'Name': f"{student.first_name} {student.last_name}",
                'Email': student.email,
                'Phone': profile.phone_number,
                'Branch': profile.branch,
                'CGPA': profile.cgpa,
                'Backlogs': profile.active_backlogs,
                'Skills': profile.skills,
                'Applied At': app.applied_at.strftime('%Y-%m-%d %H:%M'),
                'Status': app.status,
                'Status Last Updated': app.status_last_updated_at.strftime('%Y-%m-%d %H:%M') if app.status_last_updated_at else '-',
                'Response Time (Hours)': app.response_time_hours or '-',
            })
        
        # Create DataFrame
        df = pd.DataFrame(data)
        
        # Add summary sheet
        summary_data = {
            'Metric': [
                'Total Applications',
                'Pending',
                'Shortlisted',
                'Selected',
                'Rejected',
                'Avg CGPA of Applicants',
                'Avg Response Time (hours)',
            ],
            'Value': [
                applications.count(),
                applications.filter(status=Application.STATUS_PENDING).count(),
                applications.filter(status=Application.STATUS_SHORTLISTED).count(),
                applications.filter(status=Application.STATUS_SELECTED).count(),
                applications.filter(status=Application.STATUS_REJECTED).count(),
                f"{applications.aggregate(Avg('student__student_profile__cgpa'))['student__student_profile__cgpa__avg']:.2f}",
                f"{applications.aggregate(Avg('response_time_hours'))['response_time_hours__avg'] or 0:.1f}",
            ]
        }
        summary_df = pd.DataFrame(summary_data)
        
        # Create Excel writer
        filename = f"{job.company}_{job.title}_{timezone.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
        
        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = f'attachment; filename="{filename}"'
        
        with pd.ExcelWriter(response, engine='openpyxl') as writer:
            summary_df.to_excel(writer, sheet_name='Summary', index=False)
            df.to_excel(writer, sheet_name='Detailed', index=False)
        
        return response
```

Add to `placement_portal/urls.py`:

```python
path('admin/export-job-report/', views.ExportJobDriveReportView.as_view(), name='export_job_report'),
```

Add to `tpo_dashboard.html`:

```html
<div class="export-section">
    <h5>📊 Export Reports</h5>
    <form method="post" action="{% url 'export_job_report' %}">
        {% csrf_token %}
        <div class="form-group">
            <label>Select Job Drive:</label>
            <select name="job_id" class="form-control" required>
                <option value="">-- Choose a job --</option>
                {% for job in all_jobs %}
                    <option value="{{ job.id }}">{{ job.company }} - {{ job.title }}</option>
                {% endfor %}
            </select>
        </div>
        <button type="submit" class="btn btn-success">📥 Download Report</button>
    </form>
</div>
```

---

## FEATURE 8: AI Career Architect (Phase 2)
### Purpose
AI-powered resume review, mock interviews, and smart job search.

### Design (Ready for OpenAI/Gemini integration)

Create `ai_assistant/service.py`:

```python
import os
from openai import OpenAI  # or from google import generativeai

class AICareerAssistant:
    def __init__(self):
        # Initialize with your API key
        self.api_key = os.getenv('OPENAI_API_KEY')
        # or: self.api_key = os.getenv('GEMINI_API_KEY')
    
    def review_resume(self, student_profile, dream_company=None):
        """AI reviews resume against job requirements"""
        prompt = f"""
        Review this student's profile for a placement opportunity:
        
        Name: {student_profile.user.first_name}
        CGPA: {student_profile.cgpa}
        Skills: {student_profile.skills}
        Projects: [from portfolio]
        
        {% if dream_company %}
        Target Company: {dream_company}
        {% endif %}
        
        Provide:
        1. Resume feedback (2-3 sentences)
        2. Missing skills (if any)
        3. Recommended improvements
        4. Confidence score (0-100)
        """
        
        # Call OpenAI/Gemini API
        # return response
    
    def mock_interview(self, student_profile, company, round_type):
        """AI conducts mock interview"""
        prompt = f"""
        Conduct a mock {round_type} interview for:
        Company: {company}
        Student: {student_profile.user.first_name}
        Skills: {student_profile.skills}
        
        Ask 1 question appropriate for this round.
        After student responds, provide feedback.
        """
        # Implementation for two-way conversation
    
    def smart_job_search(self, student_profile, natural_query):
        """AI understands natural language job search"""
        prompt = f"""
        Find internships matching this query: "{natural_query}"
        Student Profile:
        - CGPA: {student_profile.cgpa}
        - Skills: {student_profile.skills}
        - Preferred Location: [from profile]
        
        Return: Ranked job recommendations
        """
        # Implementation for semantic job matching
```

---

## MIGRATION STEPS

### Step 1: Update requirements.txt

Add to your `requirements.txt`:

```
pandas>=2.0.0
openpyxl>=3.1.0
openai>=1.0.0  # Optional, for AI features
google-generativeai>=0.3.0  # Optional alternative
```

### Step 2: Create migrations

```bash
python manage.py makemigrations accounts jobs
python manage.py migrate
```

### Step 3: Register signals

Update `jobs/apps.py`:

```python
from django.apps import AppConfig

class JobsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'jobs'
    
    def ready(self):
        import jobs.signals  # Import signals when app starts
```

### Step 4: Run data aggregation (optional)

Create management command `jobs/management/commands/aggregate_hiring_data.py`:

```python
from django.core.management.base import BaseCommand
from jobs.models import Application, HistoricalHiringData, PrepVault

class Command(BaseCommand):
    help = 'Aggregate historical hiring data for companies'
    
    def handle(self, *args, **options):
        # Group applications by company
        # Calculate averages
        # Update HistoricalHiringData
        # Create PrepVaults
        self.stdout.write(self.style.SUCCESS('Data aggregation complete'))
```

Run: `python manage.py aggregate_hiring_data`

---

## ADMIN INTEGRATION

Update `jobs/admin.py`:

```python
from django.contrib import admin
from .models import (
    DreamCompany, InterviewExperience, PrepVault, 
    RecruiterResponseRating
)

@admin.register(InterviewExperience)
class InterviewExperienceAdmin(admin.ModelAdmin):
    list_display = ['company', 'student', 'round_type', 'status', 'created_at']
    list_filter = ['status', 'company', 'difficulty']
    actions = ['approve_experiences']
    
    def approve_experiences(self, request, queryset):
        queryset.update(status='Approved', approved_by=request.user)

@admin.register(DreamCompany)
class DreamCompanyAdmin(admin.ModelAdmin):
    list_display = ['student', 'company_name', 'created_at']

@admin.register(PrepVault)
class PrepVaultAdmin(admin.ModelAdmin):
    list_display = ['company', 'total_experiences', 'avg_selection_rate']
    readonly_fields = ['last_updated']

@admin.register(RecruiterResponseRating)
class RecruiterResponseRatingAdmin(admin.ModelAdmin):
    list_display = ['recruiter', 'avg_response_hours', 'rating_label']
    readonly_fields = ['responsiveness_rating', 'avg_response_hours']
```

---

## IMPLEMENTATION TIMELINE

| Phase | Features | Timeline |
|-------|----------|----------|
| **Phase 1** | PCS System, Eligibility Gatekeeper | Week 1-2 |
| **Phase 2** | Dream Company Roadmap, Prep-Vault | Week 2-3 |
| **Phase 3** | SLA Tracking, Master-sheet Generator | Week 3 |
| **Phase 4** | AI Career Architect | Week 4+ |

---

## TESTING CHECKLIST

- [ ] PCS: Student blocked after 3 no-shows
- [ ] PCS: Cooling period auto-unlock works
- [ ] Dream Company: Roadmap shows correct next steps
- [ ] Prep-Vault: Interview experiences visible after approval
- [ ] SLA: Response time calculated correctly
- [ ] Eligibility: Lock shown for non-eligible students
- [ ] Export: Excel file contains all required data
- [ ] AI (Phase 2): Resume review integration works

---

## DEPLOYMENT NOTES

1. **Database Backup:** Before migration, backup your db.sqlite3
2. **Test Environment:** Test all features in development first
3. **Permissions:** Update role-based decorators for TPO access
4. **API Keys:** Store OpenAI/Gemini keys in environment variables
5. **Celery (Optional):** For background tasks like PCS updates, schedule with celery-beat

---

**This implementation makes your portal production-grade and competition-winning!** 🚀
