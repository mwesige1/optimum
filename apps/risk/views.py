from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import RiskArea, RiskMatrix
from .forms import RiskAreaForm, RiskMatrixForm
from apps.engagements.models import Engagement


# ============================================================
# Risk Matrix View
# Shows the full risk matrix for one engagement
# Creates the matrix if it doesn't exist yet
# ============================================================
@login_required
def risk_matrix(request, engagement_id):
    engagement = get_object_or_404(Engagement, pk=engagement_id)

    # get or create the risk matrix for this engagement
    matrix, created = RiskMatrix.objects.get_or_create(
        engagement=engagement,
        defaults={
            'prepared_by': request.user,
            'overall_risk': 'moderate',
        }
    )

    # get all risk areas for this engagement
    risk_areas = RiskArea.objects.filter(
        engagement=engagement
    ).order_by('area')

    # calculate summary stats
    high_count   = risk_areas.filter(overall_risk='high').count()
    medium_count = risk_areas.filter(overall_risk='medium').count()
    low_count    = risk_areas.filter(overall_risk='low').count()

    # overall risk score — average of all areas
    if risk_areas.exists():
        total_score = sum(area.combined_risk_score for area in risk_areas)
        avg_score   = round(total_score / risk_areas.count())
    else:
        avg_score = 0

    matrix_form = RiskMatrixForm(instance=matrix)

    if request.method == 'POST' and 'update_matrix' in request.POST:
        matrix_form = RiskMatrixForm(request.POST, instance=matrix)
        if matrix_form.is_valid():
            matrix_form.save()
            messages.success(request, 'Risk matrix updated successfully.')
            return redirect('risk:matrix', engagement_id=engagement_id)

    return render(request, 'risk/matrix.html', {
        'engagement':   engagement,
        'matrix':       matrix,
        'matrix_form':  matrix_form,
        'risk_areas':   risk_areas,
        'high_count':   high_count,
        'medium_count': medium_count,
        'low_count':    low_count,
        'avg_score':    avg_score,
    })


# ============================================================
# Add Risk Area View
# ============================================================
@login_required
def add_risk_area(request, engagement_id):
    engagement = get_object_or_404(Engagement, pk=engagement_id)
    form       = RiskAreaForm()

    if request.method == 'POST':
        form = RiskAreaForm(request.POST)
        if form.is_valid():
            risk_area              = form.save(commit=False)
            risk_area.engagement   = engagement
            risk_area.assessed_by  = request.user
            risk_area.save()
            messages.success(
                request,
                f'{risk_area.get_area_name()} risk area added.'
            )
            return redirect('risk:matrix', engagement_id=engagement_id)

    return render(request, 'risk/area_form.html', {
        'form':       form,
        'engagement': engagement,
        'title':      'Add Risk Area',
    })


# ============================================================
# Edit Risk Area View
# ============================================================
@login_required
def edit_risk_area(request, pk):
    risk_area  = get_object_or_404(RiskArea, pk=pk)
    engagement = risk_area.engagement
    form       = RiskAreaForm(instance=risk_area)

    if request.method == 'POST':
        form = RiskAreaForm(request.POST, instance=risk_area)
        if form.is_valid():
            form.save()
            messages.success(
                request,
                f'{risk_area.get_area_name()} updated.'
            )
            return redirect('risk:matrix', engagement_id=engagement.pk)

    return render(request, 'risk/area_form.html', {
        'form':       form,
        'engagement': engagement,
        'risk_area':  risk_area,
        'title':      'Edit Risk Area',
    })


# ============================================================
# Delete Risk Area View
# ============================================================
@login_required
def delete_risk_area(request, pk):
    risk_area  = get_object_or_404(RiskArea, pk=pk)
    engagement = risk_area.engagement

    if request.method == 'POST':
        name = risk_area.get_area_name()
        risk_area.delete()
        messages.success(request, f'{name} risk area deleted.')
        return redirect('risk:matrix', engagement_id=engagement.pk)

    return render(request, 'risk/confirm_delete.html', {
        'risk_area':  risk_area,
        'engagement': engagement,
    })


# ============================================================
# Approve Risk Matrix View
# Only partners and managers can approve the risk matrix
# ============================================================
@login_required
def approve_matrix(request, engagement_id):
    engagement = get_object_or_404(Engagement, pk=engagement_id)
    matrix     = get_object_or_404(RiskMatrix, engagement=engagement)

    if request.user.role not in ['partner', 'manager']:
        messages.error(
            request,
            'Only Partners and Managers can approve the risk matrix.'
        )
        return redirect('risk:matrix', engagement_id=engagement_id)

    if request.method == 'POST':
        matrix.is_approved  = True
        matrix.approved_by  = request.user
        matrix.save()
        messages.success(
            request,
            'Risk matrix approved successfully.'
        )

    return redirect('risk:matrix', engagement_id=engagement_id)