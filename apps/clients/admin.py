from django.contrib import admin
from .models import AuditClient


@admin.register(AuditClient)
class AuditClientAdmin(admin.ModelAdmin):
    # columns shown in the list view
    list_display  = ('name', 'industry', 'contact_person', 'contact_email', 'created_at')
    search_fields = ('name', 'contact_person', 'contact_email')
    list_filter   = ('industry', 'created_at')