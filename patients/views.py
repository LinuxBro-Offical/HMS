from rest_framework import viewsets, permissions
from .models import Patient, PatientCondition, PatientAllergy, PatientReport
from .serializers import PatientSerializer, PatientConditionSerializer, PatientAllergySerializer, PatientReportSerializer


class PatientViewSet(viewsets.ModelViewSet):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer
    permission_classes = [permissions.IsAuthenticated]


class PatientConditionViewSet(viewsets.ModelViewSet):
    queryset = PatientCondition.objects.all()
    serializer_class = PatientConditionSerializer
    permission_classes = [permissions.IsAuthenticated]


class PatientAllergyViewSet(viewsets.ModelViewSet):
    queryset = PatientAllergy.objects.all()
    serializer_class = PatientAllergySerializer
    permission_classes = [permissions.IsAuthenticated]


class PatientReportViewSet(viewsets.ModelViewSet):
    queryset = PatientReport.objects.all()
    serializer_class = PatientReportSerializer
    permission_classes = [permissions.IsAuthenticated]