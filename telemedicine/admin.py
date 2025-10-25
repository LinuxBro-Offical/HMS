from django.contrib import admin
from .models import TelemedicineSession, TelemedicinePrescription, TelemedicineFollowUp, TelemedicineDevice

@admin.register(TelemedicineSession)
class TelemedicineSessionAdmin(admin.ModelAdmin):
    list_display = ['session_id', 'patient', 'doctor', 'session_type', 'status', 'scheduled_start_time']
    list_filter = ['session_type', 'status', 'platform']
    search_fields = ['session_id', 'patient__full_name']

@admin.register(TelemedicinePrescription)
class TelemedicinePrescriptionAdmin(admin.ModelAdmin):
    list_display = ['session', 'medicine_name', 'is_issued']
    list_filter = ['is_issued']

@admin.register(TelemedicineFollowUp)
class TelemedicineFollowUpAdmin(admin.ModelAdmin):
    list_display = ['session', 'follow_up_type', 'status', 'scheduled_date']
    list_filter = ['follow_up_type', 'status']

@admin.register(TelemedicineDevice)
class TelemedicineDeviceAdmin(admin.ModelAdmin):
    list_display = ['patient', 'device_name', 'device_type', 'is_active']
    list_filter = ['device_type', 'is_active']
