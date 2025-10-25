from django.contrib import admin
from .models import AuditLog, DataPrivacyConsent, ComplianceReport, DataBreachIncident

@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = ['user', 'action', 'model_name', 'risk_level', 'timestamp']
    list_filter = ['action', 'risk_level']
    search_fields = ['user__username', 'model_name']

@admin.register(DataPrivacyConsent)
class DataPrivacyConsentAdmin(admin.ModelAdmin):
    list_display = ['patient', 'consent_type', 'granted', 'granted_at']
    list_filter = ['consent_type', 'granted']

@admin.register(ComplianceReport)
class ComplianceReportAdmin(admin.ModelAdmin):
    list_display = ['title', 'report_type', 'status', 'created_by', 'created_at']
    list_filter = ['report_type', 'status']

@admin.register(DataBreachIncident)
class DataBreachIncidentAdmin(admin.ModelAdmin):
    list_display = ['incident_title', 'incident_type', 'severity', 'status', 'discovered_at']
    list_filter = ['incident_type', 'severity', 'status']
