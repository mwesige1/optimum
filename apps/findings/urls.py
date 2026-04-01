from django.urls import path
from . import views

app_name = 'findings'

urlpatterns = [
    path('',                            views.finding_list,             name='list'),
    path('create/',                     views.finding_create,           name='create'),
    path('<int:pk>/',                    views.finding_detail,           name='detail'),
    path('<int:pk>/edit/',               views.finding_edit,             name='edit'),
    path('<int:pk>/delete/',             views.finding_delete,           name='delete'),
    path('<int:pk>/resolve/',            views.finding_resolve,          name='resolve'),
    path('<int:pk>/response/',           views.add_management_response,  name='add_response'),
]