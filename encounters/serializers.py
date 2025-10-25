from rest_framework import serializers
from .models import Encounter, Prescription, PrescriptionItem, EncounterReport


class EncounterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Encounter
        fields = '__all__'


class PrescriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Prescription
        fields = '__all__'


class PrescriptionItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = PrescriptionItem
        fields = '__all__'


class EncounterReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = EncounterReport
        fields = '__all__'
