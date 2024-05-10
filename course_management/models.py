from django.db import models
from datetime import datetime
from user_management.models import User
from django.utils.translation import gettext_lazy as _


class Course(models.Model):
    code = models.CharField(max_length=10, unique=True, help_text=_("Enter the unique course code."))
    title = models.CharField(max_length=100, help_text=_("Enter the full title of the course."))

    class Meta:
        app_label = 'course_management'
        ordering = ['code']

    def __str__(self):
        return f"{self.code} - {self.title}"


SEMESTER_DATES = {
    'Spring': ('01-22', '05-09'),
    'Summer': ('06-24', '08-17'),
    'Fall': ('09-03', '12-12'),
    'UWinteriM': ('01-02', '01-20'),
}


class Section(models.Model):
    SECTION_TYPES = [
        ('LEC', 'Lecture'),
        ('LAB', 'Lab'),
        ('SEM', 'Seminar'),
        ('DIS', 'Discussion'),
        ('IND', 'Individual'),
        ('FLD', 'Field')
    ]

    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='sections', help_text="Select the associated course.")
    number = models.CharField(max_length=10, help_text="Enter the section number.")
    section_type = models.CharField(max_length=3, choices=SECTION_TYPES, help_text="Select the section type.")
    crn = models.CharField(max_length=10, unique=True, help_text="Enter the Course Reference Number (CRN) for the section.")
    instructional_method = models.CharField(max_length=50, default='Unknown', help_text=_("Specify the instructional method (e.g., 'In Person', 'Online')."))
    max_enrollment = models.IntegerField(help_text="Maximum enrollment for the section", null=True, blank=True)
    meeting_time = models.CharField(max_length=100, help_text="Time and days when the section meets", null=True, blank=True)
    meeting_room = models.CharField(max_length=100, help_text="Room where the section meets", null=True, blank=True)
    campus = models.CharField(max_length=100, help_text="Specify the campus where the section meets.")
    start_date = models.DateField(help_text="Enter the start date of the section.")
    end_date = models.DateField(help_text="Enter the end date of the section.")
    course_credits = models.CharField(max_length=10, help_text="HTML field for possible credit hours for the course", null=True, blank=True)
    credits = models.IntegerField(help_text="Enter the number of credits for the section.", null=True, blank=True)
    is_cancelled = models.BooleanField(default=False, help_text="Is this course cancelled? If yes, check this box")
    semester = models.CharField(max_length=20, help_text="Automatically set based on start date")
    year = models.IntegerField(help_text="Automatically set based on start date")
    instructor = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='sections_taught', help_text=_("Select the section instructor."))
    tas = models.ManyToManyField(User, related_name='assisting_sections', help_text=_("Select the teaching assistants for the section."))
    registration_restrictions = models.TextField(help_text="Any restrictions or prerequisites for registration", null=True, blank=True)
    class_notes = models.TextField(help_text="Notes related to the section", null=True, blank=True)
    attribute_description = models.CharField(max_length=100, help_text="Attribute description of the section", null=True, blank=True)

    def save(self, *args, **kwargs):
        if self.start_date is not None:
            # Determine the semester based on the start date
            for semester, (start_str, end_str) in SEMESTER_DATES.items():
                start_month, start_day = map(int, start_str.split('-'))
                end_month, end_day = map(int, end_str.split('-'))

                start_date = datetime(self.start_date.year, start_month, start_day)
                end_date = datetime(self.start_date.year, end_month, end_day)

                if start_date <= self.start_date <= end_date:
                    self.semester = semester
                    break
            else:
                self.semester = 'Unknown'   # Default to 'Unknown'

            # Assign the year from the start date
            self.year = self.start_date.year

        super().save(*args, **kwargs)

    class Meta:
        app_label = 'course_management'
        ordering = ['course', 'number']
        unique_together = ['course', 'number']

    def __str__(self):
        return f"{self.course.code} {self.number} ({self.section_type})"
