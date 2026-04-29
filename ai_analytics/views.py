from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.utils import timezone
import json

from accounts.models import CustomUser, StudentProfile, RecruiterProfile
from jobs.models import JobPost, Application
from .models import (
    StudentSkillAnalysis, PlacementAnalytics, StudentCompanyMatch,
    DreamCompanyAnalysis, CompanySkillDemand
)
from .utils import skill_analyzer, placement_analyzer, career_advisor, SkillAnalyzer


def get_job_skill_text(job):
    """Build skill-related text from a job object safely."""
    text_parts = [job.description or '']
    if hasattr(job, 'skills_required'):
        text_parts.append(job.skills_required or '')
    elif hasattr(job, 'common_skills'):
        text_parts.append(job.common_skills or '')
    return ' '.join(part for part in text_parts if part).strip()


@login_required
def student_ai_dashboard(request):
    """AI-powered student dashboard with skill analysis and recommendations"""
    if not request.user.is_student:
        messages.error(request, "Access denied. Student access only.")
        return redirect('home')

    # Get latest analysis
    latest_analysis = StudentSkillAnalysis.objects.filter(
        student=request.user,
        is_latest=True
    ).first()

    # Get recent company matches
    recent_matches = StudentCompanyMatch.objects.filter(
        student=request.user
    ).order_by('-created_at')[:5]

    # Get dream company analysis
    dream_analysis = DreamCompanyAnalysis.objects.filter(
        student=request.user
    ).order_by('-created_at').first()

    context = {
        'latest_analysis': latest_analysis,
        'recent_matches': recent_matches,
        'dream_analysis': dream_analysis,
    }

    return render(request, 'ai_analytics/student_dashboard.html', context)

@login_required
@require_POST
def analyze_student_skills(request):
    """AJAX endpoint to analyze student skills"""
    if not request.user.is_student:
        return JsonResponse({'error': 'Access denied'})

    try:
        student_profile = request.user.student_profile

        # Extract skills from profile
        skills_text = student_profile.skills or ""
        current_skills = skill_analyzer.extract_skills_from_text(skills_text)

        # Get all job postings for company matching
        job_posts = JobPost.objects.filter(status='Open')
        company_matches = []

        for job in job_posts:
            job_skills = skill_analyzer.extract_skills_from_text(
                get_job_skill_text(job)
            )

            match_score = skill_analyzer.calculate_skill_match_score(
                current_skills, job_skills
            )

            if match_score > 20:  # Only show reasonable matches
                company_matches.append({
                    'company': job.company,
                    'job_title': job.title,
                    'match_score': match_score,
                    'job_type': job.job_type
                })

        # Sort by match score
        company_matches.sort(key=lambda x: x['match_score'], reverse=True)
        top_companies = company_matches[:10]

        # Identify skill gaps based on top companies
        all_required_skills = set()
        for job in job_posts:
            job_skills = skill_analyzer.extract_skills_from_text(
                get_job_skill_text(job)
            )
            all_required_skills.update(job_skills)

        skill_gaps = skill_analyzer.identify_skill_gaps(
            current_skills, list(all_required_skills)
        )

        # Generate career suggestions
        career_suggestions = generate_career_suggestions(current_skills, skill_gaps)

        # Save analysis
        analysis = StudentSkillAnalysis.objects.create(
            student=request.user,
            current_skills=json.dumps(current_skills),
            skill_gaps=json.dumps(skill_gaps),
            recommended_companies=json.dumps(top_companies),
            career_suggestions=json.dumps(career_suggestions)
        )

        return JsonResponse({
            'success': True,
            'analysis': {
                'current_skills': current_skills,
                'skill_gaps': skill_gaps,
                'top_companies': top_companies,
                'career_suggestions': career_suggestions
            }
        })

    except Exception as e:
        return JsonResponse({'error': str(e)})

