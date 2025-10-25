from rest_framework import viewsets, permissions
from .models import Encounter, Prescription, PrescriptionItem, EncounterReport
from .serializers import EncounterSerializer, PrescriptionSerializer, PrescriptionItemSerializer, EncounterReportSerializer


class EncounterViewSet(viewsets.ModelViewSet):
    queryset = Encounter.objects.all()
    serializer_class = EncounterSerializer
    permission_classes = [permissions.IsAuthenticated]


class PrescriptionViewSet(viewsets.ModelViewSet):
    queryset = Prescription.objects.all()
    serializer_class = PrescriptionSerializer
    permission_classes = [permissions.IsAuthenticated]


class PrescriptionItemViewSet(viewsets.ModelViewSet):
    queryset = PrescriptionItem.objects.all()
    serializer_class = PrescriptionItemSerializer
    permission_classes = [permissions.IsAuthenticated]


class EncounterReportViewSet(viewsets.ModelViewSet):
    queryset = EncounterReport.objects.all()
    serializer_class = EncounterReportSerializer
    permission_classes = [permissions.IsAuthenticated]