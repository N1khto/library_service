from django.urls import path, include
from rest_framework import routers

from payments.views import PaymentViewSet, StripeCheckoutView

router = routers.DefaultRouter()
router.register("", PaymentViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path("create-checkout", StripeCheckoutView.as_view(), name="create_checkout")
]

app_name = "payments"
