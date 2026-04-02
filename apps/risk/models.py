from django.db import models
from apps.accounts.models import AuditUser
from apps.engagements.models import Engagement


# ============================================================
# RiskArea Model
# Represents one area of the audit being risk assessed
# e.g. Revenue, Cash & Bank, Inventory, Payroll etc.
# Each engagement has its own set of risk areas
# ============================================================
class RiskArea(models.Model):

    # predefined audit areas — these are the standard areas
    # assessed in every external audit
    AREA_CHOICES = [
        ('revenue',         'Revenue & Receivables'),
        ('cash',            'Cash & Bank'),
        ('inventory',       'Inventory & Stock'),
        ('payroll',         'Payroll & Staff Costs'),
        ('fixed_assets',    'Fixed Assets'),
        ('payables',        'Payables & Liabilities'),
        ('tax',             'Tax & Statutory Compliance'),
        ('it_controls',     'IT General Controls'),
        ('financial_close', 'Financial Close & Reporting'),
        ('other',           'Other'),
    ]

    RISK_LEVEL_CHOICES = [
        ('high',    'High'),
        ('medium',  'Medium'),
        ('low',     'Low'),
    ]

    # which engagement this risk area belongs to
    engagement      = models.ForeignKey(
                        Engagement,
                        on_delete=models.CASCADE,
                        related_name='risk_areas'
                      )

    # the audit area being assessed
    area            = models.CharField(
                        max_length=30,
                        choices=AREA_CHOICES,
                        default='other'
                      )

    # custom name if area is 'other'
    custom_area_name = models.CharField(
                        max_length=100,
                        blank=True,
                        help_text='Only fill this if area is Other'
                      )

    # --------------------------------------------------------
    # The three risk components
    # Each is a percentage from 0 to 100
    # --------------------------------------------------------

    # Inherent Risk — how naturally risky is this area
    # before considering any controls?
    # High inherent risk = complex transactions, large amounts,
    # high volume, history of errors
    inherent_risk   = models.IntegerField(
                        default=0,
                        help_text='0-100. How naturally risky is this area before controls?'
                      )

    # Control Risk — how effective are the client's controls
    # over this area?
    # High control risk = weak or missing controls
    control_risk    = models.IntegerField(
                        default=0,
                        help_text='0-100. How effective are the controls? Higher = weaker controls'
                      )

    # Detection Risk — what is the risk that auditors miss
    # a material misstatement in this area?
    # This is set by the audit team based on planned procedures
    detection_risk  = models.IntegerField(
                        default=0,
                        help_text='0-100. Risk that audit procedures miss a material error'
                      )

    # overall risk assessment for this area
    # calculated automatically from the three components
    overall_risk    = models.CharField(
                        max_length=10,
                        choices=RISK_LEVEL_CHOICES,
                        default='medium',
                        editable=False   # set automatically by save()
                      )

    # key risks identified in this area — free text
    key_risks       = models.TextField(
                        blank=True,
                        help_text='Describe the specific risks identified in this area'
                      )

    # audit response — what procedures will the team perform
    audit_response  = models.TextField(
                        blank=True,
                        help_text='What audit procedures will address these risks?'
                      )

    # who assessed this risk area
    assessed_by     = models.ForeignKey(
                        AuditUser,
                        on_delete=models.SET_NULL,
                        null=True,
                        related_name='risk_assessments'
                      )

    created_at      = models.DateTimeField(auto_now_add=True)
    updated_at      = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['area']
        # prevent the same area being assessed twice
        # on the same engagement
        unique_together = ('engagement', 'area')

    def __str__(self):
        return f"{self.get_area_display()} — {self.engagement.name}"

    def save(self, *args, **kwargs):
        # automatically calculate overall risk from the three components
        # overall risk = average of inherent + control + detection
        average = (self.inherent_risk + self.control_risk + self.detection_risk) / 3
        if average >= 65:
            self.overall_risk = 'high'
        elif average >= 35:
            self.overall_risk = 'medium'
        else:
            self.overall_risk = 'low'
        super().save(*args, **kwargs)

    def get_area_name(self):
        # returns custom name if area is 'other'
        # otherwise returns the standard display name
        if self.area == 'other' and self.custom_area_name:
            return self.custom_area_name
        return self.get_area_display()

    @property
    def combined_risk_score(self):
        # returns the average risk score as a number
        return round(
            (self.inherent_risk + self.control_risk + self.detection_risk) / 3
        )


# ============================================================
# RiskMatrix Model
# The overall risk matrix for an engagement
# Summarises all risk areas and gives an engagement-level
# risk conclusion
# ============================================================
class RiskMatrix(models.Model):

    OVERALL_RISK_CHOICES = [
        ('high',     'High — Extensive audit procedures required'),
        ('moderate', 'Moderate — Standard audit procedures with selected extensions'),
        ('low',      'Low — Reduced audit procedures acceptable'),
    ]

    # one risk matrix per engagement
    engagement          = models.OneToOneField(
                            Engagement,
                            on_delete=models.CASCADE,
                            related_name='risk_matrix'
                          )

    # overall engagement risk conclusion
    overall_risk        = models.CharField(
                            max_length=10,
                            choices=OVERALL_RISK_CHOICES,
                            default='moderate'
                          )

    # materiality — the threshold below which errors are ignored
    overall_materiality = models.DecimalField(
                            max_digits=15,
                            decimal_places=2,
                            null=True,
                            blank=True,
                            help_text='Overall materiality threshold (UGX)'
                          )

    # performance materiality is usually 75% of overall materiality
    performance_materiality = models.DecimalField(
                                max_digits=15,
                                decimal_places=2,
                                null=True,
                                blank=True,
                                help_text='Performance materiality (usually 75% of overall)'
                              )

    # basis for materiality calculation
    materiality_basis   = models.CharField(
                            max_length=255,
                            blank=True,
                            help_text='e.g. 5% of total revenue, 1% of total assets'
                          )

    # overall conclusion and approach
    audit_approach      = models.TextField(
                            blank=True,
                            help_text='Overall audit approach and strategy'
                          )

    # who prepared and approved the risk matrix
    prepared_by         = models.ForeignKey(
                            AuditUser,
                            on_delete=models.SET_NULL,
                            null=True,
                            related_name='risk_matrices_prepared'
                          )
    approved_by         = models.ForeignKey(
                            AuditUser,
                            on_delete=models.SET_NULL,
                            null=True,
                            blank=True,
                            related_name='risk_matrices_approved'
                          )

    is_approved         = models.BooleanField(default=False)
    created_at          = models.DateTimeField(auto_now_add=True)
    updated_at          = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Risk Matrix — {self.engagement.name}"