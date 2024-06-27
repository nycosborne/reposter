""" Views for the post app. """

# from drf_spectacular.utils import (
#     extend_schema,
#     extend_schema_view,
#     OpenApiParameter,
#     OpenApiTypes,
# )
from rest_framework import viewsets

from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import IsAdminUser
from rest_framework.permissions import AllowAny

from core.models import SocialAccounts
from services import serializers as servicesSerializers


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
