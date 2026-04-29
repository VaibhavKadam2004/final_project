from django.db import models
from django.conf import settings
from django.utils import timezone
import json

class SkillMapping(models.Model):
    """Maps skills to standardized categories and difficulty levels"""
    skill_name = models.CharField(max_length=100, unique=True)
    category = models.CharField(max_length=50, help_text="e.g., Programming, Database, Web Development")
    difficulty_level = models.CharField(max_length=20, choices=[
        ('Beginner', 'Beginner'),
        ('Intermediate', 'Intermediate'),
        ('Advanced', 'Advanced'),
        ('Expert', 'Expert')
    ], default='Beginner')
    related_skills = models.TextField(blank=True, help_text="Comma separated related skills")
    industry_relevance = models.IntegerField(default=5, help_text="1-10 scale")

    def __str__(self):
        return f"{self.skill_name} ({self.category})"

class CompanySkillDemand(models.Model):
    """Tracks skills demanded by companies based on job postings"""
    company_name = models.CharField(max_length=200)
    skill = models.CharField(max_length=100)
    demand_score = models.IntegerField(default=1, help_text="How much this skill is demanded")
    job_type = models.CharField(max_length=50, choices=[
        ('Internship', 'Internship'),
        ('Full-time', 'Full-time'),
        ('Both', 'Both')
    ], default='Both')
    last_updated = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('company_name', 'skill', 'job_type')

    def __str__(self):
        return f"{self.company_name} - {self.skill}"

class StudentSkillAnalysis(models.Model):
    """AI analysis results for student skills and recommendations"""
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                               related_name='skill_analyses', limit_choices_to={'role_type': 'STUDENT'})
    current_skills = models.TextField(help_text="JSON list of current skills with proficiency levels")
    skill_gaps = models.TextField(blank=True, help_text="JSON list of skills needed for improvement")
    recommended_companies = models.TextField(blank=True, help_text="JSON list of company matches with scores")
    career_suggestions = models.TextField(blank=True, help_text="AI career path suggestions")
    analysis_date = models.DateTimeField(auto_now_add=True)
    is_latest = models.BooleanField(default=True)

    def __str__(self):
        return f"Analysis for {self.student.username} - {self.analysis_date.date()}"

    def save(self, *args, **kwargs):
        # Mark previous analyses as not latest
        if self.is_latest:
            StudentSkillAnalysis.objects.filter(
                student=self.student,
                is_latest=True
            ).exclude(pk=self.pk).update(is_latest=False)
        super().save(*args, **kwargs)

class PlacementAnalytics(models.Model):
    """AI-powered placement analytics for TPO dashboard"""
    analysis_type = models.CharField(max_length=50, choices=[
        ('overall_placement', 'Overall Placement Analysis'),
        ('skill_demand', 'Skill Demand Analysis'),
        ('student_recommendation', 'Student Recommendations'),
        ('company_trends', 'Company Trends Analysis')
    ])
    analysis_data = models.TextField(help_text="JSON data containing analysis results")
    generated_at = models.DateTimeField(auto_now_add=True)
    generated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
                                   null=True, limit_choices_to={'role_type': 'TPO'})

    def __str__(self):
        return f"{self.analysis_type} - {self.generated_at.date()}"

class StudentCompanyMatch(models.Model):
    """AI matching scores between students and companies"""
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                               related_name='company_matches', limit_choices_to={'role_type': 'STUDENT'})
    company_name = models.CharField(max_length=200)
    job_title = models.CharField(max_length=200)
    match_score = models.DecimalField(max_digits=5, decimal_places=2, help_text="0-100 match percentage")
    matching_skills = models.TextField(help_text="JSON list of matching skills")
    missing_skills = models.TextField(blank=True, help_text="JSON list of required but missing skills")
    recommendations = models.TextField(blank=True, help_text="AI recommendations for improvement")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-match_score', '-created_at']

    def __str__(self):
        return f"{self.student.username} - {self.company_name} ({self.match_score}%)"

class DreamCompanyAnalysis(models.Model):
    """Analysis for student's dream company aspirations"""
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                               related_name='dream_company_analyses', limit_choices_to={'role_type': 'STUDENT'})
    dream_company = models.CharField(max_length=200)
    current_match_percentage = models.DecimalField(max_digits=5, decimal_places=2)
    required_skills = models.TextField(help_text="JSON list of skills required by dream company")
    skill_gaps = models.TextField(help_text="JSON list of skills student needs to acquire")
    timeline_months = models.IntegerField(help_text="Estimated months to reach required skill level")
    learning_path = models.TextField(blank=True, help_text="JSON structured learning recommendations")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student.username} - Dream: {self.dream_company} ({self.current_match_percentage}%)"
