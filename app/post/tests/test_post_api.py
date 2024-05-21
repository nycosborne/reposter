""" Tests for Post API """
from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from django.contrib.auth import get_user_model
from core.models import Post
from post.serializers import (
    PostSerializer,
    PostDetailSerializer,
)

POST_URL = reverse('post:post-list')


def detail_url(post_id):
    """Return post detail URL"""
    return reverse('post:post-detail', args=[post_id])


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


class PrivatePostApiTests(TestCase):
    """Test the authorized user Post API"""

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            'testUser@example.com',
            'password123',
        )
        self.client.force_authenticate(self.user)

    def test_retrieve_posts(self):
        """Test retrieving posts"""
        create_post(user=self.user)
        create_post(user=self.user)

        response = self.client.get(POST_URL)

        posts = Post.objects.all().order_by('-id')
        serializer = PostSerializer(posts, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_posts_limited_to_user(self):
        """Test that posts returned are for the authenticated user"""
        user2 = get_user_model().objects.create_user(
            'testUser2@example.com',
            'password123',
        )
        create_post(user=user2)
        create_post(user=self.user)

        response = self.client.get(POST_URL)
        posts = Post.objects.filter(user=self.user)
        serializer = PostSerializer(posts, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data, serializer.data)

    def test_get_post_detail(self):
        """Test retrieving post detail"""
        post = create_post(user=self.user)
        url = detail_url(post.id)
        response = self.client.get(url)
        serializer = PostDetailSerializer(post)
        self.assertEqual(response.data, serializer.data)
