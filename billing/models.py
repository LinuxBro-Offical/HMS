from django.db import models
from django.utils import timezone
import uuid
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

PAYMENT_METHODS = [
    ('CASH', 'Cash'),
    ('CARD', 'Card'),
    ('UPI', 'UPI'),
    ('WALLET', 'Wallet'),
    ('NETBANK', 'NetBanking'),
    ('OTHER', 'Other'),
]

INVOICE_STATUS = [
    ('DRAFT', 'Draft'),
    ('ISSUED', 'Issued'),
    ('PARTIALLY_PAID', 'Partially Paid'),
    ('PAID', 'Paid'),
    ('CANCELLED', 'Cancelled'),
    ('REFUNDED', 'Refunded'),
]


class ChargeType(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    code = models.SlugField(max_length=100, unique=True)
    name = models.CharField(max_length=255)
    category = models.CharField(max_length=100, blank=True, null=True)
    default_price = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    is_taxable = models.BooleanField(default=True)
    taxable_rate = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.code})"


class InvoiceCounter(models.Model):
    """Tenant-scoped invoice counter. Use to generate tenant-scoped invoice numbers."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    prefix = models.CharField(max_length=50, blank=True, null=True)  # e.g., AC-202510
    counter = models.PositiveIntegerField(default=0)
    updated_at = models.DateTimeField(auto_now=True)

    def next(self):
        self.counter += 1
        self.save(update_fields=['counter', 'updated_at'])
        return self.counter

    def formatted(self):
        seq = str(self.counter).zfill(4)
        if self.prefix:
            return f"{self.prefix}-{seq}"
        return seq

    def __str__(self):
        return f"{self.prefix or 'GEN'} - {self.counter}"


class Invoice(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    invoice_no = models.CharField(max_length=100, unique=True)
    patient = models.ForeignKey('patients.Patient', on_delete=models.CASCADE, related_name='invoices')
    created_by = models.ForeignKey('users.User', on_delete=models.SET_NULL, null=True, blank=True, related_name='created_invoices')
    encounter = models.ForeignKey('encounters.Encounter', on_delete=models.SET_NULL, null=True, blank=True, related_name='invoices')
    appointment = models.ForeignKey('appointments.Appointment', on_delete=models.SET_NULL, null=True, blank=True, related_name='invoices')
    date = models.DateTimeField(default=timezone.now)

    subtotal = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    tax_total = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    discount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    total = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    status = models.CharField(max_length=20, choices=INVOICE_STATUS, default='DRAFT')
    notes = models.TextField(blank=True, null=True)
    metadata = models.JSONField(default=dict, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return f"{self.invoice_no} - {self.patient.patient_code} - {self.total}"

    def recalc(self):
        items = self.items.all()
        self.subtotal = sum([it.amount for it in items])
        self.tax_total = sum([it.tax_amount for it in items])
        self.total = self.subtotal + self.tax_total - (self.discount or 0)
        self.save(update_fields=['subtotal', 'tax_total', 'total'])

    def outstanding_amount(self):
        allocated = sum([alloc.amount for alloc in self.allocations.all()])
        return float(self.total) - float(allocated)


class InvoiceItem(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, related_name='items')
    charge_type = models.ForeignKey(ChargeType, on_delete=models.PROTECT)
    description = models.CharField(max_length=512)
    unit_price = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    quantity = models.DecimalField(max_digits=8, decimal_places=2, default=1)
    amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    tax_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    discount = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    content_type = models.ForeignKey(ContentType, on_delete=models.SET_NULL, null=True, blank=True)
    object_id = models.CharField(max_length=255, null=True, blank=True)
    source_object = GenericForeignKey('content_type', 'object_id')

    validity_days = models.PositiveIntegerField(null=True, blank=True)
    valid_until = models.DateField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.amount:
            self.amount = (self.unit_price * self.quantity) - (self.discount or 0)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.description} - {self.amount}"


class Payment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    paid_by = models.ForeignKey('users.User', on_delete=models.SET_NULL, null=True, blank=True, related_name='payments')
    payer_name = models.CharField(max_length=255, blank=True, null=True)
    payment_method = models.CharField(max_length=50, choices=PAYMENT_METHODS)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    paid_at = models.DateTimeField(default=timezone.now)
    transaction_ref = models.CharField(max_length=255, blank=True, null=True)
    metadata = models.JSONField(default=dict, blank=True)
    is_advance = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.payment_method} - {self.amount} @ {self.paid_at.date()}"


class PaymentAllocation(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    payment = models.ForeignKey(Payment, on_delete=models.CASCADE, related_name='allocations')
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, related_name='allocations')
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    allocated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [models.Index(fields=['invoice']), models.Index(fields=['payment'])]

    def __str__(self):
        return f"{self.payment} -> {self.invoice.invoice_no} : {self.amount}"


class Refund(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    payment = models.ForeignKey(Payment, on_delete=models.SET_NULL, null=True, blank=True)
    invoice = models.ForeignKey(Invoice, on_delete=models.SET_NULL, null=True, blank=True)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    reason = models.TextField(blank=True, null=True)
    processed_by = models.ForeignKey('users.User', on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Refund {self.amount} for {self.invoice}"