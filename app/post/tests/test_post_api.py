""" Tests for Post API """
from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Post
from post.serializers import PostSerializer

POST_URL = reverse('post:post-list')


def create_post(user, **params):
    """Helper function to create a post"""
    defaults = {
        'title': 'Test Post Title',
        'content': 'Test Post Content',
        'description': 'Test Description',
        'link': 'https://testlink.com',
    }

    defaults.update(params)

    return Post.objects.create(user=user, **params)


class PublicPostApiTests(TestCase):
    """Test the publicly available Post API"""
    def setUp(self):
        self.client = APIClient()

    def test_login_required(self):
        """Test that login is required for retrieving posts"""
        res = self.client.get(POST_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)
