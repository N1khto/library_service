from rest_framework.permissions import AllowAny, BasePermission
from rest_framework.viewsets import ModelViewSet

from books_inventory.models import Book
from books_inventory.permissions import IsAdminOrIfAuthenticatedReadOnly
from books_inventory.serializers import BookSerializer


class BookViewSet(ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    def get_permissions(self) -> list[BasePermission]:
        if self.action == "list":
            permission_classes = (AllowAny,)
        else:
            permission_classes = (IsAdminOrIfAuthenticatedReadOnly,)
        return [permission() for permission in permission_classes]
