from django.db import models
from apps.accounts.models import AuditUser
from apps.engagements.models import Engagement


# ============================================================
# Workpaper Model
# Represents a single working paper in an engagement
# e.g. "WP-2100 Cash and Bank" or "E315 Revenue Analytics"
# Every procedure performed during the audit is documented
# in a workpaper
# ============================================================
class Workpaper(models.Model):

    STATUS_CHOICES = [
        ('draft',       'Draft'),           # being prepared by staff
        ('in_review',   'In Review'),       # submitted for senior review
        ('reviewed',    'Reviewed'),        # reviewed by senior auditor
        ('signed_off',  'Signed Off'),      # final sign off by partner/manager
    ]

    SECTION_CHOICES = [
        ('planning',    'Planning'),
        ('controls',    'Internal Controls'),
        ('substantive', 'Substantive Procedures'),
        ('completion',  'Completion'),
        ('other',       'Other'),
    ]

    # which engagement this workpaper belongs to
    engagement      = models.ForeignKey(
                        Engagement,
                        on_delete=models.CASCADE,
                        related_name='workpapers'
                      )

    # index reference e.g. WP-2100, E315, A100
    reference       = models.CharField(max_length=50)

    title           = models.CharField(max_length=255)
    section         = models.CharField(max_length=20, choices=SECTION_CHOICES, default='other')
    status          = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')

    # the main body of the workpaper — what was done, what was found
    description     = models.TextField(blank=True)

    # who prepared and who reviewed
    prepared_by     = models.ForeignKey(
                        AuditUser,
                        on_delete=models.SET_NULL,
                        null=True,
                        related_name='workpapers_prepared'
                      )
    reviewed_by     = models.ForeignKey(
                        AuditUser,
                        on_delete=models.SET_NULL,
                        null=True, blank=True,
                        related_name='workpapers_reviewed'
                      )

    # dates
    prepared_date   = models.DateField(auto_now_add=True)
    reviewed_date   = models.DateField(null=True, blank=True)

    # review comments from the senior/partner
    review_comments = models.TextField(blank=True)

    created_at      = models.DateTimeField(auto_now_add=True)
    updated_at      = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['reference']    # order by reference number

    def __str__(self):
        return f"{self.reference} — {self.title}"


# ============================================================
# WorkpaperFile Model
# File attachments on a workpaper
# e.g. scanned documents, Excel schedules, bank statements
# A workpaper can have multiple file attachments
# ============================================================
class WorkpaperFile(models.Model):
    workpaper   = models.ForeignKey(
                    Workpaper,
                    on_delete=models.CASCADE,
                    related_name='files'
                  )
    file        = models.FileField(upload_to='workpapers/')  # saved to media/workpapers/
    filename    = models.CharField(max_length=255, blank=True)  # display name
    uploaded_by = models.ForeignKey(
                    AuditUser,
                    on_delete=models.SET_NULL,
                    null=True
                  )
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.filename or self.file.name