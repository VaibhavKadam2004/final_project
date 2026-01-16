from django.contrib import admin
from .models import (
    JobPost, Application, DreamCompany, HistoricalHiringData,
    InterviewExperience, PrepVault, RecruiterResponseRating
)

@admin.register(JobPost)
class JobPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'company', 'posted_by', 'status', 'deadline', 'package')
    list_filter = ('status', 'job_type', 'deadline')
    search_fields = ('title', 'company', 'description')
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        ('Job Details', {
            'fields': ('title', 'company', 'description', 'job_type', 'posted_by')
        }),
        ('Eligibility Criteria', {
            'fields': ('min_cgpa', 'max_backlogs', 'branches')
        }),
        ('Compensation & Deadline', {
            'fields': ('package', 'deadline')
        }),
        ('Status & Timestamps', {
            'fields': ('status', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    actions = ['open_jobs', 'close_jobs']

    def open_jobs(self, request, queryset):
        """Bulk action to open jobs"""
        updated = queryset.update(status='Open')
        self.message_user(request, f'{updated} job(s) have been opened.')
    open_jobs.short_description = "Open selected jobs"

    def close_jobs(self, request, queryset):
        """Bulk action to close jobs"""
        updated = queryset.update(status='Closed')
        self.message_user(request, f'{updated} job(s) have been closed.')
    close_jobs.short_description = "Close selected jobs"

@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ('job', 'student', 'status', 'applied_at', 'response_time_hours')
    list_filter = ('status', 'applied_at', 'is_closed')
    search_fields = ('student__username', 'job__title')
    readonly_fields = ('applied_at', 'first_status_change_at', 'status_last_updated_at', 'response_time_hours')


# ============================================================
# ADVANCED FEATURES: Admin Registration
# ============================================================

@admin.register(DreamCompany)
class DreamCompanyAdmin(admin.ModelAdmin):
    list_display = ('student', 'company_name', 'avg_cgpa_required', 'created_at')
    list_filter = ('created_at', 'avg_cgpa_required')
    search_fields = ('student__username', 'company_name')
    readonly_fields = ('created_at', 'updated_at')
    
    def get_readiness(self, obj):
        return f"{obj.get_readiness_percentage()}%"
    get_readiness.short_description = "Readiness"


@admin.register(HistoricalHiringData)
class HistoricalHiringDataAdmin(admin.ModelAdmin):
    list_display = ('company_name', 'avg_cgpa', 'success_rate', 'students_hired', 'avg_interview_rounds')
    list_filter = ('success_rate', 'avg_cgpa')
    search_fields = ('company_name',)
    readonly_fields = ('last_visited_date',)


@admin.register(InterviewExperience)
class InterviewExperienceAdmin(admin.ModelAdmin):
    list_display = ('student', 'company', 'round_number', 'difficulty', 'status', 'created_at')
    list_filter = ('status', 'difficulty', 'created_at', 'selected_after')
    search_fields = ('student__username', 'company', 'questions_asked')
    readonly_fields = ('created_at', 'views_count', 'helpful_count')
    actions = ['approve_experiences', 'reject_experiences']
    
    def approve_experiences(self, request, queryset):
        """Bulk approve experiences"""
        updated = queryset.update(
            status=InterviewExperience.STATUS_APPROVED,
            approved_by=request.user
        )
        self.message_user(request, f'{updated} experience(s) approved!')
    approve_experiences.short_description = "Approve selected experiences"
    
    def reject_experiences(self, request, queryset):
        """Bulk reject experiences"""
        updated = queryset.update(
            status=InterviewExperience.STATUS_REJECTED,
            approved_by=request.user
        )
        self.message_user(request, f'{updated} experience(s) rejected!')
    reject_experiences.short_description = "Reject selected experiences"


@admin.register(PrepVault)
class PrepVaultAdmin(admin.ModelAdmin):
    list_display = ('company', 'total_experiences', 'avg_selection_rate', 'last_updated')
    list_filter = ('avg_selection_rate', 'last_updated')
    search_fields = ('company__company_name',)
    readonly_fields = ('last_updated',)


@admin.register(RecruiterResponseRating)
class RecruiterResponseRatingAdmin(admin.ModelAdmin):
    list_display = ('recruiter', 'rating_label', 'responsiveness_rating', 'avg_response_hours', 'total_applications')
    list_filter = ('responsiveness_rating', 'last_updated')
    search_fields = ('recruiter__username', 'rating_label')
    readonly_fields = ('last_updated', 'avg_response_hours')
    
    def has_add_permission(self, request):
        """Ratings are auto-created, don't allow manual creation"""
        return False
