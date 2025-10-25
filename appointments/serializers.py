from rest_framework import serializers
from .models import Appointment, DoctorSchedule, TokenCounter


class AppointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = '__all__'


class DoctorScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = DoctorSchedule
        fields = '__all__'


class TokenCounterSerializer(serializers.ModelSerializer):
    class Meta:
        model = TokenCounter
        fields = '__all__'
