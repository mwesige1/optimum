from django.urls import path
from . import views

app_name = 'workpapers'

urlpatterns = [
    path('',                                views.workpaper_list,   name='list'),
    path('create/',                         views.workpaper_create, name='create'),
    path('<int:pk>/',                        views.workpaper_detail, name='detail'),
    path('<int:pk>/edit/',                   views.workpaper_edit,   name='edit'),
    path('<int:pk>/delete/',                 views.workpaper_delete, name='delete'),
    path('<int:pk>/upload/',                 views.upload_file,      name='upload_file'),
    path('<int:pk>/files/<int:file_id>/delete/', views.delete_file,  name='delete_file'),
    path('<int:pk>/signoff/',                views.sign_off,         name='sign_off'),
]