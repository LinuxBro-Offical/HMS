from django.contrib import admin
from .models import ChargeType, InvoiceCounter, Invoice, InvoiceItem, Payment, PaymentAllocation, Refund


@admin.register(ChargeType)
class ChargeTypeAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'category', 'default_price', 'is_active')
    search_fields = ('code', 'name', 'category')
    list_filter = ('is_active', 'category', 'is_taxable')


@admin.register(InvoiceCounter)
class InvoiceCounterAdmin(admin.ModelAdmin):
    list_display = ('prefix', 'counter', 'updated_at')
    search_fields = ('prefix',)


@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ('invoice_no', 'patient', 'date', 'total', 'status')
    search_fields = ('invoice_no', 'patient__full_name', 'patient__patient_code')
    list_filter = ('status', 'date')
    readonly_fields = ('subtotal', 'tax_total', 'total')


@admin.register(InvoiceItem)
class InvoiceItemAdmin(admin.ModelAdmin):
    list_display = ('invoice', 'charge_type', 'description', 'unit_price', 'quantity', 'amount')
    search_fields = ('description', 'invoice__invoice_no')
    list_filter = ('charge_type',)


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('payment_method', 'amount', 'paid_at', 'transaction_ref', 'is_advance')
    search_fields = ('transaction_ref', 'payer_name')
    list_filter = ('payment_method', 'is_advance', 'paid_at')


@admin.register(PaymentAllocation)
class PaymentAllocationAdmin(admin.ModelAdmin):
    list_display = ('payment', 'invoice', 'amount', 'allocated_at')
    search_fields = ('invoice__invoice_no',)
    list_filter = ('allocated_at',)


@admin.register(Refund)
class RefundAdmin(admin.ModelAdmin):
    list_display = ('invoice', 'amount', 'processed_by', 'created_at')
    search_fields = ('invoice__invoice_no', 'reason')
    list_filter = ('created_at',)