from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('staff/',     views.staff_directory, name='staff'),
    path('risk-analytics/', views.risk_analytics_overview, name='risk_analytics'),


]