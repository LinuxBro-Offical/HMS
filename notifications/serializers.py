from rest_framework import serializers
from .models import TenantNotificationSetting, NotificationTemplate, NotificationEvent, NotificationLog


class TenantNotificationSettingSerializer(serializers.ModelSerializer):
    class Meta:
        model = TenantNotificationSetting
        fields = '__all__'


class NotificationTemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = NotificationTemplate
        fields = '__all__'


class NotificationEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = NotificationEvent
        fields = '__all__'


class NotificationLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = NotificationLog
        fields = '__all__'
