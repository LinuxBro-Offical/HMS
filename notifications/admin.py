from django.contrib import admin
from .models import TenantNotificationSetting, NotificationTemplate, NotificationEvent, NotificationLog


@admin.register(TenantNotificationSetting)
class TenantNotificationSettingAdmin(admin.ModelAdmin):
    list_display = ('tenant', 'sms_enabled', 'whatsapp_enabled', 'sms_provider', 'whatsapp_provider')
    search_fields = ('tenant',)
    list_filter = ('sms_enabled', 'whatsapp_enabled', 'sms_provider', 'whatsapp_provider')


@admin.register(NotificationTemplate)
class NotificationTemplateAdmin(admin.ModelAdmin):
    list_display = ('tenant', 'event', 'channel', 'is_active', 'created_at')
    search_fields = ('tenant', 'event', 'channel')
    list_filter = ('event', 'channel', 'is_active', 'created_at')


@admin.register(NotificationEvent)
class NotificationEventAdmin(admin.ModelAdmin):
    list_display = ('tenant', 'event', 'channel', 'to', 'status', 'created_at')
    search_fields = ('tenant', 'to', 'event')
    list_filter = ('status', 'event', 'channel', 'created_at')
    readonly_fields = ('status', 'attempts', 'last_error')


@admin.register(NotificationLog)
class NotificationLogAdmin(admin.ModelAdmin):
    list_display = ('event', 'channel', 'to', 'status', 'sent_at')
    search_fields = ('to', 'event__tenant')
    list_filter = ('status', 'channel', 'sent_at')