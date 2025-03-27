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


class Event(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(blank=True)

    date_start = models.DateTimeField(blank=False, null=False)
    latitude = models.FloatField(blank=False, null=False)
    longitude = models.FloatField(blank=False, null=False)
    # type = models.CharField(max_length=64, choices=TYPE_CHOICES, default="OTHER", blank=False)
    # participants = models.ManyToManyField(User, related_name="events", blank=True)  # Dodanie uczestników

    def __str__(self):
        return f"{self.name} ({self.pk}) {self.date_start}"
