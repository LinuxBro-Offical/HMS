from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import AuditLog, DataPrivacyConsent, ComplianceReport, DataBreachIncident
from .serializers import AuditLogSerializer, DataPrivacyConsentSerializer, ComplianceReportSerializer, DataBreachIncidentSerializer

class AuditLogViewSet(viewsets.ModelViewSet):
    queryset = AuditLog.objects.all()
    serializer_class = AuditLogSerializer
    permission_classes = [IsAuthenticated]

class DataPrivacyConsentViewSet(viewsets.ModelViewSet):
    queryset = DataPrivacyConsent.objects.all()
    serializer_class = DataPrivacyConsentSerializer
    permission_classes = [IsAuthenticated]

class ComplianceReportViewSet(viewsets.ModelViewSet):
    queryset = ComplianceReport.objects.all()
    serializer_class = ComplianceReportSerializer
    permission_classes = [IsAuthenticated]

class DataBreachIncidentViewSet(viewsets.ModelViewSet):
    queryset = DataBreachIncident.objects.all()
    serializer_class = DataBreachIncidentSerializer
    permission_classes = [IsAuthenticated]
