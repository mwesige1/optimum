from django.shortcuts import render, redirect
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import ProfileForm, ChangePasswordForm, FirmForm
from apps.accounts.models import AuditUser


# ============================================================
# Settings Home
# ============================================================
@login_required
def settings_home(request):
    return redirect('settings_app:profile')


# ============================================================
# Edit Profile View
# ============================================================
@login_required
def profile_view(request):
    form = ProfileForm(instance=request.user)

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully.')
            return redirect('settings_app:profile')

    return render(request, 'settings_app/profile.html', {'form': form})


# ============================================================
# Change Password View
# ============================================================
@login_required
def change_password_view(request):
    form = ChangePasswordForm(user=request.user)

    if request.method == 'POST':
        form = ChangePasswordForm(user=request.user, data=request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Password changed successfully.')
            return redirect('settings_app:change_password')

    return render(request, 'settings_app/change_password.html', {'form': form})


# ============================================================
# Firm Settings View — partner only
# ============================================================
@login_required
def firm_settings_view(request):
    if request.user.role != 'partner':
        messages.error(request, 'Only Partners can access firm settings.')
        return redirect('settings_app:profile')

    firm = request.user.firm
    form = FirmForm(instance=firm)

    if request.method == 'POST':
        form = FirmForm(request.POST, request.FILES, instance=firm)
        if form.is_valid():
            form.save()
            messages.success(request, 'Firm settings updated successfully.')
            return redirect('settings_app:firm')

    return render(request, 'settings_app/firm.html', {
        'form': form,
        'firm': firm,
    })


# ============================================================
# Manage Users View — partner and manager only
# ============================================================
@login_required
def manage_users_view(request):
    if request.user.role not in ['partner', 'manager']:
        messages.error(request, 'Access restricted to Partners and Managers.')
        return redirect('settings_app:profile')

    users = AuditUser.objects.filter(
        firm=request.user.firm
    ).order_by('role', 'first_name')

    return render(request, 'settings_app/users.html', {'users': users})


# ============================================================
# Toggle User Active — partner only
# ============================================================
@login_required
def toggle_user_active(request, user_id):
    if request.user.role != 'partner':
        messages.error(request, 'Only Partners can deactivate users.')
        return redirect('settings_app:users')

    try:
        user = AuditUser.objects.get(id=user_id, firm=request.user.firm)
        if user == request.user:
            messages.error(request, 'You cannot deactivate your own account.')
        else:
            user.is_active = not user.is_active
            user.save()
            status = 'activated' if user.is_active else 'deactivated'
            messages.success(
                request,
                f'{user.get_full_name()} has been {status}.'
            )
    except AuditUser.DoesNotExist:
        messages.error(request, 'User not found.')

    next_url = request.POST.get('next', '')
    if next_url:
        return redirect(next_url)
    return redirect('settings_app:users')