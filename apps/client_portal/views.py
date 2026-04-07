from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.hashers import check_password
from django.utils import timezone
from functools import wraps
from .models import ClientUser
from .forms import (
    ClientRegistrationForm, ClientLoginForm,
    ClientProfileForm, ClientChangePasswordForm
)
from apps.findings.models import Finding
from apps.engagements.models import Engagement


# ============================================================
# Client Authentication Helpers
# We use a simple session-based approach for client users
# Completely separate from the audit firm's auth system
# ============================================================

def client_login_session(request, client_user):
    # store the client user's id in the session
    request.session['client_user_id'] = client_user.id
    request.session['is_client']      = True


def client_logout_session(request):
    # clear the client session
    request.session.pop('client_user_id', None)
    request.session.pop('is_client', None)


def get_client_user(request):
    # retrieve the logged-in client user from the session
    client_user_id = request.session.get('client_user_id')
    if client_user_id:
        try:
            return ClientUser.objects.get(
                id=client_user_id,
                is_active=True,
                is_approved=True
            )
        except ClientUser.DoesNotExist:
            return None
    return None


def client_required(view_func):
    # decorator — ensures only approved logged-in client users
    # can access client portal views
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        client_user = get_client_user(request)
        if not client_user:
            messages.error(request, 'Please log in to access the client portal.')
            return redirect('client_portal:login')
        request.client_user = client_user
        return view_func(request, *args, **kwargs)
    return wrapper


# ============================================================
# Client Registration View
# Anyone can register — Partner approves before they can log in
# ============================================================
def client_register(request):
    if get_client_user(request):
        return redirect('client_portal:dashboard')

    form = ClientRegistrationForm()

    if request.method == 'POST':
        form = ClientRegistrationForm(request.POST)
        if form.is_valid():
            client_user = form.save()

            # automatically create an AuditClient record
            from apps.clients.models import AuditClient
            audit_client = AuditClient.objects.create(
                name           = client_user.company_name,
                contact_person = client_user.contact_person,
                contact_email  = client_user.email,
                contact_phone  = client_user.phone,
                status         = 'pending',
            )

            # link portal user to audit client
            client_user.client = audit_client
            client_user.save()

            messages.success(
                request,
                'Registration successful! Your account is pending '
                'approval by the audit firm.'
            )
            return redirect('client_portal:login')

        else:
            # form is invalid — errors show in template
            messages.error(
                request,
                'Please correct the errors below.'
            )

    return render(request, 'client_portal/register.html', {
        'form': form
    })

# ============================================================
# Client Login View
# ============================================================
def client_login(request):
    # if already logged in go to dashboard
    if get_client_user(request):
        return redirect('client_portal:dashboard')

    form = ClientLoginForm()

    if request.method == 'POST':
        form = ClientLoginForm(request.POST)
        if form.is_valid():
            email    = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')

            try:
                client_user = ClientUser.objects.get(email=email)

                if not client_user.check_password(password):
                    messages.error(request, 'Invalid email or password.')

                elif not client_user.is_approved:
                    messages.warning(
                        request,
                        'Your account is pending approval by the audit firm. '
                        'Please check back later or contact the audit team.'
                    )

                elif not client_user.is_active:
                    messages.error(
                        request,
                        'Your account has been deactivated. '
                        'Please contact the audit firm.'
                    )

                else:
                    # successful login
                    client_login_session(request, client_user)
                    messages.success(
                        request,
                        f'Welcome back, {client_user.contact_person}!'
                    )
                    return redirect('client_portal:dashboard')

            except ClientUser.DoesNotExist:
                messages.error(request, 'Invalid email or password.')

    return render(request, 'client_portal/login.html', {
        'form': form
    })


# ============================================================
# Client Logout View
# ============================================================
def client_logout(request):
    client_logout_session(request)
    messages.info(request, 'You have been logged out.')
    return redirect('client_portal:login')


