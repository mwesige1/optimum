from django.contrib import admin
from .models import AuditClient


@admin.register(AuditClient)
class AuditClientAdmin(admin.ModelAdmin):
    list_display  = (
        'name', 'industry', 'contact_person',
        'contact_email', 'status', 'created_at'
    )
    search_fields = ('name', 'contact_person', 'contact_email')
    list_filter   = ('industry', 'status', 'created_at')
    actions       = ['approve_clients', 'deactivate_clients']

    def approve_clients(self, request, queryset):
        queryset.update(status='active')
        self.message_user(request, f'{queryset.count()} client(s) approved.')
    approve_clients.short_description = 'Approve selected clients'

    def deactivate_clients(self, request, queryset):
        queryset.update(status='inactive')
        self.message_user(request, f'{queryset.count()} client(s) deactivated.')
    deactivate_clients.short_description = 'Deactivate selected clients'