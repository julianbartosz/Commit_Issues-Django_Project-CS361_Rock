from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils.translation import gettext_lazy as _


class UserManager(BaseUserManager):
    def get_by_natural_key(self, email):
        return self.get(**{self.model.USERNAME_FIELD: email})

    def create_user(self, email, first_name, last_name, password=None):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, first_name=first_name, last_name=last_name)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, first_name, last_name, password=None):
        user = self.create_user(
            email=self.normalize_email(email),
            password=password,
            first_name=first_name,
            last_name=last_name,
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    ROLE_CHOICES = (
        ('Supervisor', 'Supervisor/Administrator'),
        ('Instructor', 'Instructor'),
        ('TA', 'Teaching Assistant'),
        ('Student', 'Student')
    )

    email = models.EmailField(_('email address'), unique=True)
    first_name = models.CharField(_('first name'), max_length=150, blank=True)
    last_name = models.CharField(_('last name'), max_length=150, blank=True)
    role = models.CharField(_('role'), max_length=50, choices=ROLE_CHOICES, default='TA',
                            help_text=_('User role in the system'))
    phone = models.CharField(_('phone'), max_length=15, blank=True, null=True)
    address = models.CharField(_('address'), max_length=255, blank=True, null=True)

    emplid = models.CharField(_('emplid'), max_length=10, unique=True)
    person_id = models.CharField(_('person ID'), max_length=10, blank=True, null=True)
    epantherid = models.CharField(_('ePanther ID'), max_length=20, unique=True)
    classification = models.CharField(_('classification'), max_length=50, blank=True)
    school = models.CharField(_('school'), max_length=100, blank=True)
    year_in_school = models.CharField(_('year in school'), max_length=20, blank=True)
    building_name = models.CharField(_('building name'), max_length=100, blank=True)
    room_number = models.CharField(_('room number'), max_length=10, blank=True)

    is_active = models.BooleanField(_('active'), default=True)
    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    class Meta:
        app_label = 'user_management'
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def __str__(self):
        return self.email

    @classmethod
    def get_by_natural_key(cls, username):
        return cls.objects.get(**{cls.USERNAME_FIELD: username})

    def get_full_name(self):
        full_name = f'{self.first_name} {self.last_name}'.strip()
        return full_name or self.email

    def get_short_name(self):
        return self.first_name

    @property
    def is_staff(self):
        return self.role == 'Supervisor'

    @is_staff.setter
    def is_staff(self, value):
        if value is True:
            self.role = 'Supervisor'

    @property
    def is_superuser(self):
        return self.role == 'Supervisor'

    @is_superuser.setter
    def is_superuser(self, value):
        if value is True:
            self.role = 'Supervisor'

    def has_perm(self, perm, obj=None):
        return self.role == 'Supervisor'

    def has_module_perms(self, app_label):
        return self.role == 'Supervisor'

    @classmethod
    def create_user(cls, email, password=None, **extra_fields):
        if not email:
            raise ValueError(_('The Email must be set'))
        email = BaseUserManager.normalize_email(email)
        user = cls(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=cls._default_manager.db)
        return user

    @classmethod
    def create_superuser(cls, email, password, **extra_fields):
        extra_fields.setdefault('role', 'Supervisor')
        return cls.create_user(email, password, **extra_fields)
