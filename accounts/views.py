from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.utils import timezone
from django.views.decorators.http import require_http_methods

from ai_analytics.utils import skill_analyzer
from .forms import StudentSignUpForm
from .models import StudentProfile, RecruiterProfile, CustomUser
from .forms import StudentSignUpForm, StudentProfileForm
from .decorators import student_only
from ai_analytics.utils import SkillAnalyzer
from accounts.decorators import (
    student_only, recruiter_only, tpo_only,
    student_cannot_modify_verified_data
)

# ============================================
# AUTHENTICATION VIEWS
# ============================================

def home(request):
    """Home page with role-based navigation"""
    return render(request, 'home.html')


def student_register(request):
    """
    Student registration
    Creates CustomUser with STUDENT role and StudentProfile
    """
    if request.method == 'POST':
        form = StudentSignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Create student profile (or get existing to avoid duplicate)
            StudentProfile.objects.get_or_create(user=user)
            login(request, user)
            messages.success(request, 'Registration successful! Please complete your profile.')
            return redirect('student_dashboard')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')
    else:
        form = StudentSignUpForm()
    return render(request, 'accounts/register.html', {'form': form, 'role': 'Student'})


def recruiter_register(request):
    """
    Recruiter registration
    Creates CustomUser with RECRUITER role and RecruiterProfile
    """
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')
        company_name = request.POST.get('company_name')
        company_email = request.POST.get('company_email')
        company_website = request.POST.get('company_website', '')
        contact_phone = request.POST.get('contact_phone', '')

        # Validation
        if not all([username, email, password, password2, company_name, company_email]):
            messages.error(request, 'Please fill in all required fields')
            return render(request, 'accounts/recruiter_register.html')

        if password != password2:
            messages.error(request, 'Passwords do not match')
            return render(request, 'accounts/recruiter_register.html')

        if CustomUser.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists')
            return render(request, 'accounts/recruiter_register.html')

        if CustomUser.objects.filter(email=email).exists():
            messages.error(request, 'Email already registered')
            return render(request, 'accounts/recruiter_register.html')

        # Create user
        user = CustomUser.objects.create_user(
            username=username,
            email=email,
            password=password,
            role_type=CustomUser.RECRUITER
        )

        # Create recruiter profile (or get existing to avoid duplicate)
        RecruiterProfile.objects.get_or_create(
            user=user,
            defaults={
                'company_name': company_name,
                'company_email': company_email,
                'company_website': company_website,
                'contact_phone': contact_phone,
                'is_approved': False  # Requires TPO approval
            }
        )

        login(request, user)
        messages.success(request, 'Registration successful! Waiting for TPO approval to post jobs.')
        return redirect('recruiter_dashboard')

    return render(request, 'accounts/recruiter_register.html')


def user_login(request):
    """
    Login with role-based redirection
    """
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            
            # Role-based redirection
            if user.is_student:
                messages.success(request, f'Welcome back, {user.first_name or user.username}!')
                return redirect('student_dashboard')
            elif user.is_recruiter:
                messages.success(request, f'Welcome, {user.username}!')
                return redirect('recruiter_dashboard')
            elif user.is_tpo:
                messages.success(request, f'Welcome, TPO {user.username}!')
                return redirect('tpo_dashboard')
        else:
            messages.error(request, 'Invalid username or password')
    else:
        form = AuthenticationForm()
    
    return render(request, 'accounts/login.html', {'form': form})


def user_logout(request):
    """Logout"""
    logout(request)
    messages.success(request, 'Logged out successfully')
    return redirect('home')


# ============================================
# STUDENT VIEWS
# ============================================

@student_only
def student_dashboard(request):
    """Student dashboard"""
    profile = getattr(request.user, 'student_profile', None)
    context = {
        'profile': profile,
        'is_verified': profile.is_verified if profile else False,
        'is_blacklisted': profile.is_blacklisted if profile else False,
    }
    return render(request, 'accounts/student_dashboard.html', context)


