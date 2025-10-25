from django.db import models
from django.utils import timezone
import uuid


class ExternalSystem(models.Model):
    """
    External system integrations configuration.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    system_type = models.CharField(max_length=50, 
                                  choices=[('EMR', 'Electronic Medical Record'), 
                                          ('LIMS', 'Laboratory Information System'),
                                          ('PACS', 'Picture Archiving System'),
                                          ('PHARMACY', 'Pharmacy Management'),
                                          ('BILLING', 'Billing System'),
                                          ('INSURANCE', 'Insurance Provider'),
                                          ('GOVERNMENT', 'Government Portal'),
                                          ('PAYMENT_GATEWAY', 'Payment Gateway'),
                                          ('SMS_PROVIDER', 'SMS Provider'),
                                          ('EMAIL_PROVIDER', 'Email Provider'),
                                          ('ANALYTICS', 'Analytics Platform'),
                                          ('BACKUP', 'Backup System'),
                                          ('OTHER', 'Other')])
    
    # Connection details
    api_endpoint = models.URLField(blank=True)
    api_key = models.CharField(max_length=500, blank=True)
    api_secret = models.CharField(max_length=500, blank=True)
    username = models.CharField(max_length=100, blank=True)
    password = models.CharField(max_length=500, blank=True)
    
    # Configuration
    is_active = models.BooleanField(default=True)
    auto_sync = models.BooleanField(default=False)
    sync_frequency_minutes = models.PositiveIntegerField(default=60)
    
    # Authentication method
    auth_method = models.CharField(max_length=50, 
                                  choices=[('API_KEY', 'API Key'), 
                                          ('OAUTH2', 'OAuth 2.0'),
                                          ('BASIC_AUTH', 'Basic Authentication'),
                                          ('JWT', 'JWT Token'),
                                          ('CUSTOM', 'Custom')])
    
    # Additional settings
    settings = models.JSONField(default=dict, blank=True, 
                              help_text="System-specific configuration")
    webhook_url = models.URLField(blank=True)
    
    # Status tracking
    last_sync = models.DateTimeField(null=True, blank=True)
    last_successful_sync = models.DateTimeField(null=True, blank=True)
    connection_status = models.CharField(max_length=20, 
                                        choices=[('CONNECTED', 'Connected'), 
                                                ('DISCONNECTED', 'Disconnected'),
                                                ('ERROR', 'Error'),
                                                ('TESTING', 'Testing')])
    
    # Error tracking
    last_error = models.TextField(blank=True)
    error_count = models.PositiveIntegerField(default=0)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['name']
        indexes = [
            models.Index(fields=['system_type']),
            models.Index(fields=['is_active']),
            models.Index(fields=['connection_status']),
        ]
    
    def __str__(self):
        return f"{self.name} ({self.system_type})"


class DataSyncLog(models.Model):
    """
    Data synchronization logs for external systems.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    external_system = models.ForeignKey(ExternalSystem, on_delete=models.CASCADE, 
                                       related_name='sync_logs')
    
    # Sync details
    sync_type = models.CharField(max_length=50, 
                                choices=[('FULL_SYNC', 'Full Synchronization'), 
                                        ('INCREMENTAL', 'Incremental Sync'),
                                        ('REAL_TIME', 'Real-time Sync'),
                                        ('MANUAL', 'Manual Sync'),
                                        ('SCHEDULED', 'Scheduled Sync'),
                                        ('WEBHOOK', 'Webhook Sync')])
    
    # Status and timing
    status = models.CharField(max_length=20, 
                             choices=[('STARTED', 'Started'), 
                                     ('IN_PROGRESS', 'In Progress'),
                                     ('COMPLETED', 'Completed'),
                                     ('FAILED', 'Failed'),
                                     ('CANCELLED', 'Cancelled')])
    
    started_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    duration_seconds = models.PositiveIntegerField(null=True, blank=True)
    
    # Data processing
    records_processed = models.PositiveIntegerField(default=0)
    records_successful = models.PositiveIntegerField(default=0)
    records_failed = models.PositiveIntegerField(default=0)
    records_skipped = models.PositiveIntegerField(default=0)
    
    # Error handling
    error_message = models.TextField(blank=True)
    error_details = models.JSONField(default=dict, blank=True, 
                                    help_text="Detailed error information")
    
    # Additional information
    sync_direction = models.CharField(max_length=20, 
                                     choices=[('INBOUND', 'Inbound (External to HMS)'), 
                                             ('OUTBOUND', 'Outbound (HMS to External)'),
                                             ('BIDIRECTIONAL', 'Bidirectional')])
    
    data_types = models.JSONField(default=list, blank=True, 
                                 help_text="Types of data synchronized")
    
    # Trigger information
    triggered_by = models.ForeignKey('users.User', on_delete=models.SET_NULL, 
                                    null=True, blank=True, related_name='triggered_syncs')
    trigger_reason = models.CharField(max_length=255, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-started_at']
        indexes = [
            models.Index(fields=['external_system']),
            models.Index(fields=['status']),
            models.Index(fields=['sync_type']),
            models.Index(fields=['started_at']),
        ]
    
    def __str__(self):
        return f"{self.external_system.name} - {self.sync_type} ({self.status})"


class IntegrationMapping(models.Model):
    """
    Field mappings between HMS and external systems.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    external_system = models.ForeignKey(ExternalSystem, on_delete=models.CASCADE, 
                                       related_name='field_mappings')
    
    # Mapping details
    hms_model = models.CharField(max_length=100, 
                                help_text="HMS Django model name")
    hms_field = models.CharField(max_length=100, 
                                help_text="HMS model field name")
    external_field = models.CharField(max_length=100, 
                                     help_text="External system field name")
    
    # Data transformation
    transformation_type = models.CharField(max_length=50, 
                                         choices=[('DIRECT', 'Direct Mapping'), 
                                                 ('FORMAT', 'Format Transformation'),
                                                 ('CALCULATED', 'Calculated Field'),
                                                 ('LOOKUP', 'Lookup Table'),
                                                 ('CUSTOM', 'Custom Function')])
    
    transformation_rule = models.TextField(blank=True, 
                                         help_text="Transformation logic or rules")
    
    # Validation
    is_required = models.BooleanField(default=False)
    validation_rule = models.TextField(blank=True)
    default_value = models.CharField(max_length=255, blank=True)
    
    # Status
    is_active = models.BooleanField(default=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['hms_model', 'hms_field']
        indexes = [
            models.Index(fields=['external_system']),
            models.Index(fields=['hms_model']),
            models.Index(fields=['is_active']),
        ]
    
    def __str__(self):
        return f"{self.hms_model}.{self.hms_field} -> {self.external_field}"


class WebhookEndpoint(models.Model):
    """
    Webhook endpoints for real-time integrations.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    external_system = models.ForeignKey(ExternalSystem, on_delete=models.CASCADE, 
                                       related_name='webhook_endpoints')
    
    # Endpoint details
    name = models.CharField(max_length=255)
    url = models.URLField()
    method = models.CharField(max_length=10, 
                             choices=[('POST', 'POST'), 
                                     ('PUT', 'PUT'),
                                     ('PATCH', 'PATCH')])
    
    # Event triggers
    event_types = models.JSONField(default=list, blank=True, 
                                  help_text="List of events that trigger this webhook")
    
    # Authentication
    auth_type = models.CharField(max_length=50, 
                                choices=[('NONE', 'No Authentication'), 
                                        ('API_KEY', 'API Key'),
                                        ('BEARER_TOKEN', 'Bearer Token'),
                                        ('BASIC_AUTH', 'Basic Authentication'),
                                        ('HMAC', 'HMAC Signature')])
    
    auth_credentials = models.JSONField(default=dict, blank=True, 
                                       help_text="Authentication credentials")
    
    # Configuration
    is_active = models.BooleanField(default=True)
    retry_count = models.PositiveIntegerField(default=3)
    timeout_seconds = models.PositiveIntegerField(default=30)
    
    # Headers and payload
    custom_headers = models.JSONField(default=dict, blank=True)
    payload_template = models.TextField(blank=True, 
                                       help_text="Template for webhook payload")
    
    # Status tracking
    last_triggered = models.DateTimeField(null=True, blank=True)
    success_count = models.PositiveIntegerField(default=0)
    failure_count = models.PositiveIntegerField(default=0)
    last_error = models.TextField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['name']
        indexes = [
            models.Index(fields=['external_system']),
            models.Index(fields=['is_active']),
            models.Index(fields=['last_triggered']),
        ]
    
    def __str__(self):
        return f"{self.name} - {self.external_system.name}"


class IntegrationError(models.Model):
    """
    Integration error tracking and management.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    external_system = models.ForeignKey(ExternalSystem, on_delete=models.CASCADE, 
                                       related_name='integration_errors')
    
    # Error details
    error_type = models.CharField(max_length=50, 
                                choices=[('CONNECTION_ERROR', 'Connection Error'), 
                                        ('AUTHENTICATION_ERROR', 'Authentication Error'),
                                        ('DATA_VALIDATION_ERROR', 'Data Validation Error'),
                                        ('API_ERROR', 'API Error'),
                                        ('TIMEOUT_ERROR', 'Timeout Error'),
                                        ('RATE_LIMIT_ERROR', 'Rate Limit Error'),
                                        ('SYNC_ERROR', 'Synchronization Error'),
                                        ('WEBHOOK_ERROR', 'Webhook Error'),
                                        ('OTHER', 'Other')])
    
    error_message = models.TextField()
    error_code = models.CharField(max_length=50, blank=True)
    error_details = models.JSONField(default=dict, blank=True)
    
    # Context
    operation = models.CharField(max_length=100, blank=True, 
                                help_text="Operation that failed")
    affected_record_id = models.CharField(max_length=100, blank=True)
    affected_model = models.CharField(max_length=100, blank=True)
    
    # Status
    status = models.CharField(max_length=20, 
                              choices=[('NEW', 'New'), 
                                      ('INVESTIGATING', 'Investigating'),
                                      ('RESOLVED', 'Resolved'),
                                      ('IGNORED', 'Ignored')])
    
    # Resolution
    resolution_notes = models.TextField(blank=True)
    resolved_by = models.ForeignKey('users.User', on_delete=models.SET_NULL, 
                                    null=True, blank=True, related_name='resolved_integration_errors')
    resolved_at = models.DateTimeField(null=True, blank=True)
    
    # Retry information
    retry_count = models.PositiveIntegerField(default=0)
    last_retry_at = models.DateTimeField(null=True, blank=True)
    next_retry_at = models.DateTimeField(null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['external_system']),
            models.Index(fields=['error_type']),
            models.Index(fields=['status']),
            models.Index(fields=['created_at']),
        ]
    
    def __str__(self):
        return f"{self.error_type} - {self.external_system.name} ({self.created_at})"