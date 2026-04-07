from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings


# ============================================================
# Send Account Approved Email
# Called when a Partner approves a client registration
# ============================================================
def send_approval_email(client_user):
    subject = 'Your Optim Audit Client Portal Account Has Been Approved'

    # plain text version
    plain_message = f"""
Dear {client_user.contact_person},

Your registration for {client_user.company_name} on the Optim Audit 
Client Portal has been approved.

You can now log in to your portal using the following details:

Email:    {client_user.email}
Portal:   http://127.0.0.1:8000/client/login/

Once logged in you will be able to:
- View your audit engagements
- Review findings raised during your audit
- Submit management responses to findings
- Track the progress of your audit

If you have any questions please contact your audit team directly.

Best regards,
The Optim Audit Team
    """

    # send the email
    try:
        send_mail(
            subject        = subject,
            message        = plain_message,
            from_email     = settings.DEFAULT_FROM_EMAIL,
            recipient_list = [client_user.email],
            fail_silently  = False,
        )
        return True
    except Exception as e:
        # log the error but don't crash the approval process
        print(f"Email send error: {e}")
        return False


# ============================================================
# Send New Finding Notification Email
# Called when a new finding is raised against a client
# ============================================================
def send_new_finding_email(client_user, finding):
    subject = f'New Audit Finding Requires Your Response — {finding.title}'

    plain_message = f"""
Dear {client_user.contact_person},

The audit team has raised a new finding for {client_user.company_name} 
that requires your management response.

Finding:    {finding.title}
Risk Level: {finding.get_risk_level_display()}
Due Date:   {finding.due_date.strftime('%d %B %Y') if finding.due_date else 'Not set'}

Please log in to your portal to review the finding and submit your response:

Portal: http://127.0.0.1:8000/client/login/

Responding promptly to audit findings is important as delays may 
affect the completion of your audit.

Best regards,
The Optim Audit Team
    """

    try:
        send_mail(
            subject        = subject,
            message        = plain_message,
            from_email     = settings.DEFAULT_FROM_EMAIL,
            recipient_list = [client_user.email],
            fail_silently  = False,
        )
        return True
    except Exception as e:
        print(f"Email send error: {e}")
        return False


# ============================================================
# Send Overdue Finding Reminder Email
# Called when a finding passes its due date without a response
# ============================================================
def send_overdue_finding_email(client_user, finding):
    subject = f'OVERDUE: Audit Finding Response Required — {finding.title}'

    plain_message = f"""
Dear {client_user.contact_person},

This is a reminder that the following audit finding is now overdue 
and still requires your management response:

Finding:    {finding.title}
Risk Level: {finding.get_risk_level_display()}
Due Date:   {finding.due_date.strftime('%d %B %Y') if finding.due_date else 'Not set'}

Please log in immediately to submit your response:

Portal: http://127.0.0.1:8000/client/login/

If you have any questions please contact your audit team directly.

Best regards,
The Optim Audit Team
    """

    try:
        send_mail(
            subject        = subject,
            message        = plain_message,
            from_email     = settings.DEFAULT_FROM_EMAIL,
            recipient_list = [client_user.email],
            fail_silently  = False,
        )
        return True
    except Exception as e:
        print(f"Email send error: {e}")
        return False
    

# ============================================================
# Send Rejection Email
# Called when a Partner rejects a client registration
# ============================================================
def send_rejection_email(client_user, reason):
    subject = 'Your Optim Audit Registration Was Not Approved'

    plain_message = f"""
Dear {client_user.contact_person},

Thank you for registering on the Optim Audit Client Portal.

After reviewing your registration for {client_user.company_name},
we are unable to approve your account at this time.

Reason: {reason}

If you believe this is an error or would like more information,
please contact our audit team directly.

Best regards,
The Optim Audit Team
    """

    try:
        send_mail(
            subject        = subject,
            message        = plain_message,
            from_email     = settings.DEFAULT_FROM_EMAIL,
            recipient_list = [client_user.email],
            fail_silently  = False,
        )
        return True
    except Exception as e:
        print(f"Email send error: {e}")
        return False
    

# ============================================================
# Send Finding Resolved Email
# Called when auditor marks a finding as resolved
# ============================================================
def send_finding_resolved_email(client_user, finding):
    subject = f'Audit Finding Resolved — {finding.title}'

    plain_message = f"""
Dear {client_user.contact_person},

We are pleased to inform you that the following audit finding
for {client_user.company_name} has been marked as resolved.

Finding:    {finding.title}
Risk Level: {finding.get_risk_level_display()}
Resolved:   {finding.engagement.name}

Thank you for your cooperation in addressing this finding.

Best regards,
The Optim Audit Team
    """

    try:
        from django.core.mail import send_mail
        from django.conf import settings
        send_mail(
            subject        = subject,
            message        = plain_message,
            from_email     = settings.DEFAULT_FROM_EMAIL,
            recipient_list = [client_user.email],
            fail_silently  = False,
        )
        return True
    except Exception as e:
        print(f"Email send error: {e}")
        return False