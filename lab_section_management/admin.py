from django.contrib import admin
from .models import LabSection


class LabSectionAdmin(admin.ModelAdmin):
    list_display = ('course', 'number', 'schedule', 'display_tas')
    search_fields = ('course__code', 'course__title', 'number')
    list_filter = ('course',)

    def display_tas(self, obj):
        return ", ".join([ta.email for ta in obj.tas.all()])
    display_tas.short_description = 'Teaching Assistants'


admin.site.register(LabSection, LabSectionAdmin)