@student_only
def student_profile_view(request):
    """View and edit student profile"""
    profile = get_object_or_404(StudentProfile, user=request.user)
    
    if request.method == 'POST':
        # Check if profile is verified (cannot edit CGPA, backlogs after verification)
        if profile.is_verified:
            # Only allow editing non-verified fields
            protected_fields = ['cgpa', 'active_backlogs', 'tenth_percent', 'twelfth_percent']
            for field in protected_fields:
                if field in request.POST:
                    messages.error(request, 'Cannot modify academic details after TPO verification')
                    return redirect('student_profile')

        # Update profile fields
        profile.roll_no = request.POST.get('roll_no', profile.roll_no)
        profile.branch = request.POST.get('branch', profile.branch)
        profile.skills = request.POST.get('skills', profile.skills)
        profile.phone_number = request.POST.get('phone_number', profile.phone_number)
        profile.portfolio_url = request.POST.get('portfolio_url', profile.portfolio_url)

        if not profile.is_verified:
            # Can only edit these if not verified
            profile.tenth_percent = request.POST.get('tenth_percent') or profile.tenth_percent
            profile.twelfth_percent = request.POST.get('twelfth_percent') or profile.twelfth_percent
            profile.cgpa = request.POST.get('cgpa') or profile.cgpa
            profile.active_backlogs = request.POST.get('active_backlogs') or profile.active_backlogs

        # Handle resume upload with auto skill extraction
        if 'resume' in request.FILES:
            profile.resume = request.FILES['resume']
            # Auto-extract skills from resume
            try:
                from pyresparser import ResumeParser
                import os
                resume_path = profile.resume.path
                if os.path.exists(resume_path):
                    data = ResumeParser(resume_path).get_extracted_data()
                    if data and 'skills' in data:
                        extracted_skills = ', '.join(data['skills'])
                        if profile.skills:
                            profile.skills += ', ' + extracted_skills
                        else:
                            profile.skills = extracted_skills
                        messages.success(request, f'Skills extracted from resume: {extracted_skills}')
            except Exception as e:
                messages.warning(request, f'Resume uploaded but skill extraction failed: {str(e)}')

        # Handle profile photo upload
        if 'profile_photo' in request.FILES:
            profile.profile_photo = request.FILES['profile_photo']

        profile.save()
        messages.success(request, 'Profile updated successfully')
        return redirect('student_profile')

    context = {'profile': profile}
    return render(request, 'accounts/student_profile.html', context)


# ============================================
# RECRUITER VIEWS
# ============================================

@recruiter_only
def recruiter_dashboard(request):
    """Recruiter dashboard"""
    profile = getattr(request.user, 'recruiter_profile', None)
    context = {
        'profile': profile,
        'is_approved': profile.is_approved if profile else False,
        'is_blocked': profile.is_blocked if profile else False,
    }
    return render(request, 'accounts/recruiter_dashboard.html', context)


@recruiter_only
def recruiter_profile_view(request):
    """View recruiter profile"""
    profile = get_object_or_404(RecruiterProfile, user=request.user)
    
    if request.method == 'POST':
        # Save all profile fields
        profile.company_name = request.POST.get('company_name', profile.company_name)
        profile.company_email = request.POST.get('company_email', profile.company_email)
        profile.industry = request.POST.get('industry', profile.industry)
        profile.company_website = request.POST.get('company_website', profile.company_website)
        profile.description = request.POST.get('description', profile.description)
        profile.hr_contact_email = request.POST.get('hr_contact_email', profile.hr_contact_email)
        profile.hr_contact_phone = request.POST.get('hr_contact_phone', profile.hr_contact_phone)
        profile.save()
        messages.success(request, 'Profile updated successfully')
        return redirect('recruiter_profile')

    context = {
        'profile': profile,
        'approval_status': 'Approved' if profile.is_approved else 'Pending',
    }
    return render(request, 'accounts/recruiter_profile.html', context)


# ============================================
# TPO VIEWS
# ============================================


def get_job_skill_text(job):
    text_parts = [job.description or '']
    if getattr(job, 'skills_required', None):
        text_parts.append(job.skills_required or '')
    elif getattr(job, 'common_skills', None):
        text_parts.append(job.common_skills or '')
    return ' '.join(part for part in text_parts if part).strip()


