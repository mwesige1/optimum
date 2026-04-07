from django.urls import path
from . import views

app_name = 'clients'

urlpatterns = [
    path('',                                    views.client_list,          name='list'),
    path('pending/',                            views.pending_approvals,    name='pending_approvals'),
    path('<int:pk>/',                           views.client_detail,        name='detail'),
    path('<int:pk>/approve/',                   views.client_approve,       name='approve'),
    path('<int:pk>/deactivate/',                views.client_deactivate,    name='deactivate'),
    path('<int:pk>/delete/',                    views.client_delete,        name='delete'),
    path('portal/<int:client_user_id>/approve/', views.approve_portal_client, name='approve_portal'),
    path('portal/<int:client_user_id>/reject/',  views.reject_portal_client,  name='reject_portal'),
]