from django.db import models
import datetime
# from .models import Course
# Create your models here.
class Roles(models.TextChoices):
    Admin = "Admin"
    Instructor = "Instructor"
    TA = "TA"

class Semester(models.TextChoices):
    Fall = "Fall"
    Summer = "Summer"
    Spring = "Spring"
    Winter = "Winter"

class MyUser(models.Model):
    email = models.EmailField(max_length=92,primary_key=True,unique=True)
    firstName = models.CharField(max_length=30)
    lastName = models.CharField(max_length=20)
    password = models.CharField(max_length=92)
    role = models.CharField(max_length=11,choices=Roles.choices)
    phoneNumber = models.PositiveIntegerField()
    streetAddress = models.CharField(max_length=30)
    city = models.CharField(max_length=28)
    state = models.CharField(max_length=20)
    zipCode = models.PositiveIntegerField()


    def __str__(self):
        return self.email

class Course(models.Model):
    courseID = models.IntegerField(primary_key=True, unique=True)
    TAs = models.ManyToManyField(MyUser, related_name='ta_courses', limit_choices_to={'role':Roles.TA})
    instructor = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name='instructed_courses', limit_choices_to={'role': Roles.Instructor})
    name = models.CharField(max_length=50)
    department = models.CharField(max_length=20)
    sectionNumber = models.IntegerField()
    semester = models.CharField(max_length=6, choices=Semester.choices)
    year = models.PositiveIntegerField(default=datetime.date.today().year)

class Lab(models.Model):
    labID = models.IntegerField(primary_key=True, unique=True)
    labSection = models.IntegerField()
    courseID = models.ForeignKey(Course, on_delete=models.CASCADE)
    instructor = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name='instructor_lab', limit_choices_to={'role':Roles.Instructor})
    TA = models.ForeignKey(MyUser, on_delete=models.SET_NULL, null=True, related_name='ta_lab', limit_choices_to={'role':Roles.TA})
   # name = str(courseID.name + " " + courseID.sectionNumber + "-" + labID)

'''class Course(models.Model):
  title = models.CharField(max_length=100)
  instructor = models.CharField(max_length=50)
  ta = models.CharField(max_length=100)
  description = models.TextField()
  requirements = models.TextField()

  def add_course(self, title, ta, instructor, description, requirements):
    # Create a new Course object and save it to the database
    course = Course(title=title,
                    instructor=instructor,
                    ta=ta,
                    description=description,
                    requirements=requirements)
    course.save()

def __str__(self):
  return self.title'''