@tpo_only
def tpo_dashboard(request):
    """TPO dashboard"""
    from jobs.models import JobPost, Application
    
    total_students = CustomUser.objects.filter(role_type=CustomUser.STUDENT).count()
    verified_students = StudentProfile.objects.filter(is_verified=True).count()
    total_recruiters = CustomUser.objects.filter(role_type=CustomUser.RECRUITER).count()
    approved_recruiters = RecruiterProfile.objects.filter(is_approved=True).count()
    pending_recruiters = RecruiterProfile.objects.filter(is_approved=False, is_blocked=False).count()
    total_companies = RecruiterProfile.objects.filter(is_approved=True).count()  # Approved companies
    
    # Calculate placement status data from applications
    placement_status_counts = {
        'selected': Application.objects.filter(status='Selected').count(),
        'shortlisted': Application.objects.filter(status='Shortlisted').count(),
        'pending': Application.objects.filter(status='Pending').count(),
        'rejected': Application.objects.filter(status='Rejected').count(),
    }
    
    # Get AI-powered placement analysis summary
    placement_insights = {
        'overall_placement_rate': 0,
        'total_applications': 0,
        'total_placements': 0,
        'branch_wise': {}
    }
    try:
        from ai_analytics.views import generate_overall_placement_analysis
        placement_insights = generate_overall_placement_analysis()
    except Exception:
        # If AI analytics is unavailable, continue with default summaries
        placement_insights = {
            'overall_placement_rate': 0,
            'total_applications': Application.objects.count(),
            'total_placements': Application.objects.filter(status='Selected').count(),
            'branch_wise': {}
        }
    
    # Get placed students count (students with at least one selected application)
    placed_students = Application.objects.filter(status='Selected').values('student').distinct().count()
    
    # Get unverified students for the pending verifications table
    unverified_students = StudentProfile.objects.filter(is_verified=False).select_related('user')[:10]
    
    # Calculate best job/company match for each unverified student based on their skills
    open_jobs = JobPost.objects.filter(status='Open')
    job_skill_data = []
    for job in open_jobs:
        job_skill_data.append({
            'company': job.company,
            'title': job.title,
            'skills': skill_analyzer.extract_skills_from_text(get_job_skill_text(job))
        })

    unverified_student_matches = []
    for student in unverified_students:
        student_skills = skill_analyzer.extract_skills_from_text(student.skills or '')
        best_match = {
            'company': None,
            'job_title': None,
            'score': 0,
            'matching_skills': []
        }

        for job in job_skill_data:
            score = skill_analyzer.calculate_skill_match_score(student_skills, job['skills'])
            if score > best_match['score']:
                matching_skills = [s for s in student_skills if s.lower() in [j.lower() for j in job['skills']]]
                best_match = {
                    'company': job['company'],
                    'job_title': job['title'],
                    'score': score,
                    'matching_skills': matching_skills
                }

        unverified_student_matches.append({
            'profile': student,
            'best_company': best_match['company'],
            'best_job_title': best_match['job_title'],
            'match_score': best_match['score'],
            'matching_skills': best_match['matching_skills']
        })
    
    # Get unapproved recruiters for the pending approvals table
    unapproved_recruiters = RecruiterProfile.objects.filter(is_approved=False, is_blocked=False).select_related('user')[:10]
    
    # Get recent placements for the recent placements table
    recent_placements = Application.objects.filter(status='Selected').select_related('student', 'job__company').order_by('-applied_at')[:10]
    
    # Calculate total placements (same as placed_students for now, but could be different logic)
    total_placements = placed_students
    
    # Get top companies by average package
    from django.db.models import Avg, Count
    top_companies = RecruiterProfile.objects.filter(
        is_approved=True,
        user__job_posts__applications__status='Selected'
    ).annotate(
        avg_package=Avg('user__job_posts__applications__job__package'),
        job_count=Count('user__job_posts', distinct=True)
    ).order_by('-avg_package')[:10]
    
    context = {
        'total_students': total_students,
        'verified_students': verified_students,
        'total_recruiters': total_recruiters,
        'approved_recruiters': approved_recruiters,
        'pending_recruiters': pending_recruiters,
        'total_companies': total_companies,
        'total_jobs': JobPost.objects.count(),
        'total_applications': Application.objects.count(),
        'placed_students': placed_students,
        'total_placements': total_placements,
        'placement_status_counts': placement_status_counts,
        'placement_insights': placement_insights,
        'unverified_student_matches': unverified_student_matches,
        'unapproved_recruiters': unapproved_recruiters,
        'recent_placements': recent_placements,
        'top_companies': top_companies,
    }
    return render(request, 'accounts/tpo_dashboard.html', context)


