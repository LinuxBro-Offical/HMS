from django.db import models
from django.utils import timezone
import uuid


class Organization(models.Model):
    """Tenant/Organization model for schema-based multi-tenancy."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=100, unique=True)
    owner_name = models.CharField(max_length=255, blank=True)
    owner_email = models.EmailField(blank=True)
    contact_phone = models.CharField(max_length=30, blank=True)
    address = models.TextField(blank=True)

    # SaaS meta
    plan_expires_at = models.DateField(null=True, blank=True)
    seats = models.PositiveIntegerField(default=1)
    is_active = models.BooleanField(default=True)

    # Branding / customizations
    logo = models.URLField(blank=True, null=True)
    settings = models.JSONField(default=dict, blank=True)

    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.slug})"


class Domain(models.Model):
    """Domain model for mapping subdomains and custom domains to tenants."""
    
    domain = models.CharField(max_length=253, unique=True)
    tenant = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='domains')
    is_primary = models.BooleanField(default=False)
    display_name = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.domain


class Branch(models.Model):
    """Represents a physical branch within a tenant schema."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=50, blank=True)
    address = models.TextField(blank=True)
    phone = models.CharField(max_length=30, blank=True)
    email = models.EmailField(blank=True)
    is_primary = models.BooleanField(default=False)

    timezone = models.CharField(max_length=50, default="Asia/Kolkata")
    working_hours = models.JSONField(default=dict, blank=True)
    metadata = models.JSONField(default=dict, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=["code"]),
            models.Index(fields=["name"]),
        ]

    def __str__(self):
        return f"{self.name} ({self.code})"


class Plan(models.Model):
    """Defines a SaaS subscription plan template."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, unique=True)
    code = models.SlugField(max_length=50, unique=True)
    description = models.TextField(blank=True)

    price_monthly = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    price_yearly = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    currency = models.CharField(max_length=10, default="INR")

    max_branches = models.PositiveIntegerField(default=1)
    max_doctors = models.PositiveIntegerField(default=5)
    max_staff = models.PositiveIntegerField(default=10)
    max_patients = models.PositiveIntegerField(default=1000)
    max_storage_mb = models.PositiveIntegerField(default=512)

    allow_patient_portal = models.BooleanField(default=False)
    allow_sms = models.BooleanField(default=False)
    allow_whatsapp = models.BooleanField(default=False)
    allow_inventory = models.BooleanField(default=False)
    allow_insurance = models.BooleanField(default=False)
    allow_reports = models.BooleanField(default=True)

    features = models.JSONField(default=dict, blank=True)

    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["price_monthly"]

    def __str__(self):
        return f"{self.name} ({self.currency} {self.price_monthly}/mo)"


class Subscription(models.Model):
    """Tracks active plan subscription for each tenant (Organization)."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    organization = models.OneToOneField(
        Organization, on_delete=models.CASCADE, related_name="subscription"
    )
    plan = models.ForeignKey(Plan, on_delete=models.PROTECT)

    start_date = models.DateField(default=timezone.now)
    end_date = models.DateField(null=True, blank=True)

    is_trial = models.BooleanField(default=False)
    trial_ends_at = models.DateField(null=True, blank=True)

    is_active = models.BooleanField(default=True)
    last_notified = models.DateField(null=True, blank=True)

    notes = models.TextField(blank=True)
    metadata = models.JSONField(default=dict, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.organization.name} → {self.plan.name}"

    def is_expired(self):
        return self.end_date and self.end_date < timezone.now().date()

    def days_remaining(self):
        if not self.end_date:
            return None
        return (self.end_date - timezone.now().date()).days