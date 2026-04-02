from django.contrib import admin
from .models import RatioAnalysis, MaterialityCalculation


@admin.register(RatioAnalysis)
class RatioAnalysisAdmin(admin.ModelAdmin):
    list_display  = (
        'ratio_name', 'engagement', 'category',
        'current_year_value', 'prior_year_value',
        'variance_pct', 'requires_followup'
    )
    list_filter   = ('category', 'requires_followup')
    search_fields = ('ratio_name', 'engagement__name')


@admin.register(MaterialityCalculation)
class MaterialityCalculationAdmin(admin.ModelAdmin):
    list_display  = (
        'engagement', 'basis', 'basis_amount',
        'materiality_percentage', 'overall_materiality',
        'is_approved'
    )
    list_filter   = ('basis', 'is_approved')