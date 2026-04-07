from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from .models import Finding, ManagementResponse, Notification
from .forms import FindingForm, ManagementResponseForm
from apps.engagements.models import Engagement
from apps.accounts.permissions import role_required


# allowed roles
FINDING_VIEW_ROLES   = ['partner', 'manager', 'senior',
                         'staff', 'it_auditor', 'qc', 'trainee']
FINDING_RESOLVE_ROLES = ['partner', 'manager', 'senior']
FINDING_DELETE_ROLES  = ['partner']


# ============================================================
# Findings List View
# ============================================================
@login_required
def finding_list(request):
    user = request.user

    # role based filtering
    if user.role in ['partner', 'qc']:
        findings = Finding.objects.all()
    elif user.role == 'manager':
        engagements = Engagement.objects.filter(
            lead_auditor=user
        ) | Engagement.objects.filter(
            team_members=user
        )
        findings = Finding.objects.filter(
            engagement__in=engagements.distinct()
        )
    else:
        # seniors and staff see findings on their engagements
        from apps.engagements.models import EngagementMember
        eng_ids = EngagementMember.objects.filter(
            user=user
        ).values_list('engagement_id', flat=True)
        findings = Finding.objects.filter(
            engagement_id__in=eng_ids
        ) | Finding.objects.filter(
            raised_by=user
        ) | Finding.objects.filter(
            assigned_to=user
        )
        findings = findings.distinct()

    findings = findings.select_related(
        'engagement', 'raised_by', 'assigned_to'
    )

    # filters
    risk = request.GET.get('risk', '')
    if risk:
        findings = findings.filter(risk_level=risk)

    status = request.GET.get('status', '')
    if status:
        findings = findings.filter(status=status)

    engagement_id = request.GET.get('engagement', '')
    if engagement_id:
        findings = findings.filter(engagement_id=engagement_id)

    search = request.GET.get('search', '')
    if search:
        findings = findings.filter(title__icontains=search)

    # stats
    total         = findings.count()
    open_count    = findings.filter(
                        status__in=['open', 'in_progress']
                    ).count()
    high_count    = findings.filter(
                        risk_level='high',
                        status__in=['open', 'in_progress']
                    ).count()
    medium_count  = findings.filter(
                        risk_level='medium',
                        status__in=['open', 'in_progress']
                    ).count()
    low_count     = findings.filter(
                        risk_level='low',
                        status__in=['open', 'in_progress']
                    ).count()
    resolved_count = findings.filter(status='resolved').count()
    overdue_count = sum(
        1 for f in findings.filter(
            status__in=['open', 'in_progress']
        ) if f.is_overdue()
    )

    # findings awaiting management response
    awaiting = 0
    for f in findings.filter(status__in=['open', 'in_progress']):
        try:
            f.management_response
        except ManagementResponse.DoesNotExist:
            awaiting += 1

    engagements = Engagement.objects.all()

    return render(request, 'findings/list.html', {
        'findings':        findings,
        'engagements':     engagements,
        'risk':            risk,
        'status':          status,
        'engagement_id':   engagement_id,
        'search':          search,
        'risk_choices':    Finding.RISK_CHOICES,
        'status_choices':  Finding.STATUS_CHOICES,
        'total':           total,
        'open_count':      open_count,
        'high_count':      high_count,
        'medium_count':    medium_count,
        'low_count':       low_count,
        'resolved_count':  resolved_count,
        'overdue_count':   overdue_count,
        'awaiting':        awaiting,
        'can_create':      True,
        'can_delete':      user.role in FINDING_DELETE_ROLES,
    })


# ============================================================
# Finding Detail View
# ============================================================
@login_required
def finding_detail(request, pk):
    finding = get_object_or_404(
        Finding.objects.select_related(
            'engagement', 'raised_by', 'assigned_to'
        ),
        pk=pk
    )

    try:
        mgmt_response = finding.management_response
    except ManagementResponse.DoesNotExist:
        mgmt_response = None

    response_form = ManagementResponseForm()
    user          = request.user
    can_resolve   = user.role in FINDING_RESOLVE_ROLES
    can_delete    = user.role in FINDING_DELETE_ROLES

    # mark related notifications as read
    Notification.objects.filter(
        recipient=user,
        link=f'/findings/{pk}/',
        is_read=False
    ).update(is_read=True)

    return render(request, 'findings/detail.html', {
        'finding':       finding,
        'mgmt_response': mgmt_response,
        'response_form': response_form,
        'is_overdue':    finding.is_overdue(),
        'can_resolve':   can_resolve,
        'can_delete':    can_delete,
    })


