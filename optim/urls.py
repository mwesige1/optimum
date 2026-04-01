from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    # Django admin panel
    path('admin/', admin.site.urls),

    # accounts app urls (login, logout)
    path('accounts/', include('apps.accounts.urls')),

     # core app urls (dashboard)
    path('', include('apps.core.urls')),

]

# serves uploaded media files during development
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)