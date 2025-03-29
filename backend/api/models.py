from operator import is_
from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Product(models.Model):
    name = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    description = models.TextField(blank=True)
    # image = models.ImageField(upload_to='products/', null=True, blank=True)

    def __str__(self):
        return f"{self.pk} {self.name}"


class TrashPlace(models.Model):
    TRASH_LEVEL_CHOICES = [
        (1, "Light"),
        (2, "Moderate"),
        (3, "Extreme"),
    ]

    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    latitude = models.FloatField(blank=False, null=False)
    longitude = models.FloatField(blank=False, null=False)

    date_created = models.DateTimeField(blank=False, null=False, auto_now_add=True)

    trash_level = models.IntegerField(choices=TRASH_LEVEL_CHOICES, default=1)
    
    is_active = models.BooleanField(default=True, help_text="Is the trash place still there?")

    def __str__(self):
        return f"{self.name} ({self.pk}) {self.date_created}"


class Activity(models.Model):
    description = models.TextField(blank=True)
    date = models.DateTimeField(auto_now_add=True)
    trash_place = models.ForeignKey(
        TrashPlace, on_delete=models.CASCADE, related_name="cleanups"
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="activities")
    collected_kg = models.FloatField(
        blank=False, null=False, help_text="Kg of collected trash"
    )
    cleaned_all = models.BooleanField(
        default=False, help_text="Has the site been cleaned up completely?"
    )
    before_image = models.ImageField(
        upload_to="activity_images/before/",
        null=True,
        blank=True,
        help_text="Before cleanup image",
    )
    after_image = models.ImageField(
        upload_to="activity_images/after/",
        null=True,
        blank=True,
        help_text="After cleanup image",
    )

    def __str__(self):
        return f"Activity at {self.trash_place.name} ({self.pk}) on {self.date}"
