from django.contrib import admin
from .models import LabTest, LabOrder, LabOrderItem, LabResult

@admin.register(LabTest)
class LabTestAdmin(admin.ModelAdmin):
    list_display = ['test_name', 'test_code', 'category', 'price', 'is_active']
    list_filter = ['category', 'is_active']
    search_fields = ['test_name', 'test_code']

@admin.register(LabOrder)
class LabOrderAdmin(admin.ModelAdmin):
    list_display = ['order_number', 'patient', 'status', 'priority', 'order_date']
    list_filter = ['status', 'priority']
    search_fields = ['order_number', 'patient__full_name']

@admin.register(LabOrderItem)
class LabOrderItemAdmin(admin.ModelAdmin):
    list_display = ['lab_order', 'test', 'status', 'is_abnormal']
    list_filter = ['status', 'is_abnormal']

@admin.register(LabResult)
class LabResultAdmin(admin.ModelAdmin):
    list_display = ['lab_order_item', 'is_abnormal', 'critical_value', 'is_verified']
    list_filter = ['is_abnormal', 'critical_value', 'is_verified']
