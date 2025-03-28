import datetime
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models
from django.contrib.auth.models import AbstractUser, PermissionsMixin
from django.contrib.auth.models import BaseUserManager
from django.utils import timezone
from phone_field import PhoneField
import logging

logger = logging.getLogger(__name__)


class UserManager(BaseUserManager):

    def create_user(self, email, password=None, **extra_fields):
        """Create and save a User with the given email and password."""
        if not email:
            raise ValueError("User has to have an email address")

        email = self.normalize_email(email)

        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser has to have is_staff=True")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser has to have is_superuser=True")

        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField("email address", unique=True)
    first_name = models.CharField(
        "1st name", max_length=150, default="John", blank=True
    )
    last_name = models.CharField("last name", max_length=150, default="Doe", blank=True)

    birth_date = models.DateField(default=datetime.date(2005, 1, 1))
    phone_number = PhoneField(
        blank=True, null=False, help_text="Numer telefonu w formacie +48 123 456 789"
    )

    date_joined = models.DateTimeField("date joined", default=timezone.now)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def save(self, *args, **kwargs):
        """Ensure first and last names start with capital letters."""
        if self.first_name:
            self.first_name = self.first_name.lower().capitalize()
        if self.last_name:
            self.last_name = self.last_name.lower().capitalize()
        if self.pk:
            logger.info(f"Updating user {self.pk}: {self.email}")
        else:
            logger.info(f"Creating new user: {self.email}")
        super().save(*args, **kwargs)

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    def delete(self, *args, **kwargs):
        logger.warning(f"Deleting user {self.pk}: {self.email}")
        super().delete(*args, **kwargs)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    # username_validator = UnicodeUsernameValidator()

    # Usefull fields:
    # ROLE_CHOICES = [
    #     ('STUDENT', 'Student'),
    #     ('PARENT', 'Parent'),
    #     ('TEACHER', 'Teacher'),
    # ]
    # role = models.CharField(max_length=32, choices=ROLE_CHOICES)
    # sex = models.CharField(max_length=32, choices=[("M", "Male"), ("F", "Female")], default="M")
    # Phone number -
    # https://stackoverflow.com/questions/19130942/whats-the-best-way-to-store-a-phone-number-in-django-models
