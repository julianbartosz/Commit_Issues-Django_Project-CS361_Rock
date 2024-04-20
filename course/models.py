from django.db import models
# from .models import Course
# Create your models here.
class Course(models.Model):
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
  return self.title