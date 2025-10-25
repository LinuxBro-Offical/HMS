from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import PatientPortalActivity, PatientFeedback, PatientPortalSettings, PatientHealthGoal
from .serializers import PatientPortalActivitySerializer, PatientFeedbackSerializer, PatientPortalSettingsSerializer, PatientHealthGoalSerializer

class PatientPortalActivityViewSet(viewsets.ModelViewSet):
    queryset = PatientPortalActivity.objects.all()
    serializer_class = PatientPortalActivitySerializer
    permission_classes = [IsAuthenticated]

class PatientFeedbackViewSet(viewsets.ModelViewSet):
    queryset = PatientFeedback.objects.all()
    serializer_class = PatientFeedbackSerializer
    permission_classes = [IsAuthenticated]

class PatientPortalSettingsViewSet(viewsets.ModelViewSet):
    queryset = PatientPortalSettings.objects.all()
    serializer_class = PatientPortalSettingsSerializer
    permission_classes = [IsAuthenticated]

class PatientHealthGoalViewSet(viewsets.ModelViewSet):
    queryset = PatientHealthGoal.objects.all()
    serializer_class = PatientHealthGoalSerializer
    permission_classes = [IsAuthenticated]
