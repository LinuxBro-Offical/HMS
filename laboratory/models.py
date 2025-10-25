from django.db import models
from django.utils import timezone
import uuid


class LabTest(models.Model):
    """
    Laboratory test master data with reference ranges and pricing.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    test_code = models.CharField(max_length=50, unique=True)
    test_name = models.CharField(max_length=255)
    category = models.CharField(max_length=100, 
                               choices=[('BIOCHEMISTRY', 'Biochemistry'), 
                                       ('HEMATOLOGY', 'Hematology'),
                                       ('MICROBIOLOGY', 'Microbiology'),
                                       ('PATHOLOGY', 'Pathology'),
                                       ('IMMUNOLOGY', 'Immunology'),
                                       ('ENDOCRINOLOGY', 'Endocrinology'),
                                       ('CARDIAC', 'Cardiac Markers'),
                                       ('TUMOR', 'Tumor Markers')])
    sample_type = models.CharField(max_length=50, 
                                  choices=[('BLOOD', 'Blood'), 
                                          ('URINE', 'Urine'),
                                          ('STOOL', 'Stool'),
                                          ('SPUTUM', 'Sputum'),
                                          ('CSF', 'Cerebrospinal Fluid'),
                                          ('TISSUE', 'Tissue Biopsy'),
                                          ('SWAB', 'Swab')])
    preparation_instructions = models.TextField(blank=True, 
                                              help_text="Patient preparation instructions")
    
    # Reference ranges
    normal_range_male = models.CharField(max_length=100, blank=True)
    normal_range_female = models.CharField(max_length=100, blank=True)
    normal_range_pediatric = models.CharField(max_length=100, blank=True)
    unit = models.CharField(max_length=20, blank=True)
    
    # Pricing and availability
    price = models.DecimalField(max_digits=10, decimal_places=2)
    is_active = models.BooleanField(default=True)
    requires_fasting = models.BooleanField(default=False)
    fasting_hours = models.PositiveIntegerField(null=True, blank=True)
    
    # Additional information
    description = models.TextField(blank=True)
    methodology = models.CharField(max_length=255, blank=True)
    turnaround_time_hours = models.PositiveIntegerField(default=24)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['category', 'test_name']
        indexes = [
            models.Index(fields=['test_code']),
            models.Index(fields=['category']),
            models.Index(fields=['is_active']),
        ]
    
    def __str__(self):
        return f"{self.test_name} ({self.test_code})"


class LabOrder(models.Model):
    """
    Laboratory test orders from doctors.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    patient = models.ForeignKey('patients.Patient', on_delete=models.CASCADE, 
                               related_name='lab_orders')
    encounter = models.ForeignKey('encounters.Encounter', on_delete=models.CASCADE, 
                                 null=True, blank=True, related_name='lab_orders')
    ordered_by = models.ForeignKey('users.User', on_delete=models.CASCADE, 
                                  related_name='lab_orders')
    
    # Order details
    order_number = models.CharField(max_length=50, unique=True)
    order_date = models.DateTimeField(auto_now_add=True)
    priority = models.CharField(max_length=20, 
                               choices=[('ROUTINE', 'Routine'), 
                                       ('URGENT', 'Urgent'),
                                       ('STAT', 'STAT (Immediate)'),
                                       ('ASAP', 'ASAP')])
    status = models.CharField(max_length=20, 
                             choices=[('ORDERED', 'Ordered'), 
                                     ('COLLECTED', 'Sample Collected'),
                                     ('PROCESSING', 'Processing'),
                                     ('COMPLETED', 'Completed'),
                                     ('CANCELLED', 'Cancelled')])
    
    # Clinical information
    clinical_indication = models.TextField(blank=True, 
                                         help_text="Clinical reason for ordering")
    notes = models.TextField(blank=True)
    
    # Collection details
    collection_date = models.DateTimeField(null=True, blank=True)
    collected_by = models.ForeignKey('users.User', on_delete=models.SET_NULL, 
                                    null=True, blank=True, related_name='collected_lab_orders')
    collection_notes = models.TextField(blank=True)
    
    # Completion details
    completed_date = models.DateTimeField(null=True, blank=True)
    completed_by = models.ForeignKey('users.User', on_delete=models.SET_NULL, 
                                    null=True, blank=True, related_name='completed_lab_orders')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-order_date']
        indexes = [
            models.Index(fields=['patient']),
            models.Index(fields=['status']),
            models.Index(fields=['priority']),
            models.Index(fields=['order_date']),
        ]
    
    def __str__(self):
        return f"Lab Order {self.order_number} - {self.patient.full_name}"


