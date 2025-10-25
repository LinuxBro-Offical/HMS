from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import LabTest, LabOrder, LabResult
from .serializers import LabTestSerializer, LabOrderSerializer, LabResultSerializer


class LabTestViewSet(viewsets.ModelViewSet):
    queryset = LabTest.objects.all()
    serializer_class = LabTestSerializer
    permission_classes = [IsAuthenticated]


class LabOrderViewSet(viewsets.ModelViewSet):
    queryset = LabOrder.objects.all()
    serializer_class = LabOrderSerializer
    permission_classes = [IsAuthenticated]


class LabResultViewSet(viewsets.ModelViewSet):
    queryset = LabResult.objects.all()
    serializer_class = LabResultSerializer
    permission_classes = [IsAuthenticated]