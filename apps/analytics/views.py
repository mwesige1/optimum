from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import RatioAnalysis, MaterialityCalculation
from .forms import MaterialityForm, RatioAnalysisForm
from apps.engagements.models import Engagement


# ============================================================
# Analytics Dashboard View
# Main analytics page for one engagement
# Shows materiality + all ratio analyses
# ============================================================
@login_required
def analytics_dashboard(request, engagement_id):
    engagement = get_object_or_404(Engagement, pk=engagement_id)

    # get materiality calculation if it exists
    try:
        materiality = engagement.materiality_calc
    except MaterialityCalculation.DoesNotExist:
        materiality = None

    # get all ratio analyses grouped by category
    ratios = RatioAnalysis.objects.filter(
        engagement=engagement
    ).order_by('category', 'ratio_name')

    # group ratios by category for display
    ratios_by_category = {}
    for ratio in ratios:
        cat = ratio.get_category_display()
        if cat not in ratios_by_category:
            ratios_by_category[cat] = []
        ratios_by_category[cat].append(ratio)

    # count flagged items
    followup_count = ratios.filter(requires_followup=True).count()

    return render(request, 'analytics/dashboard.html', {
        'engagement':         engagement,
        'materiality':        materiality,
        'ratios_by_category': ratios_by_category,
        'total_ratios':       ratios.count(),
        'followup_count':     followup_count,
    })


# ============================================================
# Materiality Calculator View
# Create or update materiality for an engagement
# ============================================================
@login_required
def materiality_calculator(request, engagement_id):
    engagement = get_object_or_404(Engagement, pk=engagement_id)

    # get existing or create new
    try:
        materiality = engagement.materiality_calc
        form        = MaterialityForm(instance=materiality)
    except MaterialityCalculation.DoesNotExist:
        materiality = None
        form        = MaterialityForm()

    if request.method == 'POST':
        if materiality:
            form = MaterialityForm(request.POST, instance=materiality)
        else:
            form = MaterialityForm(request.POST)

        if form.is_valid():
            calc             = form.save(commit=False)
            calc.engagement  = engagement
            calc.prepared_by = request.user
            calc.save()
            messages.success(
                request,
                'Materiality calculated and saved successfully.'
            )
            return redirect(
                'analytics:dashboard',
                engagement_id=engagement_id
            )

    return render(request, 'analytics/materiality_form.html', {
        'form':        form,
        'engagement':  engagement,
        'materiality': materiality,
    })


# ============================================================
# Approve Materiality View
# Only partners and managers can approve
# ============================================================
@login_required
def approve_materiality(request, engagement_id):
    engagement  = get_object_or_404(Engagement, pk=engagement_id)
    materiality = get_object_or_404(
        MaterialityCalculation,
        engagement=engagement
    )

    if request.user.role not in ['partner', 'manager']:
        messages.error(
            request,
            'Only Partners and Managers can approve materiality.'
        )
        return redirect(
            'analytics:dashboard',
            engagement_id=engagement_id
        )

    if request.method == 'POST':
        materiality.is_approved = True
        materiality.approved_by = request.user
        materiality.save()
        messages.success(request, 'Materiality approved.')

    return redirect(
        'analytics:dashboard',
        engagement_id=engagement_id
    )


# ============================================================
# Add Ratio Analysis View
# ============================================================
@login_required
def add_ratio(request, engagement_id):
    engagement = get_object_or_404(Engagement, pk=engagement_id)
    form       = RatioAnalysisForm()

    if request.method == 'POST':
        form = RatioAnalysisForm(request.POST)
        if form.is_valid():
            ratio             = form.save(commit=False)
            ratio.engagement  = engagement
            ratio.prepared_by = request.user
            ratio.save()
            messages.success(
                request,
                f'"{ratio.ratio_name}" added successfully.'
            )
            return redirect(
                'analytics:dashboard',
                engagement_id=engagement_id
            )

    return render(request, 'analytics/ratio_form.html', {
        'form':       form,
        'engagement': engagement,
        'title':      'Add Ratio Analysis',
    })


# ============================================================
# Edit Ratio Analysis View
# ============================================================
@login_required
def edit_ratio(request, pk):
    ratio      = get_object_or_404(RatioAnalysis, pk=pk)
    engagement = ratio.engagement
    form       = RatioAnalysisForm(instance=ratio)

    if request.method == 'POST':
        form = RatioAnalysisForm(request.POST, instance=ratio)
        if form.is_valid():
            form.save()
            messages.success(
                request,
                f'"{ratio.ratio_name}" updated.'
            )
            return redirect(
                'analytics:dashboard',
                engagement_id=engagement.pk
            )

    return render(request, 'analytics/ratio_form.html', {
        'form':       form,
        'engagement': engagement,
        'ratio':      ratio,
        'title':      'Edit Ratio Analysis',
    })


# ============================================================
# Delete Ratio Analysis View
# ============================================================
@login_required
def delete_ratio(request, pk):
    ratio      = get_object_or_404(RatioAnalysis, pk=pk)
    engagement = ratio.engagement

    if request.method == 'POST':
        name = ratio.ratio_name
        ratio.delete()
        messages.success(request, f'"{name}" deleted.')
        return redirect(
            'analytics:dashboard',
            engagement_id=engagement.pk
        )

    return render(request, 'analytics/confirm_delete.html', {
        'ratio':      ratio,
        'engagement': engagement,
    })