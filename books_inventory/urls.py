from rest_framework import routers

from books_inventory.views import BookViewSet

router = routers.DefaultRouter()
router.register("", BookViewSet)

urlpatterns = router.urls

app_name = "books"
