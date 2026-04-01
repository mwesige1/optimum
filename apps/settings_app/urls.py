from django.urls import path
from . import views

app_name = 'settings_app'

urlpatterns = [
    path('',                        views.settings_home,       name='home'),
    path('profile/',                views.profile_view,        name='profile'),
    path('change-password/',        views.change_password_view, name='change_password'),
    path('firm/',                   views.firm_settings_view,  name='firm'),
    path('users/',                  views.manage_users_view,   name='users'),
    path('users/<int:user_id>/toggle/', views.toggle_user_active, name='toggle_user'),
]