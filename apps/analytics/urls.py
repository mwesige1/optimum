from django.urls import path
from . import views

app_name = 'analytics'

urlpatterns = [
    path('<int:engagement_id>/',
         views.analytics_dashboard,
         name='dashboard'),

    path('<int:engagement_id>/materiality/',
         views.materiality_calculator,
         name='materiality'),

    path('<int:engagement_id>/materiality/approve/',
         views.approve_materiality,
         name='approve_materiality'),

    path('<int:engagement_id>/ratio/add/',
         views.add_ratio,
         name='add_ratio'),

    path('ratio/<int:pk>/edit/',
         views.edit_ratio,
         name='edit_ratio'),

    path('ratio/<int:pk>/delete/',
         views.delete_ratio,
         name='delete_ratio'),
]