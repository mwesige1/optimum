from django.contrib import admin
from django.utils import timezone
from .models import ClientUser


@admin.register(ClientUser)
class ClientUserAdmin(admin.ModelAdmin):
    list_display  = (
        'company_name', 'contact_person', 'email',
        'is_approved', 'is_active', 'client', 'registered_at'
    )
    list_filter   = ('is_approved', 'is_active')
    search_fields = ('company_name', 'contact_person', 'email')
    actions       = ['approve_clients', 'deactivate_clients']

    def approve_clients(self, request, queryset):
        # bulk approve selected clients
        queryset.update(
            is_approved=True,
            approved_at=timezone.now()
        )
        self.message_user(
            request,
            f'{queryset.count()} client(s) approved successfully.'
        )
    approve_clients.short_description = 'Approve selected clients'

    def deactivate_clients(self, request, queryset):
        queryset.update(is_active=False)
        self.message_user(
            request,
            f'{queryset.count()} client(s) deactivated.'
        )
    deactivate_clients.short_description = 'Deactivate selected clients'