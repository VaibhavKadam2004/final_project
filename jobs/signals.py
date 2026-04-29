"""
Django signals for advanced features automation.
These run automatically when models are created/updated.
"""

from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.utils import timezone
from .models import Application, InterviewSchedule

@receiver(post_save, sender=Application)
def track_application_response_time(sender, instance, created, **kwargs):
    """
    When application status changes from Pending to anything else,
    record the response time (hours from deadline to update).
    
    This auto-populates the response_time_hours field.
    """
    if not created and instance.status != Application.STATUS_PENDING:
        # Status was changed
        if not instance.first_status_change_at:
            instance.first_status_change_at = timezone.now()
        
        # Calculate response time
        if instance.job.deadline:
            delta = instance.first_status_change_at - instance.job.deadline
            instance.response_time_hours = max(0, int(delta.total_seconds() / 3600))
        
        instance.status_last_updated_at = timezone.now()
        
        # Disconnect signal temporarily to avoid recursion
        post_save.disconnect(track_application_response_time, sender=Application)
        instance.save(update_fields=['first_status_change_at', 'response_time_hours', 'status_last_updated_at'])
        post_save.connect(track_application_response_time, sender=Application)
        
        # Recalculate recruiter rating
        try:
            recruiter_rating = instance.job.posted_by.response_rating
            recruiter_rating.calculate_rating()
        except AttributeError:
            pass  # Rating not created yet


@receiver(post_save, sender=InterviewSchedule)
def check_missed_interviews(sender, instance, created, **kwargs):
    """
    Periodically check if students missed scheduled interviews.
    
    If interview date has passed and application is still PENDING,
    apply PCS penalty for no-show.
    
    Note: In production, this should run as a background task (Celery).
    For now, it runs when InterviewSchedule is updated.
    """
    if instance.scheduled_date < timezone.now():
        app = instance.application
        
        # Check if status is still pending (student never responded)
        if app.status == Application.STATUS_PENDING:
            student_profile = app.student.student_profile
            
            # Apply no-show penalty
            if hasattr(student_profile, 'update_pcs'):
                student_profile.update_pcs(
                    'missed_interview',
                    f"No-show for {app.job.title} at {app.job.company} "
                    f"(Scheduled: {instance.scheduled_date.strftime('%Y-%m-%d %H:%M')})"
                )
