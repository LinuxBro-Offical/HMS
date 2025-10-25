from rest_framework import viewsets, permissions
from .models import TenantNotificationSetting, NotificationTemplate, NotificationEvent, NotificationLog
from .serializers import TenantNotificationSettingSerializer, NotificationTemplateSerializer, NotificationEventSerializer, NotificationLogSerializer


class TenantNotificationSettingViewSet(viewsets.ModelViewSet):
    queryset = TenantNotificationSetting.objects.all()
    serializer_class = TenantNotificationSettingSerializer
    permission_classes = [permissions.IsAuthenticated]


class NotificationTemplateViewSet(viewsets.ModelViewSet):
    queryset = NotificationTemplate.objects.all()
    serializer_class = NotificationTemplateSerializer
    permission_classes = [permissions.IsAuthenticated]


class NotificationEventViewSet(viewsets.ModelViewSet):
    queryset = NotificationEvent.objects.all()
    serializer_class = NotificationEventSerializer
    permission_classes = [permissions.IsAuthenticated]


class NotificationLogViewSet(viewsets.ModelViewSet):
    queryset = NotificationLog.objects.all()
    serializer_class = NotificationLogSerializer
    permission_classes = [permissions.IsAuthenticated]