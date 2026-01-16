from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.utils import timezone
from django.views.decorators.http import require_http_methods

from .forms import StudentSignUpForm
from .models import StudentProfile, RecruiterProfile, CustomUser
from django.contrib.auth.forms import AuthenticationForm
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

        # Handle resume upload
        if 'resume' in request.FILES:
            profile.resume = request.FILES['resume']

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
        # Can only edit company_website and contact_phone
        profile.company_website = request.POST.get('company_website', profile.company_website)
        profile.contact_phone = request.POST.get('contact_phone', profile.contact_phone)
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

@tpo_only
def tpo_dashboard(request):
    """TPO dashboard"""
    from jobs.models import JobPost, Application
    
    total_students = CustomUser.objects.filter(role_type=CustomUser.STUDENT).count()
    verified_students = StudentProfile.objects.filter(is_verified=True).count()
    total_recruiters = CustomUser.objects.filter(role_type=CustomUser.RECRUITER).count()
    approved_recruiters = RecruiterProfile.objects.filter(is_approved=True).count()
    pending_recruiters = RecruiterProfile.objects.filter(is_approved=False, is_blocked=False).count()
    
    context = {
        'total_students': total_students,
        'verified_students': verified_students,
        'total_recruiters': total_recruiters,
        'approved_recruiters': approved_recruiters,
        'pending_recruiters': pending_recruiters,
        'total_jobs': JobPost.objects.count(),
        'total_applications': Application.objects.count(),
    }
    return render(request, 'accounts/tpo_dashboard.html', context)


@tpo_only
def verify_student(request, student_id):
    """Verify student profile"""
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
    
    if verified_filter:
        students = students.filter(is_verified=verified_filter == 'true')
    if blacklisted_filter:
        students = students.filter(is_blacklisted=blacklisted_filter == 'true')
    
    context = {'students': students}
    return render(request, 'accounts/tpo_student_list.html', context)


@tpo_only
def recruiter_list(request):
    """List all recruiters for approval/blocking"""
    recruiters = RecruiterProfile.objects.select_related('user').all()
    
    # Filters
    approved_filter = request.GET.get('approved')
    blocked_filter = request.GET.get('blocked')
    
    if approved_filter:
        recruiters = recruiters.filter(is_approved=approved_filter == 'true')
    if blocked_filter:
        recruiters = recruiters.filter(is_blocked=blocked_filter == 'true')
    
    context = {'recruiters': recruiters}
    return render(request, 'accounts/tpo_recruiter_list.html', context)


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