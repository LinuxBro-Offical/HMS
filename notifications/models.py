from django.db import models
from django.utils import timezone
import uuid

CHANNEL_CHOICES = [
    ('SMS', 'SMS'),
    ('WHATSAPP', 'WhatsApp'),
    ('INAPP', 'In-App'),
]

EVENT_CHOICES = [
    ('appointment_booked', 'Appointment Booked'),
    ('appointment_reminder', 'Appointment Reminder'),
    ('invoice_issued', 'Invoice Issued'),
    ('followup_reminder', 'Follow-Up Reminder'),
]

STATUS_CHOICES = [
    ('PENDING', 'Pending'),
    ('SENT', 'Sent'),
    ('FAILED', 'Failed'),
]


class TenantNotificationSetting(models.Model):
    """Per-tenant provider config & channel toggles. Stored in tenant schema."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    tenant = models.CharField(max_length=255, help_text='Tenant slug (for reference)')

    # Channel toggles
    sms_enabled = models.BooleanField(default=True)
    whatsapp_enabled = models.BooleanField(default=True)

    # Provider credentials (store encrypted in production)
    sms_provider = models.CharField(max_length=50, default='twilio')
    sms_api_key = models.CharField(max_length=512, blank=True, null=True)
    whatsapp_provider = models.CharField(max_length=50, default='twilio_whatsapp')
    whatsapp_api_key = models.CharField(max_length=512, blank=True, null=True)

    default_from_number = models.CharField(max_length=50, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('tenant',)

    def __str__(self):
        return f"Notification Settings for {self.tenant}"


class NotificationTemplate(models.Model):
    """Templates per tenant, per event and channel. Rendered with Jinja2."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    tenant = models.CharField(max_length=255)
    event = models.CharField(max_length=50, choices=EVENT_CHOICES)
    channel = models.CharField(max_length=20, choices=CHANNEL_CHOICES)

    # Jinja2 template text
    subject = models.CharField(max_length=255, blank=True, null=True)
    template = models.TextField()

    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('tenant','event','channel')

    def __str__(self):
        return f"{self.tenant} - {self.event} - {self.channel}"


class NotificationEvent(models.Model):
    """Represents a queued notification event which will be processed by Celery tasks."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    tenant = models.CharField(max_length=255)
    event = models.CharField(max_length=50, choices=EVENT_CHOICES)
    channel = models.CharField(max_length=20, choices=CHANNEL_CHOICES)
    to = models.CharField(max_length=255)  # phone or whatsapp id
    subject = models.CharField(max_length=255, blank=True, null=True)
    message = models.TextField(blank=True, null=True)
    payload = models.JSONField(default=dict, blank=True)
    scheduled_at = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    attempts = models.PositiveSmallIntegerField(default=0)
    last_error = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.tenant} {self.event} -> {self.to} ({self.status})"


class NotificationLog(models.Model):
    """Delivery logs for auditing and debugging."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    event = models.ForeignKey(NotificationEvent, on_delete=models.SET_NULL, null=True, blank=True, related_name='logs')
    channel = models.CharField(max_length=20, choices=CHANNEL_CHOICES)
    to = models.CharField(max_length=255)
    provider_response = models.JSONField(default=dict, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    sent_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Log {self.channel} -> {self.to} : {self.status}"