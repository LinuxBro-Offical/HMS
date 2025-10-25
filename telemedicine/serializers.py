from rest_framework import serializers
from .models import TelemedicineSession, TelemedicinePrescription, TelemedicineFollowUp, TelemedicineDevice

class TelemedicineSessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = TelemedicineSession
        fields = '__all__'

class TelemedicinePrescriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = TelemedicinePrescription
        fields = '__all__'

class TelemedicineFollowUpSerializer(serializers.ModelSerializer):
    class Meta:
        model = TelemedicineFollowUp
        fields = '__all__'

class TelemedicineDeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = TelemedicineDevice
        fields = '__all__'
