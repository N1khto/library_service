from django.db import models

from borrowings.models import Borrowing


class Payment(models.Model):
    class StatusChoices(models.TextChoices):
        PENDING = "pending"
        PAID = "paid"

    class TypeChoices(models.TextChoices):
        PAYMENT = "payment"
        FINE = "fine"

    status = models.CharField(
        max_length=15, choices=StatusChoices.choices, default="pending"
    )
    type = models.CharField(
        max_length=15, choices=TypeChoices.choices, default="payment"
    )
    borrowing = models.ForeignKey(
        Borrowing, on_delete=models.CASCADE, related_name="payments"
    )
    session_url = models.URLField(max_length=255, null=True)
    session_id = models.CharField(max_length=255, null=True)
    money_to_pay = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self) -> str:
        return f"id: {self.session_id}. total: {self.money_to_pay}$"