@tpo_only
def verify_student(request, student_id):
    """Verify student profile"""
    if request.method != 'POST':
        # If GET request, redirect to profile view
        return redirect('tpo_view_student_profile', student_id=student_id)
    
    try:
        student = CustomUser.objects.get(pk=student_id, role_type=CustomUser.STUDENT)
        profile = student.student_profile
        
        profile.is_verified = True
        profile.verified_by = request.user
        profile.verified_at = timezone.now()
        profile.save()
        
        messages.success(request, f'{student.username}\'s profile verified successfully')
    except (CustomUser.DoesNotExist, StudentProfile.DoesNotExist):
        messages.error(request, 'Student profile not found')
    
    return redirect('tpo_student_list')


@tpo_only
def blacklist_student(request, student_id):
    """Blacklist student from applying"""
    try:
        student = CustomUser.objects.get(pk=student_id, role_type=CustomUser.STUDENT)
        profile = student.student_profile
        reason = request.POST.get('reason', '') if request.method == 'POST' else 'Blacklisted by TPO'
        
        profile.is_blacklisted = True
        profile.blacklist_reason = reason
        profile.save()
        
        messages.success(request, f'{student.username} has been blacklisted')
    except (CustomUser.DoesNotExist, StudentProfile.DoesNotExist):
        messages.error(request, 'Student profile not found')
    
    return redirect('tpo_student_list')


@tpo_only
def approve_recruiter(request, recruiter_id):
    """Approve recruiter registration"""
    if request.method != 'POST':
        # If GET request, redirect to profile view
        return redirect('tpo_view_recruiter_profile', recruiter_id=recruiter_id)
    
    try:
        recruiter = CustomUser.objects.get(pk=recruiter_id, role_type=CustomUser.RECRUITER)
        profile = recruiter.recruiter_profile
        
        profile.is_approved = True
        profile.approved_by = request.user
        profile.approved_at = timezone.now()
        profile.save()
        
        messages.success(request, f'{profile.company_name} approved to post jobs')
    except (CustomUser.DoesNotExist, RecruiterProfile.DoesNotExist):
        messages.error(request, 'Recruiter profile not found')
    
    return redirect('tpo_recruiter_list')


@tpo_only
def block_recruiter(request, recruiter_id):
    """Block recruiter from posting jobs"""
    try:
        recruiter = CustomUser.objects.get(pk=recruiter_id, role_type=CustomUser.RECRUITER)
        profile = recruiter.recruiter_profile
        reason = request.POST.get('reason', '') if request.method == 'POST' else 'Blocked by TPO'
        
        profile.is_blocked = True
        profile.blocked_reason = reason
        profile.save()
        
        messages.success(request, f'{profile.company_name} has been blocked')
    except (CustomUser.DoesNotExist, RecruiterProfile.DoesNotExist):
        messages.error(request, 'Recruiter profile not found')
    
    return redirect('tpo_recruiter_list')


@tpo_only
def student_list(request):
    """List all students for verification/blacklisting"""
    students = StudentProfile.objects.select_related('user').all()
    
    # Filters
    verified_filter = request.GET.get('verified')
    blacklisted_filter = request.GET.get('blacklisted')
    
    if verified_filter is not None:
        students = students.filter(is_verified=verified_filter.lower() == 'true')
        if verified_filter.lower() == 'true':
            students = students.filter(is_blacklisted=False)
    if blacklisted_filter is not None:
        students = students.filter(is_blacklisted=blacklisted_filter.lower() == 'true')

    # Sort verified students first, then alphabetically
    students = students.order_by('-is_verified', 'user__first_name', 'user__last_name')
    
    context = {'students': students}
    return render(request, 'accounts/tpo_student_list.html', context)


