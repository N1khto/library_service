from datetime import date

from django.db import transaction
from django.shortcuts import redirect
from rest_framework import mixins, status
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from books_inventory.models import Book
from borrowings.models import Borrowing
from borrowings.serializers import (
    BorrowingSerializer,
    BorrowingListSerializer,
    BorrowingDetailSerializer,
    BorrowingCreateSerializer,
)
from borrowings.notifications import borrow_notification
from payments.views import create_borrowing_payment


class BorrowingViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
    GenericViewSet,
):
    queryset = Borrowing.objects.select_related("book")
    serializer_class = BorrowingSerializer
    permission_classes = (IsAuthenticated,)

    def get_serializer_class(self):
        if self.action == "list":
            return BorrowingListSerializer
        if self.action == "retrieve":
            return BorrowingDetailSerializer
        if self.action == "create":
            return BorrowingCreateSerializer
        return BorrowingSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({"request": self.request})
        return context

    def perform_create(self, serializer):
        instance = serializer.save(user=self.request.user)
        borrow_notification(serializer.data)
        create_borrowing_payment(instance, serializer.context.get("request"))

    def get_queryset(self):
        is_active = self.request.query_params.get("is_active")
        queryset = self.queryset
        if self.request.user.is_staff:
            user_id = self.request.query_params.get("user_id")
            if user_id:
                queryset = queryset.filter(user__id=user_id)
        else:
            queryset = queryset.filter(user__id=self.request.user.id)
        if is_active:
            queryset = queryset.filter(actual_return_date__isnull=True)
        return queryset.distinct()

    @action(detail=True, methods=["post", "get"], url_path="return")
    def return_borrowing(self, request, pk=None):
        """Action used to return borrowed book.
        You cannot return book twice.
        Also you can return only book without 'actual_return_date'"""
        borrowing = self.get_object()
        book = get_object_or_404(Book, id=borrowing.book.id)
        if not borrowing.actual_return_date:
            with transaction.atomic():
                borrowing.actual_return_date = date.today()
                book.inventory += 1
                book.save()
                borrowing.save()
                return redirect(f"/api/borrowings/{pk}")

        return Response(
            data={"detail": "This book already returned"},
            status=status.HTTP_503_SERVICE_UNAVAILABLE,
        )
