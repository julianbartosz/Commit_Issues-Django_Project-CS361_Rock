from django.test import TestCase
from course_management.models import Course
# Create your tests here.


class CourseTestCase(TestCase):

  def setUp(self):
    self.course = Course.objects.create(title="Math",
                                        description="math is good",
                                        instructor="rock",
                                        requirements="nothing")

  def test_course_creation(self):
    # Test creating a new Course instance
    self.assertEqual(self.course.title, "Math")
    self.assertEqual(self.course.description, "math is good")
    self.assertEqual(self.course.instructor, "rock")
    self.assertEqual(self.course.requirements, "nothing")

  def test_class_already_stored(self):
    # Check if the class is already stored in the database
    self.course = Course.objects.create(title="Math",
                                        description="lol",
                                        instructor="adas",
                                        requirements="kmvds")
    course_exists = Course.objects.filter(title="Math",
                                          description="lol",
                                          instructor="adas",
                                          requirements="kmvds").exists()
    self.assertTrue(course_exists)