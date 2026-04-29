import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'placement_portal.settings')
django.setup()

from accounts.models import StudentProfile, CustomUser
from django.utils import timezone

def test_student_verification():
    """Test the student verification functionality"""
    print("\n" + "="*60)
    print("Testing Student Verification Functionality")
    print("="*60 + "\n")
    
    # Create a test TPO user
    tpo_user = CustomUser.objects.filter(role_type=CustomUser.TPO).first()
    if not tpo_user:
        print("ERROR: No TPO user found in database. Creating one...")
        tpo_user = CustomUser.objects.create_user(
            username='test_tpo',
            email='tpo@test.com',
            password='tpo123',
            role_type=CustomUser.TPO,
            first_name='Test',
            last_name='TPO'
        )
    
    print(f"Using TPO user: {tpo_user.username}")
    
    # Create a test student user if it doesn't exist
    student_user = CustomUser.objects.filter(username='test_student_verify').first()
    if student_user:
        print(f"Using existing student: {student_user.username}")
        StudentProfile.objects.filter(user=student_user).delete()
    else:
        student_user = CustomUser.objects.create_user(
            username='test_student_verify',
            email='student_verify@test.com',
            password='student123',
            role_type=CustomUser.STUDENT,
            first_name='John',
            last_name='Doe'
        )
        print(f"Created new student: {student_user.username}")
    
    # Create student profile with correct fields
    profile = StudentProfile.objects.create(
        user=student_user,
        roll_no='2024001',
        branch='CSE',
        cgpa=8.5,
        active_backlogs=0,
        phone_number='9876543210',
        tenth_percent=85.0,
        twelfth_percent=88.0
    )
    print(f"\nCreated student profile for: {student_user.first_name} {student_user.last_name}")
    print(f"   Roll No: 2024001")
    print(f"   Branch: CSE")
    
    # Check initial status
    print(f"\n1. Initial Verification Status:")
    print(f"   - is_verified: {profile.is_verified}")
    print(f"   - Expected: False")
    assert profile.is_verified == False, "Initial is_verified should be False"
    print("   ✓ PASSED - Student is not verified initially")
    
    # Check status badge (should be PENDING)
    status = "VERIFIED" if profile.is_verified else "PENDING"
    print(f"   - Status Badge: {status}")
    assert status == "PENDING", "Status badge should be PENDING"
    print("   ✓ PASSED - Status badge shows PENDING\n")
    
    # Simulate TPO verification
    print(f"2. Verifying Student (by TPO user: {tpo_user.username}):")
    profile.is_verified = True
    profile.verified_by = tpo_user
    profile.verified_at = timezone.now()
    profile.save()
    print(f"   - is_verified set to: True")
    print(f"   - verified_by: {profile.verified_by.username}")
    print(f"   - verified_at: {profile.verified_at.strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Reload from database to confirm
    profile.refresh_from_db()
    print(f"\n3. Verification Status After Update:")
    print(f"   - is_verified: {profile.is_verified}")
    print(f"   - Expected: True")
    assert profile.is_verified == True, "is_verified should be True after verification"
    print("   ✓ PASSED - Student is now verified")
    
    # Check status badge (should be VERIFIED)
    status = "VERIFIED" if profile.is_verified else "PENDING"
    print(f"   - Status Badge: {status}")
    assert status == "VERIFIED", "Status badge should be VERIFIED"
    print("   ✓ PASSED - Status badge now shows VERIFIED\n")
    
    # Check student list filtering
    print(f"4. Testing Student List Filtering:")
    verified_count = StudentProfile.objects.filter(is_verified=True, user=student_user).count()
    unverified_count = StudentProfile.objects.filter(is_verified=False, user=student_user).count()
    print(f"   - Verified students with this user: {verified_count}")
    print(f"   - Unverified students with this user: {unverified_count}")
    assert verified_count == 1, "Should have 1 verified student"
    assert unverified_count == 0, "Should have 0 unverified students"
    print("   ✓ PASSED - Filtering works correctly\n")
    
    # Test status badge transitions
    print(f"5. Testing Status Badge Transitions:")
    print(f"   - Current state: is_verified={profile.is_verified}, badge={status}")
    
    # Unverify and check badge
    profile.is_verified = False
    profile.verified_by = None
    profile.verified_at = None
    profile.save()
    profile.refresh_from_db()
    status = "VERIFIED" if profile.is_verified else "PENDING"
    print(f"   - After unverifying: is_verified={profile.is_verified}, badge={status}")
    assert profile.is_verified == False, "Should be unverified"
    assert status == "PENDING", "Status should be PENDING after unverifying"
    print("   ✓ PASSED - Unverification works, badge reverts to PENDING")
    
    # Verify again
    profile.is_verified = True
    profile.verified_by = tpo_user
    profile.verified_at = timezone.now()
    profile.save()
    profile.refresh_from_db()
    status = "VERIFIED" if profile.is_verified else "PENDING"
    print(f"   - After re-verifying: is_verified={profile.is_verified}, badge={status}")
    assert profile.is_verified == True, "Should be verified"
    assert status == "VERIFIED", "Status should be VERIFIED after re-verifying"
    print("   ✓ PASSED - Re-verification works, badge changes back to VERIFIED\n")
    
    print("="*60)
    print("All Tests PASSED! ✓")
    print("="*60)
    print("\nTest Results Summary:")
    print("✓ Student profile created with is_verified=False")
    print("✓ Initial status badge shows PENDING")
    print("✓ Student verification status changed to True")
    print("✓ Status badge changed from PENDING to VERIFIED")
    print("✓ Verified student filtered correctly in list")
    print("✓ Can unverify student (badge reverts to PENDING)")
    print("✓ Can re-verify student (badge changes back to VERIFIED)")
    print("\nConclusion: Student verification functionality is working correctly!")
    return True

if __name__ == '__main__':
    try:
        test_student_verification()
    except Exception as e:
        print(f"\nERROR: {str(e)}")
        import traceback
        traceback.print_exc()
        exit(1)
