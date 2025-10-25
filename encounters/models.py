from django.db import models
from django.utils import timezone
import uuid


class Encounter(models.Model):
    """
    Represents a doctor-patient consultation session.
    - One Encounter per Appointment
    - Holds diagnoses, complaints, notes, and follow-up details
    - Core EMR linkage for Prescriptions and Reports
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    patient = models.ForeignKey('patients.Patient', on_delete=models.CASCADE, related_name='encounters')
    doctor = models.ForeignKey('users.StaffProfile', on_delete=models.CASCADE, related_name='doctor_encounters')
    branch = models.ForeignKey('tenants.Branch', on_delete=models.CASCADE, related_name='encounters')
    appointment = models.OneToOneField('appointments.Appointment', on_delete=models.SET_NULL, null=True, blank=True, related_name='encounter_link')

    # Core clinical data
    encounter_date = models.DateTimeField(default=timezone.now)
    encounter_type = models.CharField(max_length=50, default='CONSULTATION', 
                                    choices=[('CONSULTATION', 'Consultation'), 
                                            ('FOLLOWUP', 'Follow-up'), 
                                            ('EMERGENCY', 'Emergency'),
                                            ('TELEMEDICINE', 'Telemedicine')])
    visit_reason = models.CharField(max_length=100, blank=True, 
                                   choices=[('ROUTINE', 'Routine Check-up'), 
                                           ('EMERGENCY', 'Emergency'), 
                                           ('FOLLOWUP', 'Follow-up'),
                                           ('SPECIALIST', 'Specialist Consultation')])
    chief_complaint = models.TextField(blank=True, null=True, help_text="Primary reason for visit")
    diagnosis = models.TextField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)

    # Clinical Decision Support
    risk_score = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, 
                                   help_text="Clinical risk assessment score")
    clinical_notes = models.TextField(blank=True, null=True, 
                                    help_text="Structured clinical notes")

    # Quality Metrics
    patient_satisfaction_score = models.PositiveIntegerField(null=True, blank=True, 
                                                           help_text="Patient satisfaction rating (1-5)")
    wait_time_minutes = models.PositiveIntegerField(null=True, blank=True, 
                                                   help_text="Patient wait time in minutes")

    # Telemedicine Support
    is_telemedicine = models.BooleanField(default=False)
    video_call_duration = models.PositiveIntegerField(null=True, blank=True, 
                                                     help_text="Video call duration in minutes")
    video_quality_rating = models.PositiveIntegerField(null=True, blank=True, 
                                                      help_text="Video quality rating (1-5)")

    # Vitals at the time of visit
    height_cm = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    weight_kg = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    temperature_c = models.DecimalField(max_digits=4, decimal_places=1, null=True, blank=True)
    blood_pressure = models.CharField(max_length=20, blank=True, null=True)
    pulse_rate = models.PositiveIntegerField(null=True, blank=True)
    oxygen_saturation = models.PositiveIntegerField(null=True, blank=True)

    # Follow-up details
    follow_up_required = models.BooleanField(default=False)
    follow_up_in_days = models.PositiveIntegerField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-encounter_date']

    def __str__(self):
        return f"{self.patient.full_name} - {self.encounter_date.strftime('%Y-%m-%d')}"

    @property
    def prescriptions(self):
        return self.encounter_prescriptions.all()

    @property
    def reports(self):
        return self.encounter_reports.all()


class Prescription(models.Model):
    """
    Prescription summary for an Encounter.
    """
    encounter = models.ForeignKey(Encounter, on_delete=models.CASCADE, related_name='encounter_prescriptions')
    prescribed_at = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(blank=True, null=True, help_text="Doctor notes or special instructions")

    def __str__(self):
        return f"Prescription for {self.encounter.patient.full_name} ({self.prescribed_at.date()})"


class PrescriptionItem(models.Model):
    """
    Individual prescribed medicines in a Prescription.
    """
    prescription = models.ForeignKey(Prescription, on_delete=models.CASCADE, related_name='items')
    medicine_name = models.CharField(max_length=255)
    dosage = models.CharField(max_length=100, help_text="e.g., 500mg")
    frequency = models.CharField(max_length=100, help_text="e.g., Twice a day")
    duration_days = models.PositiveIntegerField(default=1)
    instructions = models.TextField(blank=True, null=True)
    is_conflicting = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.medicine_name} - {self.dosage}"


class EncounterReport(models.Model):
    """
    Reports (blood test results, scans, MRI, etc.) attached to a specific Encounter.
    """
    encounter = models.ForeignKey(Encounter, on_delete=models.CASCADE, related_name='encounter_reports')
    title = models.CharField(max_length=255)
    file = models.FileField(upload_to='encounter_reports/%Y/%m/%d/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} ({self.encounter.patient.full_name})"


class ClinicalNote(models.Model):
    """
    Structured clinical notes with templates for SOAP format.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    encounter = models.ForeignKey(Encounter, on_delete=models.CASCADE, related_name='clinical_notes_set')
    note_type = models.CharField(max_length=50, 
                               choices=[('SOAP', 'SOAP Note'), 
                                       ('PROGRESS', 'Progress Note'), 
                                       ('DISCHARGE', 'Discharge Summary'),
                                       ('CONSULTATION', 'Consultation Note')])
    template_used = models.CharField(max_length=100, blank=True, 
                                   help_text="Template used for this note")
    
    # SOAP Format Fields
    subjective = models.TextField(blank=True, 
                                help_text="Patient's description of symptoms")
    objective = models.TextField(blank=True, 
                               help_text="Clinical findings and observations")
    assessment = models.TextField(blank=True, 
                                help_text="Clinical assessment and diagnosis")
    plan = models.TextField(blank=True, 
                          help_text="Treatment plan and recommendations")
    
    # Additional Notes
    additional_notes = models.TextField(blank=True, null=True)
    
    # Audit
    created_by = models.ForeignKey('users.User', on_delete=models.CASCADE, 
                                  related_name='clinical_notes')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.note_type} - {self.encounter.patient.full_name} ({self.created_at.date()})"