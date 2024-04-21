from django.db import models
from user_management.models import MyUser, Roles
from course_management.models import Course
class Lab(models.Model):
    labID = models.IntegerField(primary_key=True, unique=True)
    labSection = models.IntegerField()
    courseID = models.ForeignKey(Course, on_delete=models.CASCADE)
    instructor = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name='instructor_lab', limit_choices_to={'role':Roles.Instructor})
    TA = models.ForeignKey(MyUser, on_delete=models.SET_NULL, null=True, related_name='ta_lab', limit_choices_to={'role':Roles.TA})
   # name = str(courseID.name + " " + courseID.sectionNumber + "-" + labID)