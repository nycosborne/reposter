""" Tests for Post API """
from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

import tempfile
import os

from PIL import Image

from django.contrib.auth import get_user_model
from core.models import Post, Tag


def create_user(**params):
    return get_user_model().objects.create_user(**params)


class ServiceAPITests(TestCase):
    """Test the publicly available Post API"""

    def setUp(self):
        self.client = APIClient()
        self.user = create_user(
            email="testUser@example.com",
            password="password123"
        )

        self.client.force_authenticate(self.user)

    # def test_receiving_passcode(self):
    #     """Test that a passcode is received"""
    #     url = reverse('services:passcode')
    #     payload = {
    #         "code": "string"
    #     }
    #     response = self.client.post(url, payload)
    #     self.assertEqual(response.status_code, status.HTTP_201_CREATED)
