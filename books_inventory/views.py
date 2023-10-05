from rest_framework.permissions import AllowAny
from rest_framework.viewsets import ModelViewSet

from books_inventory.models import Book
from books_inventory.serializers import BookSerializer


class BookViewSet(ModelViewSet):
    queryset = Book.objects.all()
    Permission_classes = AllowAny
    serializer_class = BookSerializer
