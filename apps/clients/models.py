from django.db import models
from apps.accounts.models import AuditUser


# ============================================================
# AuditClient Model
# Represents a company being audited
# e.g. "Nile Breweries Uganda", "Bank of Africa"
# ============================================================
class AuditClient(models.Model):

    # industry choices
    INDUSTRY_CHOICES = [
        ('banking',        'Banking & Finance'),
        ('manufacturing',  'Manufacturing'),
        ('retail',         'Retail & Trade'),
        ('telecom',        'Telecommunications'),
        ('ngo',            'NGO / Non-profit'),
        ('government',     'Government'),
        ('healthcare',     'Healthcare'),
        ('real_estate',    'Real Estate'),
        ('hospitality',    'Hospitality'),
        ('other',          'Other'),
    ]

    name            = models.CharField(max_length=255)          # company name
    industry        = models.CharField(max_length=50, choices=INDUSTRY_CHOICES, default='other')
    contact_person  = models.CharField(max_length=255, blank=True)  # main contact at the client
    contact_email   = models.EmailField(blank=True)
    contact_phone   = models.CharField(max_length=20, blank=True)
    address         = models.TextField(blank=True)
    website         = models.URLField(blank=True)

    # the user who added this client
    created_by      = models.ForeignKey(
        AuditUser,
        on_delete=models.SET_NULL,
        null=True,
        related_name='clients_created'
    )
    created_at      = models.DateTimeField(auto_now_add=True)
    updated_at      = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']     # list clients alphabetically by default

    def __str__(self):
        return self.name