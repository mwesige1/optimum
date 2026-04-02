from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from .models import Finding, ManagementResponse
from .forms import FindingForm, ManagementResponseForm
from apps.engagements.models import Engagement


# ============================================================
# Findings List View
# ============================================================
@login_required
def finding_list(request):
    findings = Finding.objects.select_related(
        'engagement', 'raised_by', 'assigned_to'
    )

    # filter by risk level
    risk = request.GET.get('risk', '')
    if risk:
        findings = findings.filter(risk_level=risk)

    # filter by status
    status = request.GET.get('status', '')
    if status:
        findings = findings.filter(status=status)

    # filter by engagement
    engagement_id = request.GET.get('engagement', '')
    if engagement_id:
        findings = findings.filter(engagement_id=engagement_id)

    # search by title
    search = request.GET.get('search', '')
    if search:
        findings = findings.filter(title__icontains=search)

    # count by risk level for the summary bar
    high_count   = findings.filter(risk_level='high').count()
    medium_count = findings.filter(risk_level='medium').count()
    low_count    = findings.filter(risk_level='low').count()

    engagements  = Engagement.objects.all()

    return render(request, 'findings/list.html', {
        'findings':      findings,
        'engagements':   engagements,
        'risk':          risk,
        'status':        status,
        'engagement_id': engagement_id,
        'search':        search,
        'high_count':    high_count,
        'medium_count':  medium_count,
        'low_count':     low_count,
        'risk_choices':  Finding.RISK_CHOICES,
        'status_choices': Finding.STATUS_CHOICES,
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

    # get existing management response if any
    try:
        mgmt_response = finding.management_response
    except ManagementResponse.DoesNotExist:
        mgmt_response = None

    response_form = ManagementResponseForm()

    return render(request, 'findings/detail.html', {
        'finding':       finding,
        'mgmt_response': mgmt_response,
        'response_form': response_form,
        'is_overdue':    finding.is_overdue(),
    })


# ============================================================
# Create Finding View
# ============================================================
@login_required
def finding_create(request):
    engagement_id = request.GET.get('engagement', '')
    form = FindingForm(user=request.user)

    if request.method == 'POST':
        form = FindingForm(request.POST, user=request.user)
        if form.is_valid():
            finding           = form.save(commit=False)
            finding.raised_by = request.user

            # link to engagement
            eng_id = request.POST.get('engagement_id') or engagement_id
            if eng_id:
                finding.engagement = get_object_or_404(Engagement, pk=eng_id)

            finding.save()

            # notify the client by email if they have an approved portal account
            try:
                client_user = finding.engagement.client.portal_user
                if client_user and client_user.is_approved:
                    from apps.client_portal.emails import send_new_finding_email
                    send_new_finding_email(client_user, finding)
            except Exception:
                # no portal user linked to this client — skip silently
                pass

            messages.success(
                request,
                f'Finding "{finding.title}" raised successfully.'
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
    form = FindingForm(instance=finding, user=request.user)

    if request.method == 'POST':
        form = FindingForm(request.POST, instance=finding, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, f'Finding "{finding.title}" updated.')
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
# ============================================================
@login_required
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
# Quick action to mark a finding as resolved
# ============================================================
@login_required
def finding_resolve(request, pk):
    finding = get_object_or_404(Finding, pk=pk)
    if request.method == 'POST':
        finding.status = 'resolved'
        finding.save()
        messages.success(request, f'Finding "{finding.title}" marked as resolved.')
    return redirect('findings:detail', pk=pk)


# ============================================================
# Add Management Response View
# Records the client's official response to a finding
# ============================================================
@login_required
def add_management_response(request, pk):
    finding = get_object_or_404(Finding, pk=pk)

    if request.method == 'POST':
        # check if response already exists — update it if so
        try:
            existing = finding.management_response
            form = ManagementResponseForm(request.POST, instance=existing)
        except ManagementResponse.DoesNotExist:
            form = ManagementResponseForm(request.POST)

        if form.is_valid():
            response = form.save(commit=False)
            response.finding = finding
            response.save()
            messages.success(request, 'Management response saved.')

    return redirect('findings:detail', pk=pk)