from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid


# ============================================================
# Firm Model
# Represents the single audit firm using the platform
# ============================================================
class Firm(models.Model):
    name        = models.CharField(max_length=255)
    email       = models.EmailField(blank=True)
    phone       = models.CharField(max_length=20, blank=True)
    address     = models.TextField(blank=True)
    logo        = models.ImageField(upload_to='firm/logo/', blank=True, null=True)

    # registration code — new users must enter this to self-register
    # auto-generated as a short unique code e.g. "A3F9B2"
    registration_code = models.CharField(max_length=20, unique=True, blank=True)

    created_at  = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        # auto-generate registration code if not set
        if not self.registration_code:
            self.registration_code = uuid.uuid4().hex[:8].upper()
        super().save(*args, **kwargs)


# ============================================================
# AuditUser Model
# Custom user model — extends Django's built-in User
# ============================================================
class AuditUser(AbstractUser):

    ROLE_CHOICES = [
    ('partner',    'Partner'),
    ('manager',    'Manager'),
    ('senior',     'Senior Auditor'),
    ('staff',      'Staff Auditor'),
    ('it_auditor', 'IT Auditor'),
    ('qc',         'Quality Control Reviewer'),
    ('trainee',    'Trainee / Intern'),
]

    firm = models.ForeignKey(
        Firm,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='users'
    )
    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default='staff'
    )
    phone       = models.CharField(max_length=20, blank=True)
    # profile photo
    avatar      = models.ImageField(upload_to='avatars/', blank=True, null=True)

    def __str__(self):
        return f"{self.get_full_name()} ({self.get_role_display()})"