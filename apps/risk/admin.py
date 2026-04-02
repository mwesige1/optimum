from django.contrib import admin
from .models import RiskArea, RiskMatrix


@admin.register(RiskArea)
class RiskAreaAdmin(admin.ModelAdmin):
    list_display  = (
        'get_area_name', 'engagement', 'inherent_risk',
        'control_risk', 'detection_risk', 'overall_risk'
    )
    list_filter   = ('overall_risk', 'area')
    search_fields = ('engagement__name',)


@admin.register(RiskMatrix)
class RiskMatrixAdmin(admin.ModelAdmin):
    list_display  = (
        'engagement', 'overall_risk',
        'overall_materiality', 'is_approved'
    )
    list_filter   = ('overall_risk', 'is_approved')