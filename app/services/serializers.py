"""
Serializers for the api end points of the post
"""

from rest_framework import serializers

from core.models import SocialAccounts
from services.linkedinAPI import LinkedInAPI  # Modify this line


class SocialAccountsSerializer(serializers.ModelSerializer):
    """Serializer for social accounts objects"""

    class Meta:
        model = SocialAccounts
        fields = ['id', 'name']
        read_only_fields = ['id']

    def create(self, validated_data):
        """Create a new social account and return it."""
        return SocialAccounts.objects.create(**validated_data)


class CodeSerializer(serializers.Serializer):
    code = serializers.CharField(required=True)

    def save(self):
        linkedin_api = LinkedInAPI()
        code = self.validated_data['code']
        linkedin_api.get_access_token(code)
