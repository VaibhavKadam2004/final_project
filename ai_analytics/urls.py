from django.urls import path
from . import views

app_name = 'ai_analytics'

urlpatterns = [
    # Student AI features
    path('student/dashboard/', views.student_ai_dashboard, name='student_ai_dashboard'),
    path('student/analyze-skills/', views.analyze_student_skills, name='analyze_student_skills'),
    path('student/analyze-dream-company/', views.analyze_dream_company, name='analyze_dream_company'),

    # TPO AI features
    path('tpo/dashboard/', views.tpo_ai_dashboard, name='tpo_ai_dashboard'),
    path('tpo/generate-analytics/', views.generate_placement_analytics, name='generate_placement_analytics'),
    path('tpo/company-skill-demand/', views.get_company_skill_demand, name='get_company_skill_demand'),
    path('gpt-recommendations/', views.get_gpt_recommendations, name='gpt_recommendations'),
]