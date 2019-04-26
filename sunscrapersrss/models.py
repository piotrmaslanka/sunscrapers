from django.db import models


# Create your models here.
class CurrencyRate(models.Model):
    currency_from = models.TextField(max_length=3)
    currency_to = models.TextField(max_length=3)
    currency_rate = models.FloatField()
    currency_date = models.DateField()

    class Meta:
        indexes = [
            models.Index(
                fields=['currency_from', 'currency_to', 'currency_date'])
        ]
