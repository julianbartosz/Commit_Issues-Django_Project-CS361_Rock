from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    ROLE_CHOICES = (
        ('Supervisor', 'Supervisor/Administrator'),
        ('Instructor', 'Instructor'),
        ('TA', 'Teaching Assistant'),
    )

    email = models.EmailField(_('email address'), unique=True)
    role = models.CharField(max_length=25, choices=ROLE_CHOICES, default='TA', help_text=_('User role in the system'))
    phone = models.CharField(max_length=10, blank=True, null=True, help_text=_('Contact phone number'))
    address = models.CharField(max_length=95, blank=True, null=True, help_text=_('Home address'))

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    def __str__(self):
        return self.email
