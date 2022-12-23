from django.db import models


# Create your models here.
class Payment(models.Model):
    value = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3)
    description = models.TextField()

    def __str__(self):
        return self.description
