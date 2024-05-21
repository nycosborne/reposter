""" Views for the post app. """

from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import Post
from post import serializers


class PostViewSet(viewsets.ModelViewSet):
    """manage posts API."""
    serializer_class = serializers.PostSerializer
    queryset = Post.objects.all()  # Limits the queryset
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Return objects for the current authenticated user only."""
        return self.queryset.filter(user=self.request.user).order_by('-id')

    # def perform_create(self, serializer):
    #     """Create a new post."""
    #     serializer.save(user=self.request.user)
    #
    # def get_serializer_class(self):
    #     """Return appropriate serializer class."""