@tpo_only
def recruiter_list(request):
    """List all recruiters for approval/blocking"""
    recruiters = RecruiterProfile.objects.select_related('user').all()
    
    # Filters
    approved_filter = request.GET.get('approved')
    blocked_filter = request.GET.get('blocked')
    
    if approved_filter is not None:
        recruiters = recruiters.filter(is_approved=approved_filter.lower() == 'true')
        if approved_filter.lower() == 'true':
            recruiters = recruiters.filter(is_blocked=False)
    if blocked_filter is not None:
        recruiters = recruiters.filter(is_blocked=blocked_filter.lower() == 'true')

    # Sort approved recruiters first, then alphabetically
    recruiters = recruiters.order_by('-is_approved', 'company_name')
    
    context = {'recruiters': recruiters}
    return render(request, 'accounts/tpo_recruiter_list.html', context)


@tpo_only
def placed_students_list(request):
    """List all students who have been placed (selected in at least one application)"""
    from jobs.models import Application
    
    # Get students who have at least one selected application
    placed_student_ids = Application.objects.filter(
        status='Selected'
    ).values_list('student_id', flat=True).distinct()
    
    placed_students = StudentProfile.objects.select_related('user').filter(
        user_id__in=placed_student_ids
    ).order_by('user__first_name')
    
    # Calculate success rate
    total_placed = placed_students.count()
    verified_students = StudentProfile.objects.filter(is_verified=True).count()
    success_rate = 0
    if verified_students > 0:
        success_rate = (total_placed / verified_students) * 100
    
    # Add placed companies to each student profile
    for student_profile in placed_students:
        placed_companies = Application.objects.filter(
            student=student_profile.user,
            status='Selected'
        ).values_list('job__company', flat=True).distinct()
        student_profile.placed_companies = list(placed_companies)
    
    context = {
        'placed_students': placed_students,
        'total_placed': total_placed,
        'verified_students': verified_students,
        'success_rate': success_rate
    }
    return render(request, 'accounts/placed_students_list.html', context)


@tpo_only
def student_placement_details(request, student_id):
    """Show detailed placement information for a specific student"""
    from jobs.models import Application
    
    try:
        student = CustomUser.objects.get(pk=student_id, role_type=CustomUser.STUDENT)
        student_profile = student.student_profile
        
        # Get all applications for this student
        applications = Application.objects.select_related(
            'job', 'job__posted_by'
        ).filter(student=student).order_by('-applied_at')
        
        # Separate applications by status
        selected_applications = applications.filter(status='Selected')
        shortlisted_applications = applications.filter(status='Shortlisted')
        pending_applications = applications.filter(status='Pending')
        rejected_applications = applications.filter(status='Rejected')
        
        context = {
            'student': student,
            'student_profile': student_profile,
            'applications': applications,
            'selected_applications': selected_applications,
            'shortlisted_applications': shortlisted_applications,
            'pending_applications': pending_applications,
            'rejected_applications': rejected_applications,
            'total_applications': applications.count(),
            'placed_companies': selected_applications.values_list('job__company', flat=True).distinct()
        }
        return render(request, 'accounts/student_placement_details.html', context)
        
    except (CustomUser.DoesNotExist, StudentProfile.DoesNotExist):
        messages.error(request, 'Student not found')
        return redirect('placed_students_list')


