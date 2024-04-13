from django.contrib import admin
from .models import Course
from user_management.models import User


class CourseAdmin(admin.ModelAdmin):
    list_display = ('code', 'title', 'instructor_name', 'number_of_tas')
    search_fields = ('code', 'title', 'instructor__username', 'tas__username')
    list_filter = ('instructor', 'tas')

    def instructor_name(self, obj):
        return obj.instructor.username if obj.instructor else 'No instructor assigned'

    instructor_name.short_description = 'Instructor'

    def number_of_tas(self, obj):
        return obj.tas.count()

    number_of_tas.short_description = 'Number of TAs'


admin.site.register(Course, CourseAdmin)
