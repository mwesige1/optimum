from django.db import models
from apps.accounts.models import AuditUser
from apps.engagements.models import Engagement


# ============================================================
# Finding Model
# Represents a problem or deficiency discovered during audit
# e.g. "Revenue recognition cut-off errors"
# or "IT access controls — no approval workflow"
# ============================================================
class Finding(models.Model):

    RISK_CHOICES = [
        ('high',    'High'),
        ('medium',  'Medium'),
        ('low',     'Low'),
    ]

    STATUS_CHOICES = [
        ('open',        'Open'),
        ('in_progress', 'In Progress'),
        ('resolved',    'Resolved'),
        ('overdue',     'Overdue'),
    ]

    CATEGORY_CHOICES = [
        ('internal_control',    'Internal Control Deficiency'),
        ('financial_reporting', 'Financial Reporting'),
        ('compliance',          'Compliance Issue'),
        ('fraud_risk',          'Fraud Risk'),
        ('it_control',          'IT Control Weakness'),
        ('operational',         'Operational Issue'),
        ('other',               'Other'),
    ]

    # which engagement this finding belongs to
    engagement      = models.ForeignKey(
                        Engagement,
                        on_delete=models.CASCADE,
                        related_name='findings'
                      )

    # core fields
    title           = models.CharField(max_length=255)
    category        = models.CharField(
                        max_length=30,
                        choices=CATEGORY_CHOICES,
                        default='other'
                      )
    risk_level      = models.CharField(
                        max_length=10,
                        choices=RISK_CHOICES,
                        default='medium'
                      )
    status          = models.CharField(
                        max_length=20,
                        choices=STATUS_CHOICES,
                        default='open'
                      )

    # the full description of the finding
    # what is the problem, what is the criteria (what should happen),
    # what is the condition (what actually happened),
    # what is the cause, what is the effect/impact
    criteria        = models.TextField(
                        help_text='What should be happening — the standard or requirement'
                      )
    condition       = models.TextField(
                        help_text='What is actually happening — the problem observed'
                      )
    cause           = models.TextField(
                        blank=True,
                        help_text='Why is this happening'
                      )
    effect          = models.TextField(
                        blank=True,
                        help_text='What is the impact or risk of this issue'
                      )

    # recommendation from the auditor
    recommendation  = models.TextField(
                        blank=True,
                        help_text='What the client should do to fix this'
                      )

    # who raised this finding and who it is assigned to
    raised_by       = models.ForeignKey(
                        AuditUser,
                        on_delete=models.SET_NULL,
                        null=True,
                        related_name='findings_raised'
                      )
    assigned_to     = models.ForeignKey(
                        AuditUser,
                        on_delete=models.SET_NULL,
                        null=True, blank=True,
                        related_name='findings_assigned'
                      )

    # deadline for the client to resolve this finding
    due_date        = models.DateField(null=True, blank=True)

    created_at      = models.DateTimeField(auto_now_add=True)
    updated_at      = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} ({self.get_risk_level_display()})"

    def is_overdue(self):
        # returns True if the due date has passed and finding is not resolved
        from django.utils import timezone
        if self.due_date and self.status not in ['resolved']:
            return self.due_date < timezone.now().date()
        return False


# ============================================================
# ManagementResponse Model
# The client's official written response to a finding
# They either accept it and commit to fixing it,
# or they disagree and explain why
# ============================================================
class ManagementResponse(models.Model):

    RESPONSE_CHOICES = [
        ('accepted',    'Accepted'),        # client agrees and will fix it
        ('rejected',    'Rejected'),        # client disagrees with the finding
        ('partial',     'Partially Accepted'), # client accepts part of it
    ]

    finding         = models.OneToOneField(
                        Finding,
                        on_delete=models.CASCADE,
                        related_name='management_response'
                      )
    response_type   = models.CharField(
                        max_length=20,
                        choices=RESPONSE_CHOICES,
                        default='accepted'
                      )
    response_text   = models.TextField(
                        help_text='The client\'s written response to this finding'
                      )
    action_plan     = models.TextField(
                        blank=True,
                        help_text='What the client will do to fix this and by when'
                      )
    responded_by    = models.CharField(
                        max_length=255,
                        blank=True,
                        help_text='Name and title of the person responding on behalf of the client'
                      )
    response_date   = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"Response to: {self.finding.title}"
    

# ============================================================
# Notification Model
# In-app notifications for audit team members
# Appears as a badge on the dashboard
# ============================================================
class Notification(models.Model):

    TYPE_CHOICES = [
        ('finding_response',  'Client responded to finding'),
        ('finding_overdue',   'Finding is overdue'),
        ('workpaper_review',  'Workpaper needs review'),
        ('finding_resolved',  'Finding resolved'),
    ]

    # who receives this notification
    recipient       = models.ForeignKey(
                        'accounts.AuditUser',
                        on_delete=models.CASCADE,
                        related_name='notifications'
                      )

    notification_type = models.CharField(
                            max_length=30,
                            choices=TYPE_CHOICES
                        )

    # the message shown to the user
    message         = models.CharField(max_length=500)

    # link to the relevant page
    link            = models.CharField(max_length=255, blank=True)

    # has the user seen this notification
    is_read         = models.BooleanField(default=False)

    created_at      = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.recipient.get_full_name()} — {self.message}"