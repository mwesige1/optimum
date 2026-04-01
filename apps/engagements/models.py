from django.db import models
from apps.accounts.models import AuditUser
from apps.clients.models import AuditClient


# ============================================================
# Engagement Model
# Represents one audit engagement
# e.g. "Nile Breweries — FY2024 Annual Audit"
# ============================================================
class Engagement(models.Model):

    STATUS_CHOICES = [
        ('planning',    'Planning'),
        ('fieldwork',   'Fieldwork'),
        ('reporting',   'Reporting'),
        ('complete',    'Complete'),
        ('cancelled',   'Cancelled'),
    ]

    AUDIT_TYPE_CHOICES = [
        ('external',    'External Audit'),
        ('internal',    'Internal Audit'),
        ('tax',         'Tax Audit'),
        ('compliance',  'Compliance Audit'),
        ('special',     'Special Purpose Audit'),
    ]

    # core fields
    name            = models.CharField(max_length=255)          # engagement name
    client          = models.ForeignKey(
                        AuditClient,
                        on_delete=models.CASCADE,
                        related_name='engagements'
                      )
    audit_type      = models.CharField(max_length=20, choices=AUDIT_TYPE_CHOICES, default='external')
    financial_year  = models.CharField(max_length=20)           # e.g. "FY2024" or "2024"
    status          = models.CharField(max_length=20, choices=STATUS_CHOICES, default='planning')

    # dates
    start_date      = models.DateField()
    end_date        = models.DateField()

    # team
    lead_auditor    = models.ForeignKey(
                        AuditUser,
                        on_delete=models.SET_NULL,
                        null=True,
                        related_name='led_engagements'
                      )
    team_members    = models.ManyToManyField(
                        AuditUser,
                        through='EngagementMember',
                        related_name='engagements'
                      )

    # additional info
    materiality     = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)  # materiality threshold
    notes           = models.TextField(blank=True)

    created_by      = models.ForeignKey(
                        AuditUser,
                        on_delete=models.SET_NULL,
                        null=True,
                        related_name='engagements_created'
                      )
    created_at      = models.DateTimeField(auto_now_add=True)
    updated_at      = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']      # newest engagements first

    def __str__(self):
        return f"{self.name} — {self.client.name} ({self.financial_year})"


# ============================================================
# EngagementMember Model
# Links users to engagements with a specific role
# Uses a through model so we can store the role on the link
# ============================================================
class EngagementMember(models.Model):

    ROLE_CHOICES = [
        ('lead',    'Lead Auditor'),
        ('senior',  'Senior Auditor'),
        ('staff',   'Staff Auditor'),
        ('reviewer','Reviewer'),
    ]

    engagement  = models.ForeignKey(Engagement, on_delete=models.CASCADE)
    user        = models.ForeignKey(AuditUser, on_delete=models.CASCADE)
    role        = models.CharField(max_length=20, choices=ROLE_CHOICES, default='staff')
    joined_at   = models.DateTimeField(auto_now_add=True)

    class Meta:
        # prevent the same user being added to the same engagement twice
        unique_together = ('engagement', 'user')

    def __str__(self):
        return f"{self.user.get_full_name()} — {self.engagement.name}"