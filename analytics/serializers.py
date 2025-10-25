from rest_framework import serializers
from .models import PatientAnalytics, ClinicAnalytics, DoctorPerformance, RevenueAnalytics, CustomReport

class PatientAnalyticsSerializer(serializers.ModelSerializer):
    class Meta:
        model = PatientAnalytics
        fields = '__all__'

class ClinicAnalyticsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClinicAnalytics
        fields = '__all__'

class DoctorPerformanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = DoctorPerformance
        fields = '__all__'

class RevenueAnalyticsSerializer(serializers.ModelSerializer):
    class Meta:
        model = RevenueAnalytics
        fields = '__all__'

class CustomReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomReport
        fields = '__all__'
