from django.db import models
from user_management.models import MyUser, Roles
import datetime
class Semester(models.TextChoices):
    Fall = "Fall"
    Summer = "Summer"
    Spring = "Spring"
    Winter = "Winter"

class Course(models.Model):
    courseID = models.IntegerField(primary_key=True, unique=True)
    TAs = models.ManyToManyField(MyUser, related_name='ta_courses', limit_choices_to={'role':Roles.TA})
    instructor = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name='instructed_courses', limit_choices_to={'role': Roles.Instructor})
    name = models.CharField(max_length=50)
    department = models.CharField(max_length=20)
    sectionNumber = models.IntegerField()
    semester = models.CharField(max_length=6, choices=Semester.choices)
    year = models.PositiveIntegerField(default=datetime.date.today().year)
