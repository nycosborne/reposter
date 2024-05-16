""" Test for the user API. """
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

CREATE_USER_URL = reverse('user:create')
TOKEN_URL = reverse('user:token')


def create_user(**params):
    """Helper function to create a user for testing."""
    return get_user_model().objects.create_user(**params)


class PublicUserApiTests(TestCase):
    """Test the users API (public)."""

    def setUp(self):
        """Setup function for the user API test case."""
        # Create a client
        self.client = APIClient()

    def test_create_valid_user_success(self):
        """Test creating a user with valid payload is successful."""
        payload = {
            'email': 'test@example.com',
            'password': 'password123',
            'name': 'Test Name'
        }

        response = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # Get the user object from the database by email
        user = get_user_model().objects.get(email=payload['email'])
        # Check that the password is correct
        self.assertTrue(user.check_password(payload['password']))
        # Check that the password is not returned in the response
        self.assertNotIn('password', response.data)

    def test_user_exists(self):
        """Test creating a user that already exists fails."""
        payload = {
            'email': 'test@example.com',
            'password': 'password123',
            'name': 'Test Name'
        }

        create_user(**payload)

        response = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_too_short(self):
        """Test that the password must be more than 5 characters."""
        payload = {
            'email': 'test@example.com',
            'password': 'pw',
            'name': 'Test Name'
        }

        response = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        user_exists = get_user_model().objects.filter(
            email=payload['email']
        ).exists()
        self.assertFalse(user_exists)

    # todo: JWT update required
    def test_create_token_for_user(self):
        """Test that a token is created for the user."""
        user_details = {
            'name': 'Test Name',
            'email': 'test@example.com',
            'password': 'testUserpass1234'
        }
        # create a user
        create_user(**user_details)

        payload = {
            'email': user_details['email'],
            'password': user_details['password']
        }
        # login the user and get the token
        response = self.client.post(TOKEN_URL, payload)
        self.assertIn('token', response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # todo: JWT update required
    def test_create_token_invalid_credentials(self):
        """Test that token is not created if invalid credentials are given."""
        """Test that a token is created for the user."""
        user_details = {
            'name': 'Test Name',
            'email': 'test@example.com',
            'password': 'good_pass1234'
        }
        # create a user
        create_user(**user_details)
        payload = {
            'email': 'test@example.com',
            'password': 'bad_pass1234'
        }

        response = self.client.post(TOKEN_URL, payload)
        self.assertNotIn('token', response.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