@login_required
@student_only
def delete_student_account(request):
    """
    Allow students to delete their own account with confirmation
    """
    if request.method == 'POST':
        # Check for confirmation
        confirmation = request.POST.get('confirmation', '').strip().lower()
        
        if confirmation == 'delete my account':
            try:
                user = request.user
                profile = user.student_profile
                
                # Log the deletion for audit purposes
                print(f"Student account deletion requested: {user.username} ({user.email})")
                
                # Delete all related applications first (due to foreign key constraints)
                from jobs.models import Application
                Application.objects.filter(student=user).delete()
                
                # Delete the profile (this will cascade to user due to OneToOneField)
                profile.delete()
                
                # Delete the user account
                user.delete()
                
                messages.success(request, 'Your account has been successfully deleted. We\'re sorry to see you go!')
                return redirect('home')
                
            except Exception as e:
                messages.error(request, 'An error occurred while deleting your account. Please contact support.')
                print(f"Error deleting student account {request.user.username}: {e}")
                return redirect('student_profile')
        else:
            messages.error(request, 'Please type "delete my account" exactly to confirm deletion.')
            return redirect('student_profile')
    
    # GET request - show confirmation page
    context = {
        'user': request.user,
        'profile': request.user.student_profile,
    }
    return render(request, 'accounts/delete_account.html', context)


@tpo_only
def tpo_view_student_profile(request, student_id):
    """Allow TPO to view complete student profile"""
    try:
        student = CustomUser.objects.get(pk=student_id, role_type=CustomUser.STUDENT)
        profile = student.student_profile
        
        context = {
            'student': student,
            'profile': profile,
            'is_tpo_view': True,
        }
        return render(request, 'accounts/student_profile.html', context)
        
    except (CustomUser.DoesNotExist, StudentProfile.DoesNotExist):
        messages.error(request, 'Student profile not found')
        return redirect('tpo_student_list')


@tpo_only
def tpo_view_recruiter_profile(request, recruiter_id):
    """Allow TPO to view complete recruiter profile"""
    try:
        recruiter = CustomUser.objects.get(pk=recruiter_id, role_type=CustomUser.RECRUITER)
        profile = recruiter.recruiter_profile
        
        context = {
            'profile': profile,
            'is_tpo_view': True,
        }
        return render(request, 'accounts/recruiter_profile.html', context)
        
    except (CustomUser.DoesNotExist, RecruiterProfile.DoesNotExist):
        messages.error(request, 'Recruiter profile not found')
        return redirect('tpo_recruiter_list')


# ============================================================
# ADVANCED FEATURES: PCS Dashboard
# ============================================================

@login_required
@student_only
def pcs_dashboard(request):
    """
    Student PCS (Placement Credit Score) Dashboard
    Shows: Current score, status, history, and blocked status
    """
    profile = get_object_or_404(StudentProfile, user=request.user)
    
    # Parse PCS history from JSON
    import json
    history = json.loads(profile.pcs_history or '[]')
    
    # Calculate statistics
    penalties_count = len(history)
    total_penalty_points = sum(h.get('penalty', 0) for h in history)
    
    context = {
        'profile': profile,
        'pcs_score': profile.credit_score,
        'pcs_status': profile.get_pcs_status(),
        'is_blocked': profile.is_blocked,
        'blocked_until': profile.blocked_until,
        'block_reason': profile.block_reason,
        'can_apply': profile.can_apply_for_jobs(),
        'history': history,
        'penalties_count': penalties_count,
        'total_penalties': total_penalty_points,
        'status_color': {
            'Excellent': 'success',
            'Good': 'info',
            'Warning': 'warning',
            'Critical': 'danger'
        }.get(profile.get_pcs_status(), 'secondary'),
        'status_icon': {
            'Excellent': '⭐⭐⭐⭐⭐',
            'Good': '⭐⭐⭐⭐',
            'Warning': '⭐⭐⭐',
            'Critical': '⭐'
        }.get(profile.get_pcs_status(), '?'),
    }
    
    return render(request, 'accounts/pcs_dashboard.html', context)

# ============================================
# STATIC PAGES
# ============================================

def about(request):
    """About page"""
    return render(request, 'about.html')


def contact(request):
    """Contact page"""
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message_text = request.POST.get('message')
        
        if name and email and subject and message_text:
            messages.success(request, 'Thank you! Your message has been sent. We will get back to you soon.')
            return redirect('contact')
        else:
            messages.error(request, 'Please fill all fields.')
    
    return render(request, 'contact.html')