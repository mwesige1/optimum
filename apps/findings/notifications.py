# ============================================================
# notifications.py
# Helper functions to create in-app notifications
# ============================================================

def notify_finding_response(finding):
    from apps.findings.models import Notification
    from apps.accounts.models import AuditUser

    recipients = set()

    # notify the auditor who raised the finding
    if finding.raised_by:
        recipients.add(finding.raised_by)

    # also notify the lead auditor on the engagement
    if finding.engagement.lead_auditor:
        recipients.add(finding.engagement.lead_auditor)

    # fallback — if no one assigned, notify all partners
    if not recipients:
        partners = AuditUser.objects.filter(role='partner', is_active=True)
        recipients.update(partners)

    for recipient in recipients:
        Notification.objects.create(
            recipient         = recipient,
            notification_type = 'finding_response',
            message           = (
                f"{finding.engagement.client.name} has responded "
                f"to finding: \"{finding.title}\""
            ),
            link = f'/findings/{finding.pk}/',
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

def notify_client_pending_approval(client_user):
    from apps.accounts.models import AuditUser
    from apps.findings.models import Notification

    partners = AuditUser.objects.filter(role='partner', is_active=True)

    for partner in partners:
        Notification.objects.create(
            recipient=partner,
            notification_type='client_pending_approval',
            message=f"New client '{client_user.company_name}' has registered and is pending your approval.",
            link='/clients/pending/',  # ← correct URL
        )