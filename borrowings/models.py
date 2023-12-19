from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Q, F

from books_inventory.models import Book


class Borrowing(models.Model):
    borrow_date = models.DateField(auto_now_add=True)
    expected_return_date = models.DateField()
    actual_return_date = models.DateField(null=True, blank=True)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f"Book:'{self.book.title}' borrowed by {self.user.email}"

    def clean(self) -> None:
        book = Book.objects.get(id=self.book.id)
        if book.inventory < 1:
            raise ValidationError(message="This book out of stock. Come back latter.")

    def save(
        self,
        force_insert=False,
        force_update=False,
        using=None,
        update_fields=None,
    ) -> None:
        self.full_clean()
        super(Borrowing, self).save(force_insert, force_update, using, update_fields)

    class Meta:
        ordering = ["-borrow_date"]
        constraints = [
            models.CheckConstraint(
                check=Q(expected_return_date__gt=F("borrow_date")),
                name="expected_return_date_not_before_borrow_date",
            ),
            models.CheckConstraint(
                check=Q(actual_return_date__gte=F("borrow_date")),
                name="actual_return_date_not_before_borrow_date",
            ),
        ]
