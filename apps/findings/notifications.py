# ============================================================
# notifications.py
# Helper functions to create in-app notifications
# ============================================================

def notify_finding_response(finding):
    """
    Creates a notification for the auditor who raised
    the finding when the client submits a response.
    """
    from .models import Notification

    if not finding.raised_by:
        return

    Notification.objects.create(
        recipient         = finding.raised_by,
        notification_type = 'finding_response',
        message           = (
            f'{finding.engagement.client.name} has responded '
            f'to finding: "{finding.title}"'
        ),
        link              = f'/findings/{finding.pk}/',
    )


def notify_finding_overdue(finding):
    """
    Creates a notification when a finding passes its due date.
    """
    from .models import Notification
    from apps.accounts.models import AuditUser

    # notify the lead auditor on the engagement
    lead = finding.engagement.lead_auditor
    if lead:
        Notification.objects.create(
            recipient         = lead,
            notification_type = 'finding_overdue',
            message           = (
                f'Finding "{finding.title}" is overdue — '
                f'no response from client.'
            ),
            link              = f'/findings/{finding.pk}/',
        )