# ============================================================
# Client Dashboard View
# ============================================================
@client_required
def client_dashboard(request):
    client_user = request.client_user
    client      = client_user.client

    if not client:
        return render(request, 'client_portal/pending.html', {
            'client_user': client_user
        })

    # get all engagements for this client
    engagements = Engagement.objects.filter(
        client=client
    ).select_related('lead_auditor')

    # get all findings for this client
    findings = Finding.objects.filter(
        engagement__client=client
    )

    # finding statistics
    open_findings     = findings.filter(
        status__in=['open', 'in_progress']
    ).count()
    resolved_findings = findings.filter(status='resolved').count()
    high_findings     = findings.filter(
        risk_level='high',
        status__in=['open', 'in_progress']
    ).count()

    # findings awaiting management response
    awaiting_response = []
    for f in findings.filter(status__in=['open', 'in_progress']):
        try:
            f.management_response
        except:
            awaiting_response.append(f)

    # recent findings — last 5
    recent_findings = findings.select_related(
        'engagement'
    ).order_by('-created_at')[:5]

    return render(request, 'client_portal/dashboard.html', {
        'client_user':      client_user,
        'client':           client,
        'engagements':      engagements,
        'open_findings':    open_findings,
        'resolved_findings': resolved_findings,
        'high_findings':    high_findings,
        'awaiting_response': len(awaiting_response),
        'recent_findings':  recent_findings,
        'total_engagements': engagements.count(),
    })


# ============================================================
# Client Findings View
# Client sees all findings raised against their company
# ============================================================
@client_required
def client_findings(request):
    client_user = request.client_user
    client      = client_user.client

    if not client:
        return redirect('client_portal:dashboard')

    findings = Finding.objects.filter(
        engagement__client=client
    ).select_related('engagement', 'raised_by')

    # filter by status
    status = request.GET.get('status', '')
    if status:
        findings = findings.filter(status=status)

    # filter by risk
    risk = request.GET.get('risk', '')
    if risk:
        findings = findings.filter(risk_level=risk)

    return render(request, 'client_portal/findings.html', {
        'client_user':    client_user,
        'findings':       findings,
        'status':         status,
        'risk':           risk,
        'status_choices': Finding.STATUS_CHOICES,
        'risk_choices':   Finding.RISK_CHOICES,
    })


# ============================================================
# Client Finding Detail + Management Response
# ============================================================
@client_required
def client_finding_detail(request, pk):
    client_user = request.client_user
    client      = client_user.client

    if not client:
        return redirect('client_portal:dashboard')

    finding = get_object_or_404(
        Finding,
        pk=pk,
        engagement__client=client
    )

    try:
        mgmt_response = finding.management_response
    except:
        mgmt_response = None

    if request.method == 'POST':
        from apps.findings.models import ManagementResponse
        from apps.findings.forms import ManagementResponseForm

        if mgmt_response:
            form = ManagementResponseForm(request.POST, instance=mgmt_response)
        else:
            form = ManagementResponseForm(request.POST)

        if form.is_valid():
            response         = form.save(commit=False)
            response.finding = finding
            if not response.responded_by:
                response.responded_by = (
                    f"{client_user.contact_person} — "
                    f"{client_user.company_name}"
                )
            response.save()

            # auto-update finding status
            if finding.status == 'open':
                finding.status = 'in_progress'
                finding.save()

            # notify the auditor
            from apps.findings.notifications import notify_finding_response
            notify_finding_response(finding)

            messages.success(request, 'Your response has been submitted.')
            return redirect('client_portal:finding_detail', pk=pk)

    else:
        from apps.findings.forms import ManagementResponseForm
        if mgmt_response:
            form = ManagementResponseForm(instance=mgmt_response)
        else:
            form = ManagementResponseForm(initial={
                'responded_by': (
                    f"{client_user.contact_person} — "
                    f"{client_user.company_name}"
                )
            })

    return render(request, 'client_portal/finding_detail.html', {
        'client_user':   client_user,
        'finding':       finding,
        'mgmt_response': mgmt_response,
        'form':          form,
    })
