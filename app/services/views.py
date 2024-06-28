""" Views for the post app. """

# from drf_spectacular.utils import (
#     extend_schema,
#     extend_schema_view,
#     OpenApiParameter,
#     OpenApiTypes,
# )
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import IsAdminUser
from rest_framework.permissions import AllowAny

from core.models import SocialAccounts
from services import serializers as servicesSerializers

class SocialAccountsViewSet(viewsets.ModelViewSet):
    """Manage social accounts in the database."""
    serializer_class = servicesSerializers.SocialAccountsSerializer
    queryset = SocialAccounts.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions
        that this view requires.
        """
        if self.action in ['list', 'retrieve']:
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]


class ReceivingCode(APIView):
    serializer_class = servicesSerializers.CodeSerializer
    # TODO: commented for deving
    # authentication_classes = [TokenAuthentication]
    # permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        serializer = servicesSerializers.CodeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "request_code"})
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
