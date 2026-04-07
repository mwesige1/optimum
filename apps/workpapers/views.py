from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.http import JsonResponse
from .models import Workpaper, WorkpaperFile
from .forms import WorkpaperForm, WorkpaperFileForm
from apps.engagements.models import Engagement
from .reference_codes import (
    REFERENCE_CODES,
    get_title_for_reference,
    get_programme_for_reference,
)


# ============================================================
# Workpaper List View
# ============================================================
@login_required
def workpaper_list(request):
    user = request.user

    # role based filtering
    if user.role in ['partner', 'qc']:
        workpapers = Workpaper.objects.all()
    elif user.role in ['manager', 'it_auditor']:
        from apps.engagements.models import EngagementMember
        eng_ids = EngagementMember.objects.filter(
            user=user
        ).values_list('engagement_id', flat=True)
        lead_ids = Engagement.objects.filter(
            lead_auditor=user
        ).values_list('id', flat=True)
        all_ids = list(eng_ids) + list(lead_ids)
        workpapers = Workpaper.objects.filter(
            engagement_id__in=all_ids
        )
    elif user.role == 'senior':
        from apps.engagements.models import EngagementMember
        eng_ids = EngagementMember.objects.filter(
            user=user
        ).values_list('engagement_id', flat=True)
        workpapers = Workpaper.objects.filter(
            engagement_id__in=eng_ids
        )
    else:
        # staff and trainees see only their own workpapers
        workpapers = Workpaper.objects.filter(prepared_by=user)

    workpapers = workpapers.select_related(
        'engagement', 'prepared_by', 'reviewed_by'
    )

    # filter by engagement
    engagement_id = request.GET.get('engagement', '')
    if engagement_id:
        workpapers = workpapers.filter(engagement_id=engagement_id)

    # filter by status
    status = request.GET.get('status', '')
    if status:
        workpapers = workpapers.filter(status=status)

    # search
    search = request.GET.get('search', '')
    if search:
        workpapers = workpapers.filter(
            title__icontains=search
        ) | workpapers.filter(
            reference__icontains=search
        )
        workpapers = workpapers.distinct()

    engagements = Engagement.objects.all()

    # stats
    total      = workpapers.count()
    draft      = workpapers.filter(status='draft').count()
    in_review  = workpapers.filter(status='in_review').count()
    reviewed   = workpapers.filter(status='reviewed').count()
    signed_off = workpapers.filter(status='signed_off').count()

    return render(request, 'workpapers/list.html', {
        'workpapers':     workpapers,
        'engagements':    engagements,
        'engagement_id':  engagement_id,
        'status':         status,
        'search':         search,
        'status_choices': Workpaper.STATUS_CHOICES,
        'total':          total,
        'draft':          draft,
        'in_review':      in_review,
        'reviewed':       reviewed,
        'signed_off':     signed_off,
        'can_create':     True,
    })


# ============================================================
# Workpaper Detail View
# ============================================================
@login_required
def workpaper_detail(request, pk):
    workpaper = get_object_or_404(
        Workpaper.objects.select_related(
            'engagement', 'prepared_by', 'reviewed_by'
        ),
        pk=pk
    )
    files     = workpaper.files.all()
    file_form = WorkpaperFileForm()
    user      = request.user

    # determine what actions this user can take
    can_review  = user.role in ['senior', 'manager', 'partner', 'qc']
    can_signoff = user.role in ['manager', 'partner']

    return render(request, 'workpapers/detail.html', {
        'workpaper':   workpaper,
        'files':       files,
        'file_form':   file_form,
        'can_review':  can_review,
        'can_signoff': can_signoff,
    })


# ============================================================
# Create Workpaper View
# ============================================================
@login_required
def workpaper_create(request):
    engagement_id = request.GET.get('engagement', '')
    form = WorkpaperForm()

    if request.method == 'POST':
        form = WorkpaperForm(request.POST)
        if form.is_valid():
            workpaper             = form.save(commit=False)
            workpaper.prepared_by = request.user

            eng_id = request.POST.get('engagement_id') or engagement_id
            if eng_id:
                workpaper.engagement = get_object_or_404(
                    Engagement, pk=eng_id
                )

            workpaper.save()
            messages.success(
                request,
                f'Workpaper "{workpaper.reference}" created.'
            )
            return redirect('workpapers:detail', pk=workpaper.pk)

    engagements = Engagement.objects.all()

    return render(request, 'workpapers/form.html', {
        'form':           form,
        'title':          'New Workpaper',
        'engagements':    engagements,
        'engagement_id':  engagement_id,
        'reference_codes': REFERENCE_CODES,
    })