# ============================================================
# Client Engagements View
# ============================================================
@client_required
def client_engagements(request):
    client_user = request.client_user
    client      = client_user.client

    if not client:
        return redirect('client_portal:dashboard')

    engagements = Engagement.objects.filter(
        client=client
    ).select_related('lead_auditor', 'client')

    return render(request, 'client_portal/engagements.html', {
        'client_user': client_user,
        'engagements': engagements,
    })


# ============================================================
# Client Profile View
# ============================================================
@client_required
def client_profile(request):
    client_user = request.client_user
    form = ClientProfileForm(instance=client_user)

    if request.method == 'POST':
        form = ClientProfileForm(request.POST, instance=client_user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully.')
            return redirect('client_portal:profile')

    return render(request, 'client_portal/profile.html', {
        'client_user': client_user,
        'form':        form,
    })


# ============================================================
# Client Change Password View
# ============================================================
@client_required
def client_change_password(request):
    client_user = request.client_user
    form = ClientChangePasswordForm(user=client_user)

    if request.method == 'POST':
        form = ClientChangePasswordForm(
            user=client_user,
            data=request.POST
        )
        if form.is_valid():
            client_user.set_password(form.cleaned_data['new_password1'])
            client_user.save()
            # update session so user stays logged in
            client_login_session(request, client_user)
            messages.success(request, 'Password changed successfully.')
            return redirect('client_portal:change_password')

    return render(request, 'client_portal/change_password.html', {
        'client_user': client_user,
        'form':        form,
    })




# ============================================================
# Partner — Pending Approvals View
# Only accessible by audit firm staff (Partners)
# ============================================================
from django.contrib.auth.decorators import login_required
@login_required
def pending_approvals(request):
    if request.user.role != 'partner':
        messages.error(request, 'Only Partners can approve client registrations.')
        return redirect('core:dashboard')

    from apps.clients.models import AuditClient
    pending  = ClientUser.objects.filter(is_approved=False, is_active=True)
    approved = ClientUser.objects.filter(is_approved=True, is_active=True)
    clients  = AuditClient.objects.all()

    return render(request, 'client_portal/pending_approvals.html', {
        'pending':  pending,
        'approved': approved,
        'clients':  clients,
    })


@login_required
def approve_client(request, client_user_id):
    if request.user.role != 'partner':
        messages.error(request, 'Only Partners can approve clients.')
        return redirect('core:dashboard')

    client_user = get_object_or_404(ClientUser, id=client_user_id)

    if request.method == 'POST':
        client_id = request.POST.get('client_id')
        if client_id:
            from apps.clients.models import AuditClient
            try:
                audit_client            = AuditClient.objects.get(id=client_id)
                client_user.client      = audit_client
                # automatically set client status to active
                audit_client.status     = 'active'
                audit_client.save()
            except AuditClient.DoesNotExist:
                pass

        client_user.is_approved   = True
        client_user.approved_at   = timezone.now()
        client_user.approval_note = request.POST.get('note', '')
        client_user.save()

        # send approval email
        from .emails import send_approval_email
        email_sent = send_approval_email(client_user)

        if email_sent:
            messages.success(
                request,
                f'{client_user.company_name} approved and '
                f'notification sent to {client_user.email}.'
            )
        else:
            messages.warning(
                request,
                f'{client_user.company_name} approved but '
                f'email could not be sent.'
            )

    return redirect('client_portal:pending_approvals')


@login_required
def reject_client(request, client_user_id):
    if request.user.role != 'partner':
        messages.error(request, 'Only Partners can reject clients.')
        return redirect('core:dashboard')

    client_user = get_object_or_404(ClientUser, id=client_user_id)

    if request.method == 'POST':
        client_user.is_active = False
        client_user.save()
        messages.success(
            request,
            f'{client_user.company_name} registration rejected.'
        )

    return redirect('client_portal:pending_approvals')