from django.contrib import admin
from .models import ClinicalGuideline, DrugInteraction, ClinicalAlert

@admin.register(ClinicalGuideline)
class ClinicalGuidelineAdmin(admin.ModelAdmin):
    list_display = ['title', 'specialty', 'condition', 'evidence_level', 'is_active']
    list_filter = ['specialty', 'evidence_level', 'is_active']
    search_fields = ['title', 'condition', 'tags']

@admin.register(DrugInteraction)
class DrugInteractionAdmin(admin.ModelAdmin):
    list_display = ['drug1', 'drug2', 'interaction_type', 'severity', 'is_active']
    list_filter = ['interaction_type', 'severity', 'is_active']
    search_fields = ['drug1', 'drug2']

@admin.register(ClinicalAlert)
class ClinicalAlertAdmin(admin.ModelAdmin):
    list_display = ['patient', 'alert_type', 'severity', 'is_read', 'is_acknowledged']
    list_filter = ['alert_type', 'severity', 'is_read', 'is_acknowledged']
    search_fields = ['patient__full_name', 'title']