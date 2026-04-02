from django.urls import path
from . import views

app_name = 'risk'

urlpatterns = [
    path('<int:engagement_id>/',
         views.risk_matrix,
         name='matrix'),

    path('<int:engagement_id>/add/',
         views.add_risk_area,
         name='add_area'),

    path('area/<int:pk>/edit/',
         views.edit_risk_area,
         name='edit_area'),

    path('area/<int:pk>/delete/',
         views.delete_risk_area,
         name='delete_area'),

    path('<int:engagement_id>/approve/',
         views.approve_matrix,
         name='approve'),
]