@login_required
@require_POST
def analyze_dream_company(request):
    """Analyze fit for dream company"""
    if not request.user.is_student:
        return JsonResponse({'error': 'Access denied'})

    data = request.POST
    if request.content_type == 'application/json':
        try:
            data = json.loads(request.body.decode('utf-8') or '{}')
        except json.JSONDecodeError:
            data = {}

    dream_company = data.get('dream_company', '').strip()
    if not dream_company:
        return JsonResponse({'error': 'Dream company is required'})

    try:
        student_profile = request.user.student_profile

        # Get jobs from dream company
        company_jobs = JobPost.objects.filter(
            company__icontains=dream_company,
            status='Open'
        )

        if not company_jobs.exists():
            return JsonResponse({
                'error': f'No current openings found for {dream_company}'
            })

        # Aggregate required skills from all company jobs
        all_required_skills = set()
        for job in company_jobs:
            job_skills = skill_analyzer.extract_skills_from_text(
                get_job_skill_text(job)
            )
            all_required_skills.update(job_skills)

        required_skills = list(all_required_skills)

        # Analyze fit
        analysis_result = career_advisor.analyze_dream_company_fit(
            {
                'skills': student_profile.skills or "",
                'cgpa': float(student_profile.cgpa or 0),
                'branch': student_profile.branch or ""
            },
            dream_company,
            required_skills
        )

        # Save analysis
        DreamCompanyAnalysis.objects.create(
            student=request.user,
            dream_company=dream_company,
            current_match_percentage=analysis_result['current_match_percentage'],
            required_skills=json.dumps(required_skills),
            skill_gaps=json.dumps(analysis_result['skill_gaps']),
            timeline_months=analysis_result['timeline_months'],
            learning_path=json.dumps(analysis_result['learning_path'])
        )

        return JsonResponse({
            'success': True,
            'analysis': analysis_result
        })

    except Exception as e:
        return JsonResponse({'error': str(e)})

@login_required
def tpo_ai_dashboard(request):
    """AI-powered TPO dashboard with placement analytics"""
    if not request.user.is_tpo:
        messages.error(request, "Access denied. TPO access only.")
        return redirect('home')

    # Get latest analytics
    latest_analytics = PlacementAnalytics.objects.filter(
        generated_by=request.user
    ).order_by('-generated_at')[:5]

    context = {
        'latest_analytics': latest_analytics,
    }

    return render(request, 'ai_analytics/tpo_dashboard.html', context)

@login_required
@require_POST
def generate_placement_analytics(request):
    """Generate comprehensive placement analytics"""
    if not request.user.is_tpo:
        return JsonResponse({'error': 'Access denied'})

    analysis_type = request.POST.get('analysis_type', 'overall_placement')

    try:
        if analysis_type == 'overall_placement':
            analytics = generate_overall_placement_analysis()
        elif analysis_type == 'skill_demand':
            analytics = generate_skill_demand_analysis()
        elif analysis_type == 'student_recommendation':
            company_name = request.POST.get('company_name')
            if not company_name:
                return JsonResponse({'error': 'Company name required for recommendations'})
            analytics = generate_student_recommendations(company_name)
        else:
            return JsonResponse({'error': 'Invalid analysis type'})

        # Save analytics
        PlacementAnalytics.objects.create(
            analysis_type=analysis_type,
            analysis_data=json.dumps(analytics),
            generated_by=request.user
        )

        return JsonResponse({
            'success': True,
            'analytics': analytics
        })

    except Exception as e:
        return JsonResponse({'error': str(e)})

@login_required
@require_POST
def get_company_skill_demand(request):
    """Get skill demand analysis for a specific company"""
    if not request.user.is_tpo:
        return JsonResponse({'error': 'Access denied'})

    company_name = request.POST.get('company_name', '').strip()
    if not company_name:
        return JsonResponse({'error': 'Company name is required'})

    try:
        # Get all jobs from this company
        company_jobs = JobPost.objects.filter(company__icontains=company_name)

        if not company_jobs.exists():
            return JsonResponse({'error': f'No jobs found for {company_name}'})

        job_postings_data = []
        for job in company_jobs:
            job_postings_data.append({
                'company': job.company,
                'description': job.description,
                'skills_required': getattr(job, 'skills_required', '') or getattr(job, 'common_skills', '') or ''
            })

        analysis = placement_analyzer.analyze_company_skill_demand(job_postings_data)

        return JsonResponse({
            'success': True,
            'analysis': analysis
        })

    except Exception as e:
        return JsonResponse({'error': str(e)})

@login_required
@require_POST
def get_gpt_recommendations(request):
    """Get GPT-powered career recommendations"""
    if not request.user.is_student:
        return JsonResponse({'error': 'Access denied'})

    student_skills = request.POST.get('student_skills', '').split(',')
    job_requirements = request.POST.get('job_requirements', '').split(',')
    company_name = request.POST.get('company_name', '')

    try:
        analyzer = SkillAnalyzer()
        recommendations = analyzer.get_gpt_recommendations(
            [s.strip() for s in student_skills if s.strip()],
            [r.strip() for r in job_requirements if r.strip()],
            company_name
        )

        return JsonResponse({
            'success': True,
            'recommendations': recommendations
        })

    except Exception as e:
        return JsonResponse({'error': str(e)})

# Helper functions