class LabOrderItem(models.Model):
    """
    Individual tests within a lab order.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    lab_order = models.ForeignKey(LabOrder, on_delete=models.CASCADE, 
                                 related_name='items')
    test = models.ForeignKey(LabTest, on_delete=models.CASCADE)
    
    # Test-specific details
    quantity = models.PositiveIntegerField(default=1)
    special_instructions = models.TextField(blank=True)
    
    # Status tracking
    status = models.CharField(max_length=20, 
                             choices=[('ORDERED', 'Ordered'), 
                                     ('COLLECTED', 'Sample Collected'),
                                     ('PROCESSING', 'Processing'),
                                     ('COMPLETED', 'Completed'),
                                     ('CANCELLED', 'Cancelled')])
    
    # Results
    result_value = models.CharField(max_length=100, blank=True)
    result_text = models.TextField(blank=True)
    reference_range = models.CharField(max_length=100, blank=True)
    unit = models.CharField(max_length=20, blank=True)
    is_abnormal = models.BooleanField(default=False)
    abnormality_type = models.CharField(max_length=20, blank=True, 
                                       choices=[('HIGH', 'High'), 
                                               ('LOW', 'Low'),
                                               ('CRITICAL', 'Critical')])
    
    # Verification
    is_verified = models.BooleanField(default=False)
    verified_by = models.ForeignKey('users.User', on_delete=models.SET_NULL, 
                                   null=True, blank=True, related_name='verified_lab_order_items')
    verified_at = models.DateTimeField(null=True, blank=True)
    verification_notes = models.TextField(blank=True)
    
    # Completion
    completed_at = models.DateTimeField(null=True, blank=True)
    completed_by = models.ForeignKey('users.User', on_delete=models.SET_NULL, 
                                    null=True, blank=True, related_name='completed_lab_results')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['lab_order', 'test']
        indexes = [
            models.Index(fields=['lab_order']),
            models.Index(fields=['test']),
            models.Index(fields=['status']),
            models.Index(fields=['is_abnormal']),
        ]
    
    def __str__(self):
        return f"{self.test.test_name} - {self.lab_order.order_number}"


class LabResult(models.Model):
    """
    Detailed laboratory test results with attachments.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    lab_order_item = models.OneToOneField(LabOrderItem, on_delete=models.CASCADE, 
                                         related_name='detailed_result')
    
    # Result details
    result_value = models.CharField(max_length=100, blank=True)
    result_text = models.TextField(blank=True)
    reference_range = models.CharField(max_length=100, blank=True)
    unit = models.CharField(max_length=20, blank=True)
    
    # Quality control
    is_abnormal = models.BooleanField(default=False)
    abnormality_type = models.CharField(max_length=20, blank=True, 
                                       choices=[('HIGH', 'High'), 
                                               ('LOW', 'Low'),
                                               ('CRITICAL', 'Critical')])
    critical_value = models.BooleanField(default=False)
    
    # Additional information
    methodology = models.CharField(max_length=255, blank=True)
    equipment_used = models.CharField(max_length=255, blank=True)
    quality_control_passed = models.BooleanField(default=True)
    
    # Attachments
    result_file = models.FileField(upload_to='lab_results/%Y/%m/%d/', 
                                  blank=True, null=True)
    image_file = models.ImageField(upload_to='lab_images/%Y/%m/%d/', 
                                  blank=True, null=True)
    
    # Verification and approval
    is_verified = models.BooleanField(default=False)
    verified_by = models.ForeignKey('users.User', on_delete=models.SET_NULL, 
                                   null=True, blank=True, related_name='verified_lab_results')
    verified_at = models.DateTimeField(null=True, blank=True)
    verification_notes = models.TextField(blank=True)
    
    # Approval
    is_approved = models.BooleanField(default=False)
    approved_by = models.ForeignKey('users.User', on_delete=models.SET_NULL, 
                                    null=True, blank=True, related_name='approved_lab_results')
    approved_at = models.DateTimeField(null=True, blank=True)
    approval_notes = models.TextField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['is_abnormal']),
            models.Index(fields=['critical_value']),
            models.Index(fields=['is_verified']),
            models.Index(fields=['is_approved']),
        ]
    
    def __str__(self):
        return f"Result for {self.lab_order_item.test.test_name} - {self.lab_order_item.lab_order.order_number}"