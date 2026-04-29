from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth import get_user_model
from django.http import JsonResponse, HttpResponse
from django.utils import timezone
from django.contrib import messages
import io, zipfile
import pandas as pd

from .models import JobPost, Application, ApplicationStatus, InterviewSchedule
from accounts.models import StudentProfile, RecruiterProfile
from django.conf import settings
from accounts.decorators import (
    student_only, recruiter_only, tpo_only, student_can_apply,
    recruiter_can_post, recruiter_can_update_application_status,
    prevent_data_tampering
)

# ============================================
# MIXINS FOR RBAC ENFORCEMENT
# ============================================

class StudentRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    """Mixin to ensure only students can access the view"""
    def test_func(self):
        return getattr(self.request.user, 'is_student', False)

    def handle_no_permission(self):
        messages.error(self.request, "Only students can access this page")
        return redirect('home')


class RecruiterRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    """Mixin to ensure only recruiters can access the view"""
    def test_func(self):
        return getattr(self.request.user, 'is_recruiter', False)

    def handle_no_permission(self):
        messages.error(self.request, "Only recruiters can access this page")
        return redirect('home')


class TPORequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    """Mixin to ensure only TPO can access the view"""
    def test_func(self):
        return getattr(self.request.user, 'is_tpo', False)

    def handle_no_permission(self):
        messages.error(self.request, "Only TPO can access this page")
        return redirect('home')


# ============================================
# STUDENT VIEWS
# ============================================

class JobListView(ListView):
    """
    Students see only eligible jobs based on CGPA and backlog criteria
    Unauthenticated users see deadline-based filter only
    """
    model = JobPost
    template_name = 'jobs/job_list.html'
    context_object_name = 'jobs'
    paginate_by = 20

    def get_queryset(self):
        qs = JobPost.objects.filter(
            status=JobPost.STATUS_OPEN,
            deadline__gte=timezone.now()
        ).order_by('-deadline')

        user = self.request.user
        # If student, filter eligible jobs based on profile
        if user.is_authenticated and getattr(user, 'is_student', False):
            profile = getattr(user, 'student_profile', None)
            if profile and profile.is_verified and not profile.is_blacklisted:
                # Filter by eligibility criteria
                if profile.cgpa is not None and profile.active_backlogs is not None:
                    qs = qs.filter(
                        min_cgpa__lte=profile.cgpa,
                        max_backlogs__gte=profile.active_backlogs
                    )
                else:
                    # Profile incomplete
                    qs = JobPost.objects.none()
            else:
                # Profile not verified or blacklisted
                qs = JobPost.objects.none()

        return qs


class JobDetailView(DetailView):
    """Show job details with application status"""
    model = JobPost
    template_name = 'jobs/job_detail.html'
    context_object_name = 'job'

    def get_queryset(self):
        # Only show open jobs unless user is recruiter/TPO
        if self.request.user.is_authenticated and (
            getattr(self.request.user, 'is_recruiter', False) or
            getattr(self.request.user, 'is_tpo', False)
        ):
            return JobPost.objects.all()
        return JobPost.objects.filter(status=JobPost.STATUS_OPEN)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        job = self.get_object()
        applied = False
        eligibility_error = None

        if self.request.user.is_authenticated and getattr(self.request.user, 'is_student', False):
            profile = getattr(self.request.user, 'student_profile', None)
            
            # Check if already applied
            applied = Application.objects.filter(job=job, student=self.request.user).exists()
            
            # Check eligibility
            if profile:
                if profile.is_blacklisted:
                    eligibility_error = "You are blacklisted from applying"
                elif not profile.is_verified:
                    eligibility_error = "Your profile must be verified by TPO"
                elif not job.is_open_for_applications():
                    eligibility_error = "Job posting is closed or deadline passed"
                elif profile.cgpa and profile.cgpa < job.min_cgpa:
                    eligibility_error = f"Your CGPA ({profile.cgpa}) is below minimum ({job.min_cgpa})"
                elif profile.active_backlogs > job.max_backlogs:
                    eligibility_error = f"Your backlogs ({profile.active_backlogs}) exceed limit ({job.max_backlogs})"

        ctx['applied'] = applied
        ctx['eligibility_error'] = eligibility_error
        ctx['can_apply'] = not eligibility_error and not applied
        return ctx


