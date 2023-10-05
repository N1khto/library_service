from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import Q, F

from books_inventory.models import Book


class Borrowing(models.Model):
    borrow_date = models.DateField(auto_now_add=True)
    expected_return_date = models.DateField()
    actual_return_date = models.DateField(null=True, blank=True)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)

    def __str__(self):
        return f"Book:'{self.book.title}' borrowed by {self.user.email}"

    class Meta:
        ordering = ["-borrow_date"]
        constraints = [
            models.CheckConstraint(
                check=Q(expected_return_date__gt=F("borrow_date")),
                name="expected_return_date_not_before_borrow_date",
            ),
            models.CheckConstraint(
                check=Q(actual_return_date__gt=F("borrow_date")),
                name="actual_return_date_not_before_borrow_date",
            ),
        ]
