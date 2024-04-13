from user_management.models import User
from django.db import models
from django.utils.translation import gettext_lazy as _


class Course(models.Model):
    code = models.CharField(max_length=10, unique=True, help_text=_("Unique code for the course"))
    title = models.CharField(max_length=100, help_text=_("Title of the course"))
    description = models.TextField(help_text=_("Description of the course"))
    instructor = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='taught_courses', limit_choices_to={'role': 'Instructor'}, help_text=_("Instructor assigned to the course"))
    tas = models.ManyToManyField(User, related_name='assigned_courses', blank=True, limit_choices_to={'role': 'TA'}, help_text=_("TAs assigned to the course"))
    semester = models.CharField(max_length=10, choices=[('Fall', 'Fall'), ('Spring', 'Spring'), ('Summer', 'Summer')], help_text=_("Semester in which the course is offered"))
    year = models.IntegerField(help_text=_("Year in which the course is offered"))

    def __str__(self):
        return f"{self.code} - {self.title} ({self.semester} {self.year})"