# ============================================================
# Create Finding View
# ============================================================
@login_required
def finding_create(request):
    engagement_id = request.GET.get('engagement', '')
    form          = FindingForm(user=request.user)

    if request.method == 'POST':
        form = FindingForm(request.POST, user=request.user)
        if form.is_valid():
            finding           = form.save(commit=False)
            finding.raised_by = request.user

            eng_id = request.POST.get('engagement_id') or engagement_id
            if eng_id:
                finding.engagement = get_object_or_404(
                    Engagement, pk=eng_id
                )

            finding.save()

            # notify client by email if they have a portal account
            try:
                client_user = finding.engagement.client.portal_user
                if client_user and client_user.is_approved:
                    from apps.client_portal.emails import (
                        send_new_finding_email
                    )
                    send_new_finding_email(client_user, finding)
            except Exception:
                pass

            messages.success(
                request,
                f'Finding "{finding.title}" raised. '
                f'Client has been notified.'
            )
            return redirect('findings:detail', pk=finding.pk)

    engagements = Engagement.objects.all()
    return render(request, 'findings/form.html', {
        'form':          form,
        'title':         'Raise New Finding',
        'engagements':   engagements,
        'engagement_id': engagement_id,
    })


# ============================================================
# Edit Finding View
# ============================================================
@login_required
def finding_edit(request, pk):
    finding = get_object_or_404(Finding, pk=pk)
    form    = FindingForm(instance=finding, user=request.user)

    if request.method == 'POST':
        form = FindingForm(
            request.POST,
            instance=finding,
            user=request.user
        )
        if form.is_valid():
            form.save()
            messages.success(
                request,
                f'Finding "{finding.title}" updated.'
            )
            return redirect('findings:detail', pk=pk)

    engagements = Engagement.objects.all()
    return render(request, 'findings/form.html', {
        'form':          form,
        'title':         'Edit Finding',
        'finding':       finding,
        'engagements':   engagements,
        'engagement_id': finding.engagement_id,
    })


# ============================================================
# Delete Finding View
# Partners only
# ============================================================
@login_required
@role_required(FINDING_DELETE_ROLES)
def finding_delete(request, pk):
    finding = get_object_or_404(Finding, pk=pk)

    if request.method == 'POST':
        title = finding.title
        finding.delete()
        messages.success(request, f'Finding "{title}" deleted.')
        return redirect('findings:list')

    return render(request, 'findings/confirm_delete.html', {
        'finding': finding
    })


# ============================================================
# Resolve Finding View
# Seniors and above only
# Sends email to client when resolved
# ============================================================
@login_required
def finding_resolve(request, pk):
    finding = get_object_or_404(Finding, pk=pk)
    user    = request.user

    if user.role not in FINDING_RESOLVE_ROLES:
        messages.error(
            request,
            'Only Senior Auditors and above can resolve findings.'
        )
        return redirect('findings:detail', pk=pk)

    if request.method == 'POST':
        finding.status = 'resolved'
        finding.save()

        # send resolution email to client
        try:
            client_user = finding.engagement.client.portal_user
            if client_user and client_user.is_approved:
                from apps.client_portal.emails import (
                    send_finding_resolved_email
                )
                send_finding_resolved_email(client_user, finding)
        except Exception:
            pass

        messages.success(
            request,
            f'Finding "{finding.title}" resolved. '
            f'Client has been notified.'
        )

    return redirect('findings:detail', pk=pk)


# ============================================================
# Add Management Response View
# ============================================================
@login_required
def add_management_response(request, pk):
    finding = get_object_or_404(Finding, pk=pk)

    if request.method == 'POST':
        try:
            existing = finding.management_response
            form     = ManagementResponseForm(
                           request.POST,
                           instance=existing
                       )
        except ManagementResponse.DoesNotExist:
            form = ManagementResponseForm(request.POST)

        if form.is_valid():
            response         = form.save(commit=False)
            response.finding = finding
            response.save()

            # automatically move finding to In Progress
            if finding.status == 'open':
                finding.status = 'in_progress'
                finding.save()

            # create in-app notification for the auditor
            from .notifications import notify_finding_response
            notify_finding_response(finding)

            messages.success(request, 'Management response saved.')

    return redirect('findings:detail', pk=pk)


# ============================================================
# Notifications View
# Shows all notifications for the logged-in user
# ============================================================
@login_required
def notifications_view(request):
    notifications = Notification.objects.filter(
        recipient=request.user
    )

    # mark all as read
    notifications.filter(is_read=False).update(is_read=True)

    return render(request, 'findings/notifications.html', {
        'notifications': notifications,
    })


# ============================================================
# Get Unread Notification Count (AJAX)
# Used by the topbar bell icon
# ============================================================
@login_required
def unread_notifications_count(request):
    from django.http import JsonResponse
    count = Notification.objects.filter(
        recipient=request.user,
        is_read=False
    ).count()
    return JsonResponse({'count': count})