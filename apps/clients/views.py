from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import AuditClient
from .forms import ClientForm


# ============================================================
# Client List View
# Shows all clients with search
# ============================================================
@login_required
def client_list(request):
    clients = AuditClient.objects.all()

    # simple search by name
    search = request.GET.get('search', '')
    if search:
        clients = clients.filter(name__icontains=search)

    return render(request, 'clients/list.html', {
        'clients': clients,
        'search':  search,
    })


# ============================================================
# Client Detail View
# Shows full client info and their engagement history
# ============================================================
@login_required
def client_detail(request, pk):
    client = get_object_or_404(AuditClient, pk=pk)
    engagements = client.engagements.all()
    return render(request, 'clients/detail.html', {
        'client':      client,
        'engagements': engagements,
    })


# ============================================================
# Create Client View
# ============================================================
@login_required
def client_create(request):
    form = ClientForm()
    if request.method == 'POST':
        form = ClientForm(request.POST)
        if form.is_valid():
            client = form.save(commit=False)
            client.created_by = request.user
            client.save()
            messages.success(request, f'Client "{client.name}" created successfully.')
            return redirect('clients:list')
    return render(request, 'clients/form.html', {
        'form':  form,
        'title': 'Add New Client',
    })


# ============================================================
# Edit Client View
# ============================================================
@login_required
def client_edit(request, pk):
    client = get_object_or_404(AuditClient, pk=pk)
    form = ClientForm(instance=client)
    if request.method == 'POST':
        form = ClientForm(request.POST, instance=client)
        if form.is_valid():
            form.save()
            messages.success(request, f'Client "{client.name}" updated successfully.')
            return redirect('clients:detail', pk=pk)
    return render(request, 'clients/form.html', {
        'form':   form,
        'title':  'Edit Client',
        'client': client,
    })


# ============================================================
# Delete Client View
# ============================================================
@login_required
def client_delete(request, pk):
    client = get_object_or_404(AuditClient, pk=pk)
    if request.method == 'POST':
        name = client.name
        client.delete()
        messages.success(request, f'Client "{name}" deleted successfully.')
        return redirect('clients:list')
    return render(request, 'clients/confirm_delete.html', {'client': client})