# models.py
from django.db import models
from django.utils.translation import gettext_lazy as _
from user_management.models import User


class Course(models.Model):
    code = models.CharField(max_length=10, unique=True, help_text=_("Enter the unique course code."))
    title = models.CharField(max_length=100, help_text=_("Enter the full title of the course."))
    description = models.TextField(help_text=_("Provide a brief description of the course content."))
    instructor = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='courses_taught', help_text=_("Select the course instructor."))
    tas = models.ManyToManyField(User, related_name='assisting_courses', help_text=_("Select the teaching assistants for the course."))
    semester = models.CharField(max_length=20, help_text=_("Specify the semester of the course offering."))
    year = models.IntegerField(help_text=_("Enter the academic year of the course offering."))

    class Meta:
        app_label = 'course_management'

    def __str__(self):
        return f"{self.code} - {self.title}"
