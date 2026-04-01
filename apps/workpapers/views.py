from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from .models import Workpaper, WorkpaperFile
from .forms import WorkpaperForm, WorkpaperFileForm
from apps.engagements.models import Engagement


# ============================================================
# Workpaper List View
# Lists all workpapers — optionally filtered by engagement
# ============================================================
@login_required
def workpaper_list(request):
    workpapers = Workpaper.objects.select_related(
        'engagement', 'prepared_by', 'reviewed_by'
    )

    # filter by engagement if provided in URL e.g. ?engagement=3
    engagement_id = request.GET.get('engagement', '')
    if engagement_id:
        workpapers = workpapers.filter(engagement_id=engagement_id)

    # filter by status
    status = request.GET.get('status', '')
    if status:
        workpapers = workpapers.filter(status=status)

    # search by reference or title
    search = request.GET.get('search', '')
    if search:
        workpapers = workpapers.filter(title__icontains=search) | \
                     workpapers.filter(reference__icontains=search)

    engagements = Engagement.objects.all()

    return render(request, 'workpapers/list.html', {
        'workpapers':   workpapers,
        'engagements':  engagements,
        'engagement_id': engagement_id,
        'status':       status,
        'search':       search,
        'status_choices': Workpaper.STATUS_CHOICES,
    })


# ============================================================
# Workpaper Detail View
# Shows the full workpaper with files and review info
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

    return render(request, 'workpapers/detail.html', {
        'workpaper': workpaper,
        'files':     files,
        'file_form': file_form,
    })


# ============================================================
# Create Workpaper View
# ============================================================
@login_required
def workpaper_create(request):
    # pre-select engagement if passed in URL e.g. ?engagement=3
    engagement_id = request.GET.get('engagement', '')
    form = WorkpaperForm()

    if request.method == 'POST':
        form = WorkpaperForm(request.POST)
        if form.is_valid():
            workpaper = form.save(commit=False)
            workpaper.prepared_by = request.user

            # link to engagement from POST data or URL param
            eng_id = request.POST.get('engagement_id') or engagement_id
            if eng_id:
                workpaper.engagement = get_object_or_404(Engagement, pk=eng_id)

            workpaper.save()
            messages.success(request, f'Workpaper "{workpaper.reference}" created successfully.')
            return redirect('workpapers:detail', pk=workpaper.pk)

    # get all engagements for the dropdown
    engagements = Engagement.objects.all()

    return render(request, 'workpapers/form.html', {
        'form':          form,
        'title':         'New Workpaper',
        'engagements':   engagements,
        'engagement_id': engagement_id,
    })


# ============================================================
# Edit Workpaper View
# ============================================================
@login_required
def workpaper_edit(request, pk):
    workpaper = get_object_or_404(Workpaper, pk=pk)
    form = WorkpaperForm(instance=workpaper)

    if request.method == 'POST':
        form = WorkpaperForm(request.POST, instance=workpaper)
        if form.is_valid():
            form.save()
            messages.success(request, f'Workpaper "{workpaper.reference}" updated.')
            return redirect('workpapers:detail', pk=pk)

    return render(request, 'workpapers/form.html', {
        'form':       form,
        'title':      'Edit Workpaper',
        'workpaper':  workpaper,
        'engagements': Engagement.objects.all(),
        'engagement_id': workpaper.engagement_id,
    })


# ============================================================
# Delete Workpaper View
# ============================================================
@login_required
def workpaper_delete(request, pk):
    workpaper = get_object_or_404(Workpaper, pk=pk)
    if request.method == 'POST':
        ref = workpaper.reference
        workpaper.delete()
        messages.success(request, f'Workpaper "{ref}" deleted.')
        return redirect('workpapers:list')
    return render(request, 'workpapers/confirm_delete.html', {
        'workpaper': workpaper
    })


# ============================================================
# Upload File to Workpaper
# ============================================================
@login_required
def upload_file(request, pk):
    workpaper = get_object_or_404(Workpaper, pk=pk)

    if request.method == 'POST':
        form = WorkpaperFileForm(request.POST, request.FILES)
        if form.is_valid():
            wp_file = form.save(commit=False)
            wp_file.workpaper   = workpaper
            wp_file.uploaded_by = request.user
            # use original filename if display name not provided
            if not wp_file.filename:
                wp_file.filename = request.FILES['file'].name
            wp_file.save()
            messages.success(request, 'File uploaded successfully.')

    return redirect('workpapers:detail', pk=pk)


# ============================================================
# Delete File from Workpaper
# ============================================================
@login_required
def delete_file(request, pk, file_id):
    wp_file = get_object_or_404(WorkpaperFile, pk=file_id, workpaper_id=pk)
    wp_file.file.delete()   # delete from disk
    wp_file.delete()        # delete the database record
    messages.success(request, 'File removed.')
    return redirect('workpapers:detail', pk=pk)


# ============================================================
# Sign Off Workpaper
# Only managers and partners can sign off
# ============================================================
@login_required
def sign_off(request, pk):
    workpaper = get_object_or_404(Workpaper, pk=pk)

    if request.user.role not in ['partner', 'manager', 'senior']:
        messages.error(request, 'You do not have permission to sign off workpapers.')
        return redirect('workpapers:detail', pk=pk)

    if request.method == 'POST':
        action = request.POST.get('action')

        if action == 'review':
            # mark as reviewed
            workpaper.status        = 'reviewed'
            workpaper.reviewed_by   = request.user
            workpaper.reviewed_date = timezone.now().date()
            workpaper.save()
            messages.success(request, f'Workpaper "{workpaper.reference}" marked as reviewed.')

        elif action == 'signoff':
            # final sign off
            workpaper.status        = 'signed_off'
            workpaper.reviewed_by   = request.user
            workpaper.reviewed_date = timezone.now().date()
            workpaper.save()
            messages.success(request, f'Workpaper "{workpaper.reference}" signed off.')

        elif action == 'reopen':
            # send back to draft
            workpaper.status = 'draft'
            workpaper.save()
            messages.info(request, f'Workpaper "{workpaper.reference}" reopened for revision.')

    return redirect('workpapers:detail', pk=pk)