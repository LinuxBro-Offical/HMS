from django.db import models
from django.utils import timezone
import uuid


class TelemedicineSession(models.Model):
    """
    Telemedicine consultation sessions with comprehensive tracking.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    patient = models.ForeignKey('patients.Patient', on_delete=models.CASCADE, 
                               related_name='telemedicine_sessions')
    doctor = models.ForeignKey('users.StaffProfile', on_delete=models.CASCADE, 
                              related_name='telemedicine_sessions')
    appointment = models.ForeignKey('appointments.Appointment', on_delete=models.SET_NULL, 
                                   null=True, blank=True, related_name='telemedicine_sessions')
    
    # Session details
    session_id = models.CharField(max_length=100, unique=True)
    session_type = models.CharField(max_length=50, 
                                   choices=[('VIDEO_CALL', 'Video Call'), 
                                           ('AUDIO_CALL', 'Audio Call'),
                                           ('CHAT', 'Text Chat'),
                                           ('HYBRID', 'Hybrid (Video + Chat)')])
    
    # Timing
    scheduled_start_time = models.DateTimeField()
    actual_start_time = models.DateTimeField(null=True, blank=True)
    end_time = models.DateTimeField(null=True, blank=True)
    duration_minutes = models.PositiveIntegerField(null=True, blank=True)
    
    # Platform and technical details
    platform = models.CharField(max_length=50, 
                               choices=[('ZOOM', 'Zoom'), 
                                       ('TEAMS', 'Microsoft Teams'),
                                       ('GOOGLE_MEET', 'Google Meet'),
                                       ('CUSTOM', 'Custom Platform'),
                                       ('WHATSAPP', 'WhatsApp'),
                                       ('PHONE', 'Phone Call')])
    connection_quality = models.CharField(max_length=20, 
                                         choices=[('EXCELLENT', 'Excellent'), 
                                                 ('GOOD', 'Good'),
                                                 ('FAIR', 'Fair'),
                                                 ('POOR', 'Poor')])
    
    # Clinical information
    chief_complaint = models.TextField(blank=True)
    diagnosis = models.TextField(blank=True)
    prescription_given = models.BooleanField(default=False)
    follow_up_required = models.BooleanField(default=False)
    follow_up_in_days = models.PositiveIntegerField(null=True, blank=True)
    
    # Session content
    recording_url = models.URLField(blank=True, 
                                   help_text="URL to session recording if available")
    session_notes = models.TextField(blank=True)
    technical_issues = models.TextField(blank=True, 
                                      help_text="Any technical problems encountered")
    
    # Quality metrics
    patient_satisfaction_rating = models.PositiveIntegerField(null=True, blank=True, 
                                                           help_text="Rating 1-5")
    doctor_satisfaction_rating = models.PositiveIntegerField(null=True, blank=True, 
                                                           help_text="Rating 1-5")
    video_quality_rating = models.PositiveIntegerField(null=True, blank=True, 
                                                      help_text="Rating 1-5")
    audio_quality_rating = models.PositiveIntegerField(null=True, blank=True, 
                                                     help_text="Rating 1-5")
    
    # Status
    status = models.CharField(max_length=20, 
                             choices=[('SCHEDULED', 'Scheduled'), 
                                     ('IN_PROGRESS', 'In Progress'),
                                     ('COMPLETED', 'Completed'),
                                     ('CANCELLED', 'Cancelled'),
                                     ('NO_SHOW', 'No Show'),
                                     ('RESCHEDULED', 'Rescheduled')])
    
    # Cancellation details
    cancellation_reason = models.TextField(blank=True)
    cancelled_by = models.ForeignKey('users.User', on_delete=models.SET_NULL, 
                                    null=True, blank=True, related_name='cancelled_telemedicine_sessions')
    cancelled_at = models.DateTimeField(null=True, blank=True)
    
    # Audit
    created_by = models.ForeignKey('users.User', on_delete=models.CASCADE, 
                                  related_name='created_telemedicine_sessions')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-scheduled_start_time']
        indexes = [
            models.Index(fields=['patient']),
            models.Index(fields=['doctor']),
            models.Index(fields=['status']),
            models.Index(fields=['scheduled_start_time']),
            models.Index(fields=['session_type']),
        ]
    
    def __str__(self):
        return f"Telemedicine Session {self.session_id} - {self.patient.full_name}"
    
    def save(self, *args, **kwargs):
        # Calculate duration if both start and end times are available
        if self.actual_start_time and self.end_time:
            duration = self.end_time - self.actual_start_time
            self.duration_minutes = int(duration.total_seconds() / 60)
        
        super().save(*args, **kwargs)


class TelemedicinePrescription(models.Model):
    """
    Prescriptions issued during telemedicine sessions.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    session = models.ForeignKey(TelemedicineSession, on_delete=models.CASCADE, 
                              related_name='prescriptions')
    
    # Prescription details
    medicine_name = models.CharField(max_length=255)
    dosage = models.CharField(max_length=100)
    frequency = models.CharField(max_length=100)
    duration_days = models.PositiveIntegerField()
    instructions = models.TextField(blank=True)
    
    # Digital signature
    doctor_signature = models.TextField(blank=True, 
                                      help_text="Digital signature or approval")
    prescription_date = models.DateTimeField(auto_now_add=True)
    
    # Status
    is_issued = models.BooleanField(default=False)
    issued_at = models.DateTimeField(null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-prescription_date']
        indexes = [
            models.Index(fields=['session']),
            models.Index(fields=['is_issued']),
        ]
    
    def __str__(self):
        return f"Prescription for {self.session.patient.full_name} - {self.medicine_name}"


class TelemedicineFollowUp(models.Model):
    """
    Follow-up appointments scheduled after telemedicine sessions.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    session = models.ForeignKey(TelemedicineSession, on_delete=models.CASCADE, 
                              related_name='follow_ups')
    
    # Follow-up details
    follow_up_type = models.CharField(max_length=50, 
                                     choices=[('TELEMEDICINE', 'Telemedicine Follow-up'), 
                                             ('IN_PERSON', 'In-person Visit'),
                                             ('PHONE_CALL', 'Phone Call'),
                                             ('CHAT', 'Text Chat')])
    scheduled_date = models.DateTimeField()
    reason = models.TextField(blank=True)
    notes = models.TextField(blank=True)
    
    # Status
    status = models.CharField(max_length=20, 
                             choices=[('SCHEDULED', 'Scheduled'), 
                                     ('COMPLETED', 'Completed'),
                                     ('CANCELLED', 'Cancelled'),
                                     ('RESCHEDULED', 'Rescheduled')])
    
    # Completion details
    completed_at = models.DateTimeField(null=True, blank=True)
    completion_notes = models.TextField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-scheduled_date']
        indexes = [
            models.Index(fields=['session']),
            models.Index(fields=['status']),
            models.Index(fields=['scheduled_date']),
        ]
    
    def __str__(self):
        return f"Follow-up for {self.session.patient.full_name} - {self.scheduled_date.date()}"


class TelemedicineDevice(models.Model):
    """
    Patient devices used for telemedicine sessions.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    patient = models.ForeignKey('patients.Patient', on_delete=models.CASCADE, 
                               related_name='telemedicine_devices')
    
    # Device information
    device_type = models.CharField(max_length=50, 
                                  choices=[('SMARTPHONE', 'Smartphone'), 
                                          ('TABLET', 'Tablet'),
                                          ('LAPTOP', 'Laptop'),
                                          ('DESKTOP', 'Desktop Computer'),
                                          ('SMART_TV', 'Smart TV')])
    device_name = models.CharField(max_length=255)
    operating_system = models.CharField(max_length=100)
    browser = models.CharField(max_length=100, blank=True)
    
    # Network information
    internet_speed = models.CharField(max_length=50, blank=True)
    connection_type = models.CharField(max_length=50, 
                                      choices=[('WIFI', 'WiFi'), 
                                              ('MOBILE_DATA', 'Mobile Data'),
                                              ('ETHERNET', 'Ethernet'),
                                              ('UNKNOWN', 'Unknown')])
    
    # Capabilities
    has_camera = models.BooleanField(default=True)
    has_microphone = models.BooleanField(default=True)
    has_speaker = models.BooleanField(default=True)
    
    # Status
    is_active = models.BooleanField(default=True)
    last_used = models.DateTimeField(null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-last_used']
        indexes = [
            models.Index(fields=['patient']),
            models.Index(fields=['device_type']),
            models.Index(fields=['is_active']),
        ]
    
    def __str__(self):
        return f"{self.device_name} - {self.patient.full_name}"