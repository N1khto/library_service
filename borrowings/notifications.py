import requests

from django.conf import settings
from django.contrib.auth import get_user_model
from rest_framework.generics import get_object_or_404

from books_inventory.models import Book

URL = settings.BOT_URL
my_chat_id = settings.CHAT_ID


def borrow_notification(data, chat_id=my_chat_id):
    book = get_object_or_404(Book, id=data.get("book"))
    user = get_object_or_404(get_user_model(), id=data.get("user"))
    return_date = data.get("expected_return_date")
    requests.get(
        f"{URL}/sendMessage?chat_id={chat_id}&text={user.email} took {book}. "
        f"Make sure return it by {return_date}."
    )
