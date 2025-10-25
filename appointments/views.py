from rest_framework import viewsets, permissions
from .models import Appointment, DoctorSchedule, TokenCounter
from .serializers import AppointmentSerializer, DoctorScheduleSerializer, TokenCounterSerializer


class AppointmentViewSet(viewsets.ModelViewSet):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer
    permission_classes = [permissions.IsAuthenticated]


class DoctorScheduleViewSet(viewsets.ModelViewSet):
    queryset = DoctorSchedule.objects.all()
    serializer_class = DoctorScheduleSerializer
    permission_classes = [permissions.IsAuthenticated]


class TokenCounterViewSet(viewsets.ModelViewSet):
    queryset = TokenCounter.objects.all()
    serializer_class = TokenCounterSerializer
    permission_classes = [permissions.IsAuthenticated]