class ApplyJobView(StudentRequiredMixin, View):
    """
    STUDENT OPERATION: Apply for a job
    
    Validations enforced:
    - Student profile verified by TPO
    - Student not blacklisted
    - Profile complete (CGPA, backlogs filled)
    - Meets job criteria (CGPA, backlogs)
    - Job deadline not passed
    - Job status is open
    """
    def post(self, request, pk):
        job = get_object_or_404(JobPost, pk=pk)
        profile = getattr(request.user, 'student_profile', None)

        # Validation 1: Profile exists
        if not profile:
            messages.error(request, 'Student profile not found. Please complete your registration.')
            return redirect('job_detail', pk=pk)

        # Validation 2: Not blacklisted
        if profile.is_blacklisted:
            messages.error(request, f'You are blacklisted from applying. Reason: {profile.blacklist_reason}')
            return redirect('job_detail', pk=pk)

        # Validation 3: Profile verified
        if not profile.is_verified:
            messages.error(request, 'Your profile must be verified by TPO before applying')
            return redirect('job_detail', pk=pk)

        # Validation 4: Profile complete
        if profile.cgpa is None or profile.active_backlogs is None:
            messages.error(request, 'Profile incomplete. Please fill in all academic details')
            return redirect('student_profile')

        # Validation 5: Eligibility check
        if profile.cgpa < job.min_cgpa:
            messages.error(request, f'Your CGPA ({profile.cgpa}) is below the required minimum ({job.min_cgpa})')
            return redirect('job_detail', pk=pk)

        if profile.active_backlogs > job.max_backlogs:
            messages.error(request, f'Your active backlogs ({profile.active_backlogs}) exceed the limit ({job.max_backlogs})')
            return redirect('job_detail', pk=pk)

        # Validation 6: Deadline not passed
        if timezone.now() > job.deadline:
            messages.error(request, 'Application deadline has passed')
            return redirect('job_detail', pk=pk)

        # Validation 7: Job is open
        if not job.is_open_for_applications():
            messages.error(request, 'This job posting is closed')
            return redirect('job_detail', pk=pk)

        # Create application
        app, created = Application.objects.get_or_create(job=job, student=request.user)
        if created:
            ApplicationStatus.objects.create(
                application=app,
                status=app.status,
                updated_by=None,
                note='Student applied via portal'
            )
            messages.success(request, f'Successfully applied for {job.title} at {job.company}!')
            return redirect('student_applications')
        else:
            messages.warning(request, 'You have already applied for this position')
            return redirect('job_detail', pk=pk)


class StudentDashboardView(StudentRequiredMixin, TemplateView):
    """Student dashboard showing profile and applications"""
    template_name = 'accounts/student_dashboard.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        profile = getattr(self.request.user, 'student_profile', None)
        applications = Application.objects.filter(
            student=self.request.user
        ).select_related('job').order_by('-applied_at')
        
        ctx['profile'] = profile
        ctx['applications'] = applications
        ctx['total_applications'] = applications.count()
        ctx['shortlisted_count'] = applications.filter(status=Application.STATUS_SHORTLISTED).count()
        ctx['selected_count'] = applications.filter(status=Application.STATUS_SELECTED).count()
        
        return ctx


class StudentApplicationDetailView(StudentRequiredMixin, DetailView):
    """Student view their application and interview schedules"""
    model = Application
    template_name = 'jobs/student_application_detail.html'
    context_object_name = 'application'

    def get_queryset(self):
        # Student can only view their own applications
        return Application.objects.filter(student=self.request.user)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        application = self.get_object()
        ctx['status_history'] = application.status_history.all()
        ctx['interviews'] = InterviewSchedule.objects.filter(application=application).order_by('scheduled_date')
        return ctx


# ============================================
# RECRUITER VIEWS
# ============================================

