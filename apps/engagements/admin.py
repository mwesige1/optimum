from django.contrib import admin
from .models import Engagement, EngagementMember


@admin.register(Engagement)
class EngagementAdmin(admin.ModelAdmin):
    # columns shown in the list view
    list_display  = ('name', 'client', 'financial_year', 'audit_type', 'status', 'lead_auditor', 'end_date')
    search_fields = ('name', 'client__name', 'financial_year')
    list_filter   = ('status', 'audit_type', 'created_at')


@admin.register(EngagementMember)
class EngagementMemberAdmin(admin.ModelAdmin):
    # columns shown in the list view
    list_display  = ('engagement', 'user', 'role', 'joined_at')
    search_fields = ('engagement__name', 'user__username')
    list_filter   = ('role',)
