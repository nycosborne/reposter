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
from services import linkedinAPI
# Create your views here.


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
    def get(self, request, format=None):
        # linkedin_api = LinkedInAPI()
        # request_code = linkedin_api.request_code()
        print(f"Request method: {request.method}")
        print(f"Request data: {request.data}")
        print(f"GET parameters: {request.GET}")
        print(f"POST data: {request.POST}")

        return Response({"message": 'request_code'})
