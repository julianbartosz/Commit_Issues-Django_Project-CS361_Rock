from django.db import models
class User(models.Model):
    email = models.CharField(max_length=254, primary_key=True, unique=True)
    username = models.CharField(max_length=18, unique=True)
    password = models.CharField(max_length=32)
    phone = models.CharField(max_length=10, unique=True)
    address = models.CharField(max_length=95)

