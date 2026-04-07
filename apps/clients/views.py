from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import AuditClient
from apps.client_portal.models import ClientUser
from apps.accounts.permissions import (
    role_required,
    CLIENT_VIEW_ROLES,
    CLIENT_APPROVE_ROLES,
    CLIENT_DELETE_ROLES,
    CLIENT_DEACTIVATE_ROLES,
)


# ============================================================
# Client List View
# Only partners, managers and QC reviewers can see clients
# ============================================================
@login_required
@role_required(CLIENT_VIEW_ROLES)
def client_list(request):
    clients = AuditClient.objects.all()

    # search
    search = request.GET.get('search', '')
    if search:
        clients = clients.filter(
            name__icontains=search
        ) | clients.filter(
            contact_person__icontains=search
        ) | clients.filter(
            contact_email__icontains=search
        )
        clients = clients.distinct()

    # filter by industry
    industry = request.GET.get('industry', '')
    if industry:
        clients = clients.filter(industry=industry)

    # filter by status
    status = request.GET.get('status', '')
    if status:
        clients = clients.filter(status=status)

    # stats
    total_clients    = AuditClient.objects.count()
    pending_clients  = AuditClient.objects.filter(
                           status='pending'
                       ).count()
    active_clients   = AuditClient.objects.filter(
                           status='active'
                       ).count()
    inactive_clients = AuditClient.objects.filter(
                           status='inactive'
                       ).count()

    return render(request, 'clients/list.html', {
        'clients':          clients,
        'search':           search,
        'industry':         industry,
        'status':           status,
        'industry_choices': AuditClient.INDUSTRY_CHOICES,
        'status_choices':   AuditClient.STATUS_CHOICES,
        'total_clients':    total_clients,
        'pending_clients':  pending_clients,
        'active_clients':   active_clients,
        'inactive_clients': inactive_clients,
    })


# ============================================================
# Client Detail View
# Only partners, managers and QC reviewers
# ============================================================
@login_required
@role_required(CLIENT_VIEW_ROLES)
def client_detail(request, pk):
    client      = get_object_or_404(AuditClient, pk=pk)
    engagements = client.engagements.all().order_by('-created_at')

    try:
        portal_user = client.portal_user
        has_portal  = True
    except Exception:
        portal_user = None
        has_portal  = False

    return render(request, 'clients/detail.html', {
        'client':      client,
        'engagements': engagements,
        'portal_user': portal_user,
        'has_portal':  has_portal,
    })


# ============================================================
# Approve Client View
# Partners only
# ============================================================
@login_required
@role_required(CLIENT_APPROVE_ROLES)
def client_approve(request, pk):
    client = get_object_or_404(AuditClient, pk=pk)

    if request.method == 'POST':
        client.status = 'active'
        client.save()
        messages.success(
            request,
            f'"{client.name}" has been approved and is now active.'
        )

    return redirect('clients:detail', pk=pk)


# ============================================================
# Deactivate Client View
# Partners and managers
# ============================================================
@login_required
@role_required(CLIENT_DEACTIVATE_ROLES)
def client_deactivate(request, pk):
    client = get_object_or_404(AuditClient, pk=pk)

    if request.method == 'POST':
        client.status = 'inactive'
        client.save()
        messages.success(
            request,
            f'"{client.name}" has been deactivated.'
        )

    return redirect('clients:detail', pk=pk)


# ============================================================
# Delete Client View
# Partners only
# ============================================================
@login_required
@role_required(CLIENT_DELETE_ROLES)
def client_delete(request, pk):
    client = get_object_or_404(AuditClient, pk=pk)

    if request.method == 'POST':
        name = client.name
        client.delete()
        messages.success(
            request,
            f'Client "{name}" deleted successfully.'
        )
        return redirect('clients:list')

    return render(request, 'clients/confirm_delete.html', {
        'client': client
    })


# ============================================================
# Pending Approvals View
# Partners only
# ============================================================
@login_required
@role_required(CLIENT_APPROVE_ROLES)
def pending_approvals(request):
    pending  = ClientUser.objects.filter(
                   is_approved=False,
                   is_active=True
               )
    approved = ClientUser.objects.filter(
                   is_approved=True,
                   is_active=True
               )
    clients  = AuditClient.objects.all()

    return render(request, 'clients/pending_approvals.html', {
        'pending':  pending,
        'approved': approved,
        'clients':  clients,
    })


# ============================================================
# Approve Portal Client
# Partners only
# ============================================================
@login_required
@role_required(CLIENT_APPROVE_ROLES)
def approve_portal_client(request, client_user_id):
    client_user = get_object_or_404(ClientUser, id=client_user_id)

    if request.method == 'POST':
        client_id = request.POST.get('client_id')

        if client_id:
            try:
                audit_client            = AuditClient.objects.get(
                                              id=client_id
                                          )
                client_user.client      = audit_client
                audit_client.status     = 'active'
                audit_client.save()
            except AuditClient.DoesNotExist:
                pass

        elif client_user.client:
            client_user.client.status = 'active'
            client_user.client.save()

        else:
            audit_client = AuditClient.objects.create(
                name           = client_user.company_name,
                contact_person = client_user.contact_person,
                contact_email  = client_user.email,
                contact_phone  = client_user.phone,
                status         = 'active',
            )
            client_user.client = audit_client

        from django.utils import timezone
        client_user.is_approved   = True
        client_user.approved_at   = timezone.now()
        client_user.approval_note = request.POST.get('note', '')
        client_user.save()

        from apps.client_portal.emails import send_approval_email
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

    return redirect('clients:pending_approvals')


# ============================================================
# Reject Portal Client
# Partners only
# ============================================================
@login_required
@role_required(CLIENT_APPROVE_ROLES)
def reject_portal_client(request, client_user_id):
    client_user = get_object_or_404(ClientUser, id=client_user_id)

    if request.method == 'POST':
        reason = request.POST.get('reason', 'No reason provided.')

        client_user.is_active = False
        client_user.save()

        if client_user.client:
            client_user.client.delete()

        from apps.client_portal.emails import send_rejection_email
        send_rejection_email(client_user, reason)

        messages.success(
            request,
            f'{client_user.company_name} registration rejected '
            f'and notification email sent.'
        )
        return redirect('clients:pending_approvals')

    return render(request, 'clients/reject_client.html', {
        'client_user': client_user
    })