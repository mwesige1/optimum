from django.db import models
from django.contrib.auth.models import AbstractUser


class Firm(models.Model):
    name = models.CharField(max_length=255)           
    email = models.EmailField(blank=True)            
    phone = models.CharField(max_length=20, blank=True)
    address = models.TextField(blank=True)            
    created_at = models.DateTimeField(auto_now_add=True)  

    def __str__(self):
        return self.name


# ============================================================
# AuditUser Model
# Our custom user model — extends Django's built-in User
# We extend it to add role, firm, and phone number
# AbstractUser already gives us: username, email, password,
# first_name, last_name, is_active, is_staff, date_joined
# ============================================================
class AuditUser(AbstractUser):

    # Role choices — controls what each user can see and do
    ROLE_CHOICES = [
        ('partner', 'Partner'),          # highest level — full access, signs off reports
        ('manager', 'Manager'),          # manages engagements and teams
        ('senior', 'Senior Auditor'),    # leads fieldwork, reviews junior work
        ('staff', 'Staff Auditor'),      # prepares workpapers, performs tests
    ]

    # Every user belongs to a firm
    # null=True and blank=True allows the superadmin user to have no firm
    firm = models.ForeignKey(
        Firm,
        on_delete=models.CASCADE,   # if the firm is deleted, all its users are deleted too
        null=True,
        blank=True,
        related_name='users'        # lets us do firm.users.all() to get all users in a firm
    )

    # The user's role within their firm
    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default='staff'             # new users are staff by default
    )

    # Optional phone number
    phone = models.CharField(max_length=20, blank=True)

    def __str__(self):
        # shows full name and role e.g. "Patrick Ssekandi (Staff Auditor)"
        return f"{self.get_full_name()} ({self.get_role_display()})"