from django.contrib import admin
from .models import PatientAnalytics, ClinicAnalytics, DoctorPerformance, RevenueAnalytics, CustomReport

@admin.register(PatientAnalytics)
class PatientAnalyticsAdmin(admin.ModelAdmin):
    list_display = ['patient', 'metric_type', 'metric_value', 'recorded_date']
    list_filter = ['metric_type', 'source']

@admin.register(ClinicAnalytics)
class ClinicAnalyticsAdmin(admin.ModelAdmin):
    list_display = ['branch', 'metric_name', 'metric_value', 'date', 'period_type']
    list_filter = ['metric_name', 'period_type']

@admin.register(DoctorPerformance)
class DoctorPerformanceAdmin(admin.ModelAdmin):
    list_display = ['doctor', 'period_start', 'period_end', 'total_patients', 'total_revenue']
    list_filter = ['branch']

@admin.register(RevenueAnalytics)
class RevenueAnalyticsAdmin(admin.ModelAdmin):
    list_display = ['branch', 'date', 'total_revenue', 'net_profit', 'period_type']
    list_filter = ['period_type']

@admin.register(CustomReport)
class CustomReportAdmin(admin.ModelAdmin):
    list_display = ['name', 'report_type', 'created_by', 'is_public']
    list_filter = ['report_type', 'is_public']
