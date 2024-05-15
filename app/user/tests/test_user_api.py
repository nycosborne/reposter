""" Test for the user API. """
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

CREATE_USER_URL = reverse('user:create')


def create_user(**params):
    """Helper function to create a user for testing."""
    return get_user_model().objects.create_user(**params)