class JobCreateView(RecruiterRequiredMixin, CreateView):
    """
    RECRUITER OPERATION: Post a job
    
    Validations:
    - Recruiter must be approved by TPO
    - Recruiter must not be blocked
    """
    model = JobPost
    fields = ['title', 'company', 'description', 'min_cgpa', 'max_backlogs',
              'branches', 'job_type', 'package', 'deadline']
    template_name = 'jobs/job_form.html'
    success_url = reverse_lazy('recruiter_dashboard')

    def test_func(self):
        # Override parent test_func to add recruiter profile checks
        if not getattr(self.request.user, 'is_recruiter', False):
            return False
        
        profile = getattr(self.request.user, 'recruiter_profile', None)
        if not profile or not profile.can_post_jobs():
            self.permission_denied_message = "Your account must be approved by TPO to post jobs"
            return False
        
        return True

    def form_valid(self, form):
        form.instance.posted_by = self.request.user
        messages.success(self.request, 'Job posted successfully!')
        return super().form_valid(form)


class JobUpdateView(RecruiterRequiredMixin, UpdateView):
    """
    Recruiter can only update their own jobs
    Cannot modify if applications are closed
    """
    model = JobPost
    fields = ['title', 'description', 'min_cgpa', 'max_backlogs',
              'branches', 'job_type', 'package', 'deadline', 'status']
    template_name = 'jobs/job_form.html'
    success_url = reverse_lazy('recruiter_dashboard')

    def get_queryset(self):
        # Recruiter can only update jobs they posted
        return JobPost.objects.filter(posted_by=self.request.user)

    def form_valid(self, form):
        messages.success(self.request, 'Job updated successfully!')
        return super().form_valid(form)


class JobToggleStatusView(RecruiterRequiredMixin, View):
    """
    Quick toggle to open/close a job posting
    Recruiter can only toggle their own jobs
    """
    def post(self, request, pk):
        job = get_object_or_404(JobPost, pk=pk, posted_by=request.user)
        
        # Toggle status
        if job.status == JobPost.STATUS_OPEN:
            job.status = JobPost.STATUS_CLOSED
            message = 'Job posting closed successfully! No new applications will be accepted.'
        else:
            job.status = JobPost.STATUS_OPEN
            message = 'Job posting opened successfully! Students can now apply.'
        
        job.save()
        messages.success(request, message)
        return redirect('recruiter_dashboard')
        return redirect('recruiter_dashboard')


class ApplicationShortlistView(RecruiterRequiredMixin, View):
    """
    RECRUITER OPERATION: Shortlist/update application status
    
    Restrictions:
    - Only recruiter who posted the job can update
    - Cannot modify closed applications
    - Cannot modify if job is closed
    """
    def post(self, request, app_id):
        application = get_object_or_404(Application, pk=app_id)

        # Check if recruiter owns this job
        if application.job.posted_by != request.user:
            return JsonResponse({
                'success': False,
                'error': 'You can only update applications for your own job postings'
            }, status=403)

        # Prevent data tampering - check if application is closed
        if application.is_closed:
            return JsonResponse({
                'success': False,
                'error': 'Cannot modify closed applications'
            }, status=403)

        # Check if job is still open for updates
        if application.job.status == JobPost.STATUS_CLOSED:
            return JsonResponse({
                'success': False,
                'error': 'Cannot update applications for closed job postings'
            }, status=403)

        new_status = request.POST.get('status')
        note = request.POST.get('note', '')

        if new_status not in dict(Application.STATUS_CHOICES):
            return JsonResponse({
                'success': False,
                'error': 'Invalid status'
            }, status=400)

        try:
            application.add_status(new_status, request.user, note)
            messages.success(request, f'Application status updated to {new_status}')
            return JsonResponse({
                'success': True,
                'message': f'Status updated to {new_status}'
            })
        except PermissionError as e:
            return JsonResponse({
                'success': False,
                'error': str(e)
            }, status=403)


