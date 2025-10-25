from rest_framework import serializers
from .models import ClinicalGuideline, DrugInteraction, ClinicalAlert


class ClinicalGuidelineSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClinicalGuideline
        fields = '__all__'


class DrugInteractionSerializer(serializers.ModelSerializer):
    class Meta:
        model = DrugInteraction
        fields = '__all__'


class ClinicalAlertSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClinicalAlert
        fields = '__all__'
