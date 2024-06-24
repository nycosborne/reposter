""" Tests for Service API """
from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

import tempfile
import os
from django.contrib.auth import get_user_model
from core.models import SocialAccounts

SERVICE_URL = reverse('services:services-list')


def detail_url(service_id):
    """Return service detail URL"""
    return reverse('service:service_id-detail', args=[service_id])


class PublicServiceApiTests(TestCase):
    """Test the publicly available service API"""

    def setUp(self):
        self.client = APIClient()

    def test_login_required(self):
        """Test that login is required for retrieving service"""
        res = self.client.get(SERVICE_URL)
        print(res)
        # self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)
