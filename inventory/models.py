from django.db import models
from django.utils import timezone
import uuid


class Medicine(models.Model):
    """
    Medicine master data with comprehensive drug information.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255, help_text="Brand name")
    generic_name = models.CharField(max_length=255, help_text="Generic/chemical name")
    manufacturer = models.CharField(max_length=255)
    
    # Drug specifications
    dosage_form = models.CharField(max_length=50, 
                                  choices=[('TABLET', 'Tablet'), 
                                          ('CAPSULE', 'Capsule'),
                                          ('SYRUP', 'Syrup'),
                                          ('INJECTION', 'Injection'),
                                          ('OINTMENT', 'Ointment'),
                                          ('DROPS', 'Drops'),
                                          ('POWDER', 'Powder'),
                                          ('CREAM', 'Cream')])
    strength = models.CharField(max_length=100, help_text="e.g., 500mg, 10ml")
    unit = models.CharField(max_length=20, help_text="e.g., mg, ml, g")
    
    # Regulatory information
    drug_code = models.CharField(max_length=50, unique=True)
    schedule = models.CharField(max_length=10, 
                               choices=[('H1', 'Schedule H1'), 
                                       ('H', 'Schedule H'),
                                       ('X', 'Schedule X'),
                                       ('G', 'Schedule G'),
                                       ('NORMAL', 'Normal')])
    requires_prescription = models.BooleanField(default=True)
    
    # Pricing
    mrp = models.DecimalField(max_digits=10, decimal_places=2, 
                            help_text="Maximum Retail Price")
    cost_price = models.DecimalField(max_digits=10, decimal_places=2)
    
    # Medical information
    contraindications = models.TextField(blank=True)
    side_effects = models.TextField(blank=True)
    storage_conditions = models.CharField(max_length=255, blank=True)
    shelf_life_months = models.PositiveIntegerField(null=True, blank=True)
    
    # Additional information
    therapeutic_class = models.CharField(max_length=100, blank=True)
    indication = models.TextField(blank=True)
    dosage_instructions = models.TextField(blank=True)
    
    # Status
    is_active = models.BooleanField(default=True)
    is_controlled_substance = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['name']
        indexes = [
            models.Index(fields=['name']),
            models.Index(fields=['generic_name']),
            models.Index(fields=['drug_code']),
            models.Index(fields=['is_active']),
        ]
    
    def __str__(self):
        return f"{self.name} ({self.strength})"


class InventoryItem(models.Model):
    """
    Medicine inventory tracking per branch.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    medicine = models.ForeignKey(Medicine, on_delete=models.CASCADE, 
                                related_name='inventory_items')
    branch = models.ForeignKey('tenants.Branch', on_delete=models.CASCADE, 
                               related_name='inventory_items')
    
    # Stock levels
    current_stock = models.PositiveIntegerField(default=0)
    minimum_stock = models.PositiveIntegerField(default=10)
    maximum_stock = models.PositiveIntegerField(default=1000)
    reorder_level = models.PositiveIntegerField(default=20)
    
    # Batch information
    batch_number = models.CharField(max_length=100)
    expiry_date = models.DateField()
    manufacturing_date = models.DateField(null=True, blank=True)
    
    # Pricing (branch-specific)
    selling_price = models.DecimalField(max_digits=10, decimal_places=2)
    cost_price = models.DecimalField(max_digits=10, decimal_places=2)
    
    # Supplier information
    supplier_name = models.CharField(max_length=255, blank=True)
    supplier_contact = models.CharField(max_length=100, blank=True)
    purchase_date = models.DateField(null=True, blank=True)
    
    # Status
    is_active = models.BooleanField(default=True)
    is_expired = models.BooleanField(default=False)
    is_near_expiry = models.BooleanField(default=False)
    
    # Audit
    last_updated = models.DateTimeField(auto_now=True)
    last_updated_by = models.ForeignKey('users.User', on_delete=models.SET_NULL, 
                                       null=True, blank=True, related_name='inventory_updates')
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['medicine', 'expiry_date']
        indexes = [
            models.Index(fields=['medicine']),
            models.Index(fields=['branch']),
            models.Index(fields=['current_stock']),
            models.Index(fields=['expiry_date']),
            models.Index(fields=['is_expired']),
        ]
    
    def __str__(self):
        return f"{self.medicine.name} - {self.branch.name} ({self.current_stock})"
    
    def save(self, *args, **kwargs):
        # Check if medicine is near expiry (within 30 days)
        if self.expiry_date:
            days_to_expiry = (self.expiry_date - timezone.now().date()).days
            self.is_near_expiry = days_to_expiry <= 30
            self.is_expired = days_to_expiry <= 0
        
        super().save(*args, **kwargs)