class RecruiterDashboardView(RecruiterRequiredMixin, TemplateView):
    """Recruiter dashboard showing their job postings and applications"""
    template_name = 'accounts/recruiter_dashboard.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        jobs = JobPost.objects.filter(posted_by=self.request.user).order_by('-created_at')
        
        # Recruitment statistics
        total_applications = Application.objects.filter(job__posted_by=self.request.user).count()
        shortlisted = Application.objects.filter(
            job__posted_by=self.request.user,
            status=Application.STATUS_SHORTLISTED
        ).count()
        selected = Application.objects.filter(
            job__posted_by=self.request.user,
            status=Application.STATUS_SELECTED
        ).count()
        
        # Get recruiter profile
        recruiter_profile = getattr(self.request.user, 'recruiter_profile', None)
        
        # Get lists of shortlisted and selected students
        shortlisted_applications = Application.objects.filter(
            job__posted_by=self.request.user,
            status=Application.STATUS_SHORTLISTED
        ).select_related('student__student_profile', 'job').order_by('-status_last_updated_at')[:10]  # Limit to 10 for dashboard
        
        selected_applications = Application.objects.filter(
            job__posted_by=self.request.user,
            status=Application.STATUS_SELECTED
        ).select_related('student__student_profile', 'job').order_by('-status_last_updated_at')[:10]  # Limit to 10 for dashboard
        
        ctx['recruiter_profile'] = recruiter_profile
        ctx['jobs'] = jobs
        ctx['total_jobs'] = jobs.count()
        ctx['total_applications'] = total_applications
        ctx['shortlisted'] = shortlisted
        ctx['selected'] = selected
        ctx['shortlisted_applications'] = shortlisted_applications
        ctx['selected_applications'] = selected_applications
        
        return ctx


class RecruiterDownloadShortlistedResumes(RecruiterRequiredMixin, View):
    """
    Download resumes of shortlisted candidates
    Only for recruiter who posted the job
    """
    def get(self, request, job_id):
        job = get_object_or_404(JobPost, pk=job_id)
        
        # Verify recruiter owns this job
        if request.user != job.posted_by:
            messages.error(request, 'You can only download resumes for your own jobs')
            return JsonResponse({'error': 'Forbidden'}, status=403)

        applications = Application.objects.filter(
            job=job,
            status=Application.STATUS_SHORTLISTED
        ).select_related('student')

        if not applications.exists():
            messages.warning(request, 'No shortlisted candidates yet')
            return JsonResponse({'error': 'No shortlisted applications'}, status=400)

        buf = io.BytesIO()
        z = zipfile.ZipFile(buf, 'w')
        
        for app in applications:
            profile = getattr(app.student, 'student_profile', None)
            if profile and profile.resume:
                try:
                    z.write(
                        profile.resume.path,
                        arcname=f"{app.student.username}_{profile.resume.name.split('/')[-1]}"
                    )
                except Exception:
                    continue

        z.close()
        buf.seek(0)
        
        resp = HttpResponse(buf.read(), content_type='application/zip')
        resp['Content-Disposition'] = f'attachment; filename=shortlisted_resumes_job_{job_id}.zip'
        return resp


class ScheduleInterviewView(RecruiterRequiredMixin, View):
    """Recruiter schedules an interview for shortlisted candidate"""
    def post(self, request, app_id):
        application = get_object_or_404(Application, pk=app_id)
        
        if application.job.posted_by != request.user:
            return JsonResponse({'success': False, 'error': 'Forbidden'}, status=403)
        
        if application.status != Application.STATUS_SHORTLISTED:
            return JsonResponse({
                'success': False,
                'error': 'Can only schedule interviews for shortlisted candidates'
            }, status=400)

        round_name = request.POST.get('round')
        scheduled_date = request.POST.get('scheduled_date')
        location = request.POST.get('location', '')

        interview = InterviewSchedule.objects.create(
            application=application,
            round=round_name,
            scheduled_date=scheduled_date,
            location=location,
            created_by=request.user
        )

        messages.success(request, 'Interview scheduled successfully')
        return JsonResponse({'success': True, 'interview_id': interview.id})


# ============================================
# TPO / ADMIN VIEWS
# ============================================

