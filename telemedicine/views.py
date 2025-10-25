from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import TelemedicineSession, TelemedicinePrescription, TelemedicineFollowUp, TelemedicineDevice
from .serializers import TelemedicineSessionSerializer, TelemedicinePrescriptionSerializer, TelemedicineFollowUpSerializer, TelemedicineDeviceSerializer

class TelemedicineSessionViewSet(viewsets.ModelViewSet):
    queryset = TelemedicineSession.objects.all()
    serializer_class = TelemedicineSessionSerializer
    permission_classes = [IsAuthenticated]

class TelemedicinePrescriptionViewSet(viewsets.ModelViewSet):
    queryset = TelemedicinePrescription.objects.all()
    serializer_class = TelemedicinePrescriptionSerializer
    permission_classes = [IsAuthenticated]

class TelemedicineFollowUpViewSet(viewsets.ModelViewSet):
    queryset = TelemedicineFollowUp.objects.all()
    serializer_class = TelemedicineFollowUpSerializer
    permission_classes = [IsAuthenticated]

class TelemedicineDeviceViewSet(viewsets.ModelViewSet):
    queryset = TelemedicineDevice.objects.all()
    serializer_class = TelemedicineDeviceSerializer
    permission_classes = [IsAuthenticated]
