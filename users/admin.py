from django.contrib import admin
from .models import User, Role, StaffProfile, DeviceRefreshToken


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'full_name', 'phone', 'is_active', 'is_staff', 'created_at')
    search_fields = ('email', 'full_name', 'phone')
    list_filter = ('is_active', 'is_staff', 'created_at')
    ordering = ('-created_at',)


@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'default')
    search_fields = ('name', 'description')


@admin.register(StaffProfile)
class StaffProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'employee_id', 'designation', 'specialization', 'is_consulting')
    search_fields = ('user__email', 'user__full_name', 'employee_id', 'designation')
    list_filter = ('designation', 'is_consulting')


@admin.register(DeviceRefreshToken)
class DeviceRefreshTokenAdmin(admin.ModelAdmin):
    list_display = ('user', 'jti', 'revoked', 'created_at', 'last_used_at')
    search_fields = ('user__email', 'jti')
    list_filter = ('revoked', 'created_at')