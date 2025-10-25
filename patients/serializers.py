from rest_framework import serializers
from .models import Patient, PatientCondition, PatientAllergy, PatientReport


class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = '__all__'


class PatientConditionSerializer(serializers.ModelSerializer):
    class Meta:
        model = PatientCondition
        fields = '__all__'


class PatientAllergySerializer(serializers.ModelSerializer):
    class Meta:
        model = PatientAllergy
        fields = '__all__'


class PatientReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = PatientReport
        fields = '__all__'
