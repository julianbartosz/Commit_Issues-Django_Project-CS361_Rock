from django.db import models
class Roles(models.TextChoices):
    Admin = "Admin"
    Instructor = "Instructor"
    TA = "TA"


class MyUser(models.Model):
    email = models.EmailField(max_length=92,primary_key=True,unique=True)
    password = models.CharField(max_length=92)
    role = models.CharField(max_length=11,choices=Roles.choices)

    def __str__(self):
        return self.email


