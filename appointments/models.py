from django.db import models
from django.utils import timezone
import uuid


class DoctorSchedule(models.Model):
    """
    Defines the weekly availability of a doctor for appointment booking.
    """
    doctor = models.ForeignKey('users.StaffProfile', on_delete=models.CASCADE, related_name='schedules')
    branch = models.ForeignKey('tenants.Branch', on_delete=models.CASCADE, related_name='doctor_schedules')

    WEEKDAY_CHOICES = [
        (0, 'Monday'), (1, 'Tuesday'), (2, 'Wednesday'),
        (3, 'Thursday'), (4, 'Friday'), (5, 'Saturday'), (6, 'Sunday')
    ]
    weekday = models.IntegerField(choices=WEEKDAY_CHOICES)
    start_time = models.TimeField()
    end_time = models.TimeField()
    slot_duration_minutes = models.PositiveIntegerField(default=15)
    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('doctor', 'branch', 'weekday')
        ordering = ['doctor', 'weekday']

    def __str__(self):
        return f"{self.doctor.user.email} ({self.get_weekday_display()} {self.start_time}-{self.end_time})"


class TokenCounter(models.Model):
    """
    Manages token numbers per doctor per day.
    """
    doctor = models.ForeignKey('users.StaffProfile', on_delete=models.CASCADE, related_name='tokens')
    branch = models.ForeignKey('tenants.Branch', on_delete=models.CASCADE)
    date = models.DateField(default=timezone.now)
    last_token = models.PositiveIntegerField(default=0)

    class Meta:
        unique_together = ('doctor', 'branch', 'date')

    def get_next_token(self):
        self.last_token += 1
        self.save(update_fields=['last_token'])
        return self.last_token

    def __str__(self):
        return f"{self.doctor.user.email} - {self.date} ({self.last_token})"


class Appointment(models.Model):
    """
    Core appointment record. Each appointment is linked to one patient and one doctor.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    patient = models.ForeignKey('patients.Patient', on_delete=models.CASCADE, related_name='appointments')
    doctor = models.ForeignKey('users.StaffProfile', on_delete=models.CASCADE, related_name='appointments')
    branch = models.ForeignKey('tenants.Branch', on_delete=models.CASCADE, related_name='appointments')

    appointment_date = models.DateField()
    appointment_time = models.TimeField(null=True, blank=True)
    token_number = models.PositiveIntegerField(null=True, blank=True)
    source = models.CharField(
        max_length=20,
        choices=[('CALL', 'Call'), ('WHATSAPP', 'WhatsApp'), ('DIRECT', 'Direct Walk-in')],
        default='DIRECT'
    )

    STATUS_CHOICES = [
        ('BOOKED', 'Booked'),
        ('CONFIRMED', 'Confirmed'),
        ('IN_PROGRESS', 'In Progress'),
        ('COMPLETED', 'Completed'),
        ('CANCELLED', 'Cancelled'),
        ('NO_SHOW', 'No Show'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='BOOKED')

    encounter = models.OneToOneField('encounters.Encounter', on_delete=models.SET_NULL, null=True, blank=True, related_name='appointment_link')
    remarks = models.TextField(blank=True, null=True)
    notified = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['appointment_date', 'appointment_time']

    def __str__(self):
        return f"{self.patient.full_name} - {self.doctor.user.email} ({self.appointment_date})"

    def mark_status(self, new_status, updated_by=None):
        """
        Change appointment status and log it to history.
        """
        old_status = self.status
        self.status = new_status
        self.save(update_fields=['status'])
        AppointmentStatusHistory.objects.create(
            appointment=self,
            old_status=old_status,
            new_status=new_status,
            updated_by=updated_by
        )


class AppointmentStatusHistory(models.Model):
    """
    Keeps audit of all appointment status changes.
    """
    appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE, related_name='status_history')
    old_status = models.CharField(max_length=20)
    new_status = models.CharField(max_length=20)
    changed_at = models.DateTimeField(auto_now_add=True)
    updated_by = models.ForeignKey('users.User', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.appointment.patient.full_name}: {self.old_status} → {self.new_status}"