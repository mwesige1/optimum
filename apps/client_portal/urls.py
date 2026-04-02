from django.urls import path
from . import views

app_name = 'client_portal'

urlpatterns = [
    # auth
    path('login/',      views.client_login,    name='login'),
    path('register/',   views.client_register, name='register'),
    path('logout/',     views.client_logout,   name='logout'),

    # client portal pages
    path('dashboard/',          views.client_dashboard,       name='dashboard'),
    path('findings/',           views.client_findings,        name='findings'),
    path('findings/<int:pk>/',  views.client_finding_detail,  name='finding_detail'),
    path('engagements/',        views.client_engagements,     name='engagements'),
    path('profile/',            views.client_profile,         name='profile'),
    path('change-password/',    views.client_change_password, name='change_password'),

    # partner approval (inside audit firm)
    path('approvals/',
         views.pending_approvals,
         name='pending_approvals'),
    path('approvals/<int:client_user_id>/approve/',
         views.approve_client,
         name='approve_client'),
    path('approvals/<int:client_user_id>/reject/',
         views.reject_client,
         name='reject_client'),
]