class TPODashboardView(TPORequiredMixin, TemplateView):
    """TPO dashboard with analytics and management"""
    template_name = 'accounts/tpo_dashboard.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        User = get_user_model()
        
        # Statistics
        ctx['total_students'] = User.objects.filter(role_type='STUDENT').count()
        ctx['verified_students'] = StudentProfile.objects.filter(is_verified=True).count()
        ctx['total_recruiters'] = User.objects.filter(role_type='RECRUITER').count()
        ctx['approved_recruiters'] = RecruiterProfile.objects.filter(is_approved=True).count()
        ctx['total_jobs'] = JobPost.objects.count()
        ctx['total_applications'] = Application.objects.count()
        ctx['placed_count'] = Application.objects.filter(status=Application.STATUS_SELECTED).count()
        
        # Additional context
        ctx['total_companies'] = ctx['total_recruiters']
        ctx['total_placements'] = ctx['placed_count']
        ctx['unverified_students'] = StudentProfile.objects.filter(is_verified=False)
        ctx['unapproved_recruiters'] = RecruiterProfile.objects.filter(is_approved=False)

        # Placement status counts for dashboard chart
        ctx['placement_status_counts'] = {
            'selected': Application.objects.filter(status=Application.STATUS_SELECTED).count(),
            'shortlisted': Application.objects.filter(status=Application.STATUS_SHORTLISTED).count(),
            'pending': Application.objects.filter(status=Application.STATUS_PENDING).count(),
            'rejected': Application.objects.filter(status=Application.STATUS_REJECTED).count(),
        }

        # AI placement insights for branch-wise analytics
        ctx['placement_insights'] = {
            'overall_placement_rate': 0,
            'total_applications': ctx['total_applications'],
            'total_placements': ctx['total_placements'],
            'branch_wise': {}
        }
        try:
            from ai_analytics.views import generate_overall_placement_analysis
            ctx['placement_insights'] = generate_overall_placement_analysis()
        except Exception:
            pass

        return ctx


class TPOVerifyStudentView(TPORequiredMixin, View):
    """TPO verifies student profile"""
    def post(self, request, student_id):
        from django.contrib.auth import get_user_model
        from accounts.models import StudentProfile
        
        User = get_user_model()
        student = get_object_or_404(User, pk=student_id, role_type='STUDENT')
        profile = student.student_profile

        profile.is_verified = True
        profile.verified_by = request.user
        profile.verified_at = timezone.now()
        profile.save()

        messages.success(request, f'{student.username}\'s profile verified')
        return JsonResponse({'success': True, 'message': 'Profile verified'})


class TPOBlacklistStudentView(TPORequiredMixin, View):
    """TPO can blacklist students from applying"""
    def post(self, request, student_id):
        from django.contrib.auth import get_user_model
        from accounts.models import StudentProfile
        
        User = get_user_model()
        student = get_object_or_404(User, pk=student_id, role_type='STUDENT')
        profile = student.student_profile
        reason = request.POST.get('reason', '')

        profile.is_blacklisted = True
        profile.blacklist_reason = reason
        profile.save()

        messages.success(request, f'{student.username} blacklisted')
        return JsonResponse({'success': True, 'message': 'Student blacklisted'})


class TPOApproveRecruiterView(TPORequiredMixin, View):
    """TPO approves recruiter to post jobs"""
    def post(self, request, recruiter_id):
        from django.contrib.auth import get_user_model
        from accounts.models import RecruiterProfile
        
        User = get_user_model()
        recruiter = get_object_or_404(User, pk=recruiter_id, role_type='RECRUITER')
        profile = recruiter.recruiter_profile

        profile.is_approved = True
        profile.approved_by = request.user
        profile.approved_at = timezone.now()
        profile.save()

        messages.success(request, f'{recruiter.username}\'s company approved')
        return JsonResponse({'success': True, 'message': 'Recruiter approved'})


class TPOBlockRecruiterView(TPORequiredMixin, View):
    """TPO can block recruiters from posting jobs"""
    def post(self, request, recruiter_id):
        from django.contrib.auth import get_user_model
        from accounts.models import RecruiterProfile
        
        User = get_user_model()
        recruiter = get_object_or_404(User, pk=recruiter_id, role_type='RECRUITER')
        profile = recruiter.recruiter_profile
        reason = request.POST.get('reason', '')

        profile.is_blocked = True
        profile.blocked_reason = reason
        profile.save()

        messages.success(request, f'{recruiter.username}\'s account blocked')
        return JsonResponse({'success': True, 'message': 'Recruiter blocked'})


class TPOExportPlacedView(TPORequiredMixin, View):
    """TPO exports placed students to Excel"""
    def get(self, request):
        qs = Application.objects.filter(
            status=Application.STATUS_SELECTED
        ).select_related('student', 'job').select_related('student__student_profile')

        rows = []
        for app in qs:
            profile = getattr(app.student, 'student_profile', None)
            selected_entry = app.status_history.filter(status=Application.STATUS_SELECTED).first()
            selected_date = selected_entry.timestamp.strftime('%Y-%m-%d') if selected_entry else (app.status_last_updated_at.strftime('%Y-%m-%d') if app.status_last_updated_at else '')
            rows.append({
                'Student Name': app.student.get_full_name() or app.student.username,
                'Email': app.student.email,
                'Roll No': getattr(profile, 'roll_no', ''),
                'CGPA': getattr(profile, 'cgpa', ''),
                'Company': app.job.company,
                'Position': app.job.title,
                'Package (LPA)': app.job.package,
                'Applied Date': app.applied_at.strftime('%Y-%m-%d'),
                'Selected Date': selected_date,
            })

        df = pd.DataFrame(rows)
        output = io.BytesIO()
        
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df.to_excel(writer, index=False, sheet_name='Placed')
        
        output.seek(0)
        resp = HttpResponse(
            output.read(),
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        resp['Content-Disposition'] = 'attachment; filename=placed_students.xlsx'
        return resp


def placement_stats(request):
    """API endpoint for TPO analytics dashboard"""
    if not request.user.is_authenticated or not getattr(request.user, 'is_tpo', False):
        return JsonResponse({'error': 'Unauthorized'}, status=403)

    total_jobs = JobPost.objects.count()
    total_applications = Application.objects.count()
    placed = Application.objects.filter(status=Application.STATUS_SELECTED).count()
    shortlisted = Application.objects.filter(status=Application.STATUS_SHORTLISTED).count()
    pending = Application.objects.filter(status=Application.STATUS_PENDING).count()
    rejected = Application.objects.filter(status=Application.STATUS_REJECTED).count()

    data = {
        'total_jobs': total_jobs,
        'total_applications': total_applications,
        'placed': placed,
        'shortlisted': shortlisted,
        'pending': pending,
        'rejected': rejected,
        'placement_percentage': round((placed / total_applications * 100), 2) if total_applications > 0 else 0,
    }
    
    return JsonResponse(data)


class StudentApplicationStatusView(StudentRequiredMixin, ListView):
    """
    Display all job applications for the logged-in student
    with real-time status updates and timeline
    """
    model = Application
    template_name = 'jobs/student_applications.html'
    context_object_name = 'applications'
    paginate_by = 10

    def get_queryset(self):
        """Get all applications for the current student, ordered by applied_at"""
        return Application.objects.filter(
            student=self.request.user
        ).select_related('job').order_by('-applied_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_applied'] = self.get_queryset().count()
        context['shortlisted_count'] = self.get_queryset().filter(status=Application.STATUS_SHORTLISTED).count()
        context['selected_count'] = self.get_queryset().filter(status=Application.STATUS_SELECTED).count()
        context['rejected_count'] = self.get_queryset().filter(status=Application.STATUS_REJECTED).count()
        return context


class ApplicationStatusAPIView(StudentRequiredMixin, View):
    """
    JSON API to fetch a single application's status
    Used by AJAX calls for real-time updates
    """
    def get(self, request, app_id):
        application = get_object_or_404(Application, id=app_id, student=request.user)
        
        data = {
            'id': application.id,
            'job': {
                'id': application.job.id,
                'title': application.job.title,
                'company': application.job.company,
            },
            'status': application.status,
            'applied_at': application.applied_at.isoformat(),
        }
        
        return JsonResponse(data)


class RecruiterApplicationsListView(RecruiterRequiredMixin, TemplateView):
    """
    Recruiter view to see all applications for a specific job
    and update application status with notes
    """
    template_name = 'jobs/recruiter_applications.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        job_id = self.kwargs.get('job_id')
        job = get_object_or_404(JobPost, pk=job_id)
        
        # Verify recruiter owns this job
        if job.posted_by != self.request.user:
            raise PermissionError("You can only view applications for your own job postings")
        
        context['job'] = job
        context['applications'] = Application.objects.filter(job=job).select_related('student', 'student__student_profile').order_by('-applied_at')
        
        # Count by status
        context['total_applications'] = context['applications'].count()
        context['pending_count'] = context['applications'].filter(status=Application.STATUS_PENDING).count()
        context['shortlisted_count'] = context['applications'].filter(status=Application.STATUS_SHORTLISTED).count()
        context['selected_count'] = context['applications'].filter(status=Application.STATUS_SELECTED).count()
        context['rejected_count'] = context['applications'].filter(status=Application.STATUS_REJECTED).count()
        
        # Status choices for dropdown
        context['status_choices'] = Application.STATUS_CHOICES
        
        return context

    def post(self, request, job_id):
        """Handle status update from form submission"""
        job = get_object_or_404(JobPost, pk=job_id)
        
        # Verify recruiter owns this job
        if job.posted_by != request.user:
            messages.error(request, 'You can only update applications for your own job postings')
            return redirect('recruiter_applications', job_id=job_id)
        
        app_id = request.POST.get('app_id')
        new_status = request.POST.get('status')
        note = request.POST.get('note', '')
        
        application = get_object_or_404(Application, pk=app_id, job=job)
        
        # Validate status
        if new_status not in dict(Application.STATUS_CHOICES):
            messages.error(request, 'Invalid status')
            return redirect('recruiter_applications', job_id=job_id)
        
        # Check if application can be modified
        if application.is_closed:
            messages.error(request, 'Cannot modify closed applications')
            return redirect('recruiter_applications', job_id=job_id)
        
        try:
            application.add_status(new_status, request.user, note)
            messages.success(request, f'Application status updated to {new_status}')
        except PermissionError as e:
            messages.error(request, str(e))
        
        return redirect('recruiter_applications', job_id=job_id)

# ============================================================
# ADVANCED FEATURES: Dream Company & Eligibility Views
# ============================================================

@student_only
def dream_company_view(request):
    """
    Student Dream Company Roadmap
    Shows readiness, next steps, and historical company data
    """
    from .models import DreamCompany, HistoricalHiringData
    
    profile = request.user.student_profile
    dream_company = DreamCompany.objects.filter(student=request.user).first()
    hiring_data = None
    
    if request.method == 'POST':
        company_name = request.POST.get('company_name', '')
        if company_name:
            # Find or create hiring data for this company
            hiring_data, _ = HistoricalHiringData.objects.get_or_create(
                company_name=company_name,
                defaults={
                    'avg_cgpa': 7.0,
                    'avg_backlogs': 0.5,
                    'most_common_skills': 'Python, Data Structures',
                    'avg_interview_rounds': 3,
                    'students_hired': 0,
                    'total_applicants': 1,
                }
            )
            
            dream_company, created = DreamCompany.objects.update_or_create(
                student=request.user,
                defaults={
                    'company_name': company_name,
                    'avg_cgpa_required': hiring_data.avg_cgpa,
                    'common_skills': hiring_data.most_common_skills,
                    'typical_interview_rounds': hiring_data.avg_interview_rounds,
                }
            )
            messages.success(request, f'Dream company set to {company_name}')
            return redirect('dream_company')
    
    readiness = dream_company.get_readiness_percentage() if dream_company else 0
    next_steps = dream_company.get_next_steps() if dream_company else []
    
    context = {
        'dream_company': dream_company,
        'readiness_percentage': readiness,
        'next_steps': next_steps,
        'profile': profile,
        'hiring_data': hiring_data,
    }
    return render(request, 'jobs/dream_company.html', context)


@student_only
def job_eligibility_check(request, job_id):
    """
    Check eligibility for a specific job
    Shows detailed reasons for acceptance/rejection
    """
    job = get_object_or_404(JobPost, pk=job_id)
    is_eligible, reasons = job.check_student_eligibility(request.user)
    badge = job.get_eligibility_badge(request.user)
    
    context = {
        'job': job,
        'is_eligible': is_eligible,
        'reasons': reasons,
        'badge': badge,
        'can_apply': badge['can_apply'],
    }
    return render(request, 'jobs/eligibility_check.html', context)


@student_only
def prep_vault_view(request):
    """
    Browse Prep Vault - Interview experiences by company
    Filter by company, difficulty, and round type
    """
    from .models import InterviewExperience, PrepVault
    
    experiences = InterviewExperience.objects.filter(
        status=InterviewExperience.STATUS_APPROVED
    ).select_related('student')
    
    # Filters
    company_filter = request.GET.get('company')
    difficulty_filter = request.GET.get('difficulty')
    round_type_filter = request.GET.get('round_type')
    
    if company_filter:
        experiences = experiences.filter(company__icontains=company_filter)
    if difficulty_filter:
        experiences = experiences.filter(difficulty=difficulty_filter)
    if round_type_filter:
        experiences = experiences.filter(round_type=round_type_filter)
    
    # Get company list for filter dropdown
    companies = experiences.values_list('company', flat=True).distinct()
    
    context = {
        'experiences': experiences.order_by('-created_at'),
        'companies': sorted(set(companies)),
        'current_company': company_filter,
        'current_difficulty': difficulty_filter,
        'current_round_type': round_type_filter,
        'round_types': [r[0] for r in InterviewExperience.ROUND_TYPE_CHOICES],
        'difficulties': [d[0] for d in InterviewExperience.DIFFICULTY_CHOICES],
    }
    return render(request, 'jobs/prep_vault.html', context)


@student_only
def interview_experience_submit(request):
    """
    Student submits interview experience for Prep Vault
    Gets TPO approval before being visible to others
    """
    from .models import InterviewExperience
    
    if request.method == 'POST':
        experience = InterviewExperience.objects.create(
            student=request.user,
            company=request.POST.get('company'),
            job_title=request.POST.get('job_title'),
            round_number=int(request.POST.get('round_number', 1)),
            round_type=request.POST.get('round_type'),
            duration_minutes=int(request.POST.get('duration_minutes', 60)),
            difficulty=request.POST.get('difficulty', 'Medium'),
            questions_asked=request.POST.get('questions_asked'),
            your_experience=request.POST.get('your_experience'),
            tips_for_others=request.POST.get('tips_for_others'),
            selected_after=request.POST.get('selected_after') == 'on',
            status=InterviewExperience.STATUS_PENDING,
        )
        messages.success(request, 'Experience submitted! TPO will review it shortly.')
        return redirect('prep_vault')
    
    context = {
        'round_types': InterviewExperience.ROUND_TYPE_CHOICES,
        'difficulties': InterviewExperience.DIFFICULTY_CHOICES,
    }
    return render(request, 'jobs/interview_experience_form.html', context)


@tpo_only
def interview_experience_approve(request, experience_id):
    """
    TPO approves interview experience for Prep Vault
    Once approved, all students can see it
    """
    from .models import InterviewExperience, PrepVault, HistoricalHiringData
    
    experience = get_object_or_404(InterviewExperience, pk=experience_id)
    
    if request.method == 'POST':
        action = request.POST.get('action')
        
        if action == 'approve':
            experience.status = InterviewExperience.STATUS_APPROVED
            experience.approved_by = request.user
            experience.save()
            
            # Update Prep Vault for this company
            hiring_data, _ = HistoricalHiringData.objects.get_or_create(
                company_name=experience.company
            )
            prep_vault, _ = PrepVault.objects.get_or_create(company=hiring_data)
            prep_vault.total_experiences = InterviewExperience.objects.filter(
                company=experience.company,
                status=InterviewExperience.STATUS_APPROVED
            ).count()
            prep_vault.save()
            
            messages.success(request, f'Experience from {experience.student.username} approved!')
        
        elif action == 'reject':
            experience.status = InterviewExperience.STATUS_REJECTED
            experience.approved_by = request.user
            experience.save()
            messages.warning(request, 'Experience rejected.')
    
    return redirect('tpo_interview_experiences')


@tpo_only
def tpo_interview_experiences(request):
    """
    TPO Dashboard - Review and approve interview experiences
    """
    from .models import InterviewExperience
    
    status_filter = request.GET.get('status', 'Pending')
    experiences = InterviewExperience.objects.all()
    
    if status_filter:
        experiences = experiences.filter(status=status_filter)
    
    context = {
        'experiences': experiences.order_by('-created_at'),
        'pending_count': InterviewExperience.objects.filter(
            status=InterviewExperience.STATUS_PENDING
        ).count(),
        'approved_count': InterviewExperience.objects.filter(
            status=InterviewExperience.STATUS_APPROVED
        ).count(),
        'current_status': status_filter,
    }
    return render(request, 'jobs/tpo_interview_experiences.html', context)


@recruiter_only
def recruiter_rating_view(request):
    """
    Recruiter's own response rating and performance
    Shows how fast they respond to applications
    """
    from .models import RecruiterResponseRating
    
    rating, _ = RecruiterResponseRating.objects.get_or_create(recruiter=request.user)
    rating.calculate_rating()
    
    context = {
        'rating': rating,
        'stars_display': rating.rating_label,
        'avg_hours': rating.avg_response_hours,
        'total_applications': rating.total_applications,
    }
    return render(request, 'jobs/recruiter_rating.html', context)