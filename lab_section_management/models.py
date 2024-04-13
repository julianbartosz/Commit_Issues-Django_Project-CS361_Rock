from django.db import models
from django.utils.translation import gettext_lazy as _
from course_management.models import Course
from user_management.models import User

class LabSection(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='lab_sections', help_text=_("The course this lab section belongs to."))
    number = models.CharField(max_length=10, help_text=_("Lab section number or identifier."))
    tas = models.ManyToManyField(User, related_name='lab_sections', blank=True, limit_choices_to={'role': 'TA'}, help_text=_("TAs assigned to this lab section."))
    schedule = models.CharField(max_length=50, help_text=_("Schedule or timing details for the lab section."))

    def __str__(self):
        return f"{self.course.code} - Lab {self.number} ({self.schedule})"
