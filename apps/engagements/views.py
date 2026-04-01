from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Engagement, EngagementMember
from .forms import EngagementForm
from apps.accounts.models import AuditUser


# ============================================================
# Engagement List View
# ============================================================
@login_required
def engagement_list(request):
    engagements = Engagement.objects.select_related('client', 'lead_auditor')

    # filter by status
    status = request.GET.get('status', '')
    if status:
        engagements = engagements.filter(status=status)

    # search by name or client
    search = request.GET.get('search', '')
    if search:
        engagements = engagements.filter(name__icontains=search) | \
                      engagements.filter(client__name__icontains=search)

    return render(request, 'engagements/list.html', {
        'engagements': engagements,
        'status':      status,
        'search':      search,
        'status_choices': Engagement.STATUS_CHOICES,
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
    members = EngagementMember.objects.filter(
        engagement=engagement
    ).select_related('user')

    return render(request, 'engagements/detail.html', {
        'engagement': engagement,
        'members':    members,
    })


# ============================================================
# Create Engagement View
# ============================================================
@login_required
def engagement_create(request):
    form = EngagementForm(user=request.user)
    if request.method == 'POST':
        form = EngagementForm(request.POST, user=request.user)
        if form.is_valid():
            engagement = form.save(commit=False)
            engagement.created_by = request.user
            engagement.save()
            messages.success(request, f'Engagement "{engagement.name}" created successfully.')
            return redirect('engagements:detail', pk=engagement.pk)
    return render(request, 'engagements/form.html', {
        'form':  form,
        'title': 'New Engagement',
    })


# ============================================================
# Edit Engagement View
# ============================================================
@login_required
def engagement_edit(request, pk):
    engagement = get_object_or_404(Engagement, pk=pk)
    form = EngagementForm(instance=engagement, user=request.user)
    if request.method == 'POST':
        form = EngagementForm(request.POST, instance=engagement, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, f'Engagement "{engagement.name}" updated successfully.')
            return redirect('engagements:detail', pk=pk)
    return render(request, 'engagements/form.html', {
        'form':       form,
        'title':      'Edit Engagement',
        'engagement': engagement,
    })


# ============================================================
# Delete Engagement View
# ============================================================
@login_required
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
def add_member(request, pk):
    engagement = get_object_or_404(Engagement, pk=pk)

    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        role    = request.POST.get('role', 'staff')
        try:
            user = AuditUser.objects.get(id=user_id)
            # add the user to the engagement if not already a member
            EngagementMember.objects.get_or_create(
                engagement=engagement,
                user=user,
                defaults={'role': role}
            )
            messages.success(request, f'{user.get_full_name()} added to engagement.')
        except AuditUser.DoesNotExist:
            messages.error(request, 'User not found.')

    return redirect('engagements:detail', pk=pk)


# ============================================================
# Remove Team Member View
# ============================================================
@login_required
def remove_member(request, pk, user_id):
    engagement = get_object_or_404(Engagement, pk=pk)
    EngagementMember.objects.filter(
        engagement=engagement,
        user_id=user_id
    ).delete()
    messages.success(request, 'Team member removed.')
    return redirect('engagements:detail', pk=pk)