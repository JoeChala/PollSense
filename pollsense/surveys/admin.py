from django.contrib import admin
from .models import Survey

@admin.register(Survey)
class SurveyAdmin(admin.ModelAdmin):
    list_display = ("title", "survey_id", "owner", "created_at")
    readonly_fields = ("survey_id", "slug", "created_at")
