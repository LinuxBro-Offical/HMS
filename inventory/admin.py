from django.contrib import admin
from .models import Medicine, InventoryItem, PurchaseOrder, PurchaseOrderItem, StockAlert

@admin.register(Medicine)
class MedicineAdmin(admin.ModelAdmin):
    list_display = ['name', 'generic_name', 'dosage_form', 'strength', 'mrp', 'is_active']
    list_filter = ['dosage_form', 'schedule', 'is_active']
    search_fields = ['name', 'generic_name']

@admin.register(InventoryItem)
class InventoryItemAdmin(admin.ModelAdmin):
    list_display = ['medicine', 'branch', 'current_stock', 'minimum_stock', 'is_expired']
    list_filter = ['branch', 'is_expired', 'is_near_expiry']

@admin.register(PurchaseOrder)
class PurchaseOrderAdmin(admin.ModelAdmin):
    list_display = ['order_number', 'supplier_name', 'status', 'total_amount', 'order_date']
    list_filter = ['status']

@admin.register(StockAlert)
class StockAlertAdmin(admin.ModelAdmin):
    list_display = ['inventory_item', 'alert_type', 'severity', 'is_active']
    list_filter = ['alert_type', 'severity', 'is_active']