class PurchaseOrder(models.Model):
    """
    Medicine purchase orders for inventory management.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    branch = models.ForeignKey('tenants.Branch', on_delete=models.CASCADE, 
                              related_name='purchase_orders')
    supplier_name = models.CharField(max_length=255)
    supplier_contact = models.CharField(max_length=100, blank=True)
    
    # Order details
    order_number = models.CharField(max_length=50, unique=True)
    order_date = models.DateTimeField(auto_now_add=True)
    expected_delivery_date = models.DateField(null=True, blank=True)
    
    # Status
    status = models.CharField(max_length=20, 
                             choices=[('DRAFT', 'Draft'), 
                                     ('ORDERED', 'Ordered'),
                                     ('PARTIALLY_RECEIVED', 'Partially Received'),
                                     ('RECEIVED', 'Received'),
                                     ('CANCELLED', 'Cancelled')])
    
    # Financial
    total_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    tax_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    discount_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    final_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    
    # Notes
    notes = models.TextField(blank=True)
    
    # Audit
    created_by = models.ForeignKey('users.User', on_delete=models.CASCADE, 
                                  related_name='created_purchase_orders')
    approved_by = models.ForeignKey('users.User', on_delete=models.SET_NULL, 
                                    null=True, blank=True, related_name='approved_purchase_orders')
    approved_at = models.DateTimeField(null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-order_date']
        indexes = [
            models.Index(fields=['branch']),
            models.Index(fields=['status']),
            models.Index(fields=['order_date']),
        ]
    
    def __str__(self):
        return f"PO {self.order_number} - {self.supplier_name}"


class PurchaseOrderItem(models.Model):
    """
    Individual items in a purchase order.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    purchase_order = models.ForeignKey(PurchaseOrder, on_delete=models.CASCADE, 
                                      related_name='items')
    medicine = models.ForeignKey(Medicine, on_delete=models.CASCADE)
    
    # Quantities
    quantity_ordered = models.PositiveIntegerField()
    quantity_received = models.PositiveIntegerField(default=0)
    
    # Pricing
    unit_cost = models.DecimalField(max_digits=10, decimal_places=2)
    total_cost = models.DecimalField(max_digits=12, decimal_places=2)
    
    # Batch information
    batch_number = models.CharField(max_length=100, blank=True)
    expiry_date = models.DateField(null=True, blank=True)
    
    # Status
    status = models.CharField(max_length=20, 
                             choices=[('ORDERED', 'Ordered'), 
                                     ('PARTIALLY_RECEIVED', 'Partially Received'),
                                     ('RECEIVED', 'Received'),
                                     ('CANCELLED', 'Cancelled')])
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['purchase_order', 'medicine']
        indexes = [
            models.Index(fields=['purchase_order']),
            models.Index(fields=['medicine']),
            models.Index(fields=['status']),
        ]
    
    def __str__(self):
        return f"{self.medicine.name} - {self.quantity_ordered} units"


class StockAlert(models.Model):
    """
    Automated stock alerts for inventory management.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    inventory_item = models.ForeignKey(InventoryItem, on_delete=models.CASCADE, 
                                      related_name='stock_alerts')
    
    alert_type = models.CharField(max_length=20, 
                                 choices=[('LOW_STOCK', 'Low Stock'), 
                                         ('OUT_OF_STOCK', 'Out of Stock'),
                                         ('EXPIRY_WARNING', 'Expiry Warning'),
                                         ('EXPIRED', 'Expired')])
    severity = models.CharField(max_length=20, 
                               choices=[('HIGH', 'High'), 
                                       ('MEDIUM', 'Medium'),
                                       ('LOW', 'Low')])
    message = models.TextField()
    
    # Status
    is_active = models.BooleanField(default=True)
    is_acknowledged = models.BooleanField(default=False)
    acknowledged_by = models.ForeignKey('users.User', on_delete=models.SET_NULL, 
                                       null=True, blank=True, related_name='acknowledged_stock_alerts')
    acknowledged_at = models.DateTimeField(null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['inventory_item']),
            models.Index(fields=['alert_type']),
            models.Index(fields=['severity']),
            models.Index(fields=['is_active']),
        ]
    
    def __str__(self):
        return f"{self.alert_type} - {self.inventory_item.medicine.name}"