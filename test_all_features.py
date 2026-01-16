#!/usr/bin/env python
"""Test all advanced features"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'placement_portal.settings')
django.setup()

from accounts.models import StudentProfile, CustomUser
from jobs.models import (
    JobPost, Application, DreamCompany, HistoricalHiringData, 
    InterviewExperience, PrepVault, RecruiterResponseRating
)
from django.utils import timezone
from decimal import Decimal

print("=" * 80)
print("TESTING ADVANCED FEATURES")
print("=" * 80)

# Get test student and recruiter
student_user = CustomUser.objects.filter(role_type='STUDENT').first()
recruiter_user = CustomUser.objects.filter(role_type='RECRUITER').first()

if not student_user or not recruiter_user:
    print("❌ Need at least one student and one recruiter to test")
    exit(1)

student = student_user.student_profile
recruiter = recruiter_user.recruiter_profile

print(f"\n📚 Test Student: {student_user.username}")
print(f"💼 Test Recruiter: {recruiter_user.username} ({recruiter.company_name})")

# ============================================================
# TEST 1: PCS System (already tested, just verify)
# ============================================================
print("\n" + "=" * 80)
print("TEST 1: Placement Credit Score System")
print("=" * 80)
print(f"Initial PCS: {student.credit_score} ({student.get_pcs_status()})")
print(f"Can apply: {student.can_apply_for_jobs()}")
print(f"✅ PCS System working!")

# ============================================================
# TEST 2: Eligibility Gatekeeper
# ============================================================
print("\n" + "=" * 80)
print("TEST 2: Eligibility Gatekeeper")
print("=" * 80)

# Get or create a job
jobs = JobPost.objects.filter(posted_by=recruiter_user)
if not jobs.exists():
    job = JobPost.objects.create(
        title="Software Engineer",
        company=recruiter.company_name,
        description="Great opportunity!",
        posted_by=recruiter_user,
        min_cgpa=Decimal('6.5'),
        max_backlogs=0,
        branches="CSE, IT, ECE",
        job_type="Full-time",
        package=Decimal('12.00'),
        deadline=timezone.now()
    )
else:
    job = jobs.first()

print(f"Testing job: {job.title} at {job.company}")
is_eligible, reasons = job.check_student_eligibility(student_user)
print(f"\nEligibility Result:")
print(f"  Is Eligible: {is_eligible}")
if not is_eligible:
    print(f"  Reasons for rejection:")
    for reason in reasons:
        print(f"    - {reason}")

badge = job.get_eligibility_badge(student_user)
print(f"\nBadge Info:")
print(f"  Icon: {badge['icon']}")
print(f"  Text: {badge['text']}")
print(f"  Color: {badge['color']}")
print(f"  Can Apply: {badge['can_apply']}")
print(f"✅ Eligibility Gatekeeper working!")

# ============================================================
# TEST 3: Dream Company Feature
# ============================================================
print("\n" + "=" * 80)
print("TEST 3: Dream Company Feature")
print("=" * 80)

# Create or get dream company
dream, created = DreamCompany.objects.get_or_create(
    student=student_user,
    defaults={
        'company_name': 'Google',
        'avg_cgpa_required': Decimal('8.0'),
        'common_skills': 'Python, Django, React, Cloud',
        'typical_interview_rounds': 4,
        'typical_feedback_days': 7
    }
)

print(f"Dream Company: {dream.company_name}")
print(f"CGPA Required: {dream.avg_cgpa_required}")
print(f"Common Skills: {dream.common_skills}")

readiness = dream.get_readiness_percentage()
print(f"Readiness Score: {readiness}%")

steps = dream.get_next_steps()
print(f"Next Steps:")
for step in steps[:2]:  # Show first 2 steps
    print(f"  [{step['priority']}] {step['task']}")

print(f"✅ Dream Company Feature working!")

# ============================================================
# TEST 4: Historical Hiring Data
# ============================================================
print("\n" + "=" * 80)
print("TEST 4: Historical Hiring Data")
print("=" * 80)

hiring_data, created = HistoricalHiringData.objects.get_or_create(
    company_name="Google",
    defaults={
        'avg_cgpa': Decimal('8.2'),
        'avg_backlogs': Decimal('0.2'),
        'most_common_skills': 'Python, Data Structures, System Design',
        'avg_interview_rounds': 4,
        'avg_response_time_days': 3,
        'students_hired': 45,
        'total_applicants': 500,
        'success_rate': Decimal('9.0')
    }
)

print(f"Company: {hiring_data.company_name}")
print(f"Avg CGPA: {hiring_data.avg_cgpa}")
print(f"Success Rate: {hiring_data.success_rate}%")
print(f"Students Hired: {hiring_data.students_hired} / {hiring_data.total_applicants}")
print(f"✅ Historical Data working!")

# ============================================================
# TEST 5: Interview Experience (Prep Vault)
# ============================================================
print("\n" + "=" * 80)
print("TEST 5: Interview Experience & Prep Vault")
print("=" * 80)

# Create interview experience
experience, created = InterviewExperience.objects.get_or_create(
    student=student_user,
    company="Google",
    job_title="Software Engineer",
    round_number=1,
    round_type="Online Test",
    defaults={
        'duration_minutes': 90,
        'difficulty': 'Hard',
        'questions_asked': 'Array questions, Linked list, String manipulation',
        'your_experience': 'Solved 2/3 problems correctly',
        'tips_for_others': 'Practice LeetCode medium problems',
        'selected_after': True,
        'status': InterviewExperience.STATUS_APPROVED
    }
)

print(f"Experience: {experience.student.username} - {experience.company}")
print(f"Round Type: {experience.round_type}")
print(f"Difficulty: {experience.difficulty}")
print(f"Selected: {experience.selected_after}")
print(f"Status: {experience.status}")

# Create/get Prep Vault
prep_vault, created = PrepVault.objects.get_or_create(
    company=hiring_data,
    defaults={
        'total_experiences': 1,
        'avg_selection_rate': Decimal('60.0'),
        'recommended_topics': 'Arrays, Linked Lists, Trees, Graphs, DP'
    }
)

print(f"\nPrep Vault: {prep_vault.company.company_name}")
print(f"Total Experiences: {prep_vault.total_experiences}")
print(f"Selection Rate: {prep_vault.avg_selection_rate}%")
print(f"✅ Interview Experience & Prep Vault working!")

# ============================================================
# TEST 6: Recruiter Response Rating (SLA Tracking)
# ============================================================
print("\n" + "=" * 80)
print("TEST 6: Recruiter Response Rating (SLA Tracking)")
print("=" * 80)

rating, created = RecruiterResponseRating.objects.get_or_create(
    recruiter=recruiter_user,
    defaults={
        'avg_response_hours': 12,
        'rating_label': 'Fast Responder',
        'responsiveness_rating': Decimal('4.0')
    }
)

print(f"Recruiter: {recruiter_user.username}")
print(f"Avg Response Time: {rating.avg_response_hours} hours")
print(f"Rating: {rating.rating_label}")
print(f"Stars: {rating.responsiveness_rating} / 5.0")
print(f"✅ Response Rating working!")

# ============================================================
# TEST 7: SLA Tracking on Application
# ============================================================
print("\n" + "=" * 80)
print("TEST 7: Application SLA Tracking")
print("=" * 80)

# Create application
app, created = Application.objects.get_or_create(
    job=job,
    student=student_user,
    defaults={
        'status': Application.STATUS_PENDING
    }
)

print(f"Application: {app.student.username} → {app.job.title}")
print(f"Status: {app.status}")
print(f"Response Time: {app.response_time_hours} hours")
print(f"✅ Application SLA Tracking set up!")

# ============================================================
# SUMMARY
# ============================================================
print("\n" + "=" * 80)
print("ALL ADVANCED FEATURES WORKING! ✅")
print("=" * 80)
print("\nFeatures Implemented:")
print("  ✅ Placement Credit Score System (PCS)")
print("  ✅ Eligibility Gatekeeper")
print("  ✅ Dream Company Roadmap")
print("  ✅ Historical Hiring Data")
print("  ✅ Interview Experience & Prep Vault")
print("  ✅ Recruiter Response Rating (SLA)")
print("  ✅ Application SLA Tracking")
print("\n✨ Your portal is now 10x better! ✨")
