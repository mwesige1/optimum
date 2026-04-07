# ============================================================
# permissions.py
# Centralised role-based access control helpers
# ============================================================

from django.shortcuts import redirect
from django.contrib import messages
from functools import wraps


# Client permissions
CLIENT_VIEW_ROLES       = ['partner', 'manager', 'qc']
CLIENT_APPROVE_ROLES    = ['partner']
CLIENT_DELETE_ROLES     = ['partner']
CLIENT_DEACTIVATE_ROLES = ['partner', 'manager']

# Engagement permissions
ENGAGEMENT_VIEW_ROLES   = ['partner', 'manager', 'senior',
                            'staff', 'it_auditor', 'qc', 'trainee']
ENGAGEMENT_CREATE_ROLES = ['partner', 'manager']
ENGAGEMENT_EDIT_ROLES   = ['partner', 'manager']
ENGAGEMENT_DELETE_ROLES = ['partner']


def role_required(allowed_roles, redirect_url='core:dashboard'):
    """
    Decorator that checks if the logged-in user has
    one of the allowed roles. If not redirects to
    redirect_url with an error message.
    """
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            if request.user.role not in allowed_roles:
                messages.error(
                    request,
                    'You do not have permission to access this page.'
                )
                return redirect(redirect_url)
            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator