from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Firm, AuditUser


# ============================================================
# Firm Admin
# Registers the Firm model in the admin panel
# ============================================================
@admin.register(Firm)
class FirmAdmin(admin.ModelAdmin):
    # columns to show in the list view
    list_display = ('name', 'email', 'phone', 'created_at')
    # fields you can search by
    search_fields = ('name', 'email')
    # filter sidebar on the right
    list_filter = ('created_at',)


# ============================================================
# AuditUser Admin
# We extend Django's built-in UserAdmin so we keep all the
# default user fields and just add our custom ones on top
# ============================================================
@admin.register(AuditUser)
class AuditUserAdmin(UserAdmin):
    # columns to show in the list view
    list_display = ('username', 'get_full_name', 'email', 'firm', 'role', 'is_active')
    # filter sidebar on the right
    list_filter = ('role', 'firm', 'is_active')
    # fields you can search by
    search_fields = ('username', 'first_name', 'last_name', 'email')

    # adds our custom fields (firm, role, phone) to the user detail page in admin
    fieldsets = UserAdmin.fieldsets + (
        ('Audit Profile', {
            'fields': ('firm', 'role', 'phone')
        }),
    )

    # adds our custom fields to the create user page in admin
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Audit Profile', {
            'fields': ('firm', 'role', 'phone')
        }),
    )
