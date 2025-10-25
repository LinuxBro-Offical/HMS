from django.db import models
from django.utils import timezone
import uuid


class Patient(models.Model):
    """Core patient record with enhanced administrative and communication fields."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    patient_code = models.CharField(max_length=30, unique=True)
    full_name = models.CharField(max_length=255)
    date_of_birth = models.DateField(null=True, blank=True)

    GENDER_CHOICES = (('M', 'Male'), ('F', 'Female'), ('O', 'Other'))
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, null=True, blank=True)

    phone = models.CharField(max_length=20)
    email = models.EmailField(blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    city = models.CharField(max_length=100, blank=True)
    state = models.CharField(max_length=100, blank=True)
    pin_code = models.CharField(max_length=10, blank=True)

    # Administrative fields
    date_registered = models.DateField(default=timezone.now)
    last_visit_date = models.DateField(null=True, blank=True)
    total_visits = models.PositiveIntegerField(default=0)
    referral_source = models.CharField(max_length=100, blank=True, null=True)
    is_vip = models.BooleanField(default=False)
    remarks = models.TextField(blank=True, null=True)

    # Communication preferences
    CONTACT_CHOICES = (('SMS','SMS'),('WHATSAPP','WhatsApp'),('EMAIL','Email'))
    preferred_contact_method = models.CharField(max_length=20, choices=CONTACT_CHOICES, default='SMS')
    consent_to_notify = models.BooleanField(default=True)

    # Branch linkage
    branches = models.ManyToManyField('tenants.Branch', related_name='patients', blank=True)

    # Emergency Contact Information
    emergency_contact_name = models.CharField(max_length=255, blank=True)
    emergency_contact_phone = models.CharField(max_length=20, blank=True)
    emergency_contact_relation = models.CharField(max_length=100, blank=True)

    # Insurance & Payment Information
    insurance_provider = models.CharField(max_length=255, blank=True)
    insurance_policy_number = models.CharField(max_length=100, blank=True)
    insurance_valid_until = models.DateField(null=True, blank=True)

    # Patient Portal Access
    portal_username = models.CharField(max_length=100, blank=True, null=True, unique=True)
    portal_password_hash = models.CharField(max_length=255, blank=True)
    portal_enabled = models.BooleanField(default=False)

    # Privacy & Consent Management
    data_sharing_consent = models.BooleanField(default=False)
    marketing_consent = models.BooleanField(default=False)
    research_consent = models.BooleanField(default=False)

    # Modern Identifiers
    aadhaar_number = models.CharField(max_length=12, blank=True, null=True, unique=True)
    passport_number = models.CharField(max_length=50, blank=True)

    # Social Determinants of Health
    occupation = models.CharField(max_length=100, blank=True)
    education_level = models.CharField(max_length=50, blank=True)
    marital_status = models.CharField(max_length=20, blank=True)

    # Risk Factors & Lifestyle
    smoking_status = models.CharField(max_length=20, blank=True)
    alcohol_consumption = models.CharField(max_length=20, blank=True)
    exercise_frequency = models.CharField(max_length=20, blank=True)

    # Audit
    registered_by = models.ForeignKey('users.User', on_delete=models.SET_NULL, null=True, blank=True, related_name='registered_patients')
    last_updated_by = models.ForeignKey('users.User', on_delete=models.SET_NULL, null=True, blank=True, related_name='patient_updates')

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-date_registered']
        indexes = [
            models.Index(fields=['patient_code']),
            models.Index(fields=['phone']),
        ]

    def __str__(self):
        return f"{self.full_name} ({self.patient_code})"

    def age(self):
        if self.date_of_birth:
            return int((timezone.now().date() - self.date_of_birth).days / 365.25)
        return None


class PatientCondition(models.Model):
    """Structured chronic/important conditions for a patient."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='conditions')
    name = models.CharField(max_length=255)
    diagnosed_date = models.DateField(null=True, blank=True)
    notes = models.TextField(blank=True, null=True)
    active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.patient.patient_code})"


class PatientAllergy(models.Model):
    """Structured allergy records for conflict checking."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='allergies_list')
    allergen = models.CharField(max_length=255)
    reaction = models.CharField(max_length=255, blank=True, null=True)
    severity = models.CharField(max_length=50, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.allergen} ({self.patient.patient_code})"


class PatientReport(models.Model):
    """Patient-level reports (general uploads). Encounter-specific reports stored on Encounter model."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='reports')
    title = models.CharField(max_length=255)
    file = models.FileField(upload_to='patient_reports/%Y/%m/%d/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    uploaded_by = models.ForeignKey('users.User', on_delete=models.SET_NULL, null=True, blank=True, related_name='uploaded_patient_reports')

    def __str__(self):
        return f"{self.title} ({self.patient.patient_code})"