from django.contrib import admin
from .models import Patient, PatientCondition, PatientAllergy, PatientReport


@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ('patient_code', 'full_name', 'phone', 'gender', 'date_registered', 'is_active')
    search_fields = ('patient_code', 'full_name', 'phone', 'email')
    list_filter = ('gender', 'is_active', 'date_registered', 'is_vip')
    ordering = ('-date_registered',)


@admin.register(PatientCondition)
class PatientConditionAdmin(admin.ModelAdmin):
    list_display = ('patient', 'name', 'diagnosed_date', 'active')
    search_fields = ('patient__full_name', 'patient__patient_code', 'name')
    list_filter = ('active', 'diagnosed_date')


@admin.register(PatientAllergy)
class PatientAllergyAdmin(admin.ModelAdmin):
    list_display = ('patient', 'allergen', 'reaction', 'severity')
    search_fields = ('patient__full_name', 'patient__patient_code', 'allergen')
    list_filter = ('severity',)


@admin.register(PatientReport)
class PatientReportAdmin(admin.ModelAdmin):
    list_display = ('patient', 'title', 'uploaded_at', 'uploaded_by')
    search_fields = ('patient__full_name', 'patient__patient_code', 'title')
    list_filter = ('uploaded_at',)