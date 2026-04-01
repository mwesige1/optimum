from django.urls import path
from . import views

# namespace allows us to refer to these urls as 'accounts:login'
app_name = 'accounts'

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
]