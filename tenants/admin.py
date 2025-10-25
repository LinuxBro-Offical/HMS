from django.contrib import admin
from .models import Organization, Domain, Branch, Plan, Subscription


@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'owner_email', 'is_active', 'created_on')
    search_fields = ('name', 'slug', 'owner_email')
    list_filter = ('is_active', 'created_on')


@admin.register(Domain)
class DomainAdmin(admin.ModelAdmin):
    list_display = ('domain', 'tenant', 'is_primary', 'display_name')
    search_fields = ('domain', 'tenant__name')
    list_filter = ('is_primary',)


@admin.register(Branch)
class BranchAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'is_primary', 'phone', 'created_at')
    search_fields = ('name', 'code', 'phone')
    list_filter = ('is_primary', 'created_at')


@admin.register(Plan)
class PlanAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'price_monthly', 'currency', 'is_active')
    search_fields = ('name', 'code')
    list_filter = ('is_active', 'currency')


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('organization', 'plan', 'start_date', 'end_date', 'is_active')
    search_fields = ('organization__name', 'plan__name')
    list_filter = ('is_active', 'is_trial', 'start_date')