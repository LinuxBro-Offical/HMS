from django.contrib import admin
from .models import DoctorSchedule, TokenCounter, Appointment, AppointmentStatusHistory


@admin.register(DoctorSchedule)
class DoctorScheduleAdmin(admin.ModelAdmin):
    list_display = ('doctor', 'branch', 'weekday', 'start_time', 'end_time', 'is_active')
    search_fields = ('doctor__user__email', 'doctor__user__full_name', 'branch__name')
    list_filter = ('weekday', 'is_active', 'branch')


@admin.register(TokenCounter)
class TokenCounterAdmin(admin.ModelAdmin):
    list_display = ('doctor', 'branch', 'date', 'last_token')
    search_fields = ('doctor__user__email', 'branch__name')
    list_filter = ('date', 'branch')


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('patient', 'doctor', 'appointment_date', 'appointment_time', 'status', 'source')
    search_fields = ('patient__full_name', 'patient__patient_code', 'doctor__user__email')
    list_filter = ('status', 'source', 'appointment_date', 'branch')
    ordering = ('-appointment_date', '-appointment_time')


@admin.register(AppointmentStatusHistory)
class AppointmentStatusHistoryAdmin(admin.ModelAdmin):
    list_display = ('appointment', 'old_status', 'new_status', 'changed_at', 'updated_by')
    search_fields = ('appointment__patient__full_name', 'appointment__patient__patient_code')
    list_filter = ('old_status', 'new_status', 'changed_at')