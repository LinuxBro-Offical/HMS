from django.db import models
from django.utils import timezone
import uuid


class AuditLog(models.Model):
    """
    Comprehensive audit log for all system activities.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey('users.User', on_delete=models.SET_NULL, 
                            null=True, blank=True, related_name='audit_logs')
    
    # Action details
    action = models.CharField(max_length=50, 
                             choices=[('CREATE', 'Create'), 
                                     ('READ', 'Read'),
                                     ('UPDATE', 'Update'),
                                     ('DELETE', 'Delete'),
                                     ('LOGIN', 'Login'),
                                     ('LOGOUT', 'Logout'),
                                     ('EXPORT', 'Export'),
                                     ('IMPORT', 'Import'),
                                     ('PRINT', 'Print'),
                                     ('DOWNLOAD', 'Download'),
                                     ('UPLOAD', 'Upload'),
                                     ('APPROVE', 'Approve'),
                                     ('REJECT', 'Reject'),
                                     ('CANCEL', 'Cancel'),
                                     ('RESET', 'Reset')])
    
    model_name = models.CharField(max_length=100, 
                                 help_text="Django model name (e.g., 'Patient', 'Appointment')")
    object_id = models.CharField(max_length=100, 
                               help_text="ID of the affected object")
    
    # Data changes
    old_values = models.JSONField(default=dict, blank=True, 
                                help_text="Previous values before change")
    new_values = models.JSONField(default=dict, blank=True, 
                                help_text="New values after change")
    
    # Technical details
    ip_address = models.GenericIPAddressField()
    user_agent = models.TextField(blank=True)
    session_id = models.CharField(max_length=100, blank=True)
    
    # Additional context
    reason = models.TextField(blank=True, 
                            help_text="Reason for the action")
    additional_data = models.JSONField(default=dict, blank=True, 
                                      help_text="Additional context data")
    
    # Risk assessment
    risk_level = models.CharField(max_length=20, 
                                 choices=[('LOW', 'Low Risk'), 
                                         ('MEDIUM', 'Medium Risk'),
                                         ('HIGH', 'High Risk'),
                                         ('CRITICAL', 'Critical Risk')])
    
    timestamp = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['user']),
            models.Index(fields=['action']),
            models.Index(fields=['model_name']),
            models.Index(fields=['timestamp']),
            models.Index(fields=['risk_level']),
            models.Index(fields=['ip_address']),
        ]
    
    def __str__(self):
        return f"{self.action} {self.model_name} by {self.user} at {self.timestamp}"


class DataPrivacyConsent(models.Model):
    """
    Patient data privacy consent management.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    patient = models.ForeignKey('patients.Patient', on_delete=models.CASCADE, 
                               related_name='privacy_consents')
    
    # Consent details
    consent_type = models.CharField(max_length=50, 
                                   choices=[('DATA_COLLECTION', 'Data Collection'), 
                                           ('DATA_SHARING', 'Data Sharing'),
                                           ('RESEARCH', 'Research Use'),
                                           ('MARKETING', 'Marketing Communications'),
                                           ('TELEMEDICINE', 'Telemedicine Services'),
                                           ('RECORDING', 'Audio/Video Recording'),
                                           ('THIRD_PARTY', 'Third Party Sharing'),
                                           ('EMERGENCY_CONTACT', 'Emergency Contact Sharing')])
    
    consent_text = models.TextField(help_text="Full consent text shown to patient")
    granted = models.BooleanField(default=False)
    
    # Consent lifecycle
    granted_at = models.DateTimeField(null=True, blank=True)
    expires_at = models.DateTimeField(null=True, blank=True)
    withdrawn_at = models.DateTimeField(null=True, blank=True)
    
    # Withdrawal details
    withdrawal_reason = models.TextField(blank=True)
    withdrawn_by = models.ForeignKey('users.User', on_delete=models.SET_NULL, 
                                     null=True, blank=True, related_name='withdrawn_consents')
    
    # Legal compliance
    legal_basis = models.CharField(max_length=100, 
                                  choices=[('CONSENT', 'Consent'), 
                                          ('LEGAL_OBLIGATION', 'Legal Obligation'),
                                          ('VITAL_INTERESTS', 'Vital Interests'),
                                          ('PUBLIC_TASK', 'Public Task'),
                                          ('LEGITIMATE_INTERESTS', 'Legitimate Interests')])
    
    # Version control
    version = models.CharField(max_length=20, default='1.0')
    previous_version = models.ForeignKey('self', on_delete=models.SET_NULL, 
                                        null=True, blank=True, related_name='newer_versions')
    
    # Additional metadata
    consent_method = models.CharField(max_length=50, 
                                     choices=[('DIGITAL_SIGNATURE', 'Digital Signature'), 
                                             ('CHECKBOX', 'Checkbox'),
                                             ('VERBAL', 'Verbal Consent'),
                                             ('WRITTEN', 'Written Consent'),
                                             ('IMPLIED', 'Implied Consent')])
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-granted_at']
        indexes = [
            models.Index(fields=['patient']),
            models.Index(fields=['consent_type']),
            models.Index(fields=['granted']),
            models.Index(fields=['granted_at']),
            models.Index(fields=['expires_at']),
        ]
    
    def __str__(self):
        return f"{self.patient.full_name} - {self.consent_type} ({'Granted' if self.granted else 'Not Granted'})"


