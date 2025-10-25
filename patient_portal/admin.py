from django.contrib import admin
from .models import PatientPortalActivity, PatientFeedback, PatientPortalSettings, PatientHealthGoal

@admin.register(PatientPortalActivity)
class PatientPortalActivityAdmin(admin.ModelAdmin):
    list_display = ['patient', 'activity_type', 'created_at']
    list_filter = ['activity_type', 'device_type']
    search_fields = ['patient__full_name']

@admin.register(PatientFeedback)
class PatientFeedbackAdmin(admin.ModelAdmin):
    list_display = ['patient', 'rating', 'category', 'status', 'created_at']
    list_filter = ['rating', 'category', 'status']

@admin.register(PatientPortalSettings)
class PatientPortalSettingsAdmin(admin.ModelAdmin):
    list_display = ['patient', 'email_notifications', 'sms_notifications', 'language']
    list_filter = ['email_notifications', 'sms_notifications']

@admin.register(PatientHealthGoal)
class PatientHealthGoalAdmin(admin.ModelAdmin):
    list_display = ['patient', 'goal_type', 'title', 'status', 'target_date']
    list_filter = ['goal_type', 'status']
