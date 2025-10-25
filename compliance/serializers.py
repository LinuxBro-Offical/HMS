from rest_framework import serializers
from .models import AuditLog, DataPrivacyConsent, ComplianceReport, DataBreachIncident

class AuditLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = AuditLog
        fields = '__all__'

class DataPrivacyConsentSerializer(serializers.ModelSerializer):
    class Meta:
        model = DataPrivacyConsent
        fields = '__all__'

class ComplianceReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = ComplianceReport
        fields = '__all__'

class DataBreachIncidentSerializer(serializers.ModelSerializer):
    class Meta:
        model = DataBreachIncident
        fields = '__all__'
