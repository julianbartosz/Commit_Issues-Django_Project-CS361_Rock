from django.contrib import admin
from lab_section_management.models import LabSection


class LabSectionAdmin(admin.ModelAdmin):
    list_display = ('course', 'number', 'schedule', 'display_tas', 'has_credits', 'credits')  # Include new fields
    search_fields = ('course__code', 'course__title', 'number')
    list_filter = ('course', 'has_credits')  # Add filter for has_credits

    def display_tas(self, obj):
        return ", ".join([ta.email for ta in obj.tas.all()])
    display_tas.short_description = 'Teaching Assistants'

    def get_fields(self, request, obj=None):
        # Display credits only if the lab section has credits
        fields = super().get_fields(request, obj)
        if obj and obj.has_credits:
            return fields
        return [field for field in fields if field != 'credits']


admin.site.register(LabSection, LabSectionAdmin)