class ComplianceReport(models.Model):
    """
    Compliance reports and regulatory documentation.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    branch = models.ForeignKey('tenants.Branch', on_delete=models.CASCADE, 
                              related_name='compliance_reports')
    
    # Report details
    report_type = models.CharField(max_length=50, 
                                  choices=[('AUDIT_REPORT', 'Audit Report'), 
                                          ('PRIVACY_REPORT', 'Privacy Compliance Report'),
                                          ('SECURITY_REPORT', 'Security Report'),
                                          ('DATA_BREACH', 'Data Breach Report'),
                                          ('REGULATORY', 'Regulatory Compliance'),
                                          ('INTERNAL_AUDIT', 'Internal Audit'),
                                          ('EXTERNAL_AUDIT', 'External Audit')])
    
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    
    # Report period
    report_period_start = models.DateField()
    report_period_end = models.DateField()
    
    # Status
    status = models.CharField(max_length=20, 
                              choices=[('DRAFT', 'Draft'), 
                                      ('PENDING_REVIEW', 'Pending Review'),
                                      ('APPROVED', 'Approved'),
                                      ('REJECTED', 'Rejected'),
                                      ('SUBMITTED', 'Submitted')])
    
    # Report data
    report_data = models.JSONField(default=dict, blank=True, 
                                  help_text="Structured report data")
    findings = models.TextField(blank=True)
    recommendations = models.TextField(blank=True)
    
    # File attachments
    report_file = models.FileField(upload_to='compliance_reports/%Y/%m/%d/', 
                                  blank=True, null=True)
    
    # Approval workflow
    created_by = models.ForeignKey('users.User', on_delete=models.CASCADE, 
                                  related_name='created_compliance_reports')
    reviewed_by = models.ForeignKey('users.User', on_delete=models.SET_NULL, 
                                    null=True, blank=True, related_name='reviewed_compliance_reports')
    reviewed_at = models.DateTimeField(null=True, blank=True)
    approved_by = models.ForeignKey('users.User', on_delete=models.SET_NULL, 
                                    null=True, blank=True, related_name='approved_compliance_reports')
    approved_at = models.DateTimeField(null=True, blank=True)
    
    # Submission details
    submitted_at = models.DateTimeField(null=True, blank=True)
    submission_reference = models.CharField(max_length=100, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['branch']),
            models.Index(fields=['report_type']),
            models.Index(fields=['status']),
            models.Index(fields=['report_period_start']),
        ]
    
    def __str__(self):
        return f"{self.title} - {self.branch.name} ({self.report_period_start})"


class DataBreachIncident(models.Model):
    """
    Data breach incident tracking and reporting.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    branch = models.ForeignKey('tenants.Branch', on_delete=models.CASCADE, 
                              related_name='data_breach_incidents')
    
    # Incident details
    incident_title = models.CharField(max_length=255)
    incident_description = models.TextField()
    incident_type = models.CharField(max_length=50, 
                                    choices=[('UNAUTHORIZED_ACCESS', 'Unauthorized Access'), 
                                            ('DATA_THEFT', 'Data Theft'),
                                            ('SYSTEM_BREACH', 'System Breach'),
                                            ('PHISHING', 'Phishing Attack'),
                                            ('MALWARE', 'Malware Infection'),
                                            ('INSIDER_THREAT', 'Insider Threat'),
                                            ('PHYSICAL_THEFT', 'Physical Theft'),
                                            ('LOST_DEVICE', 'Lost/Stolen Device'),
                                            ('OTHER', 'Other')])
    
    # Timeline
    discovered_at = models.DateTimeField()
    occurred_at = models.DateTimeField(null=True, blank=True)
    contained_at = models.DateTimeField(null=True, blank=True)
    resolved_at = models.DateTimeField(null=True, blank=True)
    
    # Impact assessment
    severity = models.CharField(max_length=20, 
                               choices=[('LOW', 'Low'), 
                                       ('MEDIUM', 'Medium'),
                                       ('HIGH', 'High'),
                                       ('CRITICAL', 'Critical')])
    
    affected_records_count = models.PositiveIntegerField(null=True, blank=True)
    affected_patients_count = models.PositiveIntegerField(null=True, blank=True)
    affected_data_types = models.JSONField(default=list, blank=True, 
                                          help_text="Types of data affected")
    
    # Response actions
    immediate_actions = models.TextField(blank=True)
    containment_measures = models.TextField(blank=True)
    recovery_actions = models.TextField(blank=True)
    
    # Notification
    patients_notified = models.BooleanField(default=False)
    patients_notified_at = models.DateTimeField(null=True, blank=True)
    authorities_notified = models.BooleanField(default=False)
    authorities_notified_at = models.DateTimeField(null=True, blank=True)
    
    # Status
    status = models.CharField(max_length=20, 
                              choices=[('INVESTIGATING', 'Investigating'), 
                                      ('CONTAINED', 'Contained'),
                                      ('RESOLVED', 'Resolved'),
                                      ('CLOSED', 'Closed')])
    
    # Reporting
    report_generated = models.BooleanField(default=False)
    report_file = models.FileField(upload_to='breach_reports/%Y/%m/%d/', 
                                  blank=True, null=True)
    
    # Audit
    reported_by = models.ForeignKey('users.User', on_delete=models.CASCADE, 
                                    related_name='reported_breach_incidents')
    assigned_to = models.ForeignKey('users.User', on_delete=models.SET_NULL, 
                                    null=True, blank=True, related_name='assigned_breach_incidents')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-discovered_at']
        indexes = [
            models.Index(fields=['branch']),
            models.Index(fields=['incident_type']),
            models.Index(fields=['severity']),
            models.Index(fields=['status']),
            models.Index(fields=['discovered_at']),
        ]
    
    def __str__(self):
        return f"{self.incident_title} - {self.branch.name} ({self.discovered_at.date()})"