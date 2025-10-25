from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import ExternalSystem, DataSyncLog, IntegrationMapping, WebhookEndpoint, IntegrationError
from .serializers import ExternalSystemSerializer, DataSyncLogSerializer, IntegrationMappingSerializer, WebhookEndpointSerializer, IntegrationErrorSerializer

class ExternalSystemViewSet(viewsets.ModelViewSet):
    queryset = ExternalSystem.objects.all()
    serializer_class = ExternalSystemSerializer
    permission_classes = [IsAuthenticated]

class DataSyncLogViewSet(viewsets.ModelViewSet):
    queryset = DataSyncLog.objects.all()
    serializer_class = DataSyncLogSerializer
    permission_classes = [IsAuthenticated]

class IntegrationMappingViewSet(viewsets.ModelViewSet):
    queryset = IntegrationMapping.objects.all()
    serializer_class = IntegrationMappingSerializer
    permission_classes = [IsAuthenticated]

class WebhookEndpointViewSet(viewsets.ModelViewSet):
    queryset = WebhookEndpoint.objects.all()
    serializer_class = WebhookEndpointSerializer
    permission_classes = [IsAuthenticated]

class IntegrationErrorViewSet(viewsets.ModelViewSet):
    queryset = IntegrationError.objects.all()
    serializer_class = IntegrationErrorSerializer
    permission_classes = [IsAuthenticated]
