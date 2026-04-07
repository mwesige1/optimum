from django.db import models
from apps.accounts.models import AuditUser


# ============================================================
# AuditClient Model
# Represents a company being audited
# The client manages their own information through the portal
# The audit firm can view and delete but not edit
# ============================================================
class AuditClient(models.Model):

    INDUSTRY_CHOICES = [
        ('banking',       'Banking & Finance'),
        ('manufacturing', 'Manufacturing'),
        ('retail',        'Retail & Trade'),
        ('telecom',       'Telecommunications'),
        ('ngo',           'NGO / Non-profit'),
        ('government',    'Government'),
        ('healthcare',    'Healthcare'),
        ('real_estate',   'Real Estate'),
        ('hospitality',   'Hospitality'),
        ('other',         'Other'),
    ]

    STATUS_CHOICES = [
        ('pending',  'Pending Approval'),
        ('active',   'Active'),
        ('inactive', 'Inactive'),
    ]

    # core information
    name            = models.CharField(max_length=255)
    industry        = models.CharField(
                        max_length=50,
                        choices=INDUSTRY_CHOICES,
                        default='other'
                      )
    contact_person  = models.CharField(max_length=255, blank=True)
    contact_email   = models.EmailField(blank=True)
    contact_phone   = models.CharField(max_length=20, blank=True)
    address         = models.TextField(blank=True)
    website         = models.URLField(blank=True)

    # status of the client
    status          = models.CharField(
                        max_length=20,
                        choices=STATUS_CHOICES,
                        default='pending'
                      )

    # who added this client
    created_by      = models.ForeignKey(
                        AuditUser,
                        on_delete=models.SET_NULL,
                        null=True,
                        related_name='clients_created'
                      )
    created_at      = models.DateTimeField(auto_now_add=True)
    updated_at      = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name