def generate_career_suggestions(current_skills, skill_gaps):
    """Generate career path suggestions based on skills"""
    suggestions = []

    has_programming = any(s.lower() in ['python', 'java', 'javascript', 'c++']
                         for s in current_skills)
    has_web = any(s.lower() in ['html', 'css', 'react', 'django', 'flask']
                  for s in current_skills)
    has_data = any(s.lower() in ['pandas', 'numpy', 'scikit-learn', 'sql']
                   for s in current_skills)

    if has_programming and has_web:
        suggestions.append({
            'role': 'Full Stack Developer',
            'match_score': 85,
            'reason': 'Strong programming and web development skills',
            'next_steps': ['Learn advanced frameworks', 'Build portfolio projects']
        })

    if has_data:
        suggestions.append({
            'role': 'Data Analyst',
            'match_score': 75,
            'reason': 'Data manipulation and analysis skills',
            'next_steps': ['Learn advanced statistics', 'Practice with real datasets']
        })

    if has_programming:
        suggestions.append({
            'role': 'Software Engineer',
            'match_score': 80,
            'reason': 'Solid programming foundation',
            'next_steps': ['Master algorithms', 'Learn system design']
        })

    # Default suggestion
    if not suggestions:
        suggestions.append({
            'role': 'Software Developer',
            'match_score': 60,
            'reason': 'Entry-level programming skills',
            'next_steps': ['Focus on core programming', 'Build projects']
        })

    return suggestions

def generate_overall_placement_analysis():
    """Generate overall placement statistics"""
    from django.db import models

    total_students = CustomUser.objects.filter(role_type='STUDENT').count()
    total_applications = Application.objects.count()
    total_placements = Application.objects.filter(status='Selected').count()

    # Branch-wise analysis
    branch_stats = {}
    students_by_branch = StudentProfile.objects.values('branch').annotate(
        count=models.Count('branch')
    )

    for stat in students_by_branch:
        branch = stat['branch'] or 'Unknown'
        placed_in_branch = Application.objects.filter(
            student__student_profile__branch=branch,
            status='Selected'
        ).count()

        branch_stats[branch] = {
            'total_students': stat['count'],
            'placed': placed_in_branch,
            'placement_rate': round((placed_in_branch / stat['count']) * 100, 2) if stat['count'] > 0 else 0
        }

    # Company-wise placements
    company_stats = {}
    applications_by_company = Application.objects.values('job__company').annotate(
        total=models.Count('id'),
        selected=models.Count('id', filter=models.Q(status='Selected'))
    )

    for stat in applications_by_company:
        company = stat['job__company']
        company_stats[company] = {
            'applications': stat['total'],
            'selections': stat['selected'],
            'selection_rate': round((stat['selected'] / stat['total']) * 100, 2) if stat['total'] > 0 else 0
        }

    return {
        'total_students': total_students,
        'total_applications': total_applications,
        'total_placements': total_placements,
        'overall_placement_rate': round((total_placements / total_students) * 100, 2) if total_students > 0 else 0,
        'branch_wise': branch_stats,
        'company_wise': company_stats
    }

def generate_skill_demand_analysis():
    """Analyze which skills are most demanded"""
    job_posts = JobPost.objects.filter(status='Open')

    job_postings_data = []
    for job in job_posts:
        job_postings_data.append({
            'company': job.company,
            'description': job.description,
            'skills_required': getattr(job, 'skills_required', '') or getattr(job, 'common_skills', '') or ''
        })

    return placement_analyzer.analyze_company_skill_demand(job_postings_data)

def generate_student_recommendations(company_name):
    """Generate student recommendations for a company"""
    # Get company's job requirements
    company_jobs = JobPost.objects.filter(
        company__icontains=company_name,
        status='Open'
    )

    if not company_jobs.exists():
        return {'error': f'No active jobs found for {company_name}'}

    # Aggregate required skills
    all_required_skills = set()
    for job in company_jobs:
        job_skills = skill_analyzer.extract_skills_from_text(
            get_job_skill_text(job)
        )
        all_required_skills.update(job_skills)

    job_requirements = list(all_required_skills)

    # Get eligible students
    eligible_students = []
    students = CustomUser.objects.filter(role_type='STUDENT')

    for student in students:
        if hasattr(student, 'student_profile') and student.student_profile.can_apply_for_jobs():
            eligible_students.append({
                'id': student.id,
                'name': student.get_full_name() or student.username,
                'skills': student.student_profile.skills or "",
                'cgpa': float(student.student_profile.cgpa or 0),
                'branch': student.student_profile.branch or ""
            })

    recommendations = placement_analyzer.recommend_students_for_company(
        company_name, job_requirements, eligible_students
    )

    return {
        'company': company_name,
        'required_skills': job_requirements,
        'recommendations': recommendations
    }
