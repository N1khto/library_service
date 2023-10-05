from rest_framework import mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet

from borrowings.models import Borrowing
from borrowings.serializers import BorrowingSerializer, BorrowingListDetailSerializer, BorrowingCreateSerializer


class BorrowingViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
    GenericViewSet
):
    queryset = Borrowing.objects.all()
    serializer_class = BorrowingSerializer
    permission_classes = (IsAuthenticated,)

    def get_serializer_class(self):
        if self.action in ("list", "retrieve"):
            return BorrowingListDetailSerializer
        if self.action == "create":
            return BorrowingCreateSerializer
        return BorrowingSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        queryset = self.queryset
        if not self.request.user.is_staff:
            queryset = queryset.filter(user__id=self.request.user.id)
        return queryset.distinct()
