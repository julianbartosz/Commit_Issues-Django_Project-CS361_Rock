from django.db import models

class Roles(models.TextChoices):
    Admin = "Admin"
    Instructor = "Instructor"
    TA = "TA"

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