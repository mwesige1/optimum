from django.db import models
from apps.accounts.models import AuditUser
from apps.engagements.models import Engagement


# ============================================================
# RatioAnalysis Model
# Stores financial ratios for an engagement
# Auditors compare current year vs prior year
# to identify unusual movements that need investigation
# ============================================================
class RatioAnalysis(models.Model):

    RATIO_CATEGORY_CHOICES = [
        ('profitability', 'Profitability Ratios'),
        ('liquidity',     'Liquidity Ratios'),
        ('efficiency',    'Efficiency Ratios'),
        ('leverage',      'Leverage / Gearing Ratios'),
        ('revenue',       'Revenue Analysis'),
        ('expense',       'Expense Analysis'),
        ('other',         'Other'),
    ]

    engagement          = models.ForeignKey(
                            Engagement,
                            on_delete=models.CASCADE,
                            related_name='ratio_analyses'
                          )

    # the name of the ratio or analysis
    # e.g. "Gross Profit Margin", "Current Ratio", "Revenue Growth"
    ratio_name          = models.CharField(max_length=255)
    category            = models.CharField(
                            max_length=20,
                            choices=RATIO_CATEGORY_CHOICES,
                            default='other'
                          )

    # current year value
    current_year_value  = models.DecimalField(
                            max_digits=20,
                            decimal_places=2,
                            null=True,
                            blank=True
                          )

    # prior year value for comparison
    prior_year_value    = models.DecimalField(
                            max_digits=20,
                            decimal_places=2,
                            null=True,
                            blank=True
                          )

    # unit — e.g. %, UGX, times, days
    unit                = models.CharField(
                            max_length=20,
                            default='%',
                            blank=True
                          )

    # variance calculated automatically
    variance            = models.DecimalField(
                            max_digits=20,
                            decimal_places=2,
                            null=True,
                            blank=True,
                            editable=False
                          )

    # variance percentage
    variance_pct        = models.DecimalField(
                            max_digits=10,
                            decimal_places=2,
                            null=True,
                            blank=True,
                            editable=False
                          )

    # auditor's explanation of the movement
    explanation         = models.TextField(
                            blank=True,
                            help_text='Explain the reason for the movement between years'
                          )

    # is this movement acceptable or does it need investigation?
    requires_followup   = models.BooleanField(
                            default=False,
                            help_text='Flag if this movement is unusual and needs further audit work'
                          )

    prepared_by         = models.ForeignKey(
                            AuditUser,
                            on_delete=models.SET_NULL,
                            null=True,
                            related_name='ratio_analyses'
                          )

    created_at          = models.DateTimeField(auto_now_add=True)
    updated_at          = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['category', 'ratio_name']

    def __str__(self):
        return f"{self.ratio_name} — {self.engagement.name}"

    def save(self, *args, **kwargs):
        # automatically calculate variance and variance %
        if self.current_year_value is not None and \
           self.prior_year_value is not None:
            self.variance = self.current_year_value - self.prior_year_value
            if self.prior_year_value != 0:
                self.variance_pct = round(
                    (self.variance / abs(self.prior_year_value)) * 100, 2
                )
            else:
                self.variance_pct = None
        super().save(*args, **kwargs)


# ============================================================
# MaterialityCalculation Model
# Records the materiality calculation for an engagement
# Materiality is the threshold below which errors are ignored
# ============================================================
class MaterialityCalculation(models.Model):

    BASIS_CHOICES = [
        ('revenue',       'Total Revenue'),
        ('total_assets',  'Total Assets'),
        ('gross_profit',  'Gross Profit'),
        ('net_profit',    'Net Profit Before Tax'),
        ('equity',        'Total Equity'),
        ('expenditure',   'Total Expenditure'),
    ]

    # one materiality calculation per engagement
    engagement              = models.OneToOneField(
                                Engagement,
                                on_delete=models.CASCADE,
                                related_name='materiality_calc'
                              )

    # the financial figure used as the basis
    basis                   = models.CharField(
                                max_length=20,
                                choices=BASIS_CHOICES,
                                default='revenue'
                              )

    # the actual amount of the basis figure e.g. total revenue = 500 billion
    basis_amount            = models.DecimalField(
                                max_digits=20,
                                decimal_places=2,
                                help_text='The actual financial figure used as basis (UGX)'
                              )

    # the percentage applied to the basis
    # e.g. 5% of revenue, 1% of total assets
    materiality_percentage  = models.DecimalField(
                                max_digits=5,
                                decimal_places=2,
                                help_text='Percentage applied to the basis e.g. 5 for 5%'
                              )

    # overall materiality — calculated automatically
    overall_materiality     = models.DecimalField(
                                max_digits=20,
                                decimal_places=2,
                                editable=False,
                                default=0
                              )

    # performance materiality — usually 60-75% of overall
    performance_pct         = models.DecimalField(
                                max_digits=5,
                                decimal_places=2,
                                default=75,
                                help_text='Performance materiality as % of overall e.g. 75'
                              )

    # performance materiality amount — calculated automatically
    performance_materiality = models.DecimalField(
                                max_digits=20,
                                decimal_places=2,
                                editable=False,
                                default=0
                              )

    # clearly trivial threshold — usually 3-5% of overall materiality
    trivial_pct             = models.DecimalField(
                                max_digits=5,
                                decimal_places=2,
                                default=5,
                                help_text='Clearly trivial as % of overall e.g. 5'
                              )

    # clearly trivial amount — calculated automatically
    trivial_threshold       = models.DecimalField(
                                max_digits=20,
                                decimal_places=2,
                                editable=False,
                                default=0
                              )

    # justification for the basis and percentage chosen
    justification           = models.TextField(
                                blank=True,
                                help_text='Explain why this basis and percentage were chosen'
                              )

    prepared_by             = models.ForeignKey(
                                AuditUser,
                                on_delete=models.SET_NULL,
                                null=True,
                                related_name='materiality_calcs'
                              )

    is_approved             = models.BooleanField(default=False)
    approved_by             = models.ForeignKey(
                                AuditUser,
                                on_delete=models.SET_NULL,
                                null=True,
                                blank=True,
                                related_name='materiality_approved'
                              )

    created_at              = models.DateTimeField(auto_now_add=True)
    updated_at              = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Materiality — {self.engagement.name}"

    def save(self, *args, **kwargs):
        # automatically calculate all materiality amounts
        if self.basis_amount and self.materiality_percentage:
            self.overall_materiality = round(
                self.basis_amount * self.materiality_percentage / 100, 2
            )
            self.performance_materiality = round(
                self.overall_materiality * self.performance_pct / 100, 2
            )
            self.trivial_threshold = round(
                self.overall_materiality * self.trivial_pct / 100, 2
            )
        super().save(*args, **kwargs)