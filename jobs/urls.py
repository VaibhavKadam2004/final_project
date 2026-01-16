from django.urls import path
from . import views

urlpatterns = [
    path('', views.JobListView.as_view(), name='job_list'),
    path('<int:pk>/', views.JobDetailView.as_view(), name='job_detail'),
    path('<int:pk>/apply/', views.ApplyJobView.as_view(), name='apply_job'),
    path('<int:pk>/edit/', views.JobUpdateView.as_view(), name='job_edit'),
    path('<int:pk>/toggle-status/', views.JobToggleStatusView.as_view(), name='job_toggle_status'),
    path('tpo/export/placed/', views.TPOExportPlacedView.as_view(), name='tpo_export_placed'),
    path('<int:job_id>/recruiter/shortlisted_zip/', views.RecruiterDownloadShortlistedResumes.as_view(), name='recruiter_shortlisted_zip'),
    path('create/', views.JobCreateView.as_view(), name='job_create'),
    path('placement_stats/', views.placement_stats, name='placement_stats'),
    path('student/applications/', views.StudentApplicationStatusView.as_view(), name='student_applications'),
    path('api/application/<int:app_id>/status/', views.ApplicationStatusAPIView.as_view(), name='api_application_status'),
    path('recruiter/<int:job_id>/applications/', views.RecruiterApplicationsListView.as_view(), name='recruiter_applications'),
    
    # Advanced Features URLs
    path('dream-company/', views.dream_company_view, name='dream_company'),
    path('<int:job_id>/eligibility/', views.job_eligibility_check, name='job_eligibility'),
    path('prep-vault/', views.prep_vault_view, name='prep_vault'),
    path('interview-experience/submit/', views.interview_experience_submit, name='interview_experience_submit'),
    path('interview-experience/<int:experience_id>/approve/', views.interview_experience_approve, name='interview_experience_approve'),
    path('tpo/interview-experiences/', views.tpo_interview_experiences, name='tpo_interview_experiences'),
    path('recruiter/rating/', views.recruiter_rating_view, name='recruiter_rating'),
]