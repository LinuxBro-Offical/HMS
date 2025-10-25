from django.contrib import admin
from .models import ExternalSystem, DataSyncLog, IntegrationMapping, WebhookEndpoint, IntegrationError

@admin.register(ExternalSystem)
class ExternalSystemAdmin(admin.ModelAdmin):
    list_display = ['name', 'system_type', 'is_active', 'connection_status', 'last_sync']
    list_filter = ['system_type', 'is_active', 'connection_status']

@admin.register(DataSyncLog)
class DataSyncLogAdmin(admin.ModelAdmin):
    list_display = ['external_system', 'sync_type', 'status', 'started_at', 'records_processed']
    list_filter = ['sync_type', 'status']

@admin.register(IntegrationMapping)
class IntegrationMappingAdmin(admin.ModelAdmin):
    list_display = ['external_system', 'hms_model', 'hms_field', 'external_field', 'is_active']
    list_filter = ['hms_model', 'is_active']

@admin.register(WebhookEndpoint)
class WebhookEndpointAdmin(admin.ModelAdmin):
    list_display = ['name', 'external_system', 'is_active', 'last_triggered']
    list_filter = ['is_active']

@admin.register(IntegrationError)
class IntegrationErrorAdmin(admin.ModelAdmin):
    list_display = ['external_system', 'error_type', 'status', 'created_at']
    list_filter = ['error_type', 'status']
