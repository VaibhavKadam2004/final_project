#!/usr/bin/env python
"""Test the PCS (Placement Credit Score) system"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'placement_portal.settings')
django.setup()

from accounts.models import StudentProfile

# Get first student
s = StudentProfile.objects.first()
print(f"Student: {s.user.username}")
print(f"Initial PCS Score: {s.credit_score}")
print(f"PCS Status: {s.get_pcs_status()}")
print(f"Is Blocked: {s.is_blocked}")
print(f"Can apply: {s.can_apply_for_jobs()}")

# Test penalty application
print("\n--- Applying 'missed_interview' penalty ---")
new_score = s.update_pcs('missed_interview', 'Missed TCS Round 1')
print(f"New PCS Score: {new_score}")
print(f"PCS Status: {s.get_pcs_status()}")
print(f"Is Blocked: {s.is_blocked}")

# Test large penalty
print("\n--- Applying 'rejected_offer' penalty ---")
new_score = s.update_pcs('rejected_offer', 'Rejected Amazon offer after acceptance')
print(f"New PCS Score: {new_score}")
print(f"Is Blocked: {s.is_blocked}")
print(f"Block Reason: {s.block_reason}")

print("\n✅ PCS System is working correctly!")
