from django.db import models
from django.utils import timezone
import uuid


class PatientAnalytics(models.Model):
    """
    Patient-level analytics and metrics tracking.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    patient = models.ForeignKey('patients.Patient', on_delete=models.CASCADE, 
                               related_name='analytics')
    
    # Metric details
    metric_type = models.CharField(max_length=50, 
                                  choices=[('VISIT_FREQUENCY', 'Visit Frequency'), 
                                          ('RISK_SCORE', 'Risk Score'),
                                          ('SATISFACTION_SCORE', 'Satisfaction Score'),
                                          ('WAIT_TIME', 'Average Wait Time'),
                                          ('TREATMENT_COMPLIANCE', 'Treatment Compliance'),
                                          ('COST_PER_VISIT', 'Cost per Visit'),
                                          ('READMISSION_RISK', 'Readmission Risk'),
                                          ('CHRONIC_DISEASE_MANAGEMENT', 'Chronic Disease Management')])
    metric_value = models.DecimalField(max_digits=10, decimal_places=2)
    metric_unit = models.CharField(max_length=20, blank=True)
    
    # Time period
    recorded_date = models.DateField()
    period_start = models.DateField(null=True, blank=True)
    period_end = models.DateField(null=True, blank=True)
    
    # Source and context
    source = models.CharField(max_length=100, 
                             choices=[('ENCOUNTER', 'Encounter Data'), 
                                     ('SURVEY', 'Patient Survey'),
                                     ('CALCULATED', 'Calculated Metric'),
                                     ('EXTERNAL', 'External System'),
                                     ('MANUAL', 'Manual Entry')])
    recorded_by = models.ForeignKey('users.User', on_delete=models.SET_NULL, 
                                   null=True, blank=True, related_name='recorded_patient_analytics')
    
    # Additional context
    context_data = models.JSONField(default=dict, blank=True, 
                                   help_text="Additional context and metadata")
    notes = models.TextField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-recorded_date']
        indexes = [
            models.Index(fields=['patient']),
            models.Index(fields=['metric_type']),
            models.Index(fields=['recorded_date']),
            models.Index(fields=['source']),
        ]
    
    def __str__(self):
        return f"{self.patient.full_name} - {self.metric_type} ({self.recorded_date})"


class ClinicAnalytics(models.Model):
    """
    Clinic/branch-level analytics and performance metrics.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    branch = models.ForeignKey('tenants.Branch', on_delete=models.CASCADE, 
                              related_name='analytics')
    
    # Date and period
    date = models.DateField()
    period_type = models.CharField(max_length=20, 
                                  choices=[('DAILY', 'Daily'), 
                                          ('WEEKLY', 'Weekly'),
                                          ('MONTHLY', 'Monthly'),
                                          ('QUARTERLY', 'Quarterly'),
                                          ('YEARLY', 'Yearly')])
    
    # Key metrics
    metric_name = models.CharField(max_length=100, 
                                   choices=[('PATIENT_COUNT', 'Patient Count'), 
                                           ('APPOINTMENT_COUNT', 'Appointment Count'),
                                           ('REVENUE', 'Revenue'),
                                           ('AVERAGE_WAIT_TIME', 'Average Wait Time'),
                                           ('PATIENT_SATISFACTION', 'Patient Satisfaction'),
                                           ('DOCTOR_UTILIZATION', 'Doctor Utilization'),
                                           ('CANCELLATION_RATE', 'Cancellation Rate'),
                                           ('NO_SHOW_RATE', 'No-show Rate'),
                                           ('AVERAGE_CONSULTATION_TIME', 'Average Consultation Time'),
                                           ('REVENUE_PER_PATIENT', 'Revenue per Patient'),
                                           ('COST_PER_VISIT', 'Cost per Visit'),
                                           ('PROFIT_MARGIN', 'Profit Margin')])
    metric_value = models.DecimalField(max_digits=15, decimal_places=2)
    metric_unit = models.CharField(max_length=20, blank=True)
    
    # Additional metadata
    metadata = models.JSONField(default=dict, blank=True, 
                               help_text="Additional metric-specific data")
    
    # Calculation details
    calculation_method = models.CharField(max_length=100, blank=True)
    data_source = models.CharField(max_length=100, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-date']
        indexes = [
            models.Index(fields=['branch']),
            models.Index(fields=['date']),
            models.Index(fields=['metric_name']),
            models.Index(fields=['period_type']),
        ]
    
    def __str__(self):
        return f"{self.branch.name} - {self.metric_name} ({self.date})"


class DoctorPerformance(models.Model):
    """
    Doctor-specific performance analytics and metrics.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    doctor = models.ForeignKey('users.StaffProfile', on_delete=models.CASCADE, 
                              related_name='performance_analytics')
    branch = models.ForeignKey('tenants.Branch', on_delete=models.CASCADE, 
                              related_name='doctor_performance')
    
    # Time period
    period_start = models.DateField()
    period_end = models.DateField()
    
    # Performance metrics
    total_patients = models.PositiveIntegerField(default=0)
    total_appointments = models.PositiveIntegerField(default=0)
    completed_appointments = models.PositiveIntegerField(default=0)
    cancelled_appointments = models.PositiveIntegerField(default=0)
    no_show_appointments = models.PositiveIntegerField(default=0)
    
    # Time metrics
    average_consultation_time = models.PositiveIntegerField(null=True, blank=True, 
                                                          help_text="Average consultation time in minutes")
    total_consultation_time = models.PositiveIntegerField(default=0, 
                                                         help_text="Total consultation time in minutes")
    
    # Quality metrics
    average_patient_satisfaction = models.DecimalField(max_digits=3, decimal_places=2, 
                                                      null=True, blank=True)
    average_wait_time = models.PositiveIntegerField(null=True, blank=True, 
                                                   help_text="Average patient wait time in minutes")
    
    # Revenue metrics
    total_revenue = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    revenue_per_patient = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    
    # Efficiency metrics
    utilization_rate = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, 
                                         help_text="Doctor utilization percentage")
    productivity_score = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    
    # Additional metrics
    prescription_count = models.PositiveIntegerField(default=0)
    lab_order_count = models.PositiveIntegerField(default=0)
    follow_up_count = models.PositiveIntegerField(default=0)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-period_end']
        indexes = [
            models.Index(fields=['doctor']),
            models.Index(fields=['branch']),
            models.Index(fields=['period_start']),
            models.Index(fields=['period_end']),
        ]
    
    def __str__(self):
        return f"{self.doctor.user.full_name} - {self.period_start} to {self.period_end}"


class RevenueAnalytics(models.Model):
    """
    Revenue and financial analytics tracking.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    branch = models.ForeignKey('tenants.Branch', on_delete=models.CASCADE, 
                              related_name='revenue_analytics')
    
    # Time period
    date = models.DateField()
    period_type = models.CharField(max_length=20, 
                                  choices=[('DAILY', 'Daily'), 
                                          ('WEEKLY', 'Weekly'),
                                          ('MONTHLY', 'Monthly'),
                                          ('QUARTERLY', 'Quarterly'),
                                          ('YEARLY', 'Yearly')])
    
    # Revenue metrics
    total_revenue = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    consultation_revenue = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    lab_revenue = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    pharmacy_revenue = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    procedure_revenue = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    
    # Payment metrics
    cash_payments = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    card_payments = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    upi_payments = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    insurance_payments = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    
    # Cost metrics
    total_costs = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    staff_costs = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    equipment_costs = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    medication_costs = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    
    # Profit metrics
    gross_profit = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    net_profit = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    profit_margin = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    
    # Patient metrics
    total_patients = models.PositiveIntegerField(default=0)
    new_patients = models.PositiveIntegerField(default=0)
    returning_patients = models.PositiveIntegerField(default=0)
    revenue_per_patient = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-date']
        indexes = [
            models.Index(fields=['branch']),
            models.Index(fields=['date']),
            models.Index(fields=['period_type']),
        ]
    
    def __str__(self):
        return f"{self.branch.name} - Revenue ({self.date})"


class CustomReport(models.Model):
    """
    Custom analytics reports and dashboards.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    
    # Report configuration
    report_type = models.CharField(max_length=50, 
                                  choices=[('PATIENT_ANALYTICS', 'Patient Analytics'), 
                                          ('REVENUE_ANALYTICS', 'Revenue Analytics'),
                                          ('DOCTOR_PERFORMANCE', 'Doctor Performance'),
                                          ('OPERATIONAL_METRICS', 'Operational Metrics'),
                                          ('CUSTOM', 'Custom Report')])
    
    # Filters and parameters
    filters = models.JSONField(default=dict, blank=True, 
                              help_text="Report filters and parameters")
    date_range_start = models.DateField(null=True, blank=True)
    date_range_end = models.DateField(null=True, blank=True)
    
    # Report data
    report_data = models.JSONField(default=dict, blank=True, 
                                  help_text="Generated report data")
    
    # Access control
    created_by = models.ForeignKey('users.User', on_delete=models.CASCADE, 
                                  related_name='created_reports')
    is_public = models.BooleanField(default=False)
    shared_with = models.ManyToManyField('users.User', blank=True, 
                                        related_name='shared_reports')
    
    # Schedule
    is_scheduled = models.BooleanField(default=False)
    schedule_frequency = models.CharField(max_length=20, blank=True, 
                                         choices=[('DAILY', 'Daily'), 
                                                 ('WEEKLY', 'Weekly'),
                                                 ('MONTHLY', 'Monthly')])
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['created_by']),
            models.Index(fields=['report_type']),
            models.Index(fields=['is_public']),
        ]
    
    def __str__(self):
        return f"{self.name} - {self.report_type}"