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
    def post(self, request):
        try:
            checkout_session = stripe.checkout.Session.create(
                line_items=[
                    {
                        'price': 'price_1O0JC0F3PkC8kkFzwpSLHv6g',
                        'quantity': 1,
                    },
                ],
                mode='payment',
                success_url="http://127.0.0.1:8000/api/borrowings" + '/?success=true',
                cancel_url="http://127.0.0.1:8000/api/borrowings" + '/?cancelled=true',
            )
            return redirect(checkout_session.url)
        except Exception as e:
            return Response(
                {"error": "stripe session error"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

