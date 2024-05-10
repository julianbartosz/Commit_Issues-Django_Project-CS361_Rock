from django.contrib import admin
from course_management.models import Course, Section


class CourseAdmin(admin.ModelAdmin):
    list_display = ('code', 'title')
    search_fields = ('code', 'title')
    list_filter = ()

    def instructor_name(self, obj):
        return obj.instructor.email if obj.instructor else 'No instructor assigned'

    instructor_name.short_description = 'Instructor'

    def number_of_tas(self, obj):
        return obj.tas.count()

    number_of_tas.short_description = 'Number of TAs'


class SectionAdmin(admin.ModelAdmin):
    list_display = ('course', 'number', 'section_type', 'campus', 'start_date', 'end_date', 'credits')
    search_fields = ('course__code', 'number', 'section_type', 'campus')
    list_filter = ('section_type', 'campus', 'start_date', 'end_date')

    def course_code(self, obj):
        return obj.course.code

    course_code.short_description = 'Course Code'


admin.site.register(Course, CourseAdmin)
admin.site.register(Section, SectionAdmin)
