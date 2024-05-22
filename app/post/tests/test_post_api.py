""" Tests for Post API """
from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from django.contrib.auth import get_user_model
from core.models import Post
from post.serializers import PostSerializer, PostDetailSerializer

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

    post = Post.objects.create(user=user, **defaults)
    return post


def create_user(**params):
    return get_user_model().objects.create_user(**params)


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
        self.user = create_user(
            email="testUser@example.com",
            password="password123"
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
        # assert that this is not empty
        self.assertTrue(len(response.data) > 0)

    def test_posts_limited_to_user(self):
        """Test that posts returned are for the authenticated user"""
        user2 = create_user(
            email="testUser2@example.com",
            password="password123"
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

    def test_create_basic_post(self):
        """Test creating a post"""
        payload = {
            'title': 'Test Post Title',
            'content': 'Test Post Content',
            'description': 'Test Description',
            'link': 'https://testlink.com',
        }

        response = self.client.post(POST_URL, payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        post = Post.objects.get(id=response.data['id'])
        # Looper over all post and print the title
        for key in payload.keys():
            self.assertEqual(payload[key], getattr(post, key))
        self.assertEqual(post.user, self.user)

    def test_partial_update_post(self):
        """Test updating a post with patch"""
        post = create_post(user=self.user)
        new_title = 'Updated Title'
        payload = {'title': new_title}
        url = detail_url(post.id)
        update = self.client.patch(url, payload)
        self.assertEqual(update.status_code, status.HTTP_200_OK)
        post.refresh_from_db()
        self.assertEqual(post.title, new_title)
        self.assertEqual(post.user, self.user)

    def test_full_update_post(self):
        """Test updating a post with put"""
        post = create_post(user=self.user)
        payload = {
            'title': 'Updated Title',
            'content': 'Updated Content',
            'description': 'Updated Description',
            'link': 'https://updatedlink.com',
        }
        url = detail_url(post.id)
        update = self.client.put(url, payload)
        self.assertEqual(update.status_code, status.HTTP_200_OK)
        post.refresh_from_db()
        for key in payload.keys():
            self.assertEqual(payload[key], getattr(post, key))
        self.assertEqual(post.user, self.user)

    def test_delete_post(self):
        """Test deleting a post"""
        post = create_post(user=self.user)
        url = detail_url(post.id)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Post.objects.filter(id=post.id).count(), 0)

    def test_unauthorized_user_delete_post(self):
        """Test deleting a post unauthorized"""
        user2 = create_user(
            email="testUser2@example.com",
            password="password123",
        )
        post = create_post(user=user2)

        url = detail_url(post.id)
        response_using_setup_client = self.client.delete(url)
        self.assertEqual(
            response_using_setup_client.status_code,
            status.HTTP_404_NOT_FOUND
        )
