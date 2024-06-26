""" Test for the user API. """
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

CREATE_USER_URL = reverse('user:create')
TOKEN_URL = reverse('user:token')
ME_URL = reverse('user:me')


def create_user(**params):
    """Helper function to create a user for testing."""
    return get_user_model().objects.create_user(**params)


class PublicUserApiTests(TestCase):
    """Test the users API (public)."""

    def setUp(self):
        """Setup function for the user API test case."""
        # Create a client
        self.client = APIClient()
        self.payload = {
            'email': 'test@example.com',
            'password': 'password123',
            'first_name': 'Jim',
            'last_name': 'Django',
            'reddit': 'True',
            'linkedin': 'False',
        }

    def test_create_valid_user_success(self):
        """Test creating a user with valid payload is successful."""
        response = self.client.post(CREATE_USER_URL, self.payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # Get the user object from the database by email
        user = get_user_model().objects.get(email=self.payload['email'])
        # Check that the password is correct
        self.assertTrue(user.check_password(self.payload['password']))
        # Check that the password is not returned in the response
        self.assertNotIn('password', response.data)

    def test_user_exists(self):
        """Test creating a user that already exists fails."""
        payload = {
            'email': 'test@example.com',
            'password': 'password123',
            'first_name': 'Jim',
            'last_name': 'Django',
            'reddit': 'True',
            'linkedin': 'False',
        }

        create_user(**payload)

        response = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_too_short(self):
        short_password_payload = {
            'email': 'test@example.com',
            'password': '1',
            'first_name': 'Jim',
            'last_name': 'Django',
        }

        """Test that the password must be more than 5 characters."""
        response = self.client.post(CREATE_USER_URL, short_password_payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        user_exists = get_user_model().objects.filter(
            email=short_password_payload['email']
        ).exists()
        self.assertFalse(user_exists)

    def test_create_token_for_user(self):  # todo: JWT update required
        """Test that a token is created for the user."""
        # create a user
        create_user(**self.payload)

        response_payload = {
            'email': self.payload['email'],
            'password': self.payload['password']
        }
        # login the user and get the token
        response = self.client.post(TOKEN_URL, response_payload)
        self.assertIn('token', response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # todo: JWT update required
    def test_create_token_invalid_credentials(self):
        """Test that token is not created if invalid credentials are given."""
        """Test that a token is created for the user."""
        # create a user
        create_user(**self.payload)
        payload = {
            'email': 'test@example.com',
            'password': 'bad_pass1234'
        }

        response = self.client.post(TOKEN_URL, payload)
        self.assertNotIn('token', response.data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_retrieve_user_unauthorized(self):
        """Test that authentication is required for users."""
        response = self.client.get(ME_URL)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateUserApiTests(TestCase):
    """Test API requests that require authentication."""

    def setUp(self):
        """Setup function for the user API test case."""
        """Create a user and authenticate the client."""
        self.user = create_user(
            email='test@example.com',
            password='password123',
            first_name='Jim',
            last_name='Django'

        )

        self.client = APIClient()
        # todo: JWT update required (maybe)
        self.client.force_authenticate(user=self.user)

    def test_retrieve_profile_success(self):
        """Test retrieving profile for logged in used."""
        response = self.client.get(ME_URL)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {
            'first_name': self.user.first_name,
            'last_name': self.user.last_name,
            'email': self.user.email,
            'reddit': self.user.reddit,
            'linkedin': self.user.linkedin,
        })

    def test_post_me_not_allowed(self):
        """Test that POST is not allowed on the ME URL."""
        response = self.client.post(ME_URL, {})

        self.assertEqual(response.status_code,
                         status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_update_user_profile(self):
        """Test updating the user profile for authenticated user."""
        payload = {
            'first_name': 'New',
            'last_name': 'Name',
            'password': 'newpassword123'
        }

        response = self.client.patch(ME_URL, payload)

        self.user.refresh_from_db()
        self.assertEqual(self.user.first_name, payload['first_name'])
        self.assertEqual(self.user.last_name, payload['last_name'])
        self.assertTrue(self.user.check_password(payload['password']))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
