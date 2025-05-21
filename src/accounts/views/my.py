from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.serializers import MyInfoSerializer
from accounts.services.my import MyInfoService
from core.authentication import CsrfExemptSessionAuthentication


class MyInfoView(APIView):
    authentication_classes = [CsrfExemptSessionAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request: Request) -> Response:
        serializer = MyInfoSerializer(MyInfoService().get_my_info(request))
        return Response(serializer.data, status=status.HTTP_200_OK)