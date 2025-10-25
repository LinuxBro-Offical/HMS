from django.db import models
from django.utils import timezone
import uuid


class ClinicalGuideline(models.Model):
    """
    Evidence-based clinical guidelines for decision support.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    specialty = models.CharField(max_length=100, 
                               choices=[('CARDIOLOGY', 'Cardiology'), 
                                       ('NEUROLOGY', 'Neurology'),
                                       ('PEDIATRICS', 'Pediatrics'),
                                       ('ONCOLOGY', 'Oncology'),
                                       ('EMERGENCY', 'Emergency Medicine'),
                                       ('GENERAL', 'General Medicine')])
    condition = models.CharField(max_length=255, 
                                help_text="Medical condition or disease")
    guideline_text = models.TextField()
    evidence_level = models.CharField(max_length=20, 
                                     choices=[('A', 'Level A - Strong Evidence'), 
                                             ('B', 'Level B - Moderate Evidence'),
                                             ('C', 'Level C - Weak Evidence'),
                                             ('D', 'Level D - Expert Opinion')])
    last_updated = models.DateField()
    is_active = models.BooleanField(default=True)
    
    # Additional metadata
    source = models.CharField(max_length=255, blank=True, 
                            help_text="Source of the guideline")
    version = models.CharField(max_length=20, blank=True)
    tags = models.CharField(max_length=500, blank=True, 
                           help_text="Comma-separated tags for search")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-last_updated', 'title']
        indexes = [
            models.Index(fields=['specialty']),
            models.Index(fields=['condition']),
            models.Index(fields=['evidence_level']),
        ]
    
    def __str__(self):
        return f"{self.title} - {self.specialty}"


class DrugInteraction(models.Model):
    """
    Drug-drug interaction database for clinical decision support.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    drug1 = models.CharField(max_length=255, help_text="First drug name")
    drug2 = models.CharField(max_length=255, help_text="Second drug name")
    interaction_type = models.CharField(max_length=50, 
                                      choices=[('MAJOR', 'Major Interaction'), 
                                              ('MODERATE', 'Moderate Interaction'),
                                              ('MINOR', 'Minor Interaction'),
                                              ('CONTRAINDICATED', 'Contraindicated')])
    description = models.TextField(help_text="Description of the interaction")
    severity = models.CharField(max_length=20, 
                               choices=[('HIGH', 'High Risk'), 
                                       ('MEDIUM', 'Medium Risk'),
                                       ('LOW', 'Low Risk')])
    recommendation = models.TextField(help_text="Clinical recommendation")
    
    # Additional information
    mechanism = models.TextField(blank=True, 
                               help_text="Mechanism of interaction")
    onset = models.CharField(max_length=100, blank=True, 
                           help_text="Onset of interaction")
    management = models.TextField(blank=True, 
                                help_text="Management strategies")
    
    # Metadata
    evidence_level = models.CharField(max_length=20, 
                                     choices=[('A', 'Level A'), 
                                             ('B', 'Level B'),
                                             ('C', 'Level C'),
                                             ('D', 'Level D')])
    last_reviewed = models.DateField()
    is_active = models.BooleanField(default=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['severity', 'interaction_type']
        indexes = [
            models.Index(fields=['drug1']),
            models.Index(fields=['drug2']),
            models.Index(fields=['severity']),
            models.Index(fields=['interaction_type']),
        ]
    
    def __str__(self):
        return f"{self.drug1} + {self.drug2} ({self.severity})"


class ClinicalAlert(models.Model):
    """
    System-generated clinical alerts for patient safety.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    patient = models.ForeignKey('patients.Patient', on_delete=models.CASCADE, 
                               related_name='clinical_alerts')
    encounter = models.ForeignKey('encounters.Encounter', on_delete=models.CASCADE, 
                                 null=True, blank=True, related_name='alerts')
    
    alert_type = models.CharField(max_length=50, 
                                 choices=[('DRUG_INTERACTION', 'Drug Interaction'), 
                                         ('ALLERGY', 'Allergy Alert'),
                                         ('CONTRAINDICATION', 'Contraindication'),
                                         ('DOSAGE', 'Dosage Alert'),
                                         ('LAB_RESULT', 'Lab Result Alert'),
                                         ('VITAL_SIGN', 'Vital Sign Alert'),
                                         ('CLINICAL_RULE', 'Clinical Rule Violation')])
    severity = models.CharField(max_length=20, 
                               choices=[('CRITICAL', 'Critical'), 
                                       ('HIGH', 'High'),
                                       ('MEDIUM', 'Medium'),
                                       ('LOW', 'Low')])
    title = models.CharField(max_length=255)
    message = models.TextField()
    
    # Alert details
    triggered_by = models.CharField(max_length=255, blank=True, 
                                  help_text="What triggered this alert")
    related_drugs = models.CharField(max_length=500, blank=True, 
                                    help_text="Comma-separated drug names")
    related_conditions = models.CharField(max_length=500, blank=True, 
                                        help_text="Comma-separated conditions")
    
    # Status and acknowledgment
    is_read = models.BooleanField(default=False)
    is_acknowledged = models.BooleanField(default=False)
    acknowledged_by = models.ForeignKey('users.User', on_delete=models.SET_NULL, 
                                       null=True, blank=True, related_name='acknowledged_alerts')
    acknowledged_at = models.DateTimeField(null=True, blank=True)
    
    # Resolution
    is_resolved = models.BooleanField(default=False)
    resolution_notes = models.TextField(blank=True)
    resolved_by = models.ForeignKey('users.User', on_delete=models.SET_NULL, 
                                   null=True, blank=True, related_name='resolved_alerts')
    resolved_at = models.DateTimeField(null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['patient']),
            models.Index(fields=['alert_type']),
            models.Index(fields=['severity']),
            models.Index(fields=['is_read']),
        ]
    
    def __str__(self):
        return f"{self.alert_type} - {self.patient.full_name} ({self.severity})"
    
    def acknowledge(self, user):
        """Mark alert as acknowledged by a user."""
        self.is_acknowledged = True
        self.acknowledged_by = user
        self.acknowledged_at = timezone.now()
        self.save()
    
    def resolve(self, user, notes=""):
        """Mark alert as resolved by a user."""
        self.is_resolved = True
        self.resolved_by = user
        self.resolved_at = timezone.now()
        self.resolution_notes = notes
        self.save()