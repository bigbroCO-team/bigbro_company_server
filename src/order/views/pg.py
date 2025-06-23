from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from core.authentication import CsrfExemptSessionAuthentication
from order.services.pg import PaymentService


class PGView(APIView):
    authentication_classes = (CsrfExemptSessionAuthentication, )
    permission_classes = (IsAuthenticated, )

    pg_service = PaymentService()

    def get(self, request: Request) -> Response:
        self.pg_service.process_payment(
            user=request.user,
            payment_key=request.GET.get('paymentKey'),
            order_id=request.GET.get('orderId'),
            amount=request.GET.get('amount')
        )
        return Response(
            headers={'Location': 'https://www.bigbro.company/success'},
            status=status.HTTP_302_FOUND
        )