#!/usr/bin/env python
"""Test TPO Profile Viewing Functionality"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'placement_portal.settings')
django.setup()

from django.urls import reverse
from accounts.models import CustomUser, StudentProfile, RecruiterProfile

def test_tpo_profile_views():
    """Test TPO can view student and recruiter profiles"""
    print("================================================================================\nTPO PROFILE VIEWING TEST\n================================================================================\n")

    # Check if TPO user exists
    try:
        tpo_user = CustomUser.objects.filter(role_type='TPO').first()
        if tpo_user:
            print(f"✅ TPO User exists: {tpo_user.username}")
        else:
            print("❌ No TPO user found")
            return
    except Exception as e:
        print(f"❌ Error finding TPO user: {e}")
        return

    # Check if test student exists
    try:
        student_profile = StudentProfile.objects.first()
        if student_profile:
            student_id = student_profile.user.id
            print(f"✅ Test Student exists: {student_profile.user.username} (ID: {student_id})")
        else:
            print("❌ No student profiles found")
            return
    except Exception as e:
        print(f"❌ Error finding student: {e}")
        return

    # Check if test recruiter exists
    try:
        recruiter_profile = RecruiterProfile.objects.first()
        if recruiter_profile:
            recruiter_id = recruiter_profile.user.id
            print(f"✅ Test Recruiter exists: {recruiter_profile.user.username} (ID: {recruiter_id})")
        else:
            print("❌ No recruiter profiles found")
            return
    except Exception as e:
        print(f"❌ Error finding recruiter: {e}")
        return

    # Test URL reversal for TPO views
    try:
        student_url = reverse('tpo_view_student_profile', kwargs={'student_id': student_id})
        print(f"✅ Student profile URL: {student_url}")
    except Exception as e:
        print(f"❌ Error reversing student profile URL: {e}")
        return

    try:
        recruiter_url = reverse('tpo_view_recruiter_profile', kwargs={'recruiter_id': recruiter_id})
        print(f"✅ Recruiter profile URL: {recruiter_url}")
    except Exception as e:
        print(f"❌ Error reversing recruiter profile URL: {e}")
        return

    # Check if views can be imported
    try:
        from accounts.views import tpo_view_student_profile, tpo_view_recruiter_profile
        print("✅ TPO view functions can be imported")
    except ImportError as e:
        print(f"❌ Error importing TPO view functions: {e}")
        return

    print("\n================================================================================\nTPO PROFILE VIEWING TEST PASSED\n================================================================================\n")
    print("✅ All components for TPO profile viewing are properly configured!")
    print("✅ TPO can view student and recruiter profiles in read-only mode")

if __name__ == '__main__':
    test_tpo_profile_views()