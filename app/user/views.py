"""
This file defines the views for the user app.
"""

from rest_framework import generics, authentication, permissions
# todo: JWT update required
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings
# from rest_framework.authtoken.models import Token
# from rest_framework.response import Response

from user.serializers import (
    UserSerializers,
    AuthTokenSerializer,  # todo: JWT update required
)


class CreateUserView(generics.CreateAPIView):
    """Create a new user in the system."""
    serializer_class = UserSerializers


class CreateTokenView(ObtainAuthToken):  # todo: JWT update required
    """Create a new auth token for the user."""
    serializer_class = AuthTokenSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES

    # Add this method to get the user id in the response
    # def post(self, request, *args, **kwargs):
    #     serializer = self.serializer_class(data=request.data,
    #                                        context={'request': request})
    #     serializer.is_valid(raise_exception=True)
    #     user = serializer.validated_data['user']
    #     token, created = Token.objects.get_or_create(user=user)
    #     return Response({
    #         'token': token.key,
    #         'id': serializer.validated_data['id'],  # Add this line
    #     })


# RetrieveUpdateAPIView is used for get and patch/put request
class ManageUserView(generics.RetrieveUpdateAPIView):
    """Manage the authenticated user."""
    serializer_class = UserSerializers
    # todo: JWT update required
    authentication_classes = [authentication.TokenAuthentication]
    # todo: JWT update required
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        """Retrieve and return authenticated user. """
        return self.request.user