# ============================================================
# Edit Workpaper View
# ============================================================
@login_required
def workpaper_edit(request, pk):
    workpaper = get_object_or_404(Workpaper, pk=pk)

    # only the preparer, seniors, managers and partners can edit
    user = request.user
    if workpaper.prepared_by != user and \
       user.role not in ['senior', 'manager', 'partner']:
        messages.error(
            request,
            'You do not have permission to edit this workpaper.'
        )
        return redirect('workpapers:detail', pk=pk)

    form = WorkpaperForm(instance=workpaper)

    if request.method == 'POST':
        form = WorkpaperForm(request.POST, instance=workpaper)
        if form.is_valid():
            form.save()
            messages.success(
                request,
                f'Workpaper "{workpaper.reference}" updated.'
            )
            return redirect('workpapers:detail', pk=pk)

    engagements = Engagement.objects.all()

    return render(request, 'workpapers/form.html', {
        'form':           form,
        'title':          'Edit Workpaper',
        'workpaper':      workpaper,
        'engagements':    engagements,
        'engagement_id':  workpaper.engagement_id,
        'reference_codes': REFERENCE_CODES,
    })


# ============================================================
# Delete Workpaper View
# ============================================================
@login_required
def workpaper_delete(request, pk):
    workpaper = get_object_or_404(Workpaper, pk=pk)
    user      = request.user

    if workpaper.prepared_by != user and \
       user.role not in ['manager', 'partner']:
        messages.error(
            request,
            'You do not have permission to delete this workpaper.'
        )
        return redirect('workpapers:detail', pk=pk)

    if request.method == 'POST':
        ref = workpaper.reference
        workpaper.delete()
        messages.success(request, f'Workpaper "{ref}" deleted.')
        return redirect('workpapers:list')

    return render(request, 'workpapers/confirm_delete.html', {
        'workpaper': workpaper
    })


# ============================================================
# Upload File
# ============================================================
@login_required
def upload_file(request, pk):
    workpaper = get_object_or_404(Workpaper, pk=pk)

    if request.method == 'POST':
        form = WorkpaperFileForm(request.POST, request.FILES)
        if form.is_valid():
            wp_file             = form.save(commit=False)
            wp_file.workpaper   = workpaper
            wp_file.uploaded_by = request.user
            if not wp_file.filename:
                wp_file.filename = request.FILES['file'].name
            wp_file.save()
            messages.success(request, 'File uploaded successfully.')

    return redirect('workpapers:detail', pk=pk)


# ============================================================
# Delete File
# ============================================================
@login_required
def delete_file(request, pk, file_id):
    wp_file = get_object_or_404(
        WorkpaperFile, pk=file_id, workpaper_id=pk
    )
    wp_file.file.delete()
    wp_file.delete()
    messages.success(request, 'File removed.')
    return redirect('workpapers:detail', pk=pk)


# ============================================================
# Sign Off Workpaper
# Enforces the workflow: Draft → In Review → Reviewed → Signed Off
# ============================================================
@login_required
def sign_off(request, pk):
    workpaper = get_object_or_404(Workpaper, pk=pk)
    user      = request.user

    if request.method == 'POST':
        action = request.POST.get('action')

        if action == 'submit_review':
            # Staff submits for review
            if workpaper.status == 'draft':
                workpaper.status = 'in_review'
                workpaper.save()
                messages.success(
                    request,
                    f'"{workpaper.reference}" submitted for review.'
                )
            else:
                messages.error(
                    request,
                    'Only draft workpapers can be submitted for review.'
                )

        elif action == 'review':
            # Senior/Manager/Partner marks as reviewed
            if user.role not in ['senior', 'manager', 'partner', 'qc']:
                messages.error(
                    request,
                    'Only Senior Auditors and above can review workpapers.'
                )
            elif workpaper.status != 'in_review':
                messages.error(
                    request,
                    'Only workpapers in review can be marked as reviewed.'
                )
            else:
                workpaper.status        = 'reviewed'
                workpaper.reviewed_by   = user
                workpaper.reviewed_date = timezone.now().date()
                workpaper.save()
                messages.success(
                    request,
                    f'"{workpaper.reference}" marked as reviewed.'
                )

        elif action == 'signoff':
            # Manager/Partner gives final sign off
            if user.role not in ['manager', 'partner']:
                messages.error(
                    request,
                    'Only Managers and Partners can give final sign off.'
                )
            elif workpaper.status != 'reviewed':
                messages.error(
                    request,
                    'Only reviewed workpapers can be signed off.'
                )
            else:
                workpaper.status        = 'signed_off'
                workpaper.reviewed_by   = user
                workpaper.reviewed_date = timezone.now().date()
                workpaper.save()
                messages.success(
                    request,
                    f'"{workpaper.reference}" signed off.'
                )

        elif action == 'reopen':
            # Send back to draft
            if user.role not in ['senior', 'manager', 'partner']:
                messages.error(
                    request,
                    'You do not have permission to reopen workpapers.'
                )
            else:
                workpaper.status = 'draft'
                workpaper.save()
                messages.info(
                    request,
                    f'"{workpaper.reference}" reopened for revision.'
                )

    return redirect('workpapers:detail', pk=pk)


# ============================================================
# AJAX — Get reference code details
# Returns title and audit programme for a reference code
# Called by JavaScript when user selects a reference code
# ============================================================
def get_reference_details(request):
    from .reference_codes import (
        get_title_for_reference,
        get_programme_for_reference
    )
    code      = request.GET.get('code', '')
    title     = get_title_for_reference(code)
    programme = get_programme_for_reference(code)
    return JsonResponse({
        'title':     title,
        'programme': programme,
    })