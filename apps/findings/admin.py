from django.contrib import admin
from .models import Finding, ManagementResponse


@admin.register(Finding)
class FindingAdmin(admin.ModelAdmin):
    list_display  = (
        'title', 'engagement', 'category',
        'risk_level', 'status', 'raised_by', 'due_date'
    )
    search_fields = ('title', 'engagement__name')
    list_filter   = ('risk_level', 'status', 'category')


@admin.register(ManagementResponse)
class ManagementResponseAdmin(admin.ModelAdmin):
    list_display  = ('finding', 'response_type', 'responded_by', 'response_date')
    list_filter   = ('response_type',)