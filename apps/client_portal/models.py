from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from apps.clients.models import AuditClient


# ============================================================
# ClientUserManager
# Custom manager for creating client users
# ============================================================
class ClientUserManager(BaseUserManager):

    def create_user(self, email, company_name, password=None, **extra_fields):
        if not email:
            raise ValueError('Email is required')
        email = self.normalize_email(email)
        user  = self.model(
            email        = email,
            company_name = company_name,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user


# ============================================================
# ClientUser Model
# A completely separate user type from AuditUser
# Represents the client company accessing their portal
# They can only see their own data — nothing else
# ============================================================
class ClientUser(AbstractBaseUser):

    # basic info
    company_name    = models.CharField(max_length=255)
    contact_person  = models.CharField(max_length=255)
    email           = models.EmailField(unique=True)
    phone           = models.CharField(max_length=20, blank=True)

    # links this portal user to the AuditClient record
    # set by the Partner after approval
    client          = models.OneToOneField(
                        AuditClient,
                        on_delete=models.CASCADE,
                        null=True,
                        blank=True,
                        related_name='portal_user'
                      )

    # approval — Partner must approve before client can log in
    is_approved     = models.BooleanField(default=False)
    is_active       = models.BooleanField(default=True)

    # timestamps
    registered_at   = models.DateTimeField(auto_now_add=True)
    approved_at     = models.DateTimeField(null=True, blank=True)

    # approval note from the Partner
    approval_note   = models.TextField(blank=True)

    objects = ClientUserManager()

    # use email as the login field instead of username
    USERNAME_FIELD  = 'email'
    REQUIRED_FIELDS = ['company_name', 'contact_person']

    class Meta:
        ordering = ['-registered_at']

    def __str__(self):
        return f"{self.company_name} ({self.email})"

    def get_full_name(self):
        return self.contact_person

    def get_company_name(self):
        return self.company_name