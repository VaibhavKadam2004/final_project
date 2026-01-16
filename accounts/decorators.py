from django.shortcuts import redirect
from django.http import JsonResponse, HttpResponseForbidden
from functools import wraps

# ============================================
# ROLE-BASED DECORATORS
# ============================================

def student_only(view_func):
    """Allow only authenticated students"""
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        if not getattr(request.user, 'is_student', False):
            return HttpResponseForbidden("Only students can access this page")
        return view_func(request, *args, **kwargs)
    return wrapper

def recruiter_only(view_func):
    """Allow only authenticated recruiters"""
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        if not getattr(request.user, 'is_recruiter', False):
            return HttpResponseForbidden("Only recruiters can access this page")
        return view_func(request, *args, **kwargs)
    return wrapper

def tpo_only(view_func):
    """Allow only authenticated TPO users"""
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        if not getattr(request.user, 'is_tpo', False):
            return HttpResponseForbidden("Only TPO can access this page")
        return view_func(request, *args, **kwargs)
    return wrapper

# ============================================
# PERMISSION CHECKS - SPECIFIC OPERATIONS
# ============================================

def student_can_apply(view_func):
    """
    Decorator for student job applications
    Checks: Student is verified, not blacklisted, profile complete, deadline not passed
    """
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated or not getattr(request.user, 'is_student', False):
            return JsonResponse({'success': False, 'error': 'Unauthorized'}, status=401)
        
        profile = getattr(request.user, 'student_profile', None)
        if not profile:
            return JsonResponse({'success': False, 'error': 'Student profile not found'}, status=400)
        
        # Check if student is blacklisted
        if profile.is_blacklisted:
            return JsonResponse({
                'success': False, 
                'error': f'You are blacklisted from applying. Reason: {profile.blacklist_reason}'
            }, status=403)
        
        # Check if profile is verified by TPO
        if not profile.is_verified:
            return JsonResponse({
                'success': False, 
                'error': 'Your profile must be verified by TPO before applying'
            }, status=403)
        
        # Check if profile is complete
        if profile.cgpa is None or profile.active_backlogs is None:
            return JsonResponse({
                'success': False, 
                'error': 'Profile incomplete. Please fill in all academic details'
            }, status=400)
        
        return view_func(request, *args, **kwargs)
    return wrapper

def recruiter_can_post(view_func):
    """
    Decorator for recruiter job posting
    Checks: Recruiter is approved by TPO, not blocked
    """
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated or not getattr(request.user, 'is_recruiter', False):
            return HttpResponseForbidden("Only recruiters can post jobs")
        
        profile = getattr(request.user, 'recruiter_profile', None)
        if not profile:
            return HttpResponseForbidden("Recruiter profile not found")
        
        if profile.is_blocked:
            return HttpResponseForbidden(
                f"Your account is blocked by TPO. Reason: {profile.blocked_reason}"
            )
        
        if not profile.is_approved:
            return HttpResponseForbidden(
                "Your company must be approved by TPO to post jobs"
            )
        
        return view_func(request, *args, **kwargs)
    return wrapper

def recruiter_can_update_application_status(view_func):
    """
    Decorator for recruiters updating application status
    Checks: Recruiter posted the job, application not closed, job not closed
    """
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated or not getattr(request.user, 'is_recruiter', False):
            return JsonResponse({'success': False, 'error': 'Unauthorized'}, status=401)
        
        # Caller should pass 'application' in kwargs
        application = kwargs.get('application')
        if not application:
            return JsonResponse({'success': False, 'error': 'Application not found'}, status=400)
        
        # Check if recruiter posted this job
        if application.job.posted_by != request.user:
            return JsonResponse({
                'success': False, 
                'error': 'You can only update applications for your own postings'
            }, status=403)
        
        # Check if application is already closed (FORBIDDEN OPERATION)
        if application.is_closed:
            return JsonResponse({
                'success': False, 
                'error': 'Cannot modify closed applications'
            }, status=403)
        
        # Check if job posting is closed
        from jobs.models import JobPost
        if application.job.status == JobPost.STATUS_CLOSED:
            return JsonResponse({
                'success': False, 
                'error': 'Cannot update applications for closed job postings'
            }, status=403)
        
        return view_func(request, *args, **kwargs)
    return wrapper

def student_cannot_modify_verified_data(view_func):
    """
    Decorator preventing students from modifying verified academic data
    After TPO verification, student cannot change: CGPA, backlogs
    """
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated or not getattr(request.user, 'is_student', False):
            return HttpResponseForbidden("Only students can access this")
        
        profile = getattr(request.user, 'student_profile', None)
        if not profile:
            return HttpResponseForbidden("Student profile not found")
        
        # If profile is verified, student cannot edit core eligibility fields
        if profile.is_verified:
            if request.method in ['POST', 'PUT']:
                data = request.POST or request.data
                protected_fields = ['cgpa', 'active_backlogs', 'tenth_percent', 'twelfth_percent']
                if any(field in data for field in protected_fields):
                    return JsonResponse({
                        'success': False,
                        'error': 'Cannot modify academic details after TPO verification. Contact TPO for changes.'
                    }, status=403)
        
        return view_func(request, *args, **kwargs)
    return wrapper

def tpo_can_verify_student(view_func):
    """Decorator for TPO verifying student profiles"""
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated or not getattr(request.user, 'is_tpo', False):
            return HttpResponseForbidden("Only TPO can verify students")
        return view_func(request, *args, **kwargs)
    return wrapper

def tpo_can_manage_recruiter(view_func):
    """Decorator for TPO approving/blocking recruiters"""
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated or not getattr(request.user, 'is_tpo', False):
            return HttpResponseForbidden("Only TPO can manage recruiters")
        return view_func(request, *args, **kwargs)
    return wrapper

# ============================================
# FORBIDDEN OPERATIONS - System Security
# ============================================

def prevent_identity_theft(view_func):
    """Prevent users from impersonating others (except admin with explicit 'Login As' feature)"""
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        target_user_id = kwargs.get('user_id') or request.GET.get('user_id')
        
        if target_user_id and request.user.is_authenticated:
            # Only TPO can potentially use 'Login As' for support (add this feature separately)
            if not getattr(request.user, 'is_tpo', False):
                if str(request.user.id) != str(target_user_id):
                    return JsonResponse({
                        'success': False,
                        'error': 'Identity theft attempt blocked. You can only view your own data.'
                    }, status=403)
        
        return view_func(request, *args, **kwargs)
    return wrapper

def prevent_data_tampering(view_func):
    """
    Prevent modification of closed applications
    Once application is 'Closed', no one can change the history
    """
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        application = kwargs.get('application')
        
        if application and application.is_closed:
            if request.method in ['POST', 'PUT', 'PATCH', 'DELETE']:
                return JsonResponse({
                    'success': False,
                    'error': 'Cannot modify closed applications. Data is locked for audit purposes.'
                }, status=403)
        
        return view_func(request, *args, **kwargs)
    return wrapper
