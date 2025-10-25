from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import PatientAnalytics, ClinicAnalytics, DoctorPerformance, RevenueAnalytics, CustomReport
from .serializers import PatientAnalyticsSerializer, ClinicAnalyticsSerializer, DoctorPerformanceSerializer, RevenueAnalyticsSerializer, CustomReportSerializer

class PatientAnalyticsViewSet(viewsets.ModelViewSet):
    queryset = PatientAnalytics.objects.all()
    serializer_class = PatientAnalyticsSerializer
    permission_classes = [IsAuthenticated]

class ClinicAnalyticsViewSet(viewsets.ModelViewSet):
    queryset = ClinicAnalytics.objects.all()
    serializer_class = ClinicAnalyticsSerializer
    permission_classes = [IsAuthenticated]

class DoctorPerformanceViewSet(viewsets.ModelViewSet):
    queryset = DoctorPerformance.objects.all()
    serializer_class = DoctorPerformanceSerializer
    permission_classes = [IsAuthenticated]

class RevenueAnalyticsViewSet(viewsets.ModelViewSet):
    queryset = RevenueAnalytics.objects.all()
    serializer_class = RevenueAnalyticsSerializer
    permission_classes = [IsAuthenticated]

class CustomReportViewSet(viewsets.ModelViewSet):
    queryset = CustomReport.objects.all()
    serializer_class = CustomReportSerializer
    permission_classes = [IsAuthenticated]
