from django.contrib import admin
from .models import Encounter, Prescription, PrescriptionItem, EncounterReport


@admin.register(Encounter)
class EncounterAdmin(admin.ModelAdmin):
    list_display = ('patient', 'doctor', 'encounter_date', 'chief_complaint', 'follow_up_required')
    search_fields = ('patient__full_name', 'patient__patient_code', 'doctor__user__email')
    list_filter = ('encounter_date', 'follow_up_required', 'branch')
    ordering = ('-encounter_date',)


@admin.register(Prescription)
class PrescriptionAdmin(admin.ModelAdmin):
    list_display = ('encounter', 'prescribed_at')
    search_fields = ('encounter__patient__full_name', 'encounter__patient__patient_code')
    list_filter = ('prescribed_at',)


@admin.register(PrescriptionItem)
class PrescriptionItemAdmin(admin.ModelAdmin):
    list_display = ('prescription', 'medicine_name', 'dosage', 'frequency', 'duration_days')
    search_fields = ('medicine_name', 'prescription__encounter__patient__full_name')
    list_filter = ('is_conflicting',)


@admin.register(EncounterReport)
class EncounterReportAdmin(admin.ModelAdmin):
    list_display = ('encounter', 'title', 'uploaded_at')
    search_fields = ('title', 'encounter__patient__full_name', 'encounter__patient__patient_code')
    list_filter = ('uploaded_at',)