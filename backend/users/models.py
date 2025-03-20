from datetime import datetime
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models
from django.contrib.auth.models import AbstractUser, PermissionsMixin
from django.contrib.auth.models import BaseUserManager


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
            raise ValueError("Superuser musi mieć is_staff=True")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser musi mieć is_superuser=True")

        return self.create_user(email, password, **extra_fields)


class User(AbstractUser, PermissionsMixin):
    # ROLE_CHOICES = [
    #     ('STUDENT', 'Student'),
    #     ('PARENT', 'Parent'),
    #     ('TEACHER', 'Teacher'),
    # ]
    # role = models.CharField(max_length=10, choices=ROLE_CHOICES)

    username_validator = UnicodeUsernameValidator()

    username = models.CharField(
        "username",
        max_length=150,
        unique=True,
        help_text="Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.",
        validators=[username_validator],
        error_messages={
            "unique": "A user with that username already exists.",
        },
    )
    first_name = models.CharField(
        "first name", max_length=150, default="John", blank=True
    )
    last_name = models.CharField("last name", max_length=150, default="Doe", blank=True)
    email = models.EmailField("email address", default="email@example.com")

    birth_date = models.DateField(default=datetime.date(2005, 1, 1))
    sex = models.CharField(
        max_length=32, choices=[("M", "Male"), ("F", "Female")], default="M"
    )
    # Phone number -
    # https://stackoverflow.com/questions/19130942/whats-the-best-way-to-store-a-phone-number-in-django-models

    objects = UserManager()

    def save(self, *args, **kwargs):
        """Ensure first and last names start with capital letters."""
        if self.first_name:
            self.first_name = self.first_name.capitalize()
        if self.last_name:
            self.last_name = self.last_name.capitalize()
        super().save(*args, **kwargs)
