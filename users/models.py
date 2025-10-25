from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager, Group
from django.db import models
import uuid


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Email is required')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        if password:
            user.set_password(password)
        else:
            user.set_unusable_password()
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    """Custom user model for tenant schemas."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField('email address', unique=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    full_name = models.CharField(max_length=255)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)  # for django admin

    # audit/security
    last_login_ip = models.GenericIPAddressField(null=True, blank=True)
    last_active_at = models.DateTimeField(null=True, blank=True)
    device_info = models.JSONField(default=dict, blank=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.email


class Role(models.Model):
    """Custom role model mapped to Django's Group & Permission for RBAC."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, unique=True)
    group = models.OneToOneField(Group, on_delete=models.CASCADE, null=True, blank=True)
    description = models.TextField(blank=True)
    default = models.BooleanField(default=False)  # for new user assignment

    def __str__(self):
        return self.name


class StaffProfile(models.Model):
    """Profile for internal staff. Links users to branches and roles."""

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='staff_profile')
    employee_id = models.CharField(max_length=50, blank=True, null=True)
    designation = models.CharField(max_length=100, blank=True)  # Doctor, Receptionist, Lab
    specialization = models.CharField(max_length=200, blank=True, null=True)
    signature = models.ImageField(upload_to='signatures/%Y/%m/%d/', null=True, blank=True)

    # Staff can belong to multiple branches
    assigned_branches = models.ManyToManyField('tenants.Branch', blank=True, related_name='staff_members')

    # Role(s)
    roles = models.ManyToManyField(Role, blank=True, related_name='users')

    is_consulting = models.BooleanField(default=False)

    meta = models.JSONField(default=dict, blank=True)  # extra attributes

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def has_role(self, role_name):
        return self.roles.filter(name=role_name).exists()

    def __str__(self):
        return f"{self.user.email} - {self.designation}"


class DeviceRefreshToken(models.Model):
    """Track issued refresh tokens for logout, audit, and device management."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # tenant-scoped user model
    jti = models.CharField(max_length=255, unique=True)  # token jti (from token payload)
    refresh_token = models.TextField()  # store encrypted or hashed in prod, plain for dev
    revoked = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    last_used_at = models.DateTimeField(null=True, blank=True)
    device_info = models.JSONField(default=dict, blank=True)  # {platform, ua, ip}
    expires_at = models.DateTimeField(null=True, blank=True)

    def mark_revoked(self):
        self.revoked = True
        self.save(update_fields=['revoked'])

    def __str__(self):
        return f"{self.user.email} @ {self.device_info.get('device','unknown')}"