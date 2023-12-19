import datetime
import requests

from django.conf import settings
from django.contrib.auth import get_user_model
from rest_framework.generics import get_object_or_404

from books_inventory.models import Book
from borrowings.models import Borrowing

URL = settings.BOT_URL
my_chat_id = settings.CHAT_ID


def borrow_notification(data, chat_id=my_chat_id) -> None:
    """Telegram notification triggered on every new borrowing creation"""
    book = get_object_or_404(Book, id=data.get("book"))
    user = get_object_or_404(get_user_model(), id=data.get("user"))
    return_date = data.get("expected_return_date")
    requests.get(
        f"{URL}/sendMessage?chat_id={chat_id}&text={user.email} took {book}. "
        f"Make sure return it by {return_date}."
    )


def overdue_borrowings(chat_id=my_chat_id) -> None:
    """Telegram notification for displaying list of overdue borrowings in group chat"""
    overdue = Borrowing.objects.filter(
        actual_return_date__isnull=True,
        expected_return_date__lte=datetime.date.today() + datetime.timedelta(1),
    )
    if overdue:
        for borrowing in overdue:
            requests.get(
                f"{URL}/sendMessage?chat_id={chat_id}&text={borrowing.user.email} "
                f"should return book {borrowing.book} by {borrowing.expected_return_date}."
            )
    else:
        requests.get(
            f"{URL}/sendMessage?chat_id={chat_id}&text=There is no overdue borrowings for now"
        )
