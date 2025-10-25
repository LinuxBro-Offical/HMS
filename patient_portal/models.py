from django.db import models
from django.utils import timezone
import uuid


class PatientPortalActivity(models.Model):
    """
    Patient portal activity tracking and audit log.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    patient = models.ForeignKey('patients.Patient', on_delete=models.CASCADE, 
                               related_name='portal_activities')
    
    # Activity details
    activity_type = models.CharField(max_length=50, 
                                    choices=[('LOGIN', 'Login'), 
                                            ('LOGOUT', 'Logout'),
                                            ('VIEW_PROFILE', 'View Profile'),
                                            ('UPDATE_PROFILE', 'Update Profile'),
                                            ('VIEW_APPOINTMENTS', 'View Appointments'),
                                            ('BOOK_APPOINTMENT', 'Book Appointment'),
                                            ('CANCEL_APPOINTMENT', 'Cancel Appointment'),
                                            ('VIEW_MEDICAL_RECORDS', 'View Medical Records'),
                                            ('DOWNLOAD_REPORT', 'Download Report'),
                                            ('VIEW_PRESCRIPTIONS', 'View Prescriptions'),
                                            ('PAY_BILL', 'Pay Bill'),
                                            ('VIEW_BILLS', 'View Bills'),
                                            ('UPDATE_INSURANCE', 'Update Insurance'),
                                            ('CONTACT_DOCTOR', 'Contact Doctor'),
                                            ('VIEW_LAB_RESULTS', 'View Lab Results'),
                                            ('UPDATE_EMERGENCY_CONTACT', 'Update Emergency Contact'),
                                            ('GIVE_FEEDBACK', 'Give Feedback')])
    
    activity_details = models.JSONField(default=dict, blank=True, 
                                       help_text="Additional activity-specific data")
    
    # Technical details
    ip_address = models.GenericIPAddressField()
    user_agent = models.TextField(blank=True)
    device_type = models.CharField(max_length=50, blank=True, 
                                   choices=[('DESKTOP', 'Desktop'), 
                                           ('MOBILE', 'Mobile'),
                                           ('TABLET', 'Tablet')])
    browser = models.CharField(max_length=100, blank=True)
    operating_system = models.CharField(max_length=100, blank=True)
    
    # Location (if available)
    country = models.CharField(max_length=100, blank=True)
    city = models.CharField(max_length=100, blank=True)
    
    # Session information
    session_id = models.CharField(max_length=100, blank=True)
    duration_seconds = models.PositiveIntegerField(null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['patient']),
            models.Index(fields=['activity_type']),
            models.Index(fields=['created_at']),
            models.Index(fields=['ip_address']),
        ]
    
    def __str__(self):
        return f"{self.patient.full_name} - {self.activity_type} ({self.created_at})"


class PatientFeedback(models.Model):
    """
    Patient feedback and satisfaction surveys.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    patient = models.ForeignKey('patients.Patient', on_delete=models.CASCADE, 
                               related_name='feedback')
    encounter = models.ForeignKey('encounters.Encounter', on_delete=models.CASCADE, 
                                 null=True, blank=True, related_name='feedback')
    
    # Feedback details
    rating = models.PositiveIntegerField(choices=[(1, '1 - Poor'), (2, '2 - Fair'), 
                                                (3, '3 - Good'), (4, '4 - Very Good'), 
                                                (5, '5 - Excellent')])
    feedback_text = models.TextField(blank=True)
    category = models.CharField(max_length=50, 
                               choices=[('GENERAL', 'General Feedback'), 
                                       ('APPOINTMENT', 'Appointment Experience'),
                                       ('DOCTOR', 'Doctor Consultation'),
                                       ('STAFF', 'Staff Service'),
                                       ('FACILITY', 'Facility & Environment'),
                                       ('BILLING', 'Billing Process'),
                                       ('PORTAL', 'Patient Portal'),
                                       ('TELEMEDICINE', 'Telemedicine Experience')])
    
    # Specific ratings
    doctor_rating = models.PositiveIntegerField(null=True, blank=True, 
                                              choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')])
    staff_rating = models.PositiveIntegerField(null=True, blank=True, 
                                               choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')])
    facility_rating = models.PositiveIntegerField(null=True, blank=True, 
                                                  choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')])
    wait_time_rating = models.PositiveIntegerField(null=True, blank=True, 
                                                   choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')])
    
    # Privacy settings
    is_anonymous = models.BooleanField(default=False)
    allow_public_use = models.BooleanField(default=False, 
                                          help_text="Allow use in marketing materials")
    
    # Response and follow-up
    is_responded = models.BooleanField(default=False)
    response_text = models.TextField(blank=True)
    responded_by = models.ForeignKey('users.User', on_delete=models.SET_NULL, 
                                     null=True, blank=True, related_name='feedback_responses')
    responded_at = models.DateTimeField(null=True, blank=True)
    
    # Status
    status = models.CharField(max_length=20, 
                              choices=[('PENDING', 'Pending Review'), 
                                      ('REVIEWED', 'Reviewed'),
                                      ('RESPONDED', 'Responded'),
                                      ('CLOSED', 'Closed')])
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['patient']),
            models.Index(fields=['encounter']),
            models.Index(fields=['rating']),
            models.Index(fields=['category']),
            models.Index(fields=['status']),
        ]
    
    def __str__(self):
        return f"Feedback from {self.patient.full_name} - Rating: {self.rating}"


class PatientPortalSettings(models.Model):
    """
    Patient portal preferences and settings.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    patient = models.OneToOneField('patients.Patient', on_delete=models.CASCADE, 
                                  related_name='portal_settings')
    
    # Notification preferences
    email_notifications = models.BooleanField(default=True)
    sms_notifications = models.BooleanField(default=True)
    push_notifications = models.BooleanField(default=True)
    
    # Specific notification types
    appointment_reminders = models.BooleanField(default=True)
    prescription_reminders = models.BooleanField(default=True)
    lab_result_notifications = models.BooleanField(default=True)
    bill_payment_reminders = models.BooleanField(default=True)
    health_tips = models.BooleanField(default=False)
    promotional_messages = models.BooleanField(default=False)
    
    # Privacy settings
    share_data_for_research = models.BooleanField(default=False)
    allow_telemedicine = models.BooleanField(default=True)
    allow_recording = models.BooleanField(default=False)
    
    # Display preferences
    language = models.CharField(max_length=10, default='en', 
                               choices=[('en', 'English'), ('hi', 'Hindi'), 
                                       ('ta', 'Tamil'), ('te', 'Telugu')])
    timezone = models.CharField(max_length=50, default='Asia/Kolkata')
    date_format = models.CharField(max_length=20, default='DD/MM/YYYY')
    
    # Security settings
    two_factor_auth = models.BooleanField(default=False)
    session_timeout_minutes = models.PositiveIntegerField(default=30)
    
    # Accessibility
    high_contrast_mode = models.BooleanField(default=False)
    large_text_mode = models.BooleanField(default=False)
    screen_reader_support = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        indexes = [
            models.Index(fields=['patient']),
        ]
    
    def __str__(self):
        return f"Portal Settings - {self.patient.full_name}"


class PatientHealthGoal(models.Model):
    """
    Patient health goals and tracking.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    patient = models.ForeignKey('patients.Patient', on_delete=models.CASCADE, 
                               related_name='health_goals')
    
    # Goal details
    goal_type = models.CharField(max_length=50, 
                                choices=[('WEIGHT_LOSS', 'Weight Loss'), 
                                        ('WEIGHT_GAIN', 'Weight Gain'),
                                        ('EXERCISE', 'Exercise'),
                                        ('MEDICATION_COMPLIANCE', 'Medication Compliance'),
                                        ('BLOOD_PRESSURE', 'Blood Pressure Control'),
                                        ('BLOOD_SUGAR', 'Blood Sugar Control'),
                                        ('SMOKING_CESSATION', 'Smoking Cessation'),
                                        ('STRESS_MANAGEMENT', 'Stress Management'),
                                        ('SLEEP_IMPROVEMENT', 'Sleep Improvement'),
                                        ('CUSTOM', 'Custom Goal')])
    
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    
    # Goal parameters
    target_value = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    target_unit = models.CharField(max_length=20, blank=True)
    current_value = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    
    # Timeline
    start_date = models.DateField()
    target_date = models.DateField()
    achieved_date = models.DateField(null=True, blank=True)
    
    # Status
    status = models.CharField(max_length=20, 
                              choices=[('ACTIVE', 'Active'), 
                                      ('ACHIEVED', 'Achieved'),
                                      ('PAUSED', 'Paused'),
                                      ('CANCELLED', 'Cancelled')])
    
    # Progress tracking
    progress_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    milestones = models.JSONField(default=list, blank=True, 
                                help_text="Goal milestones and checkpoints")
    
    # Support
    doctor_support = models.BooleanField(default=False)
    family_support = models.BooleanField(default=False)
    reminder_frequency = models.CharField(max_length=20, 
                                         choices=[('DAILY', 'Daily'), 
                                                 ('WEEKLY', 'Weekly'),
                                                 ('MONTHLY', 'Monthly')])
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['patient']),
            models.Index(fields=['goal_type']),
            models.Index(fields=['status']),
            models.Index(fields=['target_date']),
        ]
    
    def __str__(self):
        return f"{self.patient.full_name} - {self.title}"