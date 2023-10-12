from datetime import date

import stripe
from django.shortcuts import redirect

from rest_framework import mixins, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet
from django.conf import settings

from payments.models import Payment
from payments.serializers import PaymentSerializer


stripe.api_key = settings.STRIPE_SECRET_KEY
TEST_DEFAULT_URL = "http://127.0.0.1:8000/api/borrowings"
TEST_PRODUCT = "prod_Onv2XTbUzEHGrp"


class PaymentViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    GenericViewSet,
):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        queryset = self.queryset
        if not self.request.user.is_staff:
            queryset = queryset.filter(borrowing__user__id=self.request.user.id)
        return queryset.distinct()


class StripeCheckoutView(APIView):
    """view for testing stripe session creation"""

    def post(self, request):
        try:
            checkout_session = stripe.checkout.Session.create(
                line_items=[
                    {
                        "price": "price_1O0JC0F3PkC8kkFzwpSLHv6g",
                        "quantity": 1,
                    },
                ],
                mode="payment",
                success_url=TEST_DEFAULT_URL + "/?success=true",
                cancel_url=TEST_DEFAULT_URL + "/?cancelled=true",
            )
            return redirect(checkout_session.url)
        except Exception as e:
            return Response(
                {"error": "stripe session error"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


def create_borrowing_payment(borrowing):
    """function used to receive borrowing instance, calculate total price of
    borrowing and create related payment instance. Then create new stripe checkout session
    and attach session_id and session_url to payment instance"""
    money_to_pay = (
        borrowing.expected_return_date - date.today()
    ).days * borrowing.book.daily_fee
    payment = Payment.objects.create(borrowing=borrowing, money_to_pay=money_to_pay)
    price = stripe.Price.create(
        unit_amount=int(payment.money_to_pay * 100),
        currency="usd",
        product=TEST_PRODUCT,
    )
    checkout_session = stripe.checkout.Session.create(
        line_items=[
            {
                "price": price,
                "quantity": 1,
            },
        ],
        mode="payment",
        success_url=TEST_DEFAULT_URL + "/?success=true",
        cancel_url=TEST_DEFAULT_URL + "/?cancelled=true",
    )
    payment.session_url = checkout_session.get("url")
    payment.session_id = checkout_session.get("id")
    payment.save()
