from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from books_inventory.models import Book
from books_inventory.serializers import BookSerializer

BOOK_URL = reverse("books:book-list")


def sample_book(**params) -> Book:
    defaults = {
        "title": "Bible",
        "author": "Unknown",
        "cover": "hard",
        "inventory": 666,
        "daily_fee": 13,
    }
    defaults.update(params)

    return Book.objects.create(**defaults)


def detail_url(book_id) -> str:
    return reverse("books:book-detail", args=[book_id])


class UnauthenticatedBookApiTest(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        self.book1 = sample_book()

    def test_list_auth_dont_required(self) -> None:
        res = self.client.get(BOOK_URL)
        self.assertEquals(res.status_code, status.HTTP_200_OK)

    def test_retrieve_auth_required(self) -> None:
        url = detail_url(book_id=self.book1.id)
        res = self.client.get(url)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class AuthenticatedBookApiTest(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            "test@user.com",
            "testpass",
        )
        self.client.force_authenticate(self.user)
        self.book1 = sample_book(title="first")
        self.book2 = sample_book(title="second")
        self.book3 = sample_book(title="third")

    def test_list_books(self) -> None:
        res = self.client.get(BOOK_URL)

        books = Book.objects.all()
        serializer = BookSerializer(books, many=True)

        self.assertEquals(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_retrieve_book_detail(self) -> None:
        url = detail_url(book_id=self.book1.id)
        res = self.client.get(url)

        serializer = BookSerializer(self.book1)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_create_book_forbidden(self) -> None:
        payload = {
            "title": "Bible",
            "author": "Unknown",
            "cover": "hard",
            "inventory": 666,
            "daily_fee": 13,
        }
        res = self.client.post(BOOK_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)


class AdminBookApiTests(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            "admin@test.com",
            "admintestpass",
            is_staff=True,
        )
        self.client.force_authenticate(self.user)
        self.book1 = sample_book(title="first")

    def test_create_book(self) -> None:
        payload = {
            "title": "Bible",
            "author": "Unknown",
            "cover": "hard",
            "inventory": 666,
            "daily_fee": 13,
        }

        res = self.client.post(BOOK_URL, payload)
        book = Book.objects.get(id=res.data["id"])

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        for key in payload:
            self.assertEqual(payload[key], getattr(book, key))

    def test_delete_book(self) -> None:
        book = sample_book()

        url = detail_url(book.id)

        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
