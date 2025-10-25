from rest_framework import serializers
from .models import PatientPortalActivity, PatientFeedback, PatientPortalSettings, PatientHealthGoal

class PatientPortalActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = PatientPortalActivity
        fields = '__all__'

class PatientFeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = PatientFeedback
        fields = '__all__'

class PatientPortalSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = PatientPortalSettings
        fields = '__all__'

class PatientHealthGoalSerializer(serializers.ModelSerializer):
    class Meta:
        model = PatientHealthGoal
        fields = '__all__'
