from django.urls import path
from . import views
from jobs.views import StudentDashboardView, RecruiterDashboardView, TPODashboardView

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.student_register, name='student_register'),
    path('register/recruiter/', views.recruiter_register, name='recruiter_register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('student/dashboard/', StudentDashboardView.as_view(), name='student_dashboard'),
    path('student/profile/', views.student_profile_view, name='student_profile'),
    path('recruiter/dashboard/', RecruiterDashboardView.as_view(), name='recruiter_dashboard'),
    path('recruiter/profile/', views.recruiter_profile_view, name='recruiter_profile'),
    path('tpo/dashboard/', TPODashboardView.as_view(), name='tpo_dashboard'),
    path('tpo/student/verify/<int:student_id>/', views.verify_student, name='verify_student'),
    path('tpo/student/blacklist/<int:student_id>/', views.blacklist_student, name='blacklist_student'),
    path('tpo/recruiter/approve/<int:recruiter_id>/', views.approve_recruiter, name='approve_recruiter'),
    path('tpo/recruiter/block/<int:recruiter_id>/', views.block_recruiter, name='block_recruiter'),
    path('tpo/students/', views.student_list, name='tpo_student_list'),
    path('tpo/recruiters/', views.recruiter_list, name='tpo_recruiter_list'),
    
    # Advanced Features URLs
    path('student/pcs-dashboard/', views.pcs_dashboard, name='pcs_dashboard'),
    
    # Static Pages
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
]
