from django.db import models


class Book(models.Model):
    class CoverChoices(models.TextChoices):
        HARD = "hard"
        SOFT = "soft"

    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    cover = models.CharField(max_length=15, choices=CoverChoices.choices, null=True)
    inventory = models.PositiveSmallIntegerField(default=0)
    daily_fee = models.DecimalField(max_digits=8, decimal_places=2, null=True)

    def __str__(self) -> str:
        return f"'{self.title}' by {self.author}"
