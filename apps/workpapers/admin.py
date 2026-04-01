from django.contrib import admin
from .models import Workpaper, WorkpaperFile


@admin.register(Workpaper)
class WorkpaperAdmin(admin.ModelAdmin):
    list_display  = ('reference', 'title', 'engagement', 'section', 'status', 'prepared_by', 'prepared_date')
    search_fields = ('reference', 'title', 'engagement__name')
    list_filter   = ('status', 'section')


@admin.register(WorkpaperFile)
class WorkpaperFileAdmin(admin.ModelAdmin):
    list_display  = ('filename', 'workpaper', 'uploaded_by', 'uploaded_at')