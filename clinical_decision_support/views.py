from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import ClinicalGuideline, DrugInteraction, ClinicalAlert
from .serializers import ClinicalGuidelineSerializer, DrugInteractionSerializer, ClinicalAlertSerializer


class ClinicalGuidelineViewSet(viewsets.ModelViewSet):
    queryset = ClinicalGuideline.objects.all()
    serializer_class = ClinicalGuidelineSerializer
    permission_classes = [IsAuthenticated]


class DrugInteractionViewSet(viewsets.ModelViewSet):
    queryset = DrugInteraction.objects.all()
    serializer_class = DrugInteractionSerializer
    permission_classes = [IsAuthenticated]


class ClinicalAlertViewSet(viewsets.ModelViewSet):
    queryset = ClinicalAlert.objects.all()
    serializer_class = ClinicalAlertSerializer
    permission_classes = [IsAuthenticated]