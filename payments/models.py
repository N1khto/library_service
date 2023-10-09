from django.db import models

from borrowings.models import Borrowing


class Payment(models.Model):
    class StatusChoices(models.TextChoices):
        PENDING = "pending"
        PAID = "paid"

    class TypeChoices(models.TextChoices):
        PAYMENT = "payment"
        FINE = "fine"

    status = models.CharField(max_length=15, choices=StatusChoices.choices)
    type = models.CharField(max_length=15, choices=TypeChoices.choices)
    borrowing = models.ForeignKey(Borrowing, on_delete=models.CASCADE)
    session_url = models.URLField(max_length=255)
    session_id = models.CharField(max_length=255)
    money_to_pay = models.DecimalField(max_digits=10, decimal_places=2)
