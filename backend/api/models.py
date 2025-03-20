from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    description = models.TextField(blank=True)
    #image = models.ImageField(upload_to='products/', null=True, blank=True)

    def __str__(self):
        return f"{self.pk} {self.name}"