"""
Serializers for the api end points of the user
"""

from django.contrib.auth import (
    get_user_model,
    authenticate,
)

from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed
from core.models import SocialAccounts


class SocialAccountsSerializer(serializers.ModelSerializer):
    """Serializer for social accounts objects"""

    class Meta:
        model = SocialAccounts
        fields = ['id', 'name']
        read_only_fields = ['id']


class UserSerializers(serializers.ModelSerializer):
    """Serializers for the user object."""
    soc_accounts = SocialAccountsSerializer(many=True, required=False)

    class Meta:
        model = get_user_model()
        fields = ('email', 'password', 'first_name', 'last_name', 'soc_accounts')
        extra_kwargs = {'password': {'write_only': True, 'min_length': 5}}

    def create(self, validated_data):
        """Create a new user with encrypted password and return it."""
        return get_user_model().objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        """Update a user, setting the password correctly and return it."""
        password = validated_data.pop('password', None)
        user = super().update(instance, validated_data)

        if password:
            user.set_password(password)
            user.save()

        return user


class AuthTokenSerializer(serializers.Serializer):  # todo: JWT Update this
    """Serializer for the user authentication object."""
    email = serializers.CharField()
    password = serializers.CharField(
        style={'input_type': 'password'},
        trim_whitespace=False
    )

    def validate(self, attrs):
        """Validate and authenticate the user."""
        email = attrs.get('email')
        password = attrs.get('password')

        user = authenticate(
            request=self.context.get('request'),
            username=email,
            password=password
        )

        if not user:
            raise AuthenticationFailed(
                'Sorry, I can\'t find a account with that email and pass.',
                code='authentication'
            )

        attrs['user'] = user
        # Add this line to get the user id in the response
        # attrs['id'] = user.id
        return attrs
