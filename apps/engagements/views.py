from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Engagement, EngagementMember
from .forms import EngagementForm
from apps.accounts.models import AuditUser
from apps.accounts.permissions import (
    role_required,
    ENGAGEMENT_VIEW_ROLES,
    ENGAGEMENT_CREATE_ROLES,
    ENGAGEMENT_EDIT_ROLES,
    ENGAGEMENT_DELETE_ROLES,
)


# ============================================================
# Engagement List View
# All roles can see engagements but filtered by their access
# ============================================================
@login_required
def engagement_list(request):
    user = request.user

    # role based filtering
    if user.role in ['partner', 'qc']:
        # sees all engagements firm wide
        engagements = Engagement.objects.all()
    elif user.role == 'manager':
        # sees engagements they lead or are assigned to
        engagements = Engagement.objects.filter(
            lead_auditor=user
        ) | Engagement.objects.filter(
            team_members=user
        )
        engagements = engagements.distinct()
    else:
        # seniors staff trainees IT auditors
        # only see their assigned engagements
        engagements = Engagement.objects.filter(
            team_members=user
        ) | Engagement.objects.filter(
            lead_auditor=user
        )
        engagements = engagements.distinct()

    engagements = engagements.select_related('client', 'lead_auditor')

    # filter by status
    status = request.GET.get('status', '')
    if status:
        engagements = engagements.filter(status=status)

    # search by name or client
    search = request.GET.get('search', '')
    if search:
        engagements = engagements.filter(
            name__icontains=search
        ) | engagements.filter(
            client__name__icontains=search
        )
        engagements = engagements.distinct()

    # stats — based on what the user can see
    total      = engagements.count()
    planning   = engagements.filter(status='planning').count()
    fieldwork  = engagements.filter(status='fieldwork').count()
    reporting  = engagements.filter(status='reporting').count()
    complete   = engagements.filter(status='complete').count()

    # calculate progress for each engagement
    engagement_data = []
    for eng in engagements:
        total_wp  = eng.workpapers.count()
        signed_wp = eng.workpapers.filter(status='signed_off').count()
        progress  = int((signed_wp / total_wp) * 100) if total_wp > 0 else 0
        findings_count = eng.findings.filter(
            status__in=['open', 'in_progress']
        ).count()
        engagement_data.append({
            'engagement':     eng,
            'progress':       progress,
            'total_wp':       total_wp,
            'signed_wp':      signed_wp,
            'findings_count': findings_count,
        })

    return render(request, 'engagements/list.html', {
        'engagement_data': engagement_data,
        'status':          status,
        'search':          search,
        'status_choices':  Engagement.STATUS_CHOICES,
        'total':           total,
        'planning':        planning,
        'fieldwork':       fieldwork,
        'reporting':       reporting,
        'complete':        complete,
        'can_create':      user.role in ENGAGEMENT_CREATE_ROLES,
    })


# ============================================================
# Engagement Detail View
# ============================================================
@login_required
def engagement_detail(request, pk):
    engagement = get_object_or_404(
        Engagement.objects.select_related('client', 'lead_auditor'),
        pk=pk
    )

    # check access — seniors and staff can only see
    # engagements they are assigned to
    user = request.user
    if user.role not in ['partner', 'qc']:
        is_assigned = EngagementMember.objects.filter(
            engagement=engagement, user=user
        ).exists()
        is_lead = engagement.lead_auditor == user
        if not is_assigned and not is_lead:
            messages.error(
                request,
                'You do not have access to this engagement.'
            )
            return redirect('engagements:list')

    members = EngagementMember.objects.filter(
        engagement=engagement
    ).select_related('user')

    # progress
    total_wp  = engagement.workpapers.count()
    signed_wp = engagement.workpapers.filter(
        status='signed_off'
    ).count()
    progress  = int((signed_wp / total_wp) * 100) if total_wp > 0 else 0

    # findings summary
    total_findings  = engagement.findings.count()
    open_findings   = engagement.findings.filter(
        status__in=['open', 'in_progress']
    ).count()
    high_findings   = engagement.findings.filter(
        risk_level='high',
        status__in=['open', 'in_progress']
    ).count()

    # workpapers by status
    draft_wp    = engagement.workpapers.filter(status='draft').count()
    review_wp   = engagement.workpapers.filter(status='in_review').count()
    reviewed_wp = engagement.workpapers.filter(status='reviewed').count()

    # risk matrix status
    try:
        risk_matrix   = engagement.risk_matrix
        has_risk      = True
        risk_approved = risk_matrix.is_approved
        overall_risk  = risk_matrix.overall_risk
    except Exception:
        has_risk      = False
        risk_approved = False
        overall_risk  = None

    return render(request, 'engagements/detail.html', {
        'engagement':    engagement,
        'members':       members,
        'progress':      progress,
        'total_wp':      total_wp,
        'signed_wp':     signed_wp,
        'draft_wp':      draft_wp,
        'review_wp':     review_wp,
        'reviewed_wp':   reviewed_wp,
        'total_findings': total_findings,
        'open_findings':  open_findings,
        'high_findings':  high_findings,
        'has_risk':       has_risk,
        'risk_approved':  risk_approved,
        'overall_risk':   overall_risk,
        'can_edit':       user.role in ENGAGEMENT_EDIT_ROLES,
        'can_delete':     user.role in ENGAGEMENT_DELETE_ROLES,
    })


