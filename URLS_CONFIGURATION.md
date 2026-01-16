# URLs Configuration for RBAC System
# Add these to your urls.py files

# ============================================
# placement_portal/urls.py (Main URLs)
# ============================================

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('jobs/', include('jobs.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


# ============================================
# accounts/urls.py (Auth & Profile URLs)
# ============================================

from django.urls import path
from . import views

urlpatterns = [
    # Authentication
    path('', views.home, name='home'),
    path('register/student/', views.student_register, name='student_register'),
    path('register/recruiter/', views.recruiter_register, name='recruiter_register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    
    # Student URLs
    path('student/dashboard/', views.student_dashboard, name='student_dashboard'),
    path('student/profile/', views.student_profile_view, name='student_profile'),
    
    # Recruiter URLs
    path('recruiter/dashboard/', views.recruiter_dashboard, name='recruiter_dashboard'),
    path('recruiter/profile/', views.recruiter_profile_view, name='recruiter_profile'),
    
    # TPO URLs
    path('tpo/dashboard/', views.tpo_dashboard, name='tpo_dashboard'),
    path('tpo/students/', views.student_list, name='student_list'),
    path('tpo/students/<int:student_id>/verify/', views.verify_student, name='verify_student'),
    path('tpo/students/<int:student_id>/blacklist/', views.blacklist_student, name='blacklist_student'),
    path('tpo/recruiters/', views.recruiter_list, name='recruiter_list'),
    path('tpo/recruiters/<int:recruiter_id>/approve/', views.approve_recruiter, name='approve_recruiter'),
    path('tpo/recruiters/<int:recruiter_id>/block/', views.block_recruiter, name='block_recruiter'),
]


# ============================================
# jobs/urls.py (Job & Application URLs)
# ============================================

from django.urls import path
from . import views

urlpatterns = [
    # Job Listing
    path('', views.JobListView.as_view(), name='job_list'),
    path('<int:pk>/', views.JobDetailView.as_view(), name='job_detail'),
    
    # Student Job Application
    path('<int:pk>/apply/', views.ApplyJobView.as_view(), name='apply_job'),
    path('applications/<int:app_id>/', views.StudentApplicationDetailView.as_view(), name='application_detail'),
    
    # Recruiter Job Management
    path('create/', views.JobCreateView.as_view(), name='create_job'),
    path('<int:pk>/update/', views.JobUpdateView.as_view(), name='update_job'),
    
    # Recruiter Application Management
    path('applications/<int:app_id>/shortlist/', views.ApplicationShortlistView.as_view(), name='shortlist_candidate'),
    path('applications/<int:app_id>/schedule-interview/', views.ScheduleInterviewView.as_view(), name='schedule_interview'),
    path('<int:job_id>/resumes/', views.RecruiterDownloadShortlistedResumes.as_view(), name='download_resumes'),
    
    # TPO Operations
    path('api/stats/', views.placement_stats, name='placement_stats'),
    path('export/placed/', views.TPOExportPlacedView.as_view(), name='export_placed'),
]


# ============================================
# NEXT STEPS FOR ADMIN SETUP
# ============================================

# 1. After running migrations, create TPO user:
#    python manage.py createsuperuser
#
# 2. In Django admin or via management command:
#    from django.contrib.auth import get_user_model
#    from accounts.models import CustomUser
#    User = get_user_model()
#    admin_user = User.objects.get(username='admin')
#    admin_user.role_type = CustomUser.TPO
#    admin_user.save()
#
# 3. Update admin.py to display role management:
#    See accounts/admin.py for suggested configuration
