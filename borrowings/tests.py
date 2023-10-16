from datetime import date

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from borrowings.models import Borrowing
from books_inventory.tests import sample_book
from borrowings.serializers import BorrowingListSerializer, BorrowingDetailSerializer

BORROWINGS_URL = reverse("borrowings:borrowing-list")


def sample_borrowing(**params):
    defaults = {
        "expected_return_date": "2100-01-01",
        "actual_return_date": None,
        "book": sample_book(),
        "user": None
    }
    defaults.update(params)

    return Borrowing.objects.create(**defaults)


def detail_url(borrowing_id):
    return reverse("borrowings:borrowing-detail", args=[borrowing_id])


def return_url(borrowing_id):
    """Return URL used to return borrowing"""
    return reverse("borrowings:borrowing-return-borrowing", args=[borrowing_id])


class UnauthenticatedBorrowingApiTest(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        res = self.client.get(BORROWINGS_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class AuthenticatedBorrowingApiTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            "test@user.com",
            "testpass",
        )
        self.client.force_authenticate(self.user)

    def test_list_borrowings(self):
        sample_borrowing(expected_return_date="2100-01-01", user=self.user)
        sample_borrowing(expected_return_date="2100-01-02", user=self.user)
        sample_borrowing(expected_return_date="2100-01-03", user=self.user)

        res = self.client.get(BORROWINGS_URL)

        borrowings = Borrowing.objects.all()
        serializer = BorrowingListSerializer(borrowings, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_retrieve_borrowing_detail(self):
        self.borrowing1 = sample_borrowing(expected_return_date="2100-01-01", user=self.user)
        url = detail_url(borrowing_id=self.borrowing1.id)
        res = self.client.get(url)

        serializer = BorrowingDetailSerializer(self.borrowing1)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_create_borrowing(self):
        book = sample_book()
        return_date = date(2100, 1, 1)
        payload = {
            "expected_return_date": return_date,
            "book": book.id,
            "user": self.user.id
        }

        res = self.client.post(BORROWINGS_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Borrowing.objects.count(), 1)
        self.assertEqual(Borrowing.objects.get().expected_return_date, return_date)
        self.assertEqual(Borrowing.objects.get().book.id, book.id)
        self.assertEqual(Borrowing.objects.get().user.id, self.user.id)

    def test_delete_borrowing_prohibited(self):
        borrowing = sample_borrowing(user=self.user)

        url = detail_url(borrowing.id)

        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_filter_active_borrowings(self):
        borrowing1 = sample_borrowing(expected_return_date="2100-01-01", user=self.user)
        borrowing2 = sample_borrowing(expected_return_date="2100-01-02", actual_return_date="2099-01-02", user=self.user)
        res = self.client.get(BORROWINGS_URL, {"is_active": True})

        serializer1 = BorrowingListSerializer(borrowing1)
        serializer2 = BorrowingListSerializer(borrowing2)

        self.assertIn(serializer1.data, res.data)
        self.assertNotIn(serializer2.data, res.data)

    def test_action_return_borrowing(self):
        borrowing1 = sample_borrowing(expected_return_date="2100-01-01", user=self.user)

        url = return_url(borrowing1.id)

        res = self.client.post(url, {})

        serializer = BorrowingDetailSerializer(borrowing1)

        self.assertEqual(res.status_code, status.HTTP_302_FOUND)
        self.assertIn("actual_return_date", serializer.data)


class AdminBorrowingApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            "admin@test.com",
            "admintestpass",
            is_staff=True,
        )
        self.sample_user = get_user_model().objects.create_user(
            "user@test.com",
            "usertestpass",
        )
        self.client.force_authenticate(self.user)
        self.borrowing1 = sample_borrowing(expected_return_date="2100-01-01", user=self.user)
        self.borrowing2 = sample_borrowing(expected_return_date="2100-01-02", user=self.sample_user)

    def test_filter_users_borrowings(self):
        res = self.client.get(BORROWINGS_URL, {"user_id": self.sample_user.id})

        serializer1 = BorrowingListSerializer(self.borrowing1)
        serializer2 = BorrowingListSerializer(self.borrowing2)

        self.assertNotIn(serializer1.data, res.data)
        self.assertIn(serializer2.data, res.data)