# ============================================================
# Create Engagement View
# Partners and Managers only
# ============================================================
@login_required
@role_required(ENGAGEMENT_CREATE_ROLES)
def engagement_create(request):
    form = EngagementForm(user=request.user)

    if request.method == 'POST':
        form = EngagementForm(request.POST, user=request.user)
        if form.is_valid():
            engagement             = form.save(commit=False)
            engagement.created_by  = request.user
            engagement.save()
            messages.success(
                request,
                f'Engagement "{engagement.name}" created successfully.'
            )
            return redirect('engagements:detail', pk=engagement.pk)

    return render(request, 'engagements/form.html', {
        'form':  form,
        'title': 'New Engagement',
    })


# ============================================================
# Edit Engagement View
# Partners and Managers only
# ============================================================
@login_required
@role_required(ENGAGEMENT_EDIT_ROLES)
def engagement_edit(request, pk):
    engagement = get_object_or_404(Engagement, pk=pk)
    form       = EngagementForm(instance=engagement, user=request.user)

    if request.method == 'POST':
        form = EngagementForm(
            request.POST,
            instance=engagement,
            user=request.user
        )
        if form.is_valid():
            form.save()
            messages.success(
                request,
                f'Engagement "{engagement.name}" updated.'
            )
            return redirect('engagements:detail', pk=pk)

    return render(request, 'engagements/form.html', {
        'form':       form,
        'title':      'Edit Engagement',
        'engagement': engagement,
    })


# ============================================================
# Delete Engagement View
# Partners only
# ============================================================
@login_required
@role_required(ENGAGEMENT_DELETE_ROLES)
def engagement_delete(request, pk):
    engagement = get_object_or_404(Engagement, pk=pk)

    if request.method == 'POST':
        name = engagement.name
        engagement.delete()
        messages.success(request, f'Engagement "{name}" deleted.')
        return redirect('engagements:list')

    return render(request, 'engagements/confirm_delete.html', {
        'engagement': engagement
    })


# ============================================================
# Add Team Member View
# ============================================================
@login_required
@role_required(ENGAGEMENT_EDIT_ROLES)
def add_member(request, pk):
    engagement = get_object_or_404(Engagement, pk=pk)

    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        role    = request.POST.get('role', 'staff')
        try:
            user = AuditUser.objects.get(id=user_id)
            EngagementMember.objects.get_or_create(
                engagement=engagement,
                user=user,
                defaults={'role': role}
            )
            messages.success(
                request,
                f'{user.get_full_name()} added to engagement.'
            )
        except AuditUser.DoesNotExist:
            messages.error(request, 'User not found.')

    return redirect('engagements:detail', pk=pk)


# ============================================================
# Remove Team Member View
# ============================================================
@login_required
@role_required(ENGAGEMENT_EDIT_ROLES)
def remove_member(request, pk, user_id):
    engagement = get_object_or_404(Engagement, pk=pk)
    EngagementMember.objects.filter(
        engagement=engagement,
        user_id=user_id
    ).delete()
    messages.success(request, 'Team member removed.')
    return redirect('engagements:detail', pk=pk)