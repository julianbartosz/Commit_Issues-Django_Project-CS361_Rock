from django.db import models
from user_management.models import MyUser
from django.utils.translation import gettext_lazy as _
from user_management.models import User
import datetime
class Semester(models.TextChoices):
    Fall = "Fall"
    Summer = "Summer"
    Spring = "Spring"
    Winter = "Winter"

# class Course(models.Model):
#     courseID = models.IntegerField(primary_key=True, unique=True)
#     TAs = models.ManyToManyField(MyUser, related_name='ta_courses', limit_choices_to={'role':Roles.TA})
#     instructor = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name='instructed_courses', limit_choices_to={'role': Roles.Instructor})
#     # TAs = models.CharField(max_length=50)
#     # instructor = models.CharField(max_length=20)
#     name = models.CharField(max_length=50)
#     # description = models.CharField(max_length=50)
#     # requirements = models.CharField(max_length=50)
#     department = models.CharField(max_length=20)
#     sectionNumber = models.IntegerField()
#     semester = models.CharField(max_length=6, choices=Semester.choices)
#     year = models.PositiveIntegerField(default=datetime.date.today